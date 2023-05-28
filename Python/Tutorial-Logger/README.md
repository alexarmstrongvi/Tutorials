# Tutorial-Python-Logger
Collection of examples/guides/explanations for using python logger module

# Recommended logger setup
Depending on the complexity of the code, the following approaches are helpful:
    1. *Single-use script* - see 02 file. Hard code configuration into basicConfig and use
       logging.warning, logging.info, etc...
    1. *Research project* (i.e. code is only run by developer team) - Create
       logger.py module that configures root logger and have all scripts import
       it and call `logger.configure_root()`. Or have the configuration in a
       config file and call logging.fromFile or logging.fromDict
    1. *Anything else more complex* - Use configuration file

* Goals for using logger across project
    * [X] Single function call in any module to create logger object
    * [X] Logger object globally accessible in any module
    * [X] Default configuration defined in one place
    * [X] Level configurable with user arguments to main executable
    * [X] Manually configure logger level in a specific module if desired
    * [X] Manually configure logger level in specific class instances
    * [X] Modules that might be main executable or imported module
    * [X] Capture exception messages
    * [X] Captures messages to python stdout/stderr (e.g. module warnings)
    * [X] Configurable with yaml
    * [] Captures messages to unix stdout/stderr (e.g. module warnings)
