import os
import pandas as pd

from regex_features import extract_regex_features


# --------------------------------------------------------
# KEYWORDS
# --------------------------------------------------------

KEYWORDS = {

    "contains_name": ["name"],

    "contains_email": ["email", "mail"],

    "contains_phone": ["phone", "mobile", "contact"],

    "contains_mobile": ["mobile"],

    "contains_address": ["address"],

    "contains_pan": ["pan"],

    "contains_aadhaar": ["aadhaar", "aadhar"],

    "contains_passport": ["passport"],

    "contains_account": ["account"],

    "contains_card": ["card"],

    "contains_salary": ["salary", "income"],

    "contains_age": ["age"],

    "contains_dob": ["dob", "birth"]

}


# --------------------------------------------------------
# Keyword Features
# --------------------------------------------------------

def keyword_features(column_name):

    column_name = column_name.lower()

    features = {}

    for feature, words in KEYWORDS.items():

        features[feature] = int(
            any(word in column_name for word in words)
        )

    return features


# --------------------------------------------------------
# Structural Features
# --------------------------------------------------------

def structural_features(column_name):

    return {

        "column_length": len(column_name),

        "word_count": len(column_name.replace("-", "_").split("_")),

        "contains_underscore": int("_" in column_name),

        "contains_hyphen": int("-" in column_name),

        "contains_space": int(" " in column_name),

        "contains_digits": int(any(c.isdigit() for c in column_name)),

        "is_uppercase": int(column_name.isupper()),

        "is_lowercase": int(column_name.islower()),

        "is_titlecase": int(column_name.istitle())

    }


# --------------------------------------------------------
# Sample Features
# --------------------------------------------------------

def sample_features(value):

    value = str(value)

    return {

        "sample_length": len(value),

        "sample_is_numeric": int(value.isdigit()),

        "sample_is_alpha": int(value.replace(" ", "").isalpha()),

        "sample_is_alphanumeric": int(value.replace(" ", "").isalnum())

    }


# --------------------------------------------------------
# Extract Features
# --------------------------------------------------------

def extract_features(row):

    column = str(row["Column_Name"])

    value = str(row["Sample_Value"])

    features = {}

    features.update(structural_features(column))

    features.update(keyword_features(column))

    features.update(sample_features(value))

    features.update(extract_regex_features(value))

    
    features["PII_Label"] = row["PII_Label"]
    features["Sensitivity"] = row["Sensitivity"]
    features["Transformation"] = row["Transformation"]
    

    return features


# --------------------------------------------------------
# Main
# --------------------------------------------------------

def main():

    df = pd.read_csv("data/training_columns.csv")

    feature_rows = []

    for _, row in df.iterrows():

        feature_rows.append(extract_features(row))

    feature_df = pd.DataFrame(feature_rows)

    os.makedirs("data", exist_ok=True)

    feature_df.to_csv("data/features.csv", index=False)

    print("=" * 60)

    print("Feature Extraction Complete")

    print("=" * 60)

    print(feature_df.head())

    print()

    print("Rows :", len(feature_df))

    print("Columns :", len(feature_df.columns))


if __name__ == "__main__":

    main()