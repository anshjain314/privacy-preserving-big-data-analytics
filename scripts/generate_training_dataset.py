import os
import random
import pandas as pd

from config.column_vocabulary import COLUMN_VOCABULARY
from config.labels import LABELS

from generators.sample_generators import GENERATORS
from generators.noise_generator import random_variation


ROWS_PER_COLUMN = 100


def generate_sample(category, column_name):

    generator = GENERATORS.get(category)

    if generator is None:
        return ""

    # SAFE fields use individual generators
    if category == "SAFE":
        safe_generator = generator.get(column_name)

        if safe_generator:
            return safe_generator()

        return ""

    return generator()


def generate_dataset():

    dataset = []

    for category, columns in COLUMN_VOCABULARY.items():

        label, sensitivity, transformation = LABELS[category]

        for column in columns:

            for _ in range(ROWS_PER_COLUMN):

                noisy_column = random_variation(column)

                sample_value = generate_sample(category, column)

                dataset.append({

                    "Column_Name": noisy_column,

                    "Sample_Value": sample_value,

                    "PII_Label": label,

                    "Sensitivity": sensitivity,

                    "Transformation": transformation

                })

    df = pd.DataFrame(dataset)

    df = df.sample(frac=1).reset_index(drop=True)

    os.makedirs("data", exist_ok=True)

    df.to_csv("data/training_columns.csv", index=False)

    print("=" * 60)
    print("Dataset Generated Successfully")
    print("=" * 60)
    print(f"Rows Generated : {len(df)}")
    print(f"Saved To       : data/training_columns.csv")


if __name__ == "__main__":
    generate_dataset()