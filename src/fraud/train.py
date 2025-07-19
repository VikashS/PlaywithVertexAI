import argparse
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os


def run_train(data_path: str, model_output_path: str):
    input_file = os.path.join(data_path, "processed_data.csv")
    print(f"Starting training with data from {input_file}")
    df = pd.read_csv(input_file)

    # Dummy training
    X = df[['new_feature']]
    y = [0, 1] * (len(df) // 2)

    model = RandomForestClassifier()
    model.fit(X, y)
    print("Training complete.")

    # The pipeline passes a GCS URI for the directory. We append a filename.
    output_file = os.path.join(model_output_path, 'model.joblib')
    joblib.dump(model, output_file)
    print(f"Model saved to {output_file}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-path', type=str, required=True)
    parser.add_argument('--model-output-path', type=str, required=True)
    args = parser.parse_args()

    run_train(args.data_path, args.model_output_path)