def get():
    import logging
    logger = logging.getLogger(__name__)
    import machine
    import si7021
    from utime import sleep

    #esp8266: i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
    i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
    sample = None
    try:
        sensor = si7021.Si7021(i2c)
        sample = {};
        sample["value1"] = round(sensor.relative_humidity, 1)
        sample["value2"] = round(si7021.convert_celcius_to_fahrenheit(sensor.temperature_quick), 1)
    except:
        pass
    return sample