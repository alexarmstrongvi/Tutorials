import logging
from typing import Union

import logger

class ClassWithLogger:
    '''Class with its own logger in case one wants separate instances to have
    different levels, formats, or handlers'''
    def __init__(self, log : Union[str, logging.Logger] = __name__):
        if isinstance(log, str):
            log = logger.get_logger(log)
        self.log = log
        self.log.info('Creating class with logger')

    def print_msg(self):
        self.log.info('Running print_msg()')