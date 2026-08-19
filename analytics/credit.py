import os
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


OUTPUT_FOLDER = "outputs/charts"
REPORT_FOLDER = "outputs/reports"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)


def _first_existing_column(df, candidates):
    for col in candidates:
        if col in df.columns:
            return col
    return None


def credit_risk_analysis(df):

    print("\nGenerating Credit Risk Analytics...\n")

    total_customers = len(df)

    # Support both the original expected names and the actual
    # production dataset's column names.
    credit_score_col = _first_existing_column(
        df, ["credit_score", "cibil_score"]
    )
    emi_col = _first_existing_column(
        df, ["emi_amount", "loan_emi"]
    )

    active_loans = (
        df["loan_status"] == "Active"
    ).sum() if "loan_status" in df.columns else 0

    default_loans = (
        df["loan_status"].isin(["Default", "Defaulted"])
    ).sum() if "loan_status" in df.columns else 0

    default_rate = round(
        (default_loans / total_customers) * 100,
        2
    ) if total_customers else 0

    average_loan = (
        round(df["loan_amount"].mean(), 2)
        if "loan_amount" in df.columns
        else None
    )

    average_cibil = (
        round(df[credit_score_col].mean(), 2)
        if credit_score_col is not None
        else None
    )

    average_emi = (
        round(df[emi_col].mean(), 2)
        if emi_col is not None
        else None
    )

    # ======================================================
    # Loan Status Distribution
    # ======================================================

    if "loan_status" in df.columns:

        loan_status = df["loan_status"].value_counts()

        loan_status.to_csv(
            f"{REPORT_FOLDER}/loan_status_report.csv"
        )

        plt.figure(figsize=(7,7))

        loan_status.plot(
            kind="pie",
            autopct="%1.1f%%"
        )

        plt.ylabel("")
        plt.title("Loan Status Distribution")

        plt.tight_layout()

        plt.savefig(
            f"{OUTPUT_FOLDER}/loan_status_distribution.png"
        )

        plt.close()

        print("Loan Status chart generated.")

    # ======================================================
    # Loan Amount Distribution
    # ======================================================

    if "loan_amount" in df.columns:

        plt.figure(figsize=(8,5))

        plt.hist(
            df["loan_amount"].dropna(),
            bins=30
        )

        plt.title("Loan Amount Distribution")
        plt.xlabel("Loan Amount")
        plt.ylabel("Customers")

        plt.tight_layout()

        plt.savefig(
            f"{OUTPUT_FOLDER}/loan_amount_distribution.png"
        )

        plt.close()

        print("Loan Amount chart generated.")

    # ======================================================
    # Credit Score Distribution
    # ======================================================

    if credit_score_col is not None:

        plt.figure(figsize=(8,5))

        plt.hist(
            df[credit_score_col].dropna(),
            bins=25
        )

        plt.title("Credit Score Distribution")
        plt.xlabel("Credit Score")
        plt.ylabel("Customers")

        plt.tight_layout()

        plt.savefig(
            f"{OUTPUT_FOLDER}/cibil_score_distribution.png"
        )

        plt.close()

        print("Credit Score chart generated.")

    # ======================================================
    # Default by Account Type
    # ======================================================

    if (
        "account_type" in df.columns
        and "loan_status" in df.columns
    ):

        default_account = (
            df.assign(
                default=df["loan_status"].isin(["Default", "Defaulted"])
            )
            .groupby("account_type")["default"]
            .mean() * 100
        )

        default_account.to_csv(
            f"{REPORT_FOLDER}/default_by_account_type.csv"
        )

        plt.figure(figsize=(8,5))

        default_account.plot(kind="bar")

        plt.ylabel("Default Rate (%)")
        plt.title("Loan Default by Account Type")

        plt.tight_layout()

        plt.savefig(
            f"{OUTPUT_FOLDER}/default_by_account_type.png"
        )

        plt.close()

        print("Default by Account Type generated.")

    # ======================================================
    # Default by KYC Status
    # ======================================================

    if (
        "kyc_status" in df.columns
        and "loan_status" in df.columns
    ):

        default_kyc = (
            df.assign(
                default=df["loan_status"].isin(["Default", "Defaulted"])
            )
            .groupby("kyc_status")["default"]
            .mean() * 100
        )

        default_kyc.to_csv(
            f"{REPORT_FOLDER}/default_by_kyc.csv"
        )

        plt.figure(figsize=(7,5))

        default_kyc.plot(kind="bar")

        plt.ylabel("Default Rate (%)")
        plt.title("Loan Default by KYC Status")

        plt.tight_layout()

        plt.savefig(
            f"{OUTPUT_FOLDER}/default_by_kyc.png"
        )

        plt.close()

        print("Default by KYC generated.")

    results = {

        "kpis": {

            "total_customers": total_customers,

            "active_loans": int(active_loans),

            "default_loans": int(default_loans),

            "default_rate": default_rate,

            "average_loan_amount": average_loan,

            "average_credit_score": average_cibil,

            "average_emi": average_emi

        },

        "charts": {

            "loan_status":
                f"{OUTPUT_FOLDER}/loan_status_distribution.png",

            "loan_amount":
                f"{OUTPUT_FOLDER}/loan_amount_distribution.png",

            "credit_score":
                f"{OUTPUT_FOLDER}/cibil_score_distribution.png",

            "default_account":
                f"{OUTPUT_FOLDER}/default_by_account_type.png",

            "default_kyc":
                f"{OUTPUT_FOLDER}/default_by_kyc.png"

        }

    }

    print("\nCredit Risk Analytics Complete.\n")

    return results