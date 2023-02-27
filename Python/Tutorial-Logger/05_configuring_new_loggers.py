#!/usr/bin/env python

################################################################################
# Code
################################################################################
import logging
import sys

# Configuration
logger_name = __name__ # recommended to use module name
log_level = logging.INFO
log_format = '%(levelname)8s :: (%(module)s) %(message)s'
log_stream = sys.stderr # default

# Initialize
formatter = logging.Formatter(log_format)

handler = logging.StreamHandler(stream=log_stream) # default behavior
handler.setFormatter(formatter)

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
# $ ./05_configuring_new_loggers.py
#    INFO :: (log_msg_module) Info message 
#   DEBUG :: (log_msg_module) Debug message
#    INFO :: (04_making_new_loggers) Done


################################################################################
# Notes
################################################################################
# formatting output requires creating a Formatter object that gets provided to a
# Handler.
# The basic flow of messages at this point is:
# message -> Logger -> Handler -> Formatter -> Logged
# For a more detailed flow chart of messages, see
# https://docs.python.org/2/howto/logging.html#logging-flow
