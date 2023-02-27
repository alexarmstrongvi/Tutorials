#!/usr/bin/env python

################################################################################
# Code
################################################################################
import logging
#import root_log_msg_module

# Configuration
logger_name = __name__ # recommended to use module name
log_level = logging.INFO

# Initialize
handler = logging.StreamHandler()

logger = logging.getLogger(logger_name)
logger.addHandler(handler)
logger.setLevel(log_level)

# Log message from other modules
def main():
    import log_msg_module
    logger.debug("Calling module function")
    log_msg_module.do_something()
    
    logger.info("Done")

if __name__ == "__main__":
    main()

################################################################################
# Output
################################################################################
# $ ./04_making_new_loggers.py
#    INFO :: (log_msg_module) Info message 
#   DEBUG :: (log_msg_module) Debug message
# Done


################################################################################
# Notes
################################################################################
# In the simplest implementation of a logger, one must first make a handler and
# add it to the logger. 
# Handlers handle messages (LogRecord) created by the logger, sending them to the
# intended logging locations (e.g. file, stream, email, etc...)
# If no handler is added to the logger, and error message will occur whenever a
# message is provided to the logger ("No handlers could be found for logger")

# StreamHandler is the default handler for the root logger and so will give the
# same behavior. 
# It handles messages that get sent to a stream (default is stderr).
# It's default formatting is "%(message)s"
