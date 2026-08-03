import os
import json

from pyspark.sql import functions as F

# -----------------------------------------------------
# Python Paths
# -----------------------------------------------------

LOCAL_REPORT_FOLDER = "/media/sf_privacy_engine/outputs/reports/segmentation"

# -----------------------------------------------------
# Spark Paths
# -----------------------------------------------------

SPARK_REPORT_FOLDER = "file:///home/satish/analytics_output/segmentation"

os.makedirs(LOCAL_REPORT_FOLDER, exist_ok=True)


def customer_segmentation(df):

    print("\nRunning Spark Customer Segmentation...\n")

    # =====================================================
    # Age Groups
    # =====================================================

    if "age" in df.columns:

        age_df = (

            df.withColumn(

                "age_group",

                F.when(
                    (F.col("age") >= 18) &
                    (F.col("age") <= 25),
                    "18-25"
                )

                .when(
                    (F.col("age") >= 26) &
                    (F.col("age") <= 35),
                    "26-35"
                )

                .when(
                    (F.col("age") >= 36) &
                    (F.col("age") <= 45),
                    "36-45"
                )

                .when(
                    (F.col("age") >= 46) &
                    (F.col("age") <= 60),
                    "46-60"
                )

                .otherwise("60+")

            )

        )

        (

            age_df.groupBy("age_group")

                  .count()

                  .orderBy("age_group")

                  .write

                  .mode("overwrite")

                  .parquet(

                      f"{SPARK_REPORT_FOLDER}/age_groups"

                  )

        )

    # =====================================================
    # Income Segments
    # =====================================================

    if "monthly_income" in df.columns:

        income_df = (

            df.withColumn(

                "income_segment",

                F.when(
                    F.col("monthly_income") <= 50000,
                    "Low"
                )

                .when(
                    F.col("monthly_income") <= 100000,
                    "Middle"
                )

                .when(
                    F.col("monthly_income") <= 200000,
                    "Upper Middle"
                )

                .otherwise("High")

            )

        )

        (

            income_df.groupBy("income_segment")

                     .count()

                     .write

                     .mode("overwrite")

                     .parquet(

                         f"{SPARK_REPORT_FOLDER}/income_segments"

                     )

        )

    # =====================================================
    # Savings Segments
    # =====================================================

    if "savings_balance" in df.columns:

        savings_df = (

            df.withColumn(

                "savings_segment",

                F.when(
                    F.col("savings_balance") <= 100000,
                    "Low"
                )

                .when(
                    F.col("savings_balance") <= 500000,
                    "Medium"
                )

                .when(
                    F.col("savings_balance") <= 1000000,
                    "High"
                )

                .otherwise("Premium")

            )

        )

        (

            savings_df.groupBy("savings_segment")

                      .count()

                      .write

                      .mode("overwrite")

                      .parquet(

                          f"{SPARK_REPORT_FOLDER}/savings_segments"

                      )

        )

    # =====================================================
    # Account Type
    # =====================================================

    if "account_type" in df.columns:

        (

            df.groupBy("account_type")

              .count()

              .orderBy(F.desc("count"))

              .write

              .mode("overwrite")

              .parquet(

                  f"{SPARK_REPORT_FOLDER}/account_types"

              )

        )

    # =====================================================
    # Premium Customers
    # =====================================================

    premium_customers = 0

    if (

        "monthly_income" in df.columns

        and

        "savings_balance" in df.columns

    ):

        premium_customers = (

            df.filter(

                (F.col("monthly_income") >= 200000)

                &

                (F.col("savings_balance") >= 1000000)

            ).count()

        )

    # =====================================================
    # KPI Summary
    # =====================================================

    average_age = None
    average_income = None
    average_savings = None

    if "age" in df.columns:

        average_age = df.select(
            F.avg("age")
        ).first()[0]

    if "monthly_income" in df.columns:

        average_income = df.select(
            F.avg("monthly_income")
        ).first()[0]

    if "savings_balance" in df.columns:

        average_savings = df.select(
            F.avg("savings_balance")
        ).first()[0]

    kpis = {

        "total_customers": df.count(),

        "average_age":

            round(average_age, 2)

            if average_age else None,

        "average_income":

            round(average_income, 2)

            if average_income else None,

        "average_savings":

            round(average_savings, 2)

            if average_savings else None,

        "premium_customers":

            premium_customers

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

    print("\nSpark Customer Segmentation Complete.\n")

    return kpis