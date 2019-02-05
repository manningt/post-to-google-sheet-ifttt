def main(values_module_name='values_dummy'):
    import logging
    logger = logging.getLogger(__name__)
    import gc
    import ujson
    import urequests as requests
    import sys
    from utime import sleep

    if sys.platform.startswith('esp'):
        import machine
        import network
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        cfg_info = get_cfg_info("wifi_info.json")
        # wifi_info.json = {"SSID": "xx", "password": "yy"}
        if not cfg_info:
            logger.error("Could not obtain wifi configuration")
            sys.exit(1)
        wlan.connect(cfg_info['SSID'], cfg_info['password'])
        for i in range(7):
            sleep(1)
            if wlan.isconnected():
                break
        if not wlan.isconnected():
            logger.error("Could not connect to wifi: {}".format(cfg_info['SSID']))
            sys.exit(1)

        # configure timer to issue reset, so the device will reboot and retry to connect, etc.
        TIME_BEFORE_RESET = 120000  # 3 minutes in milliseconds
        tim = machine.Timer(1)
        # tim.init throws an OSError 261 after a soft reset; this is a work-around:
        try:
            tim.init(period=TIME_BEFORE_RESET, mode=machine.Timer.ONE_SHOT, callback=lambda t: machine.reset())
        except Exception as e:
            logger.warning("Exception '%s' on tim.init; No reset after a timer expiry.", e)

    event_cfg = get_cfg_info('event_cfg.json')
    # event_cfg.json = {"API_key": "xx", "event_name": "yy", "sleep_time: 1234}
    if not event_cfg:
        logger.error("unable to obtain IFTTT and sensor parameters")
        sys.exit(1)
    if 'API_key' not in event_cfg:
        logger.error("missing API_key")
        sys.exit(1)
    if 'event_name' not in event_cfg:
        logger.error("missing event_name")
        sys.exit(1)
    if 'sleep_time' not in event_cfg:
        sleep_time = 30
    else:
        sleep_time = event_cfg['sleep_time']

    event_name = event_cfg['event_name']  # 'humidity_basement'
    API_key = event_cfg['API_key']  # 'o1VXgw4KvSMkawQxQMEhzH4JZNFvfZWFLFG-Tcq16bt'
    host = 'maker.ifttt.com'
    event_prefix = '/trigger/'
    event_postfix = '/with/key/'
    endpoint = 'https://' + host + event_prefix + event_name + event_postfix + API_key
    ifttt_headers = {'Connection': 'keep-alive', 'Content-type': 'application/json'}

    try:
        values_module = __import__(values_module_name)
    except:
        logger.error("unable to load get_values module: {}".format(values_module_name))
        sys.exit(1)

    try:
        values = values_module.get()
    except:
        logger.error("Exception on executing get_values for module: {}".format(values_module_name))
        sys.exit(1)
    if values is None:
        logger.error("failure on getting values for module: {}".format(values_module_name))
        sys.exit(1)

    logger.debug("posting: {}, data={}".format(event_name, ujson.dumps(values)))
    gc.collect()
    logger.debug("free mem before post: {}".format(gc.mem_free()))

    try:
        r = requests.post(endpoint, headers=ifttt_headers, json=values)
        logger.debug("post_status: {}".format(r.status_code))
        # logger.debug("post_reply: {}".format(r.text))
        if r.status_code != 200:
            logger.error("Error on POST: code: {}  reason: {}".format(r.status_code, r.reason))
            sys.exit(1)
        r.close()
    except Exception as e:
        logger.error("Exception on POST request: {}".format(e))
        sys.exit(1)

    if sys.platform.startswith('esp'):
        logger.debug("Going to sleep for {} seconds...".format(sleep_time))
        # multiply sleep time by approx 1000 (left shift by 10) to convert from seconds to milliseconds
        machine.deepsleep(sleep_time << 10)
    else:
        sys.exit("Done!")


def get_cfg_info(filename):
    import ujson
    try:
        with open(filename) as f:
            cfg_info = ujson.load(f)
        return cfg_info
    except OSError as e:
        e_str = str(e)
        logger.error("In get_cfg_info from filename: %s   Exception: %s", filename, e_str)
        return None


''' request post notes:
    can also use form encoded:
    ifttt_headers = {'Connection': 'keep-alive', 'Content-type': 'application/x-www-form-urlencoded'}
    string = "value1=11&value2=99"
    sample = bytearray(string, 'utf-8')
    r = requests.post(endpoint, headers=ifttt_headers, data=sample)

    curl -H "Content-Type: application/json" -d '{"value1":36,"value2":55}' \
        https://maker.ifttt.com/trigger/humidity_basement/with/key/xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    Further debug using python3:
    https://stackoverflow.com/questions/10588644
'''
