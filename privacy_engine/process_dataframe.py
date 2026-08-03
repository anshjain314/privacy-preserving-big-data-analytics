import pandas as pd

from .feature_builder import build_features
from .predictor import predict_column
from .transformer import transform_column



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
        prediction_log.append({
            "Column": column,
            "PII": prediction["pii"],
            "Sensitivity": prediction["sensitivity"],
            "Strategy": prediction["strategy"]
            })
        df = transform_column(
            df,
            column,
            prediction["strategy"]
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

    