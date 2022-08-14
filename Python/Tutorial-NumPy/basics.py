#!/usr/bin/env python3
print(f"\n===== Running {__file__} =====\n")

import numpy as np
import numpy.testing as test

################################################################################
# Array creation
################################################################################
# Dimensions
arr_0d = np.array(0)

arr_1d_a = np.array([0,2,4])
arr_1d_b = np.r_[0,2,4]
arr_1d_c = np.r_[[0],[2,4]]
arr_1d_d = np.arange(0,5,2)
arr_1d_e = np.r_[0:5:2]
arr_1d_f = np.linspace(0,4,3)
arr_1d_g = np.r_[0:4:3j]
test.assert_array_equal(arr_1d_a, arr_1d_b)
test.assert_array_equal(arr_1d_a, arr_1d_c)
test.assert_array_equal(arr_1d_a, arr_1d_d)
test.assert_array_equal(arr_1d_a, arr_1d_e)
test.assert_array_equal(arr_1d_a, arr_1d_f)
test.assert_array_equal(arr_1d_a, arr_1d_g)


arr_2d_a = np.array([[1,0,0,0],
                     [0,1,0,0],
                     [0,0,1,0]])
arr_2d_b = np.identity(4)[:3] # must be square matrix
arr_2d_c = np.eye(3,4) # similar to identity but arbitrary 2D shape
test.assert_array_equal(arr_2d_a, arr_2d_b)
test.assert_array_equal(arr_2d_a, arr_2d_c)

arr_3d = np.array([[[1000,1001,1002],
                    [1010,1011,1012],
                    [1020,1021,1022]],

                   [[1100,1101,1102],
                    [1110,1111,1112],
                    [1120,1121,1122]],

                   [[1200,1201,1202],
                    [1210,1211,1212],
                    [1220,1221,1222]]])

arr_4d = np.empty( (3,3,3,3))
arr_4d = np.zeros( (3,3,3,3))
arr_4d = np.ones(  (3,3,3,3))
arr_4d = np.full(  (3,3,3,3), 2)
arr_4d = np.empty_like(arr_4d)
arr_4d = np.zeros_like(arr_4d)
arr_4d = np.ones_like(arr_4d)
arr_4d = np.full_like(arr_4d, 4)
arr_4d = np.arange(3**4).reshape((3,3,3,3))
arr_4d = np.linspace(0,1,3**4).reshape((3,3,3,3))
arr_4d = np.fromfunction(lambda i,j,k,l : i+j+k+l, (3,3,3,3))

# Data types
arr_bool    = np.array([True, 1, 2, -1, 1.1, False, 0, 0.0], dtype=bool)
arr_int     = np.array([-1, 1, 1.9], dtype=int)
arr_float   = np.array([1.5, 1/3, 0.0, -0], dtype=float)
arr_complex = np.array([1j, 1+1j, 1, 1.5-2.5j], dtype=complex)

# Grids
#see https://stackoverflow.com/questions/12402045/mesh-grid-functions-in-python-meshgrid-mgrid-ogrid-ndgrid
# Useful for situations where you might think to loop over all combinations of entries in multiple 1D arrays
#np.meshgrid()
#np.mgrid[]
#np.ogrid[]
#np.ix_()
#np.indices

# I/O
#np.fromfile


# For full list of array creation routines see
# https://numpy.org/doc/stable/reference/routines.array-creation.html

################################################################################
# Exploring
################################################################################
arr = arr_4d
print(f'array info : \tndim = {arr.ndim}; '
                 f'shape = {arr.shape}; '
                 f'size = {arr.size}; '
                 f'dtype = {arr.dtype}; '
                 f'itemsize = {arr.itemsize} bytes;\n\t\t'
                 f'sum = {arr.sum()}; '
                 f'min = {arr.min()} at idx = {arr.argmin()}; '
                 f'max = {arr.max()} at idx = {arr.argmax()}; '
                 )
print()

# Searching for value 
#np.where
#np.nonzero
#np.argsort
#np.searchsorted

################################################################################
# Accessing
################################################################################
# Nomenclature
# Axis 0 = first  axis = "Row"
# Axis 1 = second axis = "Column"
# Axis 2 = third  axis = "Depth"
# Axis 3 = fourth axis
# ...

# Select a single entry
assert arr_3d[1,1,1] == arr_3d[(1,1,1)] == arr_3d[1][1][1]

