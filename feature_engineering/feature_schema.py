"""
Feature Schema for Adaptive Privacy Engine

This file defines every feature that the ML model will receive.
All feature extractors should produce these columns.
"""

FEATURE_COLUMNS = [

    # -----------------------------
    # Column Name Features
    # -----------------------------

    "column_length",
    "word_count",
    "contains_underscore",
    "contains_hyphen",
    "contains_space",
    "contains_digits",
    "is_uppercase",
    "is_lowercase",
    "is_titlecase",

    # -----------------------------
    # Keyword Features
    # -----------------------------

    "contains_name",
    "contains_email",
    "contains_phone",
    "contains_mobile",
    "contains_address",
    "contains_pan",
    "contains_aadhaar",
    "contains_passport",
    "contains_account",
    "contains_card",
    "contains_salary",
    "contains_age",
    "contains_dob",

    # -----------------------------
    # Sample Value Features
    # -----------------------------

    "sample_length",
    "sample_is_numeric",
    "sample_is_alpha",
    "sample_is_alphanumeric",

    # -----------------------------
    # Regex Features
    # -----------------------------

    "regex_email",
    "regex_phone",
    "regex_pan",
    "regex_aadhaar",
    "regex_passport"
]

TARGET_COLUMN = "PII_Label"