import csv
import datetime
import sys

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.sql.functions import *
from pyspark.sql.types import *


from pyspark.sql import SparkSession

def process_result_data(result_data):
    # Initialize Spark session
    print("Processing result data")
    print(result_data)
    schema = StructType([
            StructField("Name", StringType(), True),
            StructField("md5", StringType(), True),
            StructField("Machine", IntegerType(), True),
            StructField("SizeOfOptionalHeader", IntegerType(), True),
            StructField("Characteristics", IntegerType(), True),
            StructField("MajorLinkerVersion", IntegerType(), True),
            StructField("MinorLinkerVersion", IntegerType(), True),
            StructField("SizeOfCode", IntegerType(), True),
            StructField("SizeOfInitializedData", IntegerType(), True),
            StructField("SizeOfUninitializedData", IntegerType(), True),
            StructField("AddressOfEntryPoint", IntegerType(), True),
            StructField("BaseOfCode", IntegerType(), True),
            StructField("BaseOfData", IntegerType(), True),
            StructField("ImageBase", LongType(), True),
            StructField("SectionAlignment", IntegerType(), True),
            StructField("FileAlignment", IntegerType(), True),
            StructField("MajorOperatingSystemVersion", IntegerType(), True),
            StructField("MinorOperatingSystemVersion", IntegerType(), True),
            StructField("MajorImageVersion", IntegerType(), True),
            StructField("MinorImageVersion", IntegerType(), True),
            StructField("MajorSubsystemVersion", IntegerType(), True),
            StructField("MinorSubsystemVersion", IntegerType(), True),
            StructField("SizeOfImage", IntegerType(), True),
            StructField("SizeOfHeaders", IntegerType(), True),
            StructField("CheckSum", IntegerType(), True),
            StructField("Subsystem", IntegerType(), True),
            StructField("DllCharacteristics", IntegerType(), True),
            StructField("SizeOfStackReserve", IntegerType(), True),
            StructField("SizeOfStackCommit", IntegerType(), True),
            StructField("SizeOfHeapReserve", IntegerType(), True),
            StructField("SizeOfHeapCommit", IntegerType(), True),
            StructField("LoaderFlags", IntegerType(), True),
            StructField("NumberOfRvaAndSizes", IntegerType(), True),
            StructField("SectionsNb", IntegerType(), True),
            StructField("SectionsMeanEntropy", DoubleType(), True),
            StructField("SectionsMinEntropy", DoubleType(), True),
            StructField("SectionsMaxEntropy", DoubleType(), True),
            StructField("SectionsMeanRawsize", DoubleType(), True),
            StructField("SectionsMinRawsize", IntegerType(), True),
            StructField("SectionMaxRawsize", IntegerType(), True),
            StructField("SectionsMeanVirtualsize", DoubleType(), True),
            StructField("SectionsMinVirtualsize", IntegerType(), True),
            StructField("SectionMaxVirtualsize", IntegerType(), True),
            StructField("ImportsNbDLL", IntegerType(), True),
            StructField("ImportsNb", IntegerType(), True),
            StructField("ImportsNbOrdinal", IntegerType(), True),
            StructField("ExportNb", IntegerType(), True),
            StructField("ResourcesNb", IntegerType(), True),
            StructField("ResourcesMeanEntropy", DoubleType(), True),
            StructField("ResourcesMinEntropy", DoubleType(), True),
            StructField("ResourcesMaxEntropy", DoubleType(), True),
            StructField("ResourcesMeanSize", DoubleType(), True),
            StructField("ResourcesMinSize", IntegerType(), True),
            StructField("ResourcesMaxSize", IntegerType(), True),
            StructField("LoadConfigurationSize", IntegerType(), True),
            StructField("VersionInformationSize", IntegerType(), True)
        ])
    
    spark = SparkSession.builder.appName("DataFrame Creation").config("spark.hadoop.fs.defaultFS", "hdfs://mfg:9000").getOrCreate()
    
    # Create an empty DataFrame with the specified schema
    result_df = spark.createDataFrame(spark.sparkContext.emptyRDD(), schema)
    
    # Create a DataFrame for the new result_data
    result_data_df = spark.createDataFrame([result_data], schema)

    # Append the new DataFrame to result_df
    result_df = result_df.union(result_data_df)

    # Write DataFrame to HDFS
    result_df.write.csv("hdfs://mfg:9000/data/result_data", header=True, mode="overwrite")