# Select a single array along one axis
print("Select row    :\n", arr_3d[1,:,:])
print("Select column :\n", arr_3d[:,1,:])
print("Select depth  :\n", arr_3d[:,:,1])
print()

# Select a single entry along one axis
print("Select an entry from each row    : ", arr_3d[:,1,1])
print("Select an entry from each column : ", arr_3d[1,:,1])
print("Select an entry from each depth  : ", arr_3d[1,1,:])
print()

# Select an arbitrary set of arrays
## Select two rows
x = arr_3d[[0,2],:,:] 
test.assert_array_equal(x[0], arr_3d[0,:,:])
test.assert_array_equal(x[1], arr_3d[2,:,:])

## Select two arbitrary entries
x = arr_3d[[0,2],[1,1],[2,0]]
assert x[0] == arr_3d[0,1,2]
assert x[1] == arr_3d[2,1,0]

## More complicated array indexing (use case?)
arr_1d = np.arange(10)*10
sel = np.array([[1,3],[2,4]])
x = arr_1d[sel] # Think of it like replaceing each entry in sel with that entry from arr_1d, keeping the shape of sel
test.assert_array_equal(x, sel*10)
# np.take

# Looping order
print("Looping order")
count = 0
for ax0_idx, ax12_arr in enumerate(arr_3d):
    test.assert_array_equal(ax12_arr, arr_3d[ax0_idx,:,:])
    for ax1_idx, ax2_arr in enumerate(ax12_arr):
        test.assert_array_equal(ax2_arr, arr_3d[ax0_idx, ax1_idx,:])
        for ax2_idx, entry in enumerate(ax2_arr):
            assert entry == arr_3d[ax0_idx, ax1_idx, ax2_idx]

            index = (ax0_idx, ax1_idx, ax2_idx)
            print(f'{count:02d}) {entry} {index}')
            
            # Arrays are unraveled in the same way as nested loops
            assert entry == arr_3d.flat[count] == arr_3d.ravel()[count] == arr_3d.reshape(-1)[count] == np.repeat(arr_3d,1)[count]
            count+=1
print()

# Slicing (start:stop:step)
#  _________________________
#  | P | y | t | h | o | n |
#  0   1   2   3   4   5   6
# -6  -5  -4  -3  -2  -1

N = 4
arr_1d = np.arange(N)
print("Array slicing [start:stop:step]")
print(f'arr_1d = {arr_1d}')
for start in range(0,N):
    for stop in range(1, N+1):
        for step in range(-N, N+1):
            # Avoid errors
            if step == 0: continue
            sel = arr_1d[start:stop:step]
            
            # Avoid empty arrays
            if start == stop: 
                assert sel.size == 0
                continue
            if start < stop and step < 0:
                assert sel.size == 0
                continue
            if start > stop and step > 0:
                assert sel.size == 0
                continue

            # Avoid unused alternatives
            if abs(stop - start) < abs(step) or (abs(stop-start) == abs(step) and abs(stop - start) > 1):
                same_sel = arr_1d[start:start+1]
                assert type(sel) == type(same_sel)
                test.assert_array_equal(sel, same_sel)
                continue

            # Full expression
            slicings  = f'arr_1d[{start:2d}:{stop:2d}:{step:2d}] = '

            # Full negative expression
            neg_start = start - N
            neg_stop = stop - N
            slicings += f'arr_1d[{neg_start:2d}:{neg_stop:2d}:{step:2d}] = '
            
            # Add compact expressions
            # Compact slicing with negative integers will not be shown

            # One default
            if start == 0 and stop != N and step != 1:
                slicings += f'arr_1d[:{stop}:{step}] = '
            if start != 0 and stop == N and step != 1:
                slicings += f'arr_1d[{start}::{step}] = '
            if start != 0 and stop != N and step == 1:
                #slicings += f'arr_1d[{start}:{stop}:] = '
                slicings += f'arr_1d[{start}:{stop}] = '
            # Two defaults
            if start != 0 and stop == N and step == 1:
                #slicings += f'arr_1d[{start}::] = '
                slicings += f'arr_1d[{start}:] = '
            if start == 0 and stop != N and step == 1:
                #slicings += f'arr_1d[:{stop}:] = '
                slicings += f'arr_1d[:{stop}] = '
            if start == 0 and stop == N and step != 1:
                slicings += f'arr_1d[::{step}] = '
            # All default
            if start == 0 and stop == N and step == 1:
                #slicings += f'arr_1d[::] = '
                #slicings += f'arr_1d[:] = '
                slicings += f'arr_1d = '
            print(slicings, sel)
