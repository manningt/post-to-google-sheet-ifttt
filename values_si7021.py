def get():
    import logging
    logger = logging.getLogger(__name__)
    import machine
    import si7021
    from utime import sleep

    # i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
    i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(23))
    try:
        sensor = si7021.Si7021(i2c)
    except:
        return None
    sample = {};
    sample["value1"] = sensor.relative_humidity
    sample["value2"] = si7021.convert_celcius_to_fahrenheit(sensor.temperature)
    return sample