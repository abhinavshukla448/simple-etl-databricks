-- Databricks notebook source
-- MAGIC %md
-- MAGIC # One-time setup
-- MAGIC Create the Unity Catalog schema used by the ETL job. Run once per target (`etl_demo` / `etl_demo_dev`).

-- COMMAND ----------

-- MAGIC %python
-- MAGIC dbutils.widgets.text("catalog", "main", "Catalog")
-- MAGIC dbutils.widgets.text("schema", "etl_demo", "Schema")
-- MAGIC catalog = dbutils.widgets.get("catalog")
-- MAGIC schema = dbutils.widgets.get("schema")
-- MAGIC spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")
-- MAGIC print(f"Ready: {catalog}.{schema}")
