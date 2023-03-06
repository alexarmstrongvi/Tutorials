#!/usr/bin/env python

################################################################################
# Code
################################################################################
import logging
import root_log_msg_module

# Configuration
log_level = logging.WARNING
log_format = '%(levelname)8s :: (%(module)s) %(message)s'

# Log message from other modules
def main():
    logging.basicConfig(level=log_level, format=log_format)
    logging.debug("Calling module function")
    root_log_msg_module.do_something()
    
    logging.info("Done")

if __name__ == "__main__":
    main()

################################################################################
# Output
################################################################################
# (Option 1) No changes
# $ ./02_logging_across_modules.py
# DEBUG:root:Calling module function
# INFO:root:Info message
# DEBUG:root:Debug message
# INFO:root:Done

# (Option 2) move call to basicConfig above import root_log_msg_module
# $ ./02_logging_across_modules.py

# (Option 3) Change log_level to logging.DEBUG
#   DEBUG :: (02_logging_across_modules) Calling module function
#    INFO :: (root_log_msg_module) Info message
#   DEBUG :: (root_log_msg_module) Debug message
#    INFO :: (02_logging_across_modules) Done

################################################################################
# Notes
################################################################################
# Using the root logger across modules is not recommended.
# The first call to basicConfig before a message is logged fixes the 
# root logger configuration for all modules run during the program.
# It is therefore not possible to configure loggers in specific modules 
# (e.g. set the message level to DEBUG for just one module) 

################################################################################
# Next steps
################################################################################
# Stop using the root logger EVER and instead instantiate separate loggers for
# each module
