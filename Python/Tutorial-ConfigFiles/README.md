# Goals for Configuration Files
1. Centralize and organize code parameters
1. Parameter inheritance, composition, and overwriting to reduce duplication
1. Importing and overwriting of parameters from other config files
1. Avoid passing massive config object around to entire program
1. Load in as desired datatypes instead of all strings
1. Be able to run code while looping over a fixed set of configurations
1. Change configurations from the command line
1. Easily able to log and recreate the config settings from previous run
    * Format log for printing and easy diff'ing with other logs
1. Interpolation or preprocessing of log values (e.g. loading shell env vars, )
1. Reference 

# Options
* Set and read environment variables
* Read in config file as dict at the top level
    * JSON (`json`)
    * YAML (`pyyaml`)
    * INI (`ConfigParser`)
    * XML (`xml.etree.ElementTree`)
    * TOML (`toml`)
* Define and import a python config class
* Use 3rd party config managers
    * Hydra (Facebook)
    * Gin config (Google)
    * Dynaconf


# Resources
* https://dxiaochuan.medium.com/summary-of-python-config-626f2d5f6041