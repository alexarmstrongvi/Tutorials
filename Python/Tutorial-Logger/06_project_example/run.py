#!/usr/bin/env python
'''
Script for testing the logger utility module.

Run as
>> for lvl in CRITICAL ERROR WARNING INFO DEBUG; do python3 run.py -l $lvl -o logs/run_${lvl}.log; done

Regardless of project logging level, expect to still see messages not going
through project logger (e.g. root logger, stdout/stderr) and module loggers with
level manually set.
'''
import argparse
import sys
import os
import subprocess
from pathlib import Path
import yaml

# Import module with its own logger (child of the project logger), to confirm it
# has the correct formatting and level.
import module as mod
# Import subpackage with its own logger utility to confirm the utilities don't
# effect one another. The logger utility module should just be a copy of this
# package logger.py file with the project logger name changed.
import subpackage.submodule as submod
# Import class that has a separate module per class
from class_with_logger import ClassWithLogger

# Test that configuring and using root logger before importing the project
# logger does not impact project log messages
import logging
import logging.config
logging.basicConfig(level=logging.DEBUG)
logging.info('Configured ROOT logger. Project log format and level should be unaffected')
extpkg_logger = logging.getLogger('ExternalPkg.Child')
extpkg_logger.info('Configured ROOT child logger as if from external package')

import logger
log = logger.get_logger(__name__)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--log-path', type=Path)
    parser.add_argument('-l', '--log-level', default='WARNING') # log_level
    parser.add_argument('-c', '--log-conf', type=Path)
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    if args.log_conf:
        with args.log_conf.open('r') as ifile:
            dict_config = yaml.safe_load(ifile)
        logging.config.dictConfig(dict_config)
    else:
        logger.basic_config(level=args.log_level, log_path=args.log_path)

    logger.log_multiline(log.debug, logger.log_hierarchy_summary_str())

    log.info('='*40)
    log.critical('Critical message')
    log.error('Error message')
    log.warning('Warning message')
    log.info('Info message')
    log.debug('Debug message')
    print('sys.stdout message')
    print('sys.stderr message', file=sys.stderr)

    # Currently not sure if system messages (i.e. fd 1 & 2) can be captured
    subprocess.run('echo Unix stdout message'.split())
    #subprocess.run('echo "Unix stderr message" >&2'.split()) # Doesn't work
    os.system('echo "Unix stderr message" >&2')

    log.info('\r'+' '*80)
    log.info('='*40)

    mod.print_messages()
    log.info('\r'+' '*80)
    log.info('='*40)

    submod.print_messages()
    log.info('\r'+' '*80)
    log.info('='*40)

    cls0 = ClassWithLogger()
    cls1 = ClassWithLogger(log="Class1")
    class_log = logger.get_logger('Class2', level='DEBUG')
    cls2 = ClassWithLogger(log=class_log)
    #cls0.print_msg()
    #cls1.print_msg()
    #cls2.print_msg()

    raise RuntimeError('Test unhandled exception')
    log.info('='*40)

if __name__ == '__main__':
    main()
