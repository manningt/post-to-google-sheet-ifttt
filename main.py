import argparse
parser = argparse.ArgumentParser(description='Start post values to google sheet loop')
parser.add_argument('-l','--loglevel', default="INFO", help='Log-level, e.g. INFO, DEBUG', required=False)
parser.add_argument('-t','--type', default="values_dummy", help='value getter module name', required=False)
args = parser.parse_args()

import logging
logging.basicConfig(level=getattr(logging, args.loglevel))
#logging.basicConfig(level=logging.DEBUG)

import post_loop
post_loop.main(values_module_name=args.type)
