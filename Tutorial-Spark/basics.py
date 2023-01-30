#!/usr/bin/env python3
################################################################################
# Basic PySpark
# - run with `./basics.py` or `spark-submit --master local[4] basics.py`
################################################################################
print("===== START =====")
import pyspark
from pyspark.sql import SparkSession

################################################################################
# Setup
################################################################################
print("\nCreating Spark Session\n")\
# Configure Builder
ses_builder = SparkSession.builder
assert(ses_builder._options == {})
ses_builder.appName("MyApp")
assert(ses_builder._options['spark.app.name'] == 'MyApp')
ses_builder.master("local")
assert(ses_builder._options['spark.master'] == 'local')

# Create SparkSession and SparkContext
spark = ses_builder.getOrCreate()
assert(spark is SparkSession._instantiatedSession)
assert(spark is SparkSession._activeSession)

# One-liner alternatives (preferred)
# spark = SparkSession.builder.getOrCreate() # default name is randomly generated
# spark = SparkSession.builder.appName("MyApp").master('local').getOrCreate()

# Get SparkContext
sc = spark.sparkContext
# OLD WAY before SparkSession (still shown in official guides)
# from pyspark import SparkConf, SparkContext
# conf = SparkConf().setAppName('MyApp').setMaster('local')
# sc = SparkContext(conf=conf)


################################################################################
#################################### MAIN ######################################
################################################################################
print("\n---- Begin Program ----\n")

################################################################################
# RDDs
################################################################################
# Creating Parallelized Collections
n_slices = 4

num_reps = 100
nums = list(range(10))
num_list =  nums * num_reps
rdd = sc.parallelize(num_list, n_slices)

key_reps = 100
keys = sorted(['A', 'a', '1'])
val = 5
key_val_pairs = [(key,val) for key in keys * key_reps] 
rdd_kv = sc.parallelize(key_val_pairs, n_slices)

# Attributes
assert(type(rdd) == pyspark.RDD)
assert(rdd.id() != rdd_kv.id())
assert(rdd.getNumPartitions() == n_slices)
assert(sc.parallelize([]).isEmpty())
assert(rdd.ctx is sc) # ctx alias for rdd.context
rdd.setName('MyName')
assert(rdd.name() == 'MyName')
#rdd.isCheckpointed()
#rdd.getCheckpointFile()
#rdd.getStorageLevel()
#rdd.partitioner

########################################
# Actions (initiate computation, returning result)
########################################

# Moving files
assert(sorted(rdd.collect()) == sorted(num_list))
# rdd.collectAsMap
# rdd.collectWithJobGroup

# Metadata
assert(rdd.count() == len(num_list))
#rdd.countApprox
#rdd.countApproxDistinct

count_dict = rdd.countByValue()
assert(sorted(count_dict.keys()) == nums)
assert(count_dict[nums[0]] == num_reps)

count_key = rdd_kv.countByKey()
assert(sorted(count_key.keys()) == keys)
assert(count_key[keys[0]] == key_reps)

# Preview
assert(rdd.first() == num_list[0])
assert(rdd.top(5) == sorted(num_list, reverse=True)[:5])
assert(rdd.take(5) == num_list[:5])
assert(rdd.takeOrdered(5) == sorted(num_list)[:5])
assert(len(rdd.takeSample(True, 5, 1)) == 5) # values are random

# Reducing 
assert(rdd.reduce(lambda a,b : a+b) == sum(num_list))
reduce_dict = rdd_kv.reduceByKeyLocally(lambda a,b : a+b)
assert(sorted(reduce_dict.keys()) == keys)
assert(reduce_dict[keys[0]] == val * key_reps)

# For Each
# rdd.foreach
# rdd.foreachPartition

# Stats
# rdd.stats
# rdd.sum
# rdd.sumApprox
# rdd.max
# rdd.min
# rdd.mean
# rdd.meanApprox
# rdd.stdev
# rdd.sampleStdev
# rdd.variance
# rdd.sampleVariance

# Saving to Disk
import os
from glob import glob
path = 'output/tmp'
rdd.saveAsTextFile(path)
txt_files = glob(path + '/part-*') # Ex: part-00001
assert(len(txt_files) == rdd.getNumPartitions())
# rdd.saveAsHadoopDataset
# rdd.saveAsHadoopFile
# rdd.saveAsNewAPIHadoopDataset
# rdd.saveAsNewAPIHadoopFile
# rdd.saveAsPickleFile
# rdd.saveAsSequenceFile
for f in glob(path+"/*") + glob(path+"/.*"): os.remove(f)
os.rmdir(path)

########################################
# Shuffle Transformations (Actions w/o collecting; return RDD)
########################################

