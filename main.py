import argparse
parser = argparse.ArgumentParser(description='Start post values to google sheet loop')
parser.add_argument('-l','--loglevel', default="INFO", help=': INFO, DEBUG, WARNING', required=False)
parser.add_argument('-g','--getter', default="values_dummy", help=': the name of python module used to get values to send to the google sheet', required=False)
args = parser.parse_args()

import logging
logging.basicConfig(level=getattr(logging, args.loglevel))
#logging.basicConfig(level=logging.DEBUG)

import post_loop
post_loop.main(values_module_name=args.type)
