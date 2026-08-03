import os
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


OUTPUT_FOLDER = "outputs/charts"
REPORT_FOLDER = "outputs/reports"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)


def descriptive_statistics(df):

    print("\nGenerating Descriptive Statistics...\n")

    # ==========================================================
    # Numeric Statistics
    # ==========================================================

    numeric_summary = df.describe()

    numeric_summary.to_csv(
        f"{REPORT_FOLDER}/numeric_statistics.csv"
    )

    print("✓ Numeric statistics saved.")

    # ==========================================================
    # Account Type Distribution
    # ==========================================================

    if "account_type" in df.columns:

        plt.figure(figsize=(8, 5))

        df["account_type"].value_counts().plot(kind="bar")

        plt.title("Account Type Distribution")
        plt.xlabel("Account Type")
        plt.ylabel("Customers")

        plt.tight_layout()

        plt.savefig(
            f"{OUTPUT_FOLDER}/account_type_distribution.png"
        )

        plt.close()

        print("✓ Account Type chart generated.")

    # ==========================================================
    # Card Network Distribution
    # ==========================================================

    if "card_network" in df.columns:

        plt.figure(figsize=(6, 6))

        df["card_network"].value_counts().plot(
            kind="pie",
            autopct="%1.1f%%"
        )

        plt.ylabel("")
        plt.title("Card Network Distribution")

        plt.tight_layout()

        plt.savefig(
            f"{OUTPUT_FOLDER}/card_network_distribution.png"
        )

        plt.close()

        print("✓ Card Network chart generated.")

    # ==========================================================
    # KYC Status
    # ==========================================================

    if "kyc_status" in df.columns:

        plt.figure(figsize=(7, 5))

        df["kyc_status"].value_counts().plot(kind="bar")

        plt.title("KYC Status")

        plt.tight_layout()

        plt.savefig(
            f"{OUTPUT_FOLDER}/kyc_status.png"
        )

        plt.close()

        print("✓ KYC Status chart generated.")

    # ==========================================================
    # Monthly Income Distribution
    # ==========================================================

    if "monthly_income" in df.columns:

        plt.figure(figsize=(8, 5))

        plt.hist(
            df["monthly_income"],
            bins=30
        )

        plt.title("Monthly Income Distribution")
        plt.xlabel("Income")
        plt.ylabel("Customers")

        plt.tight_layout()

        plt.savefig(
            f"{OUTPUT_FOLDER}/monthly_income.png"
        )

        plt.close()

        print("✓ Income distribution generated.")

    # ==========================================================
    # Prepare Results for Dashboard
    # ==========================================================

    results = {

        "numeric_statistics": numeric_summary,

        "kpis": {

            "total_customers": len(df),

            "total_columns": len(df.columns),

            "average_income":
                round(df["monthly_income"].mean(), 2)
                if "monthly_income" in df.columns else None,

            "average_savings":
                round(df["savings_balance"].mean(), 2)
                if "savings_balance" in df.columns else None,

            "average_loan":
                round(df["loan_amount"].mean(), 2)
                if "loan_amount" in df.columns else None,

        },

        "charts": {

            "account_type":
                f"{OUTPUT_FOLDER}/account_type_distribution.png",

            "card_network":
                f"{OUTPUT_FOLDER}/card_network_distribution.png",

            "kyc_status":
                f"{OUTPUT_FOLDER}/kyc_status.png",

            "monthly_income":
                f"{OUTPUT_FOLDER}/monthly_income.png"

        }

    }

    print("\nDescriptive Analytics Complete.\n")

    return results