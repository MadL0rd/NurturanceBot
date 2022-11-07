import sys
import logging
from logging import StreamHandler, Formatter, handlers

format_start = '[%(asctime)s: %(levelname)s] %(filename)s\t-> %(funcName)s[%(lineno)d] \t'
format_message = '%(message)s'
format_default = format_start + format_message
file_name = 'logs.txt'

class CustomFormatter(logging.Formatter):

  grey = "\x1b[38;20m"
  green = "\x1b[1;32m"
  yellow = "\x1b[33;20m"
  red = "\x1b[31;20m"
  bold_red = "\x1b[31;1m"
  reset = "\x1b[0m"
  
  FORMATS = {
      logging.DEBUG: green + format_start + reset + format_message,
      logging.INFO: green + format_start + reset + format_message,
      logging.WARNING: yellow + format_start + reset + format_message,
      logging.ERROR: red + format_start + reset + format_message,
      logging.CRITICAL: bold_red + format_start + reset + format_message,
  }

  def format(self, record):
      log_fmt = self.FORMATS.get(record.levelno)
      formatter = logging.Formatter(log_fmt)
      return formatter.format(record)

# logging.basicConfig(format=format, level=logging.INFO)
# logger = logging.getLogger()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# if (logger.hasHandlers()):
#   logger.handlers.clear()

stream_handler = StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(CustomFormatter())
logger.addHandler(stream_handler)

file_handler = handlers.RotatingFileHandler(file_name,
                                            mode='a',
                                            maxBytes=5*1024*1024,
                                            backupCount=2,
                                            encoding=None,
                                            delay=0)
# file_handler.setFormatter(CustomFormatter())
file_handler.setFormatter(Formatter(fmt=format_default))
logger.addHandler(file_handler)

def get_logger():
  return logger