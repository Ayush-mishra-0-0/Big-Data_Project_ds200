from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType
import os
import shutil
import time
import numpy as np
import pandas as pd
import joblib

# Load the XGBoost model
xgb_model = joblib.load("xgb_model.joblib")

# Create Spark session
spark = SparkSession.builder \
    .appName("MalwarePrediction") \
    .getOrCreate()

# Define the Kafka schema
schema = StructType().add("filename", StringType()).add("content", StringType())

# Read from Kafka topic
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", kafka_topic) \
    .load()

# Parse JSON message from Kafka
parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema).alias("data")) \
    .select("data.filename", "data.content")

# Define preprocessing functions
def convert_bytes_to_txt(content):
    if(file.endswith("bytes")):
        shutil.copyfile(file, file.split('.')[0] + "_copy.bytes")
        time.sleep(1) 
        file=file.split('.')[0]
        text_file = open(file+".txt", 'w+')
        with open(file+".bytes","r") as fp:
            lines=""
            for line in fp:
                a=line.rstrip().split(" ")[1:]
                b=' '.join(a)
                b.lower()
                b=b+"\n"
                text_file.write(b)
            fp.close()
            os.remove(file+".bytes")
        text_file.close()
        os.rename(file+"_copy.bytes",file+".bytes")
        return content

def convert_to_lowercase(input_str):
    output_str= ""
    if input_str[0]=='0' and input_str[1].isdigit():
        return input_str[1:]
    if input_str[0].isdigit() and input_str[1].isdigit():
        return input_str
    if len(input_str) == 2 and input_str[0].isupper() and input_str[1].isdigit():
        output_str = input_str[0].lower() + input_str[1]
        return output_str
    if len(input_str) >= 2 and input_str[0].isdigit() and input_str[1].isupper():
        output_str = input_str[0] + input_str[1].lower()
        return output_str
    if len(input_str) == 2 and input_str[0].isupper() and input_str[1].isupper():
        output_str = input_str[0].lower() + input_str[1].lower()
        return output_str
    else:
        return input_str

# Define UDFs (User Defined Functions) for preprocessing
convert_bytes_udf = spark.udf.register("convert_bytes_to_txt", convert_bytes_to_txt, StringType())
convert_lowercase_udf = spark.udf.register("convert_to_lowercase", convert_to_lowercase, StringType())

# Apply preprocessing UDFs to the content column
preprocessed_df = parsed_df.withColumn("preprocessed_content", convert_bytes_udf(col("content")))
preprocessed_df = preprocessed_df.withColumn("lowercase_content", convert_lowercase_udf(col("preprocessed_content")))

# Perform prediction
result_df = preprocessed_df.withColumn("prediction", predict_malware(col("filename"), col("lowercase_content")))

# Output results to console (for testing)
query = result_df \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Await termination
query.awaitTermination()
