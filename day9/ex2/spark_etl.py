from pyspark.sql import SparkSession
from pyspark.sql.functions import col, floor, months_between, current_date, upper
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType

def spark_transform(input_file_path):
    # Step 1: Initialize SparkSession
    spark = SparkSession.builder \
        .appName("CSV ETL Pipeline") \
        .getOrCreate()

    # spark.sparkContext.setLogLevel("ERROR")

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
    df = spark.read.csv(input_file_path, header=True, schema=schema)

    age = floor(months_between(current_date(), col("Date of birth")) / 12)

    # Step 3: Transform - Filter people older than 30 and uppercase city names
    transformed_df = df.withColumn("Job Title", upper(col("Job Title"))) \
                    .withColumn("Age", age) \
                    .orderBy(col("Index"))

    # Step 4: Load - Write the result to a Parquet file
    transformed_df.write.mode("overwrite").parquet("output/people_with_age.parquet")

    gender_filter_df = transformed_df.filter(col("Sex") == "Male") \
                        .filter(age > 30) \
                        .orderBy(col("Index"))
    gender_filter_df.show(10)

    return gender_filter_df.toJSON(), spark