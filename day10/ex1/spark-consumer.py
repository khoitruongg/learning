from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType, TimestampType
import os

output_file = 'output/result.csv'

# Assuming df_raw is the streaming DataFrame
def foreach_batch_function(batch_df, batch_id):
    # Count the number of rows in each batch
    batch_count = batch_df.count()
    print(f"Batch {batch_id}: Number of rows = {batch_count}")
    
    # Write the batch data to CSV
    batch_df.write \
        .mode("append") \
        .csv(output_file)

# Ensure output directory exists
output_dir = os.path.dirname(output_file)
if output_dir and not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize Spark session
spark = SparkSession.builder \
    .appName("KafkaStreamProcessor") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# Define your schema (must match CSV row structure)
# Index,User Id,First Name,Last Name,Sex,Email,Phone,Date of birth,Job Title
schema = StructType() \
    .add("Index", IntegerType()) \
    .add("User Id", IntegerType()) \
    .add("First Name", StringType()) \
    .add("Last Name", StringType()) \
    .add("Sex", StringType()) \
    .add("Email", StringType()) \
    .add("Phone", StringType()) \
    .add("Date of birth", TimestampType()) \
    .add("Job Title", StringType())

# Read from Kafka
df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "realtime-data-2") \
    .load()

# Kafka values are in binary, decode and parse JSON
df_parsed = df_raw.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select("data.*")

# Example processing: just show the data in the console
console_query = df_parsed.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Write the output to CSV files
query = df_parsed.writeStream \
    .foreachBatch(foreach_batch_function) \
    .outputMode("append") \
    .start()

query.awaitTermination()
console_query.awaitTermination()
