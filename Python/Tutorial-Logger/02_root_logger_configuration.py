#!/usr/bin/env python

################################################################################
# Code
################################################################################
import logging

# Configuration
#log_level = logging.WARNING # Default
log_level = logging.DEBUG

#log_format = '%(levelname)s:%(name)s:%(message)s' # Default
log_format = '%(levelname)8s :: %(message)s' # Simple example
#log_format = '%(levelname)8s :: (%(filename)s:%(funcName)s:L%(lineno)d) %(message)s' # Useful for debugging

# Intialize
logging.basicConfig(level=log_level, format=log_format)

# Log message at all levels using configured root logger
def main():
    logging.critical("Critical message")
    logging.error("Error message")
    logging.warning("Warning message")
    logging.info("Info message")
    logging.debug("Debug message")

if __name__ == "__main__":
    main()

################################################################################
# Output
################################################################################
# $ ./02_root_logger_configuration.py
# CRITICAL :: Critical message
#    ERROR :: Error message
#  WARNING :: Warning message
#     INFO :: Info message
#    DEBUG :: Debug message

################################################################################
# Notes
################################################################################
# Logger configuration is fixed after first message is logged so basicConfig
# must be called before any messages are logged. Test this by moving the call
# to basicConfig between log messages. You will see it has no effect.

# All formatting attributes (e.g. levelname) listed here:
# https://docs.python.org/2/library/logging.html#logrecord-attributes

################################################################################
# Next steps
################################################################################
# logging across modules and functions
