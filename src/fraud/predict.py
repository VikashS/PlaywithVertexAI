import argparse
import pandas as pd
import joblib
import os


def run_predict(data_path: str, model_path: str, predictions_output_path: str):
    input_file = os.path.join(data_path, "processed_data.csv")
    model_file = os.path.join(model_path, 'model.joblib')

    print(f"Loading model from {model_file} and data from {input_file}")
    model = joblib.load(model_file)
    df = pd.read_csv(input_file)
    X = df[['new_feature']]

    predictions = model.predict(X)
    pd.DataFrame(predictions, columns=['prediction']).to_csv(
        os.path.join(predictions_output_path, 'predictions.csv'), index=False
    )
    print(f"Predictions saved to {predictions_output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-path', type=str, required=True)
    parser.add_argument('--model-path', type=str, required=True)
    parser.add_argument('--predictions-output-path', type=str, required=True)
    args = parser.parse_args()

    run_predict(args.data_path, args.model_path, args.predictions_output_path)