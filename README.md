# post-to-google-sheet-ifttt

Requires an API key from ifttt.com

This [tutorial](https://randomnerdtutorials.com/esp32-esp8266-publish-sensor-readings-to-google-sheets/) provides
 a good walk-through of setting up ifttt.  The code in the tutorial is C based.

This repository is for posting in a micropython environment, which can be loaded on your hardware by following
the instructions [here](http://docs.micropython.org/en/latest/). It was tested using unix (macos) micropython.

To run, execute: micropython main.py
or micropython main.py -h

A dummy routine (values_dummy) allows the code to run on any hardware by using the defaults.

The code doesn't work on an ESP8266 - it runs out of memory when doing the urequest post.  This
could be resolved by using frozen modules.

For my application, I used an ESP32 and an si7021 to log relative humidity and temperature to a google sheet.

The following modules are required:
* upip install logging
* upip install argparse

2 json configuration files are required:
* wifi_info.json: {"SSID": "xx", "password": "yy"}
* event_cfg.json: {"API_key":"your_key", "event_name":"your_name", "sleep_time":21600}