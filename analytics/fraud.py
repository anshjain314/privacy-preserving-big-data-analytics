import os
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


OUTPUT_FOLDER = "outputs/charts"
REPORT_FOLDER = "outputs/reports"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)


def fraud_analysis(df):

    print("\nGenerating Fraud Analytics...\n")

    total_customers = len(df)

    fraud_cases = int(df["fraud_flag"].sum())

    fraud_rate = round(
        fraud_cases / total_customers * 100,
        2
    )

    # =====================================================
    # Fraud vs Non-Fraud
    # =====================================================

    plt.figure(figsize=(6,6))

    df["fraud_flag"].value_counts().rename({
        0:"Non Fraud",
        1:"Fraud"
    }).plot(
        kind="pie",
        autopct="%1.1f%%"
    )

    plt.ylabel("")
    plt.title("Fraud Distribution")

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_FOLDER}/fraud_distribution.png"
    )

    plt.close()

    print("✓ Fraud distribution chart generated.")

    # =====================================================
    # Fraud by Account Type
    # =====================================================

    fraud_account = (
        df.groupby("account_type")["fraud_flag"]
        .mean()*100
    )

    fraud_account.to_csv(
        f"{REPORT_FOLDER}/fraud_by_account_type.csv"
    )

    plt.figure(figsize=(8,5))

    fraud_account.plot(kind="bar")

    plt.ylabel("Fraud Rate (%)")

    plt.title("Fraud Rate by Account Type")

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_FOLDER}/fraud_by_account_type.png"
    )

    plt.close()

    print("✓ Fraud by Account Type generated.")

    # =====================================================
    # Fraud by Card Network
    # =====================================================

    fraud_card = (
        df.groupby("card_network")["fraud_flag"]
        .mean()*100
    )

    plt.figure(figsize=(8,5))

    fraud_card.plot(kind="bar")

    plt.ylabel("Fraud Rate (%)")

    plt.title("Fraud Rate by Card Network")

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_FOLDER}/fraud_by_card_network.png"
    )

    plt.close()

    print("✓ Fraud by Card Network generated.")

    # =====================================================
    # Fraud by Transaction Channel
    # =====================================================

    if "last_txn_channel" in df.columns:

        fraud_channel = (
            df.groupby("last_txn_channel")["fraud_flag"]
            .mean()*100
        )

        plt.figure(figsize=(8,5))

        fraud_channel.plot(kind="bar")

        plt.ylabel("Fraud Rate (%)")

        plt.title("Fraud by Transaction Channel")

        plt.tight_layout()

        plt.savefig(
            f"{OUTPUT_FOLDER}/fraud_by_channel.png"
        )

        plt.close()

        print("✓ Fraud by Channel generated.")

    # =====================================================
    # Fraud by 2FA
    # =====================================================

    if "2fa_enabled" in df.columns:

        fraud_2fa = (
            df.groupby("2fa_enabled")["fraud_flag"]
            .mean()*100
        )

        plt.figure(figsize=(6,5))

        fraud_2fa.plot(kind="bar")

        plt.ylabel("Fraud Rate (%)")

        plt.title("Fraud vs 2FA")

        plt.tight_layout()

        plt.savefig(
            f"{OUTPUT_FOLDER}/fraud_vs_2fa.png"
        )

        plt.close()

        print("✓ Fraud vs 2FA generated.")

    # =====================================================
    # KPI Dictionary
    # =====================================================

    results = {

        "kpis": {

            "total_customers": total_customers,

            "fraud_cases": fraud_cases,

            "fraud_rate": fraud_rate,

            "non_fraud_cases":
                total_customers - fraud_cases

        },

        "charts": {

            "fraud_distribution":
                f"{OUTPUT_FOLDER}/fraud_distribution.png",

            "fraud_account":
                f"{OUTPUT_FOLDER}/fraud_by_account_type.png",

            "fraud_card":
                f"{OUTPUT_FOLDER}/fraud_by_card_network.png",

            "fraud_channel":
                f"{OUTPUT_FOLDER}/fraud_by_channel.png",

            "fraud_2fa":
                f"{OUTPUT_FOLDER}/fraud_vs_2fa.png"

        }

    }

    print("\nFraud Analytics Complete.\n")

    return results