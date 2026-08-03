import re
import pandas as pd


# ===========================================================
# Keyword Lists
# ===========================================================

KEYWORDS = {
    "contains_name": ["name"],
    "contains_email": ["email", "mail"],
    "contains_phone": ["phone", "contact"],
    "contains_mobile": ["mobile"],
    "contains_address": ["address", "street"],
    "contains_pan": ["pan"],
    "contains_aadhaar": ["aadhaar", "aadhar"],
    "contains_passport": ["passport"],
    "contains_account": ["account", "acct"],
    "contains_card": ["card", "credit", "debit"],
    "contains_salary": ["salary", "income"],
    "contains_age": ["age"],
    "contains_dob": ["dob", "birth"]
}


# ===========================================================
# Regex Patterns
# ===========================================================

EMAIL_REGEX = re.compile(
    r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
)

PHONE_REGEX = re.compile(
    r'^[6-9]\d{9}$'
)

PAN_REGEX = re.compile(
    r'^[A-Z]{5}[0-9]{4}[A-Z]$'
)

AADHAAR_REGEX = re.compile(
    r'^\d{12}$'
)

PASSPORT_REGEX = re.compile(
    r'^[A-Z][0-9]{7}$'
)

def build_features(column_name, sample_value):

    column = str(column_name).strip()

    sample = "" if pd.isna(sample_value) else str(sample_value).strip()

    features = {}

    # -------------------------------------------------------
    # Structural Features
    # -------------------------------------------------------

    features["column_length"] = len(column)

    features["word_count"] = len(
        re.split(r"[_\-\s]+", column)
    )

    features["contains_underscore"] = int("_" in column)

    features["contains_hyphen"] = int("-" in column)

    features["contains_space"] = int(" " in column)

    features["contains_digits"] = int(
        any(ch.isdigit() for ch in column)
    )

    features["is_uppercase"] = int(column.isupper())

    features["is_lowercase"] = int(column.islower())

    features["is_titlecase"] = int(column.istitle())

    # -------------------------------------------------------
    # Keyword Features
    # -------------------------------------------------------

    lower = column.lower()

    for feature, words in KEYWORDS.items():

        features[feature] = int(
            any(word in lower for word in words)
        )

    # -------------------------------------------------------
    # Sample Features
    # -------------------------------------------------------

    features["sample_length"] = len(sample)

    features["sample_is_numeric"] = int(sample.isdigit())

    features["sample_is_alpha"] = int(sample.isalpha())

    features["sample_is_alphanumeric"] = int(sample.isalnum())

    # -------------------------------------------------------
    # Regex Features
    # -------------------------------------------------------

    features["regex_email"] = int(
        bool(EMAIL_REGEX.match(sample))
    )

    features["regex_phone"] = int(
        bool(PHONE_REGEX.match(sample))
    )

    features["regex_pan"] = int(
        bool(PAN_REGEX.match(sample))
    )

    features["regex_aadhaar"] = int(
        bool(AADHAAR_REGEX.match(sample))
    )

    features["regex_passport"] = int(
        bool(PASSPORT_REGEX.match(sample))
    )

    return features


if __name__ == "__main__":

    features = build_features(
        "Customer_Email",
        "abc@gmail.com"
    )

    for key, value in features.items():
        print(f"{key:<30} {value}")