#!/usr/bin/env python

################################################################################
# Code
################################################################################
import logging

# Log message at all levels using configured root logger
def main():
    logging.basicConfig(
        #level  = logging.WARNING, # Default
        level  = logging.DEBUG,
        #format = '%(levelname)s:%(name)s:%(message)s' # Default
        #format = '%(levelname)8s :: %(message)s' # Simple example
        format = '%(levelname)8s :: (%(filename)s:%(funcName)s:L%(lineno)d) %(message)s' # Useful for debugging
    )
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
# (Option 1) No changes
# $ ./01_simplest_use_case.py
# CRITICAL:root:Critical message
# ERROR:root:Error message
# WARNING:root:Warning message

# (Option 2) Uncomment call to basicConfig (same as above)

# (Option 3) Uncomment call, set level to DEBUG and change to another format
# $ ./01_simplest_use_case.py
# Simple format
# CRITICAL :: Critical message
#    ERROR :: Error message
#  WARNING :: Warning message
#     INFO :: Info message
#    DEBUG :: Debug message

# Debug format
# CRITICAL :: (01_simplest_use_case.py:main:L17) Critical message
#    ERROR :: (01_simplest_use_case.py:main:L18) Error message
#  WARNING :: (01_simplest_use_case.py:main:L19) Warning message
#     INFO :: (01_simplest_use_case.py:main:L20) Info message
#    DEBUG :: (01_simplest_use_case.py:main:L21) Debug message

################################################################################
# Notes
################################################################################
# Root logger configuration is fixed after first message is logged so
# basicConfig must be called before any messages are logged. Test this by moving
# the call to basicConfig between log messages. You will see it starts having no
# effect.

# All formatting attributes (e.g. levelname) listed here:
# https://docs.python.org/2/library/logging.html#logrecord-attributes

################################################################################
# Next steps
################################################################################
# logging across modules and functions
