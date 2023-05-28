import logging

logger = logging.getLogger(__name__)

def do_something():
    logger.setLevel(logging.DEBUG)
    logger.info("Info message")
    logger.debug("Debug message")

