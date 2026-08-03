"""
Regex Feature Extraction

Each function returns:
1 -> Pattern matched
0 -> Pattern not matched
"""

import re


# -----------------------------------------------------
# Email
# -----------------------------------------------------

EMAIL_REGEX = re.compile(
    r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
)

def is_email(value):

    if value is None:
        return 0

    return int(bool(EMAIL_REGEX.fullmatch(str(value).strip())))


# -----------------------------------------------------
# Phone Number (Indian)
# -----------------------------------------------------

PHONE_REGEX = re.compile(
    r'^[6-9]\d{9}$'
)

def is_phone(value):

    if value is None:
        return 0

    value = str(value).replace(" ", "").replace("-", "")

    return int(bool(PHONE_REGEX.fullmatch(value)))


# -----------------------------------------------------
# PAN Card
# Example: ABCDE1234F
# -----------------------------------------------------

PAN_REGEX = re.compile(
    r'^[A-Z]{5}[0-9]{4}[A-Z]$'
)

def is_pan(value):

    if value is None:
        return 0

    return int(bool(PAN_REGEX.fullmatch(str(value).strip().upper())))


# -----------------------------------------------------
# Aadhaar
# Example: 123412341234
# -----------------------------------------------------

AADHAAR_REGEX = re.compile(
    r'^\d{12}$'
)

def is_aadhaar(value):

    if value is None:
        return 0

    value = str(value).replace(" ", "")

    return int(bool(AADHAAR_REGEX.fullmatch(value)))


# -----------------------------------------------------
# Passport (Indian)
# Example: A1234567
# -----------------------------------------------------

PASSPORT_REGEX = re.compile(
    r'^[A-Z][0-9]{7}$'
)

def is_passport(value):

    if value is None:
        return 0

    return int(bool(PASSPORT_REGEX.fullmatch(str(value).strip().upper())))


# -----------------------------------------------------
# Run all regex checks
# -----------------------------------------------------

def extract_regex_features(value):

    return {

        "regex_email": is_email(value),

        "regex_phone": is_phone(value),

        "regex_pan": is_pan(value),

        "regex_aadhaar": is_aadhaar(value),

        "regex_passport": is_passport(value)

    }