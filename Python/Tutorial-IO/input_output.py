#!/usr/bin/env python3
print(f"\n===== Running {__file__} =====\n")
#import pandas as pd
import numpy as np
import io
import os
from math import isnan

def print_dir(obj):
    print("Object:", obj)
    print("Object Type:", type(obj))
    print("Attributes:")
    print('\t',"\n\t".join([x for x in dir(obj) if not x.startswith('_')]))

################################################################################
# Built-in (open)
#
# Resources:
# - https://docs.python.org/3/tutorial/inputoutput.html#tut-files
# - https://docs.python.org/3/library/functions.html#open
# - https://docs.python.org/3/library/io.html#module-io
################################################################################
print("Testing built-in")
# Configure
filedir        = 'input_output_files'
filename_r     = 'flat_file.txt'
filename_w     = 'flat_file_write.txt'
filename_csv_r = 'tabular_data.csv'
filename_tsv_r = 'tabular_data.tsv'
filename_csv_w = 'tabular_data_write.csv'
filename_np_r  = 'tabular_data_numpy.csv'

filepath_r     = os.path.join(filedir, filename_r)
filepath_w     = os.path.join(filedir, filename_w)
filepath_csv_r = os.path.join(filedir, filename_csv_r)
filepath_tsv_r = os.path.join(filedir, filename_tsv_r)
filepath_csv_w = os.path.join(filedir, filename_csv_w)
filepath_np_r  = os.path.join(filedir, filename_np_r)

########################################
# Open file (default = read text from beginning)
f = open(filepath_r) # default file mode = read

# File attributes
#print('\n'.join([x for x in dir(f) if not x.startswith('_')]))
assert type(f) == io.TextIOWrapper
assert issubclass(type(f), io.IOBase)

assert os.path.dirname(f.name) == filedir
assert os.path.basename(f.name) == filename_r

assert f.readable() and f.seekable() and not (f.writable() or f.closed)
assert f.tell() == 0 # Stream position

# IOBase -> fileno(), isatty() 
# TextIOBase -> encoding, errors, newlines, buffer
# TextIOWrapper -> line_buffering, write_through 

# Reading a file
assert f.readline() == 'Line 0\n'
assert f.tell() > 0
assert f.readline() == 'Line 1\n'
assert f.readline(5) == 'Line '
assert f.readline(-1) == '2\n'
assert f.readline() == ''
f.seek(0)
assert f.read() == 'Line 0\nLine 1\nLine 2\n'
assert f.read() == ''
f.seek(0)
assert f.readlines() == ['Line 0\n','Line 1\n','Line 2\n']
assert f.readlines() == []
f.seek(0)
assert f.readlines(6) == ['Line 0\n']
f.seek(0)
assert f.readlines(7) == ['Line 0\n','Line 1\n']
# reconfigure
# truncate, detach

f.close()
assert f.closed

########################################
# Write to new file
f = open(filepath_w, mode='w')
f.write('Line 0\n')
f.writelines(['Line 1\n','Line'])
f.write(' 2\n')
f.close()
with open(filepath_w) as f:
    assert f.read() == 'Line 0\nLine 1\nLine 2\n'

# Overwrite file
f = open(filepath_w, mode='w')
f.write('Line A\nLine B\n')
f.close()
with open(filepath_w) as f:
    assert f.read() == 'Line A\nLine B\n'

# Write to new file, raising error if file exists
try:
    f = open(filepath_w, mode='x')
except FileExistsError:
    os.remove(filepath_w)
f = open(filepath_w, mode='x')
f.write('Line 0\n')
f.close()
with open(filepath_w) as f:
    assert f.read() == 'Line 0\n'

# Write to file, appending if it exists, creating it otherwise
f = open(filepath_w, mode='a')
f.write('Line 1\nLine 2\n')
f.close()
with open(filepath_w) as f:
    assert f.read() == 'Line 0\nLine 1\nLine 2\n'


# Read from and write to file
# w+ vs r+? w+ overwrites file first
f = open(filepath_w, mode='r+')
text = f.readline()
f.seek(0, io.SEEK_END)
f.write(text)
f.close()
with open(filepath_w) as f:
    assert f.read() == 'Line 0\nLine 1\nLine 2\nLine 0\n'

os.remove(filepath_w)

# f.flush
########################################
# Reading and writing binary files

########################################
# Alternative buffering, encoding, errors, and newline options for open()
# closefd option
# Custom openers

################################################################################
# Tabular text file (e.g. .csv)
#
# Sources
# - https://docs.python.org/3/library/csv.html
# - https://wellsr.com/python/introduction-to-csv-dialects-with-the-python-csv-module/
################################################################################
print("Testing CSV")
import csv
# Read a csv file
with open(filepath_csv_r, newline='') as f:
    csv_reader = csv.reader(f)
    d = csv_reader.dialect
    assert type(d) != csv.Dialect # = _csv.Dialect
    assert d.delimiter        == ','
    assert d.quotechar        == '"'
    assert d.doublequote      == True
    assert d.skipinitialspace == False
    assert d.strict           == False

    assert csv_reader.line_num == 0
    assert next(csv_reader) == ['C0', 'C1', 'C2'] # Header
    assert csv_reader.line_num == 1
    for row in csv_reader:
        assert csv_reader.line_num == 2
        assert row == ['R0C0', 'R0C1', 'R0C2']
        break # only look at first row