# Repartition
tmp_rdd = sc.parallelize([1, 2, 3, 4, 5], n_slices)
assert(len(tmp_rdd.glom().collect()) == n_slices)
assert(len(tmp_rdd.repartition(n_slices*2).glom().collect()) > n_slices)
# rdd.repartitionAndSortWithinPartitions
assert(len(tmp_rdd.coalesce(n_slices-1).glom().collect()) < n_slices)

# Checking if transformation occured 
# "ShuffledRDD" appears in RDD debug string if any prior transormations,
# not just the last one, carried out a shuffle
# see https://stackoverflow.com/questions/26273664/what-are-the-spark-transformations-that-causes-a-shuffle
pipelined_rdd = tmp_rdd.repartition(n_slices)
assert('ShuffledRDD' in pipelined_rdd.toDebugString().decode('utf-8'))

# ByKey operations (must re-sort data by key to carry out action step)
pipelined_rdd = rdd_kv.groupByKey()
result = pipelined_rdd.collect()
assert(len(result) == len(keys))
assert(type(result[0][1]) == pyspark.resultiterable.ResultIterable)
assert(len(result[0][1]) == key_reps)

result = rdd_kv.reduceByKey(lambda a,b : a+b).collect()
assert(result[0][1] == val * key_reps)

#rdd.sampleByKey
#rdd.aggregateByKey
#rdd.combineByKey
#rdd.foldByKey
#rdd.sortByKey
#rdd.subtractByKey

# Joins
# rdd.join
# *rdd.fullOuterJoin
# rdd.leftOuterJoin
# rdd.rightOuterJoin
# rdd.cogroup
# rdd.intersection
# rdd.distinct
# rdd.subtract
# *rdd.cartesian
# *rdd.zip
# *rdd.zipWithIndex
# *rdd.zipWithUniqueId
# * = Probably dont initiate shuffle

########################################
# Transformations (no computation, returning RDD)
########################################

# Mapping 
my_func = lambda x: x%2==0
pipelined_rdd = rdd.map(my_func)
assert(type(pipelined_rdd) == pyspark.rdd.PipelinedRDD)
assert(issubclass(pyspark.rdd.PipelinedRDD, pyspark.RDD))
result = pipelined_rdd.collect()
assert(result == [my_func(x) for x in num_list])

del my_func
def my_func(partition_iter) : yield sum(partition_iter)
result = rdd.mapPartitions(my_func).collect()
assert(len(result) == rdd.getNumPartitions())
assert(sum(result) == sum(num_list))
#rdd.mapPartitionsWithIndex
#rdd.mapPartitionsWithSplit
#rdd.mapValues

my_func = lambda x: list(range(x%3 + 1))
result = rdd.flatMap(my_func).collect()
assert(result == [y for x in num_list for y in my_func(x)])
#rdd.flatMapValues

# Filter
my_filter = lambda x : x%2 == 0
result = rdd.filter(my_filter).collect()
assert(result == [x for x in num_list if my_filter(x)])

# Grouping
# rdd.groupBy
# rdd.groupWith

# Join
# rdd.sample
# rdd.union

# Unsorted
result = rdd_kv.keys().collect()
assert(len(result) == len(key_val_pairs))
assert(set(result) == set(keys))

result = rdd_kv.values().collect()
assert(len(result) == len(key_val_pairs))
assert(set(result) == {val})

result = rdd.glom().collect()
flat_result = [x for sublist in result for x in sublist]
assert(len(result) == rdd.getNumPartitions())
assert(sorted(flat_result) == sorted(num_list))

########################################
# Persistance
########################################
# The available storage levels in Python include:
# - MEMORY_ONLY and MEMORY_ONLY_2, 
# - MEMORY_AND_DISK and MEMORY_AND_DISK_2, 
# - DISK_ONLY, DISK_ONLY_2, and DISK_ONLY_3

# rdd.cache
# rdd.persist

########################################
# Unsorted RDD methods
########################################
# rdd.aggregate
# rdd.barrier
# rdd.checkpoint
# rdd.fold
# rdd.histogram
# rdd.keyBy
# rdd.lookup
# rdd.partitionBy
# rdd.pipe
# rdd.randomSplit
# rdd.sortBy
# rdd.toDF
# rdd.toLocalIterator
# rdd.treeAggregate
# rdd.treeReduce
# rdd.unpersist
# rdd.withResources

################################################################################
# Spark SQL and DataFrames
################################################################################
from pyspark.sql import Row
from datetime import datetime, date
import pandas as pd
def df_equal(df1, df2):
    return (df1.schema == df2.schema) and (df1.collect() == df2.collect())

