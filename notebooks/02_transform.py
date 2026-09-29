# Databricks notebook source
# MAGIC %md
# MAGIC # Transform
# MAGIC Clean and standardize customer records from the bronze table.

# COMMAND ----------

dbutils.widgets.text("bronze_table", "", "Bronze table FQN")
dbutils.widgets.text("catalog", "main", "Unity Catalog name")
dbutils.widgets.text("schema", "etl_demo", "Schema name")

bronze_table = dbutils.widgets.get("bronze_table")
catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")

if not bronze_table:
    bronze_table = dbutils.jobs.taskValues.get(
        taskKey="extract", key="bronze_table", default=""
    )

if not bronze_table:
    raise ValueError("bronze_table must be passed as a parameter or task value")

silver_table = f"{catalog}.{schema}.customers_silver"

# COMMAND ----------

from pyspark.sql import functions as F

bronze_df = spark.table(bronze_table)

silver_df = (
    bronze_df.filter(F.col("customer_id").isNotNull())
    .withColumn("name", F.trim(F.col("name")))
    .withColumn("email", F.lower(F.trim(F.col("email"))))
    .withColumn("country", F.upper(F.trim(F.col("country"))))
    .withColumn("signup_date", F.to_date("signup_date"))
    .dropDuplicates(["customer_id"])
    .withColumn("_transformed_at", F.current_timestamp())
)

silver_df.write.format("delta").mode("overwrite").saveAsTable(silver_table)

row_count = silver_df.count()
print(f"Transform complete: {row_count} rows written to {silver_table}")

dbutils.jobs.taskValues.set(key="silver_table", value=silver_table)
dbutils.jobs.taskValues.set(key="row_count", value=str(row_count))
