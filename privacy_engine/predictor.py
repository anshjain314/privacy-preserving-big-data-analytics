import os
import joblib
import pandas as pd

from .feature_builder import build_features

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_DIR = os.path.join(BASE_DIR, "models", "saved_models")

pii_model = joblib.load(
    os.path.join(MODEL_DIR, "pii_classifier.pkl")
)

pii_encoder = joblib.load(
    os.path.join(MODEL_DIR, "pii_label_encoder.pkl")
)

sensitivity_model = joblib.load(
    os.path.join(MODEL_DIR, "sensitivity_classifier.pkl")
)

sensitivity_encoder = joblib.load(
    os.path.join(MODEL_DIR, "sensitivity_classifier_encoder.pkl")
)

strategy_model = joblib.load(
    os.path.join(MODEL_DIR, "strategy_selector.pkl")
)

strategy_encoder = joblib.load(
    os.path.join(MODEL_DIR, "strategy_selector_encoder.pkl")
)

def prepare_features(column_name, sample_value):

    features = build_features(column_name, sample_value)

    return pd.DataFrame([features])

def predict_column(column_name, sample_value):

    X = prepare_features(column_name, sample_value)

    pii_prediction = pii_encoder.inverse_transform(
        pii_model.predict(X)
    )[0]

    sensitivity_prediction = sensitivity_encoder.inverse_transform(
        sensitivity_model.predict(X)
    )[0]

    strategy_prediction = strategy_encoder.inverse_transform(
        strategy_model.predict(X)
    )[0]

    return {
        "column": column_name,
        "pii": pii_prediction,
        "sensitivity": sensitivity_prediction,
        "strategy": strategy_prediction
    }

if __name__ == "__main__":

    tests = [

        ("Customer_Name", "Abhishek"),

        ("Email_Address", "abc@gmail.com"),

        ("PAN_Number", "ABCDE1234F"),

        ("Salary", "85000"),

        ("Loan_Status", "Approved"),

        ("Account_Balance", "150000"),

        ("Credit_Card", "4556737586899855")

    ]

    for column, sample in tests:

        result = predict_column(column, sample)

        print("=" * 60)

        print(result)