print()
# slice objects
arr = np.arange(20).reshape(2,10)
s = (1, slice(2,6,2))
x = arr[s]
y = arr[1, 2:6:2]
test.assert_array_equal(x,y)

# Ellipses
arr = np.arange(3**5).reshape((3,3,3,3,3))
x = arr[1,:,:,:,1]
y = arr[1,...,1]
s = (1, Ellipsis, 1)
z = arr[s]
test.assert_array_equal(x,y)
test.assert_array_equal(x,z)


# Boolean/mask filters

# Special
# arr.diagonal()

################################################################################
# Modifiying
################################################################################
# arr.reshape()
# arr.transpose()
# np.newaxis
# arr.fill()
# np.put()
# np.putmask()

# Duplicating axis in an array (np.repeat)
arr = np.arange(4).reshape((2,2))
## Get 1D array with all entries duplicated
x = np.repeat(arr, 2)
## Duplicate all rows
x = np.repeat(arr, 2, axis=0)
## Duplicate all columns
x = np.repeat(arr, 2, axis=1)
## Duplicate arbitrary rows
x = np.repeat(arr, [2,1], axis=0)
## Duplicate arbitrary columns
x = np.repeat(arr, [2,1], axis=1)

# Removing axis with only one entry
arr1 = np.arange(4).reshape((2,2))
arr2 = np.arange(4).reshape((2,1,2))
arr3 = np.arange(4).reshape((1,2,1,2,1))
# Remove all axis with one entry
x = np.squeeze(arr3)
# Remove arbitrary axis with one entry
y = np.squeeze(arr3,axis=(0,4))
test.assert_array_equal(x, arr1)
test.assert_array_equal(y, arr2)

# Swap axis
arr = np.arange(4).reshape((2,2))
x = np.swapaxes(arr,0,1)
y = np.swapaxes(arr,1,0)
z = arr.T
test.assert_array_equal(z,x)
test.assert_array_equal(z,y)


################################################################################
# Combining and splitting
################################################################################
## Concatentation
# - Possible along an axis if all other axes are of the same shape
arr_2_2_2 = np.arange(8).reshape((2,2,2))
arr_2_2_3 = np.arange(12).reshape((2,2,3))
arr_2_3_2 = np.arange(12).reshape((2,3,2))
arr_3_2_2 = np.arange(12).reshape((3,2,2))

# Stacking "rows" (i.e. first axis / axis 0)
arr_5_2_2a = np.vstack((arr_2_2_2, arr_3_2_2))
arr_5_2_2b = np.row_stack((arr_2_2_2, arr_3_2_2))
arr_5_2_2c = np.r_[arr_2_2_2, arr_3_2_2] # note the brackets
arr_5_2_2d = np.concatenate((arr_2_2_2, arr_3_2_2), axis=0)

assert arr_5_2_2a.shape == (5,2,2)
test.assert_array_equal(arr_5_2_2a, arr_5_2_2b)
test.assert_array_equal(arr_5_2_2a, arr_5_2_2c)
test.assert_array_equal(arr_5_2_2a, arr_5_2_2d)

# Stacking "columns" (i.e. second axis / axis 1)
arr_2_5_2a = np.hstack((arr_2_2_2, arr_2_3_2))
arr_2_5_2b = np.column_stack((arr_2_2_2, arr_2_3_2))
arr_2_5_2c = np.concatenate((arr_2_2_2, arr_2_3_2), axis=1)

assert arr_2_5_2a.shape == (2,5,2)
test.assert_array_equal(arr_2_5_2a, arr_2_5_2b)
test.assert_array_equal(arr_2_5_2a, arr_2_5_2c)

# Stacking "depth" (i.e. third axis / axis 2)
arr_2_2_5a = np.dstack((arr_2_2_2, arr_2_2_3))
# Stacking arbitrary axes
arr_2_2_5e = np.concatenate((arr_2_2_2, arr_2_2_3), axis=2)
arr_2_2_5f = np.r_['2', arr_2_2_2, arr_2_2_3] # note the brackets
# Stacking the last axis or axis ndim
arr_2_2_5b = np.c_[arr_2_2_2, arr_2_2_3] # note the brackets
arr_2_2_5d = np.concatenate((arr_2_2_2, arr_2_2_3), axis=-1)
arr_2_2_5c = np.r_['-1', arr_2_2_2, arr_2_2_3] # note the brackets

