import os
import json

from pyspark.sql import functions as F

# -----------------------------------------------------
# Python Paths
# -----------------------------------------------------

LOCAL_REPORT_FOLDER = "/media/sf_privacy_engine/outputs/reports/descriptive"

# -----------------------------------------------------
# Spark Paths
# -----------------------------------------------------

SPARK_REPORT_FOLDER = "file:///home/satish/analytics_output/descriptive"

os.makedirs(LOCAL_REPORT_FOLDER, exist_ok=True)


def descriptive_statistics(df):

    print("\nRunning Spark Descriptive Analytics...\n")

    # =====================================================
    # Numeric Statistics
    # =====================================================

    numeric_statistics = df.describe()

    numeric_statistics.write.mode("overwrite").parquet(
        f"{SPARK_REPORT_FOLDER}/numeric_statistics"
    )

    # =====================================================
    # Account Type Distribution
    # =====================================================

    if "account_type" in df.columns:

        (
            df.groupBy("account_type")
              .count()
              .orderBy(F.desc("count"))
              .write
              .mode("overwrite")
              .parquet(
                  f"{SPARK_REPORT_FOLDER}/account_type"
              )
        )

    # =====================================================
    # Card Network Distribution
    # =====================================================

    if "card_network" in df.columns:

        (
            df.groupBy("card_network")
              .count()
              .orderBy(F.desc("count"))
              .write
              .mode("overwrite")
              .parquet(
                  f"{SPARK_REPORT_FOLDER}/card_network"
              )
        )

    # =====================================================
    # KYC Status
    # =====================================================

    if "kyc_status" in df.columns:

        (
            df.groupBy("kyc_status")
              .count()
              .orderBy(F.desc("count"))
              .write
              .mode("overwrite")
              .parquet(
                  f"{SPARK_REPORT_FOLDER}/kyc_status"
              )
        )

    # =====================================================
    # Monthly Income Statistics
    # =====================================================

    if "monthly_income" in df.columns:

        income_stats = (

            df.agg(

                F.count("*").alias("customers"),

                F.mean("monthly_income").alias("average_income"),

                F.min("monthly_income").alias("minimum_income"),

                F.max("monthly_income").alias("maximum_income"),

                F.stddev("monthly_income").alias("std_income")

            )

        )

        income_stats.write.mode("overwrite").parquet(

            f"{SPARK_REPORT_FOLDER}/monthly_income"

        )

    # =====================================================
    # KPI Summary
    # =====================================================

    kpis = {

        "total_customers": df.count(),

        "total_columns": len(df.columns)

    }

    if "monthly_income" in df.columns:

        kpis["average_income"] = (

            df.select(

                F.avg("monthly_income")

            ).first()[0]

        )

    if "loan_amount" in df.columns:

        kpis["average_loan"] = (

            df.select(

                F.avg("loan_amount")

            ).first()[0]

        )

    if "savings_balance" in df.columns:

        kpis["average_savings"] = (

            df.select(

                F.avg("savings_balance")

            ).first()[0]

        )

    with open(

        f"{LOCAL_REPORT_FOLDER}/kpi_summary.json",

        "w"

    ) as file:

        json.dump(

            kpis,

            file,

            indent=4,

            default=float

        )

    print("\nSpark Descriptive Analytics Completed.\n")

    return kpis