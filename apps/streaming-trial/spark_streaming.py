from pyspark.sql import SparkSession

# Create a local StreamingContext with two working thread and batch interval of 1 second
import os
import time

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 pyspark-shell'
spark = SparkSession \
    .builder \
    .master("spark://spark-container-spark-master-1:7077") \
    .appName("Python streaming trial") \
    .getOrCreate()

dsraw = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "172.23.0.2:9095") \
  .option("subscribe", "quickstart") \
  .option("startingOffsets", "earliest") \
  .load()
dsraw.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

query = dsraw \
    .writeStream \
    .outputMode("update") \
    .format("console") \
    .start()

# raw = spark.sql("select * from `kafka-streaming-messages`")
# raw.show()

query.awaitTermination()