# Stacking on new axis (arrays must be the same shape)
arr_1_2_2_2 = np.stack((arr_2_2_2, arr_2_2_2), axis=0) # default
arr_2_2_1_2 = np.stack((arr_2_2_2, arr_2_2_2), axis=2) # default
arr_2_2_2_1 = np.stack((arr_2_2_2, arr_2_2_2), axis=-1) # default

assert arr_2_2_5a.shape == (2,2,5)
test.assert_array_equal(arr_2_2_5a, arr_2_2_5b)
test.assert_array_equal(arr_2_2_5a, arr_2_2_5c)
test.assert_array_equal(arr_2_2_5a, arr_2_2_5d)
test.assert_array_equal(arr_2_2_5a, arr_2_2_5e)
test.assert_array_equal(arr_2_2_5a, arr_2_2_5f)

# Adding 1D arrays as columns
x = np.arange(0,3)
y = np.arange(3,6)
z = np.arange(6,9)

xy = np.column_stack((x,y))
xy2 = np.c_[x,y]
xy3 = np.r_['1,2,0',x,y] # see below
assert xy.shape == (3,2)
test.assert_array_equal(xy,xy2)
test.assert_array_equal(xy,xy3)

xyz = np.column_stack((xy,z))
xyz2 = np.c_[xy,z]
xyz3 = np.r_['1,2,0',xy,z] # see below
assert xyz.shape == (3,3)
test.assert_array_equal(xyz,xyz2)
test.assert_array_equal(xyz,xyz3)

## Extended use of np.r_[] - reshape and concatenate
x = np.ones((2,3,4))
concat_axis = 0 # defaults to 0
output_ndim = 6 # defaults to input ndim
output_axis = 2 # defaults to (output ndim - input_ndim) so output >= input ndim
how_to_concat = f'{concat_axis},{output_ndim},{output_axis}'
y = np.r_[how_to_concat, x,x]
# Start shape : (2,3,4) & (2,3,4)
# Step 1      : (1,1,1,1,1,1) & (1,1,1,1,1,1) # all inputs will be converted to output_ndim
# Step 2      : (1,1,2,3,4,1) & (1,1,2,3,4,1) # original arrays start at output_axis
#                    ^               ^
#               output_axis      output_axis    
# Step 3      : (2,1,2,3,4,1) & (2,1,2,3,4,1) # combine along concat_axis (all other dimensions must agree)
#                ^               ^
#               concat_axis      cocat_axis    
assert y.shape == (2,1,2,3,4,1)

########################################
x = np.arange(24).reshape((2,3,4))

# Split along rows / first axis / axis 0
x1, x2 = np.vsplit(x, 2) # Split into 2
y1, y2 = np.vsplit(x, [1]) # Split rows into [:1] and [1:]
z1, z2 = np.split(x, 2, axis=0)
w1, w2 = np.array_split(x, 2, axis=0)
v1, v2 = x[0,:,:], x[1,:,:]

assert x1.shape == x2.shape == (1,3,4)
test.assert_array_equal(x1, y1)
test.assert_array_equal(x1, z1)
test.assert_array_equal(x1, w1)
test.assert_array_equal(x2, y2)
test.assert_array_equal(x2, z2)
test.assert_array_equal(x2, w2)

# Split along columns / second axis / axis 1
x1, x2, x3 = np.hsplit(x, 3)
y1, y2, y3 = np.split(x, 3, axis=1)
assert x1.shape == x2.shape == x3.shape == (2,1,4)
test.assert_array_equal(x1, y1)
test.assert_array_equal(x2, y2)
test.assert_array_equal(x3, y3)

x1, x2 = np.array_split(x, 2, axis=1) # array_split, unlike split, will unevenly split
y1, y2 = np.hsplit(x,[2])
assert x1.shape == (2,2,4)
test.assert_array_equal(x1, y1)
assert x2.shape == (2,1,4)
test.assert_array_equal(x2, y2)

# Split along depth / third axis / axis 2
# np.dsplit

# Split along arbitrary axis
# np.split
# np.array_split


