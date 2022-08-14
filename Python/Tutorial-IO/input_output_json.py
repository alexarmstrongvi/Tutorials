#!/usr/bin/env python3
################################################################################
# JSON
#
# Sources
# - https://docs.python.org/3/library/json.html
################################################################################

print(f"\n===== Running {__file__} =====\n")

import json
from math import isnan

# Configure
filepath = 'input_output_files/output.json'

# Encode python objects into JSON
py_objects = {
        "str"   : 'A',
        "int"   : 1,
        "float" : 1.1,
        "True"  : True,
        "False" : False,
        "None"  : None,
        "Inf"   : float('-inf'),
        "NaN"   : float('NaN'),
        "dict"  : {'Key' : 'Value'},
        "list"  : [1,2],
        "tuple" : (3,4),
}
# Special, non-ASCII, NaN, and unicode characters
# Non-string keys
# Circular references 
# Pretty printing (indent and sort_keys)
# 
print("Initial Python objects\n", py_objects)

json_str = json.dumps(py_objects, indent=4)
print("\nEncoding Python to JSON")
print(json_str)

# Encode and write
with open(filepath, 'w') as f:
    json.dump(py_objects, f, indent=4)

# Decoding JSON
py_objects2 = json.loads(json_str)
print("\nDecoding JSON to Python")
print(py_objects2)

# Parsing inputs (float, int, constant)

# Reading in JSON file
with open(filepath, 'r') as f:
    py_objects3 = json.load(f)
    #print(py_objects3)

for k in py_objects:
    if k == 'tuple':
        assert list(py_objects[k]) == py_objects2[k] == py_objects3[k] 
    elif k == 'NaN':
        assert isnan(py_objects[k]) and isnan(py_objects2[k]) and isnan(py_objects3[k])
    else:
        assert py_objects[k] == py_objects2[k] == py_objects3[k]

# Create custom encoder
#JSONEncoder

# Create custom encoder
#object_hook
#JSONDecoder

# Errors
#JSONDecodeError

