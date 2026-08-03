import hashlib
import pandas as pd

TOKEN_MAP = {}

TOKEN_COUNTER = 1

PSEUDONYM_MAP = {}

PSEUDONYM_COUNTER = 1

def keep_column(df, column):
    return df

def hash_column(df, column):

    df = df.copy()

    df[column] = df[column].apply(
        lambda x: hashlib.sha256(
            str(x).encode()
        ).hexdigest()
        if pd.notna(x)
        else x
    )

    return df

def tokenize_column(df, column):

    global TOKEN_COUNTER

    df = df.copy()

    def tokenize(value):

        global TOKEN_COUNTER

        if pd.isna(value):
            return value

        value = str(value)

        if value not in TOKEN_MAP:

            TOKEN_MAP[value] = f"TOKEN_{TOKEN_COUNTER:06d}"

            TOKEN_COUNTER += 1

        return TOKEN_MAP[value]

    df[column] = df[column].apply(tokenize)

    return df

def pseudonymize_column(df, column):

    global PSEUDONYM_COUNTER

    df = df.copy()

    def pseudonymize(value):

        global PSEUDONYM_COUNTER

        if pd.isna(value):
            return value

        value = str(value)

        if value not in PSEUDONYM_MAP:

            PSEUDONYM_MAP[value] = f"USER_{PSEUDONYM_COUNTER:06d}"

            PSEUDONYM_COUNTER += 1

        return PSEUDONYM_MAP[value]

    df[column] = df[column].apply(pseudonymize)

    return df

def bucketize_column(df, column):

    df = df.copy()

    def bucket(value):

        if pd.isna(value):
            return value

        try:
            value = float(value)
        except:
            return value

        col = column.lower()

        # AGE
        if "age" in col:

            if value < 18:
                return "Child"

            elif value < 30:
                return "Young Adult"

            elif value < 45:
                return "Adult"

            elif value < 60:
                return "Middle Age"

            else:
                return "Senior"

        # SALARY
        elif "salary" in col:

            if value < 25000:
                return "Low"

            elif value <= 50000:
                return "Lower Middle"

            elif value <= 100000:
                return "Middle"

            elif value <= 200000:
                return "Upper Middle"

            else:
                return "High"

        return value

    df[column] = df[column].apply(bucket)

    return df

def generalize_column(df, column):

    df = df.copy()

    def generalize(value):

        if pd.isna(value):
            return value

        value = str(value)

        col = column.lower()

        # DOB
        if "dob" in col or "birth" in col:

            # Example: 12-06-1999 -> 1999
            if "-" in value:
                return value.split("-")[-1]

            elif "/" in value:
                return value.split("/")[-1]

            return value

        # ADDRESS
        elif "address" in col:

            # Example:
            # "45 MG Road, Bengaluru, Karnataka"
            # ->
            # "Bengaluru, Karnataka"

            parts = value.split(",")

            if len(parts) >= 2:
                return ",".join(parts[-2:]).strip()

            return value

        return value

    df[column] = df[column].apply(generalize)

    return df

TRANSFORMERS = {

    "Keep": keep_column,

    "Hash": hash_column,

    "Tokenize": tokenize_column,

    "Pseudonymize": pseudonymize_column,

    "Bucketize": bucketize_column,

    "Generalize": generalize_column

}

def transform_column(df, column, strategy):

    if strategy not in TRANSFORMERS:

        raise ValueError(
            f"Unknown transformation strategy: {strategy}"
        )

    return TRANSFORMERS[strategy](df, column)

if __name__ == "__main__":

    df = pd.DataFrame({

        "Customer_Name": ["Abhishek", "Rahul"],
        "Email": ["abc@gmail.com", "xyz@gmail.com"],
        "PAN": ["ABCDE1234F", "PQRSX5678L"],
        "Age": [22, 48],
        "Address": [
            "45 MG Road, Bengaluru, Karnataka",
            "22 Brigade Road, Mysuru, Karnataka"
        ],
        "Loan_Status": ["Approved", "Rejected"]

    })

    print("Before\n")
    print(df)

    df = transform_column(df, "Customer_Name", "Pseudonymize")
    df = transform_column(df, "Email", "Hash")
    df = transform_column(df, "PAN", "Tokenize")
    df = transform_column(df, "Age", "Bucketize")
    df = transform_column(df, "Address", "Generalize")
    df = transform_column(df, "Loan_Status", "Keep")

    print("\nAfter\n")
    print(df)