from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pyspark.sql.functions import col, when
from pyspark.sql.types import DoubleType
import os

MODEL_PATH = "/app/models/machine_failure_model"
INPUT = "/app/data/processed"

host = os.getenv("POSTGRES_HOST", "postgres")
port = os.getenv("POSTGRES_PORT", "5432")
db = os.getenv("POSTGRES_DB", "industrial")
user = os.getenv("POSTGRES_USER", "industrial")
password = os.getenv("POSTGRES_PASSWORD", "industrial")
jdbc_url = f"jdbc:postgresql://{host}:{port}/{db}"
props = {"user":user,"password":password,"driver":"org.postgresql.Driver"}

spark = (SparkSession.builder.appName("SmartIndustrialPrediction").master("local[*]").getOrCreate())
spark.sparkContext.setLogLevel("WARN")
df = spark.read.parquet(INPUT)
model = PipelineModel.load(MODEL_PATH)
predictions = model.transform(df)
result = (predictions
    .withColumn("failure_probability", col("probability")[1].cast(DoubleType()))
    .withColumn("risk_level", when(col("failure_probability") >= 0.80, "HIGH").when(col("failure_probability") >= 0.50, "MEDIUM").otherwise("LOW"))
    .select("machine_id","prediction","failure_probability","risk_level","temperature","vibration","pressure","rpm","current","humidity","operating_hours"))
result.write.jdbc(url=jdbc_url, table="machine_predictions", mode="append", properties=props)
print("Predictions written to PostgreSQL.")
result.select("machine_id","prediction","failure_probability","risk_level").show(20, truncate=False)
spark.stop()
