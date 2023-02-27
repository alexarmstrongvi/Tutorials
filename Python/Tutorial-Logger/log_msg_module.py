import logging

# Configuration
logger_name = __name__ # recommended to use module name
log_level = logging.DEBUG
log_format = '%(levelname)8s :: (%(name)s) %(message)s'

# Initialize
formatter = logging.Formatter(log_format)

handler = logging.StreamHandler()
handler.setLevel(log_level)
handler.setFormatter(formatter)

logger = logging.getLogger(logger_name)
logger.addHandler(handler)
logger.setLevel(log_level)

def do_something():
    logger.info("Info message")
    logger.debug("Debug message")

