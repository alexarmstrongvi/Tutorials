from subpackage import logger
log = logger.get_logger(__name__)

def print_messages():
    log.info('Submodule info message')
