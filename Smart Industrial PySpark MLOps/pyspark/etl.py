from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, count, max as spark_max, min as spark_min, stddev, to_timestamp, when

INPUT = "/app/data/raw/machine_sensor_data.csv"
PROCESSED = "/app/data/processed"
FEATURES = "/app/data/features"

spark = SparkSession.builder.appName("SmartIndustrialETL").master("local[*]").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

schema = """
machine_id STRING,
timestamp STRING,
temperature DOUBLE,
vibration DOUBLE,
pressure DOUBLE,
rpm DOUBLE,
current DOUBLE,
humidity DOUBLE,
operating_hours DOUBLE,
failure INT
"""

df = spark.read.option("header", True).schema(schema).csv(INPUT)
clean = (df.withColumn("timestamp", to_timestamp("timestamp"))
    .dropDuplicates()
    .dropna(subset=["machine_id","timestamp","temperature","vibration","pressure","rpm","current","humidity","operating_hours","failure"])
    .filter(col("temperature").between(-20,150))
    .filter(col("vibration") >= 0)
    .filter(col("pressure") > 0)
    .filter(col("rpm") >= 0)
    .filter(col("current") >= 0)
    .filter(col("humidity").between(0,100))
    .filter(col("operating_hours") >= 0)
    .withColumn("temperature_high", when(col("temperature") >= 70, 1).otherwise(0))
    .withColumn("vibration_high", when(col("vibration") >= 3, 1).otherwise(0)))

clean.write.mode("overwrite").parquet(PROCESSED)

features = clean.groupBy("machine_id").agg(
    count("*").alias("reading_count"),
    avg("temperature").alias("temperature_avg"),
    spark_max("temperature").alias("temperature_max"),
    spark_min("temperature").alias("temperature_min"),
    avg("vibration").alias("vibration_avg"),
    spark_max("vibration").alias("vibration_max"),
    avg("pressure").alias("pressure_avg"),
    avg("rpm").alias("rpm_avg"),
    avg("current").alias("current_avg"),
    avg("humidity").alias("humidity_avg"),
    spark_max("operating_hours").alias("operating_hours_max"),
    stddev("temperature").alias("temperature_stddev"),
    stddev("vibration").alias("vibration_stddev"),
    avg("failure").alias("failure_rate"),
)
features.write.mode("overwrite").parquet(FEATURES)
print("ETL completed.")
spark.stop()
