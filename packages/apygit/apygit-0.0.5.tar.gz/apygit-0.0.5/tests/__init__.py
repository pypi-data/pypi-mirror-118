

import logging
import sys


level = logging.WARNING
if "-v" in sys.argv:
    level = logging.INFO
if "-vv" in sys.argv:
    level = logging.DEBUG

format = "%(asctime)-15s  %(levelname)5s  %(filename)s:%(lineno)d  %(message)s"
logging.basicConfig(stream=sys.stderr, level=level, format=format)
