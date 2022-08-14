#!/usr/bin/env python3
################################################################################
# Table of Contents
# * Creating
# * Exploring
# * Accessing
# * Cleaning and Augmenting
# * Operations
# * Time-series (TODO)
# * Multi-index / advanced indexing (TODO) 
################################################################################
# see https://pandas.pydata.org/docs/user_guide/index.html

import pandas as pd  # Common to use pd abbrevation
import pandas._testing as pd_test
print(f"\n===== Running {__file__} =====")
print(f"Using Pandas {pd.__version__}")
print()

################################################################################
# Creating
################################################################################
print("========================================")
print("Creating Series")
data = [0,1,2,3]
idx_names = ['A','B','C','D']
s = pd.Series(data, index=idx_names)


print("========================================")
print("Creating DataFrames")
# Create from a 2D list (same as numpy array)
data = [
	[ 'R0C0', 'R0C1', 'R0C2', 'R0C3' ],
	[ 'R1C0', 'R1C1', 'R1C2', 'R1C3' ],
	[ 'R2C0', 'R2C1', 'R2C2', 'R2C3' ],
	[ 'R3C0', 'R3C1', 'R3C2', 'R3C3' ],
]
col_names = ["C0", "C1", "C2", "C3"]
row_names = ["R0", "R1", "R2", "R3"]
# class.__subclasses__()
n_rows = len(data)
n_cols = len(data[0])
print(data)
print()

df = pd.DataFrame(data)
print("Dataframe with automatic integer labels")
print(df)
print()

print("Dataframe with user labels")
df.columns = col_names
df.index = row_names
print(df)
print()

# Create from dict of lists
# Note that the rows and columns have to be transposed compared to the 2D list
# Also note that insertation order matters
data2 = {
    "C0" : [ 'R0C0', 'R1C0', 'R2C0', 'R3C0' ],
    "C1" : [ 'R0C1', 'R1C1', 'R2C1', 'R3C1' ],
    "C2" : [ 'R0C2', 'R1C2', 'R2C2', 'R3C2' ],
    "C3" : [ 'R0C3', 'R1C3', 'R2C3', 'R3C3' ],
}

df2 = pd.DataFrame(data2)
print("Dataframe with 1D dict labels")
print(df2)
df2.index = row_names
pd_test.assert_frame_equal(df2, df)
print()

# Create from dict of dict
data3 = {
    'C0' : {
        'R0' : 'R0C0', 
        'R1' : 'R1C0', 
        'R2' : 'R2C0', 
        'R3' : 'R3C0'},
    'C1' : {
        'R0' : 'R0C1', 
        'R1' : 'R1C1', 
        'R2' : 'R2C1', 
        'R3' : 'R3C1'},
    'C2' : {
        'R0' : 'R0C2', 
        'R1' : 'R1C2', 
        'R2' : 'R2C2', 
        'R3' : 'R3C2'},
    'C3' : {
        'R0' : 'R0C3', 
        'R1' : 'R1C3', 
        'R2' : 'R2C3', 
        'R3' : 'R3C3'},
}

df3 = pd.DataFrame(data3)
print("Dataframe with 2D dict labels")
print(df3)
pd_test.assert_frame_equal(df3, df)
print()

# Create labeled DataFrame with constructor
df4 = pd.DataFrame(data = data, columns = col_names, index = row_names)
pd_test.assert_frame_equal(df3, df)

# Writing out / Reading in data files
import os
print("DataFrame dumped to .csv")
df.to_csv("dataframe.csv")
os.system("cat dataframe.csv")
df_csv = pd.read_csv("dataframe.csv", index_col=0)
pd_test.assert_frame_equal(df_csv, df)
os.system("rm dataframe.csv")
print()

#print("DataFrame dumped to .h5")
#df.to_hdf
#df.read_hdf

print("DataFrame dumped to .xlsx")
# writing requires openpyxl package
df.to_excel("dataframe.xlsx", sheet_name="Sheet1")
os.system("ls -l dataframe.xlsx")
# reading requires xlrd package
df_xlsx = pd.read_excel("dataframe.xlsx", 'Sheet1', index_col=0)
pd_test.assert_frame_equal(df_xlsx, df)
os.system("rm dataframe.xlsx")
print()

################################################################################
# Exploring
################################################################################
print("========================================")
print("Exploring")
#df.head()
#df.tail()
assert df.values.tolist()  == data
assert df.index.tolist()   == row_names
assert df.columns.tolist() == col_names == [c for c in df]
#df.describe()
assert df.shape[0]         == n_cols # First index is for columns unlike loc and iloc
assert df.shape[1]         == n_rows
assert df.size             == n_rows * n_cols
assert df.ndim             == 2 # DataFrame is always 2 dimensions
assert df.iloc[1].ndim     == 1 # Series is always 1 dimension
#df.value_counts()
print()


