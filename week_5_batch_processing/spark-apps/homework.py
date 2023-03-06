import pyspark
from pyspark.sql import SparkSession

print(pyspark.__version__)
spark = SparkSession.builder.master("local[*]").appName("homework").getOrCreate()
# spark = (
#     SparkSession.builder.master("spark://spark-master:7077")
#     .appName("homework")
#     .getOrCreate()
# )

df = spark.read.option("header", "true").csv(
    "/opt/data/fhvhv_tripdata_2021-06.csv.gz"
)

df.show()

# df.write.parquet("zones")
