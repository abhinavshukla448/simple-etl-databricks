# Databricks notebook source
# MAGIC %md
# MAGIC # Extract
# MAGIC Read raw customer CSV and persist a bronze Delta table for downstream tasks.

# COMMAND ----------

dbutils.widgets.text("raw_path", "", "Path to raw CSV")
dbutils.widgets.text("catalog", "main", "Unity Catalog name")
dbutils.widgets.text("schema", "etl_demo", "Schema name")

raw_path = dbutils.widgets.get("raw_path")
catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")

if not raw_path:
    raise ValueError("raw_path widget is required")

bronze_table = f"{catalog}.{schema}.customers_bronze"

# COMMAND ----------

from pyspark.sql import functions as F

raw_df = (
    spark.read.option("header", True)
    .option("inferSchema", True)
    .csv(raw_path)
    .withColumn("_ingested_at", F.current_timestamp())
)

raw_df.write.format("delta").mode("overwrite").saveAsTable(bronze_table)

row_count = raw_df.count()
print(f"Extract complete: {row_count} rows written to {bronze_table}")

dbutils.jobs.taskValues.set(key="bronze_table", value=bronze_table)
dbutils.jobs.taskValues.set(key="row_count", value=str(row_count))
