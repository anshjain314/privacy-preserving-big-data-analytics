import os
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


OUTPUT_FOLDER = "outputs/charts"
REPORT_FOLDER = "outputs/reports"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)


def customer_segmentation(df):

    print("\nGenerating Customer Segmentation...\n")

    segmented_df = df.copy()

    # =====================================================
    # Convert numeric columns safely
    # =====================================================

    numeric_columns = [
        "age",
        "monthly_income",
        "savings_balance"
    ]

    for col in numeric_columns:

        if col in segmented_df.columns:

            converted = pd.to_numeric(
                segmented_df[col],
                errors="coerce"
            )

            # If conversion destroyed almost everything, the privacy
            # engine already bucketized this column (e.g. Age -> "Young Adult").
            # In that case keep the original categorical values instead.
            non_null_original = segmented_df[col].dropna()

            if len(non_null_original) > 0 and converted.notna().sum() < len(non_null_original) * 0.5:
                continue

            segmented_df[col] = converted

    # =====================================================
    # Age Groups
    # =====================================================

    if "age" in segmented_df.columns:

        age_data = segmented_df["age"].dropna()

        if pd.api.types.is_numeric_dtype(age_data):

            segmented_df.loc[age_data.index, "age_group"] = pd.cut(

                age_data,

                bins=[18,25,35,45,60,100],

                labels=[
                    "18-25",
                    "26-35",
                    "36-45",
                    "46-60",
                    "60+"
                ],

                include_lowest=True

            )

        else:

            # Already bucketized by the privacy engine (e.g. "Young Adult")
            segmented_df["age_group"] = age_data

        age_group = segmented_df["age_group"].value_counts().sort_index()

        age_group.to_csv(
            f"{REPORT_FOLDER}/age_groups.csv"
        )

        plt.figure(figsize=(8,5))

        age_group.plot(kind="bar")

        plt.title("Customer Age Groups")

        plt.ylabel("Customers")

        plt.tight_layout()

        plt.savefig(
            f"{OUTPUT_FOLDER}/age_groups.png"
        )

        plt.close()

        print("Γ£ô Age Group chart generated.")

    # =====================================================
    # Income Segments
    # =====================================================

    if "monthly_income" in segmented_df.columns:

        income_data = segmented_df["monthly_income"].dropna()

        segmented_df.loc[income_data.index, "income_segment"] = pd.cut(

            income_data,

            bins=[0,50000,100000,200000,float("inf")],

            labels=[
                "Low",
                "Middle",
                "Upper Middle",
                "High"
            ],

            include_lowest=True

        )

        income_segment = segmented_df["income_segment"].value_counts()

        income_segment.to_csv(
            f"{REPORT_FOLDER}/income_segments.csv"
        )

        plt.figure(figsize=(8,5))

        income_segment.plot(kind="bar")

        plt.title("Income Segmentation")

        plt.ylabel("Customers")

        plt.tight_layout()

        plt.savefig(
            f"{OUTPUT_FOLDER}/income_segments.png"
        )

        plt.close()

        print("Γ£ô Income Segmentation generated.")

    # =====================================================
    # Savings Segments
    # =====================================================

    if "savings_balance" in segmented_df.columns:

        savings_data = segmented_df["savings_balance"].dropna()

        segmented_df.loc[savings_data.index, "savings_segment"] = pd.cut(

            savings_data,

            bins=[0,100000,500000,1000000,float("inf")],

            labels=[
                "Low",
                "Medium",
                "High",
                "Premium"
            ],

            include_lowest=True

        )

        savings_segment = segmented_df["savings_segment"].value_counts()

        savings_segment.to_csv(
            f"{REPORT_FOLDER}/savings_segments.csv"
        )

        plt.figure(figsize=(8,5))

        savings_segment.plot(kind="bar")

        plt.title("Savings Segmentation")

        plt.ylabel("Customers")

        plt.tight_layout()

        plt.savefig(
            f"{OUTPUT_FOLDER}/savings_segments.png"
        )

        plt.close()

        print("Γ£ô Savings Segmentation generated.")

    # =====================================================
    # Account Type Distribution
    # =====================================================

    if "account_type" in segmented_df.columns:

        account_type = segmented_df["account_type"].value_counts()

        plt.figure(figsize=(8,5))

        account_type.plot(kind="bar")

        plt.title("Customer Account Types")

        plt.ylabel("Customers")

        plt.tight_layout()

        plt.savefig(
            f"{OUTPUT_FOLDER}/customer_account_types.png"
        )

        plt.close()

        print("Γ£ô Account Type chart generated.")

    # =====================================================
    # Premium Customers
    # =====================================================

    premium_customers = 0

    if (
        "monthly_income" in segmented_df.columns
        and "savings_balance" in segmented_df.columns
        and pd.api.types.is_numeric_dtype(segmented_df["monthly_income"])
        and pd.api.types.is_numeric_dtype(segmented_df["savings_balance"])
    ):

        premium_customers = len(

            segmented_df[

                (segmented_df["monthly_income"] >= 200000)
                &
                (segmented_df["savings_balance"] >= 1000000)

            ]

        )

    # =====================================================
    # KPI Results
    # =====================================================

    results = {

        "kpis": {

            "total_customers": len(segmented_df),

            "average_age":
                round(segmented_df["age"].mean(),2)
                if "age" in segmented_df.columns
                and pd.api.types.is_numeric_dtype(segmented_df["age"])
                else None,

            "average_income":
                round(segmented_df["monthly_income"].mean(),2)
                if "monthly_income" in segmented_df.columns
                and pd.api.types.is_numeric_dtype(segmented_df["monthly_income"])
                else None,

            "average_savings":
                round(segmented_df["savings_balance"].mean(),2)
                if "savings_balance" in segmented_df.columns
                and pd.api.types.is_numeric_dtype(segmented_df["savings_balance"])
                else None,

            "premium_customers": premium_customers

        },

        "charts": {

            "age_groups":
                f"{OUTPUT_FOLDER}/age_groups.png",

            "income_segments":
                f"{OUTPUT_FOLDER}/income_segments.png",

            "savings_segments":
                f"{OUTPUT_FOLDER}/savings_segments.png",

            "account_types":
                f"{OUTPUT_FOLDER}/customer_account_types.png"

        }

    }

    print("\nCustomer Segmentation Complete.\n")

    return results