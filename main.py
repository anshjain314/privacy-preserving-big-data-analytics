import pandas as pd

from privacy_engine.process_dataframe import process_dataframe
from analytics.descriptive import descriptive_statistics
from analytics.fraud import fraud_analysis
from analytics.credit import credit_risk_analysis
from analytics.segmentation import customer_segmentation
from analytics.report_generator import generate_executive_report


def main():

    print("=" * 70)
    print("PRIVACY PRESERVING BIG DATA ANALYTICS")
    print("=" * 70)

    print("\nLoading Dataset...")

    df = pd.read_csv("training_data.csv")

    print(f"Records : {len(df)}")
    print(f"Columns : {len(df.columns)}")

    print("\nRunning Adaptive Privacy Engine...")

    protected_df = process_dataframe(df)
    
    descriptive_results = descriptive_statistics(protected_df)

    print("\n==============================")
    print("DESCRIPTIVE ANALYTICS SUMMARY")
    print("==============================")

    for key, value in descriptive_results["kpis"].items():
        print(f"{key:<20}: {value}")

    fraud_results = fraud_analysis(protected_df)

    print("\n==============================")
    print("FRAUD ANALYTICS")
    print("==============================")

    for key, value in fraud_results["kpis"].items():
        print(f"{key:<20}: {value}")


    credit_results = credit_risk_analysis(protected_df)

    print("\n==============================")
    print("CREDIT RISK ANALYTICS")
    print("==============================")

    for key, value in credit_results["kpis"].items():
        print(f"{key:<25}: {value}")


    segmentation_results = customer_segmentation(protected_df)

    print("\n==============================")
    print("CUSTOMER SEGMENTATION")
    print("==============================")

    for key, value in segmentation_results["kpis"].items():
        print(f"{key:<25}: {value}")


    executive_report = generate_executive_report(

        descriptive_results,

        fraud_results,

        credit_results,

        segmentation_results
    )

    protected_df.to_csv(
        "outputs/protected_dataset.csv",
        index=False
    )

    print("\nProtected dataset saved successfully.")




if __name__ == "__main__":
    main()