########################################
# Creata a DataFrame (copied from PySpark Quickstart docs)
########################################
# List of tuples
data = [
    (1, 2., 'string1', date(2000, 1, 1), datetime(2000, 1, 1, 12, 0)),
    (2, 3., 'string2', date(2000, 2, 1), datetime(2000, 1, 2, 12, 0)),
    (3, 4., 'string3', date(2000, 3, 1), datetime(2000, 1, 3, 12, 0))
]
schema = 'col1 long, col2 double, col3 string, col4 date, col5 timestamp'
df = spark.createDataFrame(data, schema)

# List of Row objects
data2 = [
    Row(col1=1, col2=2., col3='string1', col4=date(2000, 1, 1), col5=datetime(2000, 1, 1, 12, 0)),
    Row(col1=2, col2=3., col3='string2', col4=date(2000, 2, 1), col5=datetime(2000, 1, 2, 12, 0)),
    Row(col1=3, col2=4., col3='string3', col4=date(2000, 3, 1), col5=datetime(2000, 1, 3, 12, 0))
]
assert(df_equal(df, spark.createDataFrame(data2)))

# Pandas DataFrame
data3 = pd.DataFrame({
    'col1': [1, 2, 3],
    'col2': [2., 3., 4.],
    'col3': ['string1', 'string2', 'string3'],
    'col4': [date(2000, 1, 1), date(2000, 2, 1), date(2000, 3, 1)],
    'col5': [datetime(2000, 1, 1, 12, 0), datetime(2000, 1, 2, 12, 0), datetime(2000, 1, 3, 12, 0)]
})
assert(df_equal(df, spark.createDataFrame(data3)))

# RDD
data4 = spark.sparkContext.parallelize(data)
assert(df_equal(df, spark.createDataFrame(data4, schema)))

########################################
# Attributes
assert(type(df.schema) == pyspark.sql.types.StructType)

assert(df.columns == ['col1', 'col2', 'col3', 'col4', 'col5'])
assert(df.dtypes == [
    ('col1', 'bigint'), 
    ('col2', 'double'), 
    ('col3', 'string'), 
    ('col4', 'date'), 
    ('col5', 'timestamp')
])
#df.isStreaming
#df.sql_ctx
#df.storageLevel
#df.isLocal()


########################################
# Viewing
########################################
# Print Summaries
# df.printSchema()
# df.show(first_n_rows, vertical=False)
# df.explain()

# EDA
# df.count()
# df.describe()
# df.summary()
# df.first
# df.head()
# df.take
# df.tail()


# Selecting Columns
assert(type(df['col1']) == type(df.col1) == pyspark.sql.Column)
#assert(df['col1'] is df.col1) # Column object created on call

assert(type(df.select('col1')) 
    == type(df[['col1']]) 
    == pyspark.sql.dataframe.DataFrame)

#df.selectExpr

# Selecting Rows
# df.filter
# df.limit

# For Jupyter, set:
# > spark.conf.set('spark.sql.repl.eagerEval.enabled', True)
# > spark.conf.set('spark.sql.repl.eagerEval.maxNumRows', N)

########################################
# Modifying
########################################
# Add column
# df.withColumn
# df.withColumnRenamed

# Data Cleaning
assert(df.na.df is df)
#df.replace # (df.na.replace)
#df.fillna # (df.na.fill)
#df.drop
#df.dropDuplicates # (df.drop_duplicates)
#df.dropna # (df.na.drop)

# Conversions
#df.rdd
#df.toJSON()
#df.toPandas()

########################################
# Calculations
########################################
# Stats
assert(df.stat.df is df)
#df.cov (df.stat.cov)
#df.approxQuantile (df.stat.approxQuantile)
#df.sampleBy (df.stat.sampleBy)
#df.corr (df.stat.corr)
#df.freqItems (df.stat.freqItems)
#df.crosstab (df.stat.crosstab)

# Functions
from pyspark.sql import functions

# Apply user-defined functions (UDF)
# df.mapInPandas
# @pandas_udf()

########################################
# Grouping
########################################
#df.groupBy # (df.groupby)
df_grp = df.groupBy('col1')
assert(type(df_grp) == pyspark.sql.group.GroupedData)

# Group reduce
# df_grp.count()
# df_grp.sum()
# df_grp.avg() # (df_grp.mean())
# df_grp.min()
# df_grp.max()
# df_grp.agg()
# df_grp.apply()
# df_grp.applyInPandas()

# Regroup
# df_grp.pivot()
# df_grp.cogroup()

########################################
# SQL
########################################
#df.createGlobalTempView
#df.createOrReplaceTempView
#df.createTempView
#spark.udf.register()
#spark.sql()

