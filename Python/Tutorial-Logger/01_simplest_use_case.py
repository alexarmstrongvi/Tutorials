#!/usr/bin/env python

################################################################################
# Code
################################################################################
import logging

# Log message at all levels using default root logger
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
# $ ./01_simplest_use_case.py
# CRITICAL:root:Critical message
# ERROR:root:Error message
# WARNING:root:Warning message

################################################################################
# Notes
################################################################################
# The INFO and DEBUG message won't appear because the default message level is WARNING

################################################################################
# Next steps
################################################################################
# Configuring the root logger

