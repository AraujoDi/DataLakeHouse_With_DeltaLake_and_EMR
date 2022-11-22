from pyspark.sql import SparkSession
from pyspark.sql.function import col, min, max

# Criando objeto da Spark Session
spark = (SparkSession.builder.appName("DeltaExercise")
.config("spark.jars.packages", "io.delta:delta-core_2.12:1.0.0")
.config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
.config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
.getOrCreate()
)

# Importa o mdulo das tabelas delta
from delta.tables import *

# Leitura de dados
enem = (
    spark.read.format("csv")
    .option("inferSchema", True)
    .option("header", True)
    .option("delimiter", ";")
    .load("s3://dtlk-diego-edc-tf/raw/data/enem")
)

# Escrever a tabela em stagin em formato delta
print("Writing delta table...")
(
    enem
    .write
    .modo("overwrite")
    .format("delta")
    .partitionBy("year")
    .save("s3://s3://dtlk-diego-edc-tf/staging-zone/enem")
)