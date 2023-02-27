#!/usr/bin/env python

################################################################################
# Code
################################################################################
import logging
# import root_log_msg_module

# Configuration
log_level = logging.DEBUG
log_format = '%(levelname)8s :: (%(module)s) %(message)s'

# Initialize
logging.basicConfig(level=log_level, format=log_format)

# Log message from other modules
def main():
    logging.debug("Calling module function")
    import root_log_msg_module
    root_log_msg_module.do_something()
    
    logging.info("Done")

if __name__ == "__main__":
    main()

################################################################################
# Output
################################################################################
# (Option 1) No changes
# $ ./03_logging_across_modules.py
#    INFO :: (root_log_msg_module) Info message
#    INFO :: (03_logging_across_modules) Done

# (Option 2) set log_level = logging.DEBUG
# $ ./03_logging_across_modules.py
#   DEBUG :: (03_logging_across_modules) Calling module function
#    INFO :: (root_log_msg_module) Info message
#   DEBUG :: (root_log_msg_module) Debug message
#    INFO :: (03_logging_across_modules) Done

# (Option 3) move "import root_log_msg_module" to just after "import logging"
# DEBUG:root:Calling module function
# INFO:root:Info message
# DEBUG:root:Debug message
# INFO:root:Done


################################################################################
# Notes
################################################################################
# Using the root logger across modules is not recommended.
# The last module to call basicConfig before a message is logged fixes the 
# root logger configuration for all modules run during the program.
# It is therefore not possible to configure loggers in specific modules 
# (e.g. set the message level to DEBUG for just one module) 

################################################################################
# Next steps
################################################################################
# Stop using the root logger EVER and instead instantiate separate loggers for
# each module