################################################################################
# Accessing
################################################################################
# Summary of DataFrame seletion
# ---------------------------------------------------------------
#               | list | iloc | loc  | []   | attr | at   | iat
# ---------------------|------|------|------|------|------|------
# Row single    |  Y   |  Y   |  Y   |      |      |      |
# Row range     |  Y   |  Y   |  Y   |  Y   |      |      |
# Row arbitrary |  Y*  |  Y   |  Y   |      |      |      |
# Col single    |  Y*  |  Y   |  Y   |  Y   |  Y   |      |
# Col range     |  Y*  |  Y   |  Y   |      |      |      |
# Col arbitrary |  Y*  |  Y   |  Y   |  Y   |      |      |
# Entry         |  Y   |  Y   |  Y   |  Y   |  Y   |  Y   |  Y
# ---------------------------------------------------------------
# * = inconvenient
print("========================================")
print("Accessing DataFrames")
print()

print("Row Selection")
print("Single row (R1)")
list_sel = data[1]
iloc_sel = df.iloc[1]
loc_sel  = df.loc['R1']
#idx_sel  = Not Possible; df['R1':'R1'] returns DataFrame with just row 1 but not Series of row 1
pd_test.assert_series_equal(iloc_sel, loc_sel)
print(f"List : {list_sel}\nDataFrame :\n{iloc_sel}")
print()

print("Range of rows (R1-R3)")
list_sel = data[1:4]
iloc_sel = df.iloc[1:4]
loc_sel  = df.loc['R1':'R3']
idx_sel  = df['R1':'R3']
idx2_sel = df[1:4]
pd_test.assert_frame_equal(iloc_sel, loc_sel)
pd_test.assert_frame_equal(iloc_sel, idx_sel)
pd_test.assert_frame_equal(iloc_sel, idx2_sel)
print(f"List : {list_sel}\nDataFrame :\n{iloc_sel}")
print()

print("Arbitrary rows (R0 & R2)")
list_sel = [data[0], data[2]]
iloc_sel = df.iloc[[0,2]]
loc_sel  = df.loc[['R0','R2']]
#idx_sel  = Not possible; df[['R0','R2']] -> KeyError
pd_test.assert_frame_equal(iloc_sel, loc_sel)
print(f"List : {list_sel}\nDataFrame :\n{iloc_sel}")
# Alternative way of getting arbitrary rows using standard modules
from operator import itemgetter
list_sel2 = list(itemgetter(0,2)(data)) #itemgetter returns tuple
assert list_sel == list_sel2
print()

print("Column Selection")
print("Single column (C1)")
list_sel = [x[1] for x in data]
iloc_sel = df.iloc[:,1]
loc_sel  = df.loc[:,'C1']
idx_sel  = df['C1']
attr_sel = df.C1
pd_test.assert_series_equal(iloc_sel, loc_sel)
pd_test.assert_series_equal(iloc_sel, idx_sel)
pd_test.assert_series_equal(iloc_sel, attr_sel)
print(f"List : {list_sel}\nDataFrame :\n{iloc_sel}")
print()

print("Range of columns (C1-C3)")
list_sel = [x[1:4] for x in data]
iloc_sel = df.iloc[:,1:4]
loc_sel  = df.loc[:,'C1':'C3']
pd_test.assert_frame_equal(iloc_sel, loc_sel)
print(f"List : {list_sel}\nDataFrame :\n{iloc_sel}")
print()

print("Columns 0 & 2")
list_sel = [[x[0],x[2]] for x in data]
iloc_sel = df.iloc[:,[0,2]]
loc_sel  = df.loc[:,['C0','C2']]
idx_sel  = df[['C0','C2']]
pd_test.assert_frame_equal(iloc_sel, loc_sel)
pd_test.assert_frame_equal(iloc_sel, idx_sel)
print(f"List : {list_sel}\nDataFrame :\n{iloc_sel}")
print()

# Entry selection
for i, row in enumerate(df.index):
    for j, col in enumerate(df.columns):
        # .at[] and .iat() only works for accessing single entry but is ~2x faster than loc and iloc
        assert (data[i][j] 
                == df.iloc[i,j] 
                == df.iat[i,j]
                == df[col][row] # Note that []-indexing is flipped
                == df.loc[row][col] 
                == df.at[row,col] 
                )

for i in range(1, n_rows+1):
    for j in range(1, n_cols+1):
        assert data[-i][-j] == df.iloc[-i,-j]


print("========================================")
print("Boolean Selection")

# Boolean filters vs df.query()

# Conditions on entries (i.e. filter out entries)
df_cond1 = (df == 'R1C1') | (df == 'R2C2')
df_cond2 = df.isin(['R1C1','R2C2'])
pd_test.assert_frame_equal(df_cond1, df_cond2)

# Conditions on columns (i.e. filter out rows)
col_cond1 = (df['C1'] == 'R1C1') | (df['C1'] == 'R3C1')
col_cond2 = df['C1'].isin(['R1C1','R3C1'])
col_cond3 = df['C1'].str.contains('R[13]')
pd_test.assert_series_equal(col_cond1, col_cond2)
pd_test.assert_series_equal(col_cond1, col_cond3)

