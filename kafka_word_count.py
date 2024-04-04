from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split

# Create Spark session
spark = SparkSession.builder \
    .appName("WordCount") \
    .getOrCreate()

# Define Kafka parameters
kafka_topic = "file-upload-topic"
kafka_bootstrap_servers = "localhost:9092"

# Read from Kafka topic
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .load()

# Convert binary value to string and split words
words_df = df.selectExpr("CAST(value AS STRING) as text") \
    .select(explode(split("text", "\\s+")).alias("word"))

# Perform word count
word_counts_df = words_df.groupBy("word").count()

# Output results to console
query = word_counts_df \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

# Await termination
query.awaitTermination()
