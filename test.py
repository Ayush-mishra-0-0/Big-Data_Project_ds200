from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split

spark = SparkSession.builder \
    .appName("FileProcessing") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Read from Kafka topic
lines = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "file-upload-topic") \
    .load()

# Convert binary data to string
lines = lines.selectExpr("CAST(value AS STRING)")

# Split the lines into words
words = lines.select(
    explode(split(lines.value, " ")).alias("word")
)

# Generate running word count
wordCounts = words.groupBy("word").count()

# Start the streaming query
query = wordCounts \
    .writeStream \
    .outputMode("update") \
    .format("console") \
    .start()

query.awaitTermination()
