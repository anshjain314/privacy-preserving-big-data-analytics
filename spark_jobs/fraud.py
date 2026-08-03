import os
import json

from pyspark.sql import functions as F

# -----------------------------------------------------
# Python Paths
# -----------------------------------------------------

LOCAL_REPORT_FOLDER = "/media/sf_privacy_engine/outputs/reports/fraud"

# -----------------------------------------------------
# Spark Paths
# -----------------------------------------------------

SPARK_REPORT_FOLDER = "file:///home/satish/analytics_output/fraud"

os.makedirs(LOCAL_REPORT_FOLDER, exist_ok=True)


def fraud_analysis(df):

    print("\nRunning Spark Fraud Analytics...\n")

    # =====================================================
    # Overall Fraud KPIs
    # =====================================================

    total_customers = df.count()

    fraud_cases = df.filter(
        F.col("fraud_flag") == 1
    ).count()

    non_fraud_cases = total_customers - fraud_cases

    fraud_rate = round(
        (fraud_cases / total_customers) * 100,
        2
    )

    # =====================================================
    # Fraud Distribution
    # =====================================================

    (
        df.groupBy("fraud_flag")
          .count()
          .orderBy("fraud_flag")
          .write
          .mode("overwrite")
          .parquet(
              f"{SPARK_REPORT_FOLDER}/fraud_distribution"
          )
    )

    # =====================================================
    # Fraud by Account Type
    # =====================================================

    if "account_type" in df.columns:

        (
            df.groupBy("account_type")
              .agg(
                  (F.avg("fraud_flag") * 100).alias("fraud_rate")
              )
              .orderBy(F.desc("fraud_rate"))
              .write
              .mode("overwrite")
              .parquet(
                  f"{SPARK_REPORT_FOLDER}/fraud_by_account_type"
              )
        )

    # =====================================================
    # Fraud by Card Network
    # =====================================================

    if "card_network" in df.columns:

        (
            df.groupBy("card_network")
              .agg(
                  (F.avg("fraud_flag") * 100).alias("fraud_rate")
              )
              .orderBy(F.desc("fraud_rate"))
              .write
              .mode("overwrite")
              .parquet(
                  f"{SPARK_REPORT_FOLDER}/fraud_by_card_network"
              )
        )

    # =====================================================
    # Fraud by Transaction Channel
    # =====================================================

    if "last_txn_channel" in df.columns:

        (
            df.groupBy("last_txn_channel")
              .agg(
                  (F.avg("fraud_flag") * 100).alias("fraud_rate")
              )
              .orderBy(F.desc("fraud_rate"))
              .write
              .mode("overwrite")
              .parquet(
                  f"{SPARK_REPORT_FOLDER}/fraud_by_channel"
              )
        )

    # =====================================================
    # Fraud vs 2FA
    # =====================================================

    if "2fa_enabled" in df.columns:

        (
            df.groupBy("2fa_enabled")
              .agg(
                  (F.avg("fraud_flag") * 100).alias("fraud_rate")
              )
              .orderBy(F.desc("fraud_rate"))
              .write
              .mode("overwrite")
              .parquet(
                  f"{SPARK_REPORT_FOLDER}/fraud_vs_2fa"
              )
        )

    # =====================================================
    # KPI Summary
    # =====================================================

    kpis = {

        "total_customers": total_customers,

        "fraud_cases": fraud_cases,

        "non_fraud_cases": non_fraud_cases,

        "fraud_rate": fraud_rate

    }

    with open(

        f"{LOCAL_REPORT_FOLDER}/kpi_summary.json",

        "w"

    ) as file:

        json.dump(

            kpis,

            file,

            indent=4

        )

    print("\nSpark Fraud Analytics Complete.\n")

    return kpis