# Read a csv file with fieldnames in header
with open(filepath_csv_r, newline='') as f:
    csv_reader = csv.DictReader(f)
    assert type(csv_reader) == csv.DictReader
    assert csv_reader.fieldnames == ['C0', 'C1', 'C2']
    assert csv_reader.line_num == 1
    assert next(csv_reader) == {'C0': 'R0C0', 'C1': 'R0C1', 'C2': 'R0C2'}
    assert csv_reader.restkey == None
    assert csv_reader.restval == None
    # d = csv_reader.reader.dialect

# Read a csv file with a non-default dielect
with open(filepath_tsv_r, newline='') as f:
    csv_reader = csv.reader(f, delimiter='\t')
    assert next(csv_reader) == ['C0', 'C1', 'C2'] # Header

with open(filepath_tsv_r, newline='') as f:
    #csv_reader = csv.reader(f, dialect='excel-tab')
    csv_reader = csv.reader(f, dialect=csv.excel_tab)
    assert next(csv_reader) == ['C0', 'C1', 'C2'] # Header
#excel
#unix_dialect

# Create a custom CSV dialect
#Dialect
#register_dialect, unregister_dialect, get_dialect, list_dialects
#QUOTE_ALL, QUOTE_MINIMAL, QUOTE_NONE, QUOTE_NONNUMERIC
#field_size_limit
#Error

# Detect csv file dialect before reading
#Sniffer

# Write a csv file
with open(filepath_csv_w, 'w') as f:
    csv_writer = csv.writer(f)
    d = csv_writer.dialect
    assert d.quoting == csv.QUOTE_MINIMAL
    assert d.escapechar == None
    assert d.lineterminator == '\r\n'
    csv_writer.writerow(['C0','C1','C2'])
    csv_writer.writerow(['R0C0','R0C1','R0C2'])

with open(filepath_csv_w, newline='') as f:
    csv_reader = csv.reader(f)
    assert next(csv_reader) == ['C0', 'C1', 'C2'] # Header
    assert next(csv_reader) == ['R0C0', 'R0C1', 'R0C2']


# Write a csv file with header of fieldnames
with open(filepath_csv_w, 'w') as f:
    csv_writer = csv.DictWriter(f, fieldnames=['C0','C1','C2'])
    assert type(csv_writer) == csv.DictWriter
    csv_writer.writeheader()
    csv_writer.writerow({'C0':'R0C0','C1':'R0C1','C2':'R0C2'})

with open(filepath_csv_w, newline='') as f:
    csv_reader = csv.DictReader(f)
    assert next(csv_reader) == {'C0':'R0C0','C1':'R0C1','C2':'R0C2'}

os.remove(filepath_csv_w)

########################################
# NumPy
# np.loadtxt
arr = np.genfromtxt(filepath_np_r, delimiter=',')
np.testing.assert_equal(arr, [[0, 1, 2],[3, np.nan, 4]])
# np.recfromcsv

########################################
# Pandas
# pd.read_csv()
# pd.write_csv()

################################################################################
# Pickle
#
# Sources
# - https://docs.python.org/3.8/library/pickle.html
# - https://realpython.com/python-pickle-module/
################################################################################
import pickle

py_objects = {
        "str"   : 'A',
        "int"   : 1,
        "float" : 1.1,
        "True"  : True,
        "False" : False,
        "None"  : None,
        "Inf"   : float('-inf'),
        "NaN"   : float('NaN'),
        "list"  : [1,2],
        "dict"  : {'Key' : 'Value'},
        "tuple" : (3,4),
        "set"   : {5,6},
}

def func(x):
    return x**2

# (De)Serialize
pickled_str = pickle.dumps(py_objects)
py_objects2 = pickle.loads(pickled_str)
for k in py_objects:
    if k == 'NaN':
        assert isnan(py_objects[k]) and isnan(py_objects2[k])
    else:
        assert py_objects[k] == py_objects2[k]

assert func == pickle.loads(pickle.dumps(func))
assert sum == pickle.loads(pickle.dumps(sum))
#pickle.dump()
#pickle.load()

# Unpickleable objects
square = lambda x : x * x
try:
    my_pickle = pickle.dumps(square)
except pickle.PicklingError:
    pass

# Fully qualified name reference pickling of functions and classes

# Customize how class instances are pickled
#def __getstate__(self)
#def __setstate__(self)

# Persistence of External Objects

# Dispatch tables

# Create custom (de)serializers
#Pickler
#Unpickler

# Other
#HIGHEST_PROTOCOL
#DEFAULT_PROTOCOL

################################################################################
# YAML
#
# Sources
# - https://pyyaml.org/wiki/PyYAMLDocumentation
################################################################################

################################################################################
# HDF5
#
# Sources
# - https://docs.h5py.org/en/stable/
################################################################################
#import h5py