########################################
# I/O
########################################
#df.write
#df.writeTo
#df.writeStream

########################################
# Unsorted methods
########################################
# Same name as RDD
# df.sample
# df.toDF
# df.randomSplit
# df.toLocalIterator
# df.checkpoint
# df.cache
# df.unpersist
# df.persist
# df.join
# df.distinct
# df.union
# df.subtract
# df.repartition
# df.coalesce
# df.foreach
# df.foreachPartition

# Not in RDD
# df.agg
# df.alias
# df.colRegex
# df.crossJoin
# df.cube
# df.exceptAll
# df.hint
# df.inputFiles
# df.intersect
# df.intersectAll
# df.orderBy
# df.registerTempTable
# df.repartitionByRange
# df.rollup
# df.sameSemantics
# df.semanticHash
# df.sort
# df.sortWithinPartitions
# df.transform
# df.unionAll
# df.unionByName
# df.where
# df.withWatermark


################################################################################
# Shared Variables
################################################################################
# Broadcast Variables (for caching large read-only values on executor nodes)
var = [1,2]
broadcast_var = sc.broadcast(var) # ships (aka broadcasts) variable to nodes
assert((broadcast_var.value == var) and not (broadcast_var.value is var))
assert(rdd.reduce(lambda a,b : broadcast_var.value) == var)
broadcast_var.unpersist() # memory freed on executor nodes
assert(rdd.reduce(lambda a,b : broadcast_var.value) == var) # var re-broadcast 
broadcast_var.destroy() # memory freed on all nodes. Can't be re-broadcast
# rdd.reduce(lambda a,b : broadcast_var.value) raises SparkException
# "Attempted to use Broadcast after it was destroyed...Task not serializable"
assert(rdd.reduce(lambda a,b : var) == var) # inefficient. var shipped with every call

# Accumulators (for accumulating a result updated by all nodes in parallel)
accum = sc.accumulator(0)
assert(accum.value == 0)
rdd.foreach(lambda x: accum.add(x))
assert(accum.value == sum(num_list))

################################################################################
# I/O
################################################################################
# sc.textFile()

################################################################################
# Spark Session API
################################################################################
# Attributes
print('Spark Version =',spark.version) # pyspark.__version__

# # References
# spark.builder
# spark.catalog
# spark.conf
# spark.read
# spark.readStream
# spark.sparkContext
# spark.streams
# spark.udf

# # Constructors
# spark.createDataFrame()
# spark.newSession()
# spark.range()

# # Other Functions
# spark.getActiveSession()
# spark.sql()
# spark.stop()
# spark.table()

################################################################################
# Spark Context API
################################################################################
# Attributes
print('SparkContext attributes')
print('applicationId        =',sc.applicationId)
print('appName              =',sc.appName)
print('defaultMinPartitions =',sc.defaultMinPartitions)
print('defaultParallelism   =',sc.defaultParallelism)
print('master               =',sc.master)
print('resources            =',sc.resources)
#print('sparkHome            =',sc.sparkHome)
print('sparkUser            =',sc.sparkUser())
print('startTime            =',sc.startTime)
print('uiWebUrl             =',sc.uiWebUrl)
print('version              =',sc.version)
print('environment:\n\t',sc.environment)

# References
# sc.statusTracker()

########################################
# Functions
########################################
# Constructors
# sc.accumulator()
# sc.broadcast()
# sc.emptyRDD()
# sc.parallelize()
# sc.range()
# sc.union()

# I/O
# sc.addFile()
# sc.addPyFile()
# sc.binaryFiles()
# sc.binaryRecords()
# sc.hadoopFile()
# sc.hadoopRDD()
# sc.newAPIHadoopFile()
# sc.newAPIHadoopRDD()
# sc.pickleFile()
# sc.sequenceFile()
# sc.textFile()
# sc.wholeTextFile()

# Task Management
# sc.cancelAllJobs()
# sc.cancelJobGroup()
# sc.stop()
# sc.runJob()
# sc.dump_profiles()
# sc.show_profiles()

# Environment/Configuration Management
# sc.getCheckpointDir()
# sc.getConf()
# sc.getLocalProperty()
# sc.getOrCreate()
# sc.setCheckpointDir()
# sc.setJobDescription()
# sc.setJobGroup()
# sc.setLocalProperty()
# sc.setLogLevel()
# sc.setSystemProperty()

# Other/Deprecated
# sc.profiler_collector
# sc.pythonExec
# sc.pythonVer
# sc.serializer

print("\n---- End Program ----\n")
################################################################################
# Teardown
################################################################################
print("Stopping Spark Session\n")
spark.stop()

print("===== END =====")