# Conditions on rows (i.e. filter out columns)
row_cond1 = (df.loc['R1'] == 'R1C1') | (df.loc['R1'] == 'R1C3')
row_cond2 = df.loc['R1'].isin(['R1C1','R1C3'])
row_cond3 = df.loc['R1'].str.contains('C[13]')
pd_test.assert_series_equal(row_cond1, row_cond2)
pd_test.assert_series_equal(row_cond1, row_cond3)

# Apply boolean filters
print("Select two entries")
print(df[df_cond1])
print()

print("Select two rows")
print(df.loc[col_cond1])
print()

print("Select two columns")
print(df.loc[:, row_cond1])
print()

# Boolean reductions - reduce a DataFrame of booleans to Series or scalar
# Check condition applies to all entries per column
df_bool = pd.DataFrame([[ True,  False],
	                [ True,  True]])
series_bool1 = df_bool.all()
# Check condition applies to one entry per column
df_bool = pd.DataFrame([[ False, False],
	                [ True,  False]])
series_bool2 = df_bool.any()
# Check condition applies to all entries per row
df_bool = pd.DataFrame([[ True,  True],
	                [ True,  False]])
series_bool3 = df_bool.all('columns') # = df_bool.T.all()
# Check condition applies to one entry per row
df_bool = pd.DataFrame([[ False, True],
	                [ False, False]])
series_bool4 = df_bool.any('columns') # = df_bool.T.any()

# Only works because rows and columns have the same default labels
solution = pd.Series([True, False])
pd_test.assert_series_equal(series_bool1, solution)
pd_test.assert_series_equal(series_bool2, solution)
pd_test.assert_series_equal(series_bool3, solution)
pd_test.assert_series_equal(series_bool4, solution)

# Check condition applies to any entries
df_bool = pd.DataFrame([[ False, True],
	                [ False, False]])
assert df_bool.any().any()
# Check condition applies to all entries
df_bool = pd.DataFrame([[ True,  True],
	                [ True,  True]])
assert df_bool.all().all()
# Check condition applies to all entries in any column
df_bool = pd.DataFrame([[ False, True],
	                [ False, True]])
assert df_bool.all().any()
# Check condition applies to any entry in all columns
df_bool = pd.DataFrame([[ False, True],
	                [ True,  False]])
assert df_bool.any().all()
# Check condition applies to all entries in any row
df_bool = pd.DataFrame([[ True,  True],
	                [ False, False]])
assert df_bool.all('columns').any()
assert df_bool.T.all().any()
# Check condition applies to any entry in all rows
df_bool = pd.DataFrame([[ False, True],
	                [ True,  False]])
assert df_bool.any('columns').all()
assert df_bool.T.any().all()

# Check for empty DataFrame
df_bool = pd.DataFrame([[],[]])
assert df_bool.empty

# Convert single entry DataFrame into boolean
df_bool = pd.DataFrame([[True]])
assert df_bool.bool()

################################################################################
# Cleaning and Augmenting
################################################################################

print("========================================")
print("Cleaning")
print("Rearranging columns")
new_col_order = ['C3','C0','C1','C2']
df1 = df[new_col_order] 
df2 = df.loc[:,new_col_order]
pd_test.assert_frame_equal(df1, df2)
print(df1)
# Sort to get back to normal
df1 = df1.sort_index(axis='columns') # Note: Does not sort in place
df2 = df2.sort_values(by='R1', axis='columns')
pd_test.assert_frame_equal(df1, df2)
pd_test.assert_frame_equal(df1, df)
print()

print("Rearranging rows")
new_row_order = ['R3','R2','R0','R1']
df1 = df.loc[new_row_order]
print(df1)
# Sort to get back to normal
df2 = df1.sort_index(axis='index') # default
df1 = df1.sort_values(by='C1', axis='index')
pd_test.assert_frame_equal(df1, df2)
pd_test.assert_frame_equal(df1, df)
print()

# Rearrange everything
#df.T

# Remove unwanted entries
#df.dropna()
#df.fillna()
#df.isna()
#df.drop()
print()

# Rename labels
#new_row_names = ["Row1","Row2","Row3","Row4"]
#new_col_names = ["Col1","Col2","Col3","Col4"]
#df.rename()
# Update row values
# Update col values
# Update arbitrary entry values
print()

print("========================================")
print("Augmenting")
# Adding rows

# Adding columns
#df['new_col'] = data
#df.assign(my_col = data)
#df.assign(my_col = lambda df : df['col']**2 )

# Merge
#pd.concat()
#pd.merge()

# Grouping
#df.groupby()


print()
#exit()

################################################################################
# Operations
################################################################################
# df.add()
# df.sub()
# df.mul()
# df.div()
# df.apply()

# df.pipe(myfunc) vs myfunc(df)

################################################################################
# Time-series
################################################################################

################################################################################
# Multindex / advanced indexing
################################################################################
# Index names vs axis labels vs axis levels (see https://stackoverflow.com/questions/45899612/pandas-index-names-axis-labels-and-levels)

# Reshaping
#df.stack()
#df.unstack()

# Pivot tables
#pd.pivot_table()

################################################################################
# Styling
################################################################################
# df.style
# pd.Styler
# df.style.applymap(myfunc)


