import os
import joblib
import pandas as pd

from xgboost import XGBClassifier

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


def train_classifier(target_column, model_name):

    df = pd.read_csv("data/features.csv")

    X = df.drop(
        columns=[
            "PII_Label",
            "Sensitivity",
            "Transformation"
        ]
    )

    y = df[target_column]

    encoder = LabelEncoder()

    y = encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        objective="multi:softprob" if len(set(y)) > 2 else "binary:logistic",
        eval_metric="mlogloss" if len(set(y)) > 2 else "logloss",
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("=" * 60)
    print(model_name.upper())
    print("=" * 60)

    print(f"Accuracy  : {accuracy_score(y_test, predictions):.4f}")
    print(f"Precision : {precision_score(y_test, predictions, average='weighted'):.4f}")
    print(f"Recall    : {recall_score(y_test, predictions, average='weighted'):.4f}")
    print(f"F1 Score  : {f1_score(y_test, predictions, average='weighted'):.4f}")

    print("\nConfusion Matrix\n")
    print(confusion_matrix(y_test, predictions))

    print("\nClassification Report\n")
    print(classification_report(y_test, predictions))

    os.makedirs("models/saved_models", exist_ok=True)

    joblib.dump(
        model,
        f"models/saved_models/{model_name}.pkl"
    )

    joblib.dump(
        encoder,
        f"models/saved_models/{model_name}_encoder.pkl"
    )

    print("\nModel Saved Successfully!")