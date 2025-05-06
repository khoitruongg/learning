import pandas as pd
from google.cloud import bigquery
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, floor, months_between, current_date, upper
from dotenv import load_dotenv
import os
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType

load_dotenv()

project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
data_set_id = os.getenv('BIG_QUERY_DATA_SET_ID')
data_set_table_id = os.getenv('BIG_QUERY_TABLE_ID')

def spark_transform():
    # Ask for enter min value
    age_filter_input = 30 #input("Enter min age to filter: ")
    try:
        age_filter = int(age_filter_input)
    except ValueError:
        print("❌ Invalid input. Please enter a valid integer for age.")
        exit(1)

    # Step 1: Initialize SparkSession
    spark = SparkSession.builder \
        .appName("Simple ETL Pipeline") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    # Index,User Id,First Name,Last Name,Sex,Email,Phone,Date of birth,Job Title
    schema = StructType([
        StructField("Index", IntegerType(), False),
        StructField("User Id", StringType(), False),
        StructField("First Name", StringType(), True),
        StructField("Last Name", StringType(), True),
        StructField("Sex", StringType(), True),
        StructField("Email", StringType(), True),
        StructField("Phone", StringType(), True),
        StructField("Date of birth", TimestampType(), True),
        StructField("Job Title", StringType(), True)
    ])

    # Step 2: Extract - Read CSV into a DataFrame
    df = spark.read.csv("people.csv", header=True, schema=schema)

    age = floor(months_between(current_date(), col("Date of birth")) / 12)

    # Step 3: Transform - Filter people older than 30 and uppercase city names
    transformed_df = df.withColumn("Job Title", upper(col("Job Title"))) \
                    .withColumn("Age", age) \
                    .orderBy(col("Index"))

    print(f"Original row count: {transformed_df.count()}")
    # Step 4: Load - Write the result to a Parquet file
    transformed_df.write.mode("overwrite").parquet("output/people_over_30.parquet")

    print('-----Result-------')
    transformed_df.show(10)

    print('----- Filter result with Male only and older 30 -------')
    # gender_filter_df = transformed_df.filter(col("Sex") == "Male") \
    #                     .filter(age > age_filter) \                       
    #                     .orderBy(col("Index"))
    gender_filter_df = transformed_df.filter(col("Sex") == "Male") \
                        .filter(age > age_filter) \
                        .orderBy(col("Index"))
    gender_filter_df.show(10)

    # Group by calculated age and count
    print('----- Group by calculated age  -------')
    grouped_df = transformed_df.groupBy(age.alias("Age")).count().orderBy("Age")
    
    grouped_df.show()

    #Save to CSV
    csv_output_path = f"output/people_over_{age_filter}.csv"
    transformed_df.toPandas().to_csv(csv_output_path, index=False)

    # Upload to Bigquey
    upload_to_bigquery(csv_output_path)

    # Stop SparkSession
    spark.stop()

def upload_to_bigquery(csv_output_path):
    bq_client = bigquery.Client()

    table_id = f"{project_id}.{data_set_id}.{data_set_table_id}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )

    with open(csv_output_path, "rb") as source_file:
        load_job = bq_client.load_table_from_file(
            source_file,
            table_id,
            job_config=job_config
        )

    load_job.result()  # Wait for job to complete
    print(f"✅ Uploaded to BigQuery table: {table_id}")

def main():
    spark_transform()

if __name__ == '__main__':
    main()
