LABELS = {

    "PERSON_NAME": ("PII", "High", "Pseudonymize"),

    "EMAIL": ("PII", "High", "Hash"),

    "PHONE": ("PII", "High", "Tokenize"),

    "ADDRESS": ("PII", "High", "Generalize"),

    "PAN": ("PII", "Critical", "Tokenize"),

    "AADHAAR": ("PII", "Critical", "Tokenize"),

    "PASSPORT": ("PII", "Critical", "Tokenize"),

    "ACCOUNT": ("PII", "Critical", "Tokenize"),

    "CARD": ("PII", "Critical", "Tokenize"),

    "AGE": ("Non-PII", "Medium", "Bucketize"),

    "DOB": ("PII", "Medium", "Generalize"),

    "SALARY": ("Non-PII", "Medium", "Bucketize"),

    "CITY": ("Non-PII", "Low", "Keep"),

    "STATE": ("Non-PII", "Low", "Keep"),

    "COUNTRY": ("Non-PII", "Low", "Keep"),

    "SAFE": ("Non-PII", "Safe", "Keep")

}