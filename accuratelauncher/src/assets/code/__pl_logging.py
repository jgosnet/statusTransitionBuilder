""" This module is exclusively used to specify the formatting and where to write logs: to stdout """
import logging
import sys

logging.basicConfig(format='%(name)s-%(levelname)s:%(message)s',
                    level=logging.INFO,
                    stream=sys.stdout)
