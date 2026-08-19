import pandas as pd

from .feature_builder import build_features
from .predictor import predict_column
from .transformer import transform_column


# ==========================================================
# Safety-Net Overrides
# ==========================================================
# The ML classifier generalizes well to unseen column names, but can
# misfire when a real-world column's sample values differ from what
# the synthetic training data used (train/serve skew). These override
# lists act as a rule-based guardrail on top of the adaptive model:
#   - FORCE_PROTECT: critical PII that must NEVER be kept in plaintext,
#     regardless of what the model predicts.
#   - FORCE_KEEP: known-safe business/analytics fields that must NEVER
#     be transformed, since analytics modules depend on their exact
#     original values (e.g. loan_status, fraud_flag).
# ==========================================================

FORCE_PROTECT = {
    "card_number": "Tokenize",
    "credit_card": "Tokenize",
    "debit_card": "Tokenize",
    "atm_pin_hash": "Tokenize",
    "pan_number": "Tokenize",
    "aadhaar_number": "Tokenize",
    "passport_number": "Tokenize",
}

FORCE_KEEP = {
    "loan_status",
    "account_type",
    "account_status",
    "card_status",
    "kyc_status",
    "fraud_flag",
    "2fa_enabled",
    "last_txn_type",
    "last_txn_channel",
    "card_network",
    "consent_given",
    "pii_masked",
    "cibil_score",
    "credit_score",
    "loan_amount",
    "loan_emi",
    "emi_amount",
    "savings_balance",
    "monthly_income",
    "monthly_expenditure",
}


def apply_safety_overrides(column, predicted_strategy):

    col_lower = str(column).strip().lower()

    if col_lower in FORCE_PROTECT:
        return FORCE_PROTECT[col_lower], True

    if col_lower in FORCE_KEEP:
        return "Keep", True

    return predicted_strategy, False


def process_dataframe(df):

    df = df.copy()
    prediction_log = []
    for column in df.columns:
        sample = df[column].dropna()
        if sample.empty:
            sample_value = ""
        else:
            sample_value = sample.iloc[0]

        prediction = predict_column(column, sample_value)

        final_strategy, overridden = apply_safety_overrides(
            column, prediction["strategy"]
        )

        prediction_log.append({
            "Column": column,
            "PII": prediction["pii"],
            "Sensitivity": prediction["sensitivity"],
            "Strategy": final_strategy,
            "Overridden": overridden
            })
        df = transform_column(
            df,
            column,
            final_strategy
            )
    prediction_report = pd.DataFrame(prediction_log)
    print(prediction_report)
    prediction_report.to_csv(
        "prediction_report.csv",
        index=False
        )




    return df

if __name__ == "__main__":

    df = pd.read_csv("training_data.csv")
    protected_df = process_dataframe(df)

    print("\nProtected DataFrame:\n")
    print(protected_df)