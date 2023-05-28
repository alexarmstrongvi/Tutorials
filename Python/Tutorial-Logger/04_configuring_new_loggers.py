#!/usr/bin/env python

################################################################################
# Code
################################################################################
import logging
import sys

# Parameters
logger_name = __name__ # recommended to use module name
log_level = logging.INFO
log_format = '%(levelname)8s :: (%(name)s) %(message)s'
log_stream = sys.stderr # default

# (Option 1) Explicit Configuration
formatter = logging.Formatter(log_format)

handler = logging.StreamHandler(stream=log_stream) # default behavior
handler.setFormatter(formatter)

logger = logging.getLogger(logger_name)
logger.addHandler(handler)
logger.setLevel(log_level)
logger.info("Calling module function")
    
# (Option 2) Dict Configuration
# Note this could be configured in a yaml and loaded in
logger_name = logger_name + '_fromDict'
config_dict = {
    'version' : 1,
    'root' : {
        # defaults work
    },
    'loggers' : {
        logger_name : {
            "level" : log_level,
            "handlers" : ['my_handler_name'],
        },
    },
    'handlers' : {
        'my_handler_name' : {
            'class': 'logging.StreamHandler',
            'formatter': 'my_formatter_name',
            'stream': 'ext://sys.stdout',
        },
    },
    'formatters' : {
        'my_formatter_name' : {
            'format' : log_format,
        },
    },
}
import logging.config
logging.config.dictConfig(config_dict)
logger = logging.getLogger(logger_name)
logger.info("Calling module function")

logger.info("Done")

################################################################################
# Output
################################################################################
# $ ./04_configuring_new_loggers.py
#    INFO :: (__main__) Calling module function
#    INFO :: (__main___fromDict) Calling module function
#    INFO :: (__main___fromDict) Done


################################################################################
# Notes
################################################################################
# In general configuring via the root logger is sufficient if just need to log
# messages to stdout and perhaps a single log file. Anything beyond that will
# require creating a configuring a logger with custom handlers and formatters.
# formatting output requires creating a Formatter object that gets provided to a
# Handler.
# The basic flow of messages at this point is:
# message -> Logger -> Handler -> Formatter -> Logged
# For a more detailed flow chart of messages, see
# https://docs.python.org/2/howto/logging.html#logging-flow
