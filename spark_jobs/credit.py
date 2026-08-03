import os
import json

from pyspark.sql import functions as F

# -----------------------------------------------------
# Python Paths
# -----------------------------------------------------

LOCAL_REPORT_FOLDER = "/media/sf_privacy_engine/outputs/reports/credit"

# -----------------------------------------------------
# Spark Paths
# -----------------------------------------------------

SPARK_REPORT_FOLDER = "file:///home/satish/analytics_output/credit"

os.makedirs(LOCAL_REPORT_FOLDER, exist_ok=True)


def credit_risk_analysis(df):

    print("\nRunning Spark Credit Risk Analytics...\n")

    # =====================================================
    # Overall KPIs
    # =====================================================

    total_customers = df.count()

    active_loans = 0
    default_loans = 0

    if "loan_status" in df.columns:

        active_loans = df.filter(
            F.col("loan_status") == "Active"
        ).count()

        default_loans = df.filter(
            F.col("loan_status") == "Default"
        ).count()

    default_rate = round(

        (default_loans / total_customers) * 100,

        2

    ) if total_customers else 0

    # =====================================================
    # Average Values
    # =====================================================

    average_loan = None
    average_credit_score = None
    average_emi = None

    if "loan_amount" in df.columns:

        average_loan = df.select(
            F.avg("loan_amount")
        ).first()[0]

    if "credit_score" in df.columns:

        average_credit_score = df.select(
            F.avg("credit_score")
        ).first()[0]

    if "emi_amount" in df.columns:

        average_emi = df.select(
            F.avg("emi_amount")
        ).first()[0]

    # =====================================================
    # Loan Status Distribution
    # =====================================================

    if "loan_status" in df.columns:

        (
            df.groupBy("loan_status")
              .count()
              .orderBy(F.desc("count"))
              .write
              .mode("overwrite")
              .parquet(
                  f"{SPARK_REPORT_FOLDER}/loan_status"
              )
        )

    # =====================================================
    # Loan Amount Statistics
    # =====================================================

    if "loan_amount" in df.columns:

        (

            df.agg(

                F.count("loan_amount").alias("customers"),

                F.avg("loan_amount").alias("average"),

                F.min("loan_amount").alias("minimum"),

                F.max("loan_amount").alias("maximum"),

                F.stddev("loan_amount").alias("stddev")

            )

            .write

            .mode("overwrite")

            .parquet(

                f"{SPARK_REPORT_FOLDER}/loan_amount_statistics"

            )

        )

    # =====================================================
    # Credit Score Statistics
    # =====================================================

    if "credit_score" in df.columns:

        (

            df.agg(

                F.count("credit_score").alias("customers"),

                F.avg("credit_score").alias("average"),

                F.min("credit_score").alias("minimum"),

                F.max("credit_score").alias("maximum"),

                F.stddev("credit_score").alias("stddev")

            )

            .write

            .mode("overwrite")

            .parquet(

                f"{SPARK_REPORT_FOLDER}/credit_score_statistics"

            )

        )

    # =====================================================
    # Default Rate by Account Type
    # =====================================================

    if (

        "account_type" in df.columns

        and

        "loan_status" in df.columns

    ):

        (

            df.groupBy("account_type")

              .agg(

                  F.count("*").alias("total_customers"),

                  F.sum(

                      F.when(

                          F.col("loan_status") == "Default",

                          1

                      ).otherwise(0)

                  ).alias("default_cases")

              )

              .withColumn(

                  "default_rate",

                  F.round(

                      (

                          F.col("default_cases")

                          /

                          F.col("total_customers")

                      ) * 100,

                      2

                  )

              )

              .write

              .mode("overwrite")

              .parquet(

                  f"{SPARK_REPORT_FOLDER}/default_by_account_type"

              )

        )

    # =====================================================
    # Default Rate by KYC Status
    # =====================================================

    if (

        "kyc_status" in df.columns

        and

        "loan_status" in df.columns

    ):

        (

            df.groupBy("kyc_status")

              .agg(

                  F.count("*").alias("total_customers"),

                  F.sum(

                      F.when(

                          F.col("loan_status") == "Default",

                          1

                      ).otherwise(0)

                  ).alias("default_cases")

              )

              .withColumn(

                  "default_rate",

                  F.round(

                      (

                          F.col("default_cases")

                          /

                          F.col("total_customers")

                      ) * 100,

                      2

                  )

              )

              .write

              .mode("overwrite")

              .parquet(

                  f"{SPARK_REPORT_FOLDER}/default_by_kyc"

              )

        )

    # =====================================================
    # KPI Summary
    # =====================================================

    kpis = {

        "total_customers": total_customers,

        "active_loans": active_loans,

        "default_loans": default_loans,

        "default_rate": default_rate,

        "average_loan_amount":

            round(average_loan, 2)

            if average_loan else None,

        "average_credit_score":

            round(average_credit_score, 2)

            if average_credit_score else None,

        "average_emi":

            round(average_emi, 2)

            if average_emi else None

    }

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

    print("\nSpark Credit Risk Analytics Complete.\n")

    return kpis