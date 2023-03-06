import pyspark
from pyspark.sql import SparkSession

print(pyspark.__version__)
spark = SparkSession.builder.master("local[*]").appName("test").getOrCreate()
# spark = (
#     SparkSession.builder.master("spark://host.docker.internal:7077")
#     .appName("test")
#     .getOrCreate()
# )

df = spark.read.option("header", "true").csv("taxi+_zone_lookup.csv")

df.show()

df.write.parquet("zones")
