import logger
# Manually set module logger to DEBUG if one wants DEBUG messages from this
# module even if the top level project logger is set at a higher log level.
log = logger.get_logger(__name__, level='DEBUG')

def print_messages():
    log.debug('Module debug message')
