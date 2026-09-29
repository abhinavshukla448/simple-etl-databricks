# Databricks notebook source
# MAGIC %md
# MAGIC # Load
# MAGIC Publish curated customer data to a gold table for analytics.

# COMMAND ----------

dbutils.widgets.text("silver_table", "", "Silver table FQN")
dbutils.widgets.text("catalog", "main", "Unity Catalog name")
dbutils.widgets.text("schema", "etl_demo", "Schema name")

silver_table = dbutils.widgets.get("silver_table")
catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")

if not silver_table:
    silver_table = dbutils.jobs.taskValues.get(
        taskKey="transform", key="silver_table", default=""
    )

if not silver_table:
    raise ValueError("silver_table must be passed as a parameter or task value")

gold_table = f"{catalog}.{schema}.customers_gold"

# COMMAND ----------

from pyspark.sql import functions as F

silver_df = spark.table(silver_table)

gold_df = (
    silver_df.select(
        "customer_id",
        "name",
        "email",
        "country",
        "signup_date",
        F.when(F.col("country") == "US", "NA")
        .when(F.col("country").isin("UK", "DE", "IT"), "EU")
        .otherwise("OTHER")
        .alias("region"),
        "_transformed_at",
    )
    .withColumn("_loaded_at", F.current_timestamp())
)

gold_df.write.format("delta").mode("overwrite").saveAsTable(gold_table)

row_count = gold_df.count()
print(f"Load complete: {row_count} rows written to {gold_table}")

display(gold_df.orderBy("customer_id"))
