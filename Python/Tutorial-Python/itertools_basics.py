#!/usr/bin/env python3
import itertools
print("========================================")
print("Iterating over rectangular 2D arrays")
matrix = [
    [ '00', '01' ],
    [ '10', '11' ]
]
n_rows = len(matrix)
n_cols = len(matrix[0])

print("Option 1")
for i, j in itertools.product(range(n_rows), range(n_cols)):
    print(f"matrix[R{i}][C{j}] =", matrix[i][j])
print()

print("Option 2")
# Only works for 2 dimensions
for x in itertools.chain(*matrix):
    print(x)
print()

print("========================================")
print("Iterating over rectangular N-dim arrays")
list_ndim = [
    [[[ '0000', '0001' ],
      [ '0010', '0011' ]],
     [[ '0100', '0101' ],
      [ '0110', '0111' ]]],
    [[[ '1000', '1001' ],
      [ '1010', '1011' ]],
     [[ '1100', '1101' ],
      [ '1110', '1111' ]]]
]

# Determine shape of list
tmp = list_ndim.copy()
n_dim = 0
dim = ()
from collections.abc import Sequence
while isinstance(tmp, Sequence) and not isinstance(tmp, str):
    n_dim += 1
    dim += (len(tmp),)
    tmp = tmp[0]
    if n_dim > 100: break

# Print elements
for idx in itertools.product(*(range(n) for n in dim)):
    entry = list_ndim.copy()
    for i in idx:
        entry = entry[i]
    print(f"{n_dim}D matrix at {idx} = {entry}")
print()

