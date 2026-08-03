import os
import pandas as pd

REPORT_FOLDER = "outputs/reports"

os.makedirs(REPORT_FOLDER, exist_ok=True)


def generate_executive_report(
    descriptive_results,
    fraud_results,
    credit_results,
    segmentation_results
):

    print("\nGenerating Executive Report...\n")

    report = []

    # ==========================================
    # Descriptive KPIs
    # ==========================================

    for key, value in descriptive_results["kpis"].items():

        report.append({

            "Category": "Descriptive",

            "Metric": key,

            "Value": value

        })

    # ==========================================
    # Fraud KPIs
    # ==========================================

    for key, value in fraud_results["kpis"].items():

        report.append({

            "Category": "Fraud",

            "Metric": key,

            "Value": value

        })

    # ==========================================
    # Credit KPIs
    # ==========================================

    for key, value in credit_results["kpis"].items():

        report.append({

            "Category": "Credit Risk",

            "Metric": key,

            "Value": value

        })

    # ==========================================
    # Segmentation KPIs
    # ==========================================

    for key, value in segmentation_results["kpis"].items():

        report.append({

            "Category": "Customer Segmentation",

            "Metric": key,

            "Value": value

        })

    report_df = pd.DataFrame(report)

    report_df.to_csv(

        f"{REPORT_FOLDER}/executive_report.csv",

        index=False

    )

    print("✓ Executive report saved.")

    print(report_df)

    return report_df