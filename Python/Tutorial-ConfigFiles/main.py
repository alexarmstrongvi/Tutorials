#!/usr/bin/env python
'''
'''
from pathlib import Path
from pprint import pprint

import yaml


yaml_cfg = Path('config.yaml')

def main():
    '''Main'''
    with yaml_cfg.open() as ifile:
        cfg = yaml.safe_load(ifile)
    for key, val in cfg.items():
        if key in ['literal_block','folded_style']:
            key_str = repr(key)
            val_str = val
        elif isinstance(key, str) and key.startswith('Multiline'):
            key_str = key
            val_str = repr(val)
        else:
            key_str, val_str = repr(key), repr(val)   
        print(key_str,':', val_str)

if __name__ == '__main__':
    main()
