#!/usr/bin/env python

################################################################################
# Code
################################################################################
import logging
import log_msg_module

# Configuration
logger_name = __name__ # recommended to use module name
log_level = logging.INFO

# Initialize
logger = logging.getLogger(logger_name)

# Log message from other modules
def main():
    logging.basicConfig(
        level  = logging.CRITICAL,
        format = "%(levelname)8s || %(module)s :: %(message)s")
    logger.setLevel(log_level)
    logging.info("Calling root logger")
    logger.debug("Calling module function")
    log_msg_module.do_something()
    
    logger.info("Done")

if __name__ == "__main__":
    main()

################################################################################
# Output
################################################################################
# $ ./03_making_new_loggers.py
#    INFO || log_msg_module :: Info message
#   DEBUG || log_msg_module :: Debug message
#    INFO || 03_making_new_loggers :: Done

################################################################################
# Notes
################################################################################
# The module specific loggers can have their own levels apart from the root
# level. All messages making it past the log level of their individual logger
# will get passed up to the root for sending to stdout.
