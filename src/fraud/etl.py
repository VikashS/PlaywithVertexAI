import argparse
import pandas as pd
import os


def run_etl(data_path: str, processed_data_output_path: str):
    print(f"Starting ETL from {data_path}")
    df = pd.read_csv(data_path)
    # Simple ETL: drop nulls and add a feature
    df_processed = df.dropna()
    df_processed['new_feature'] = 100
    print("ETL complete.")

    # Save the processed data
    # The pipeline passes a GCS URI for the directory. We append a filename.
    output_file = os.path.join(processed_data_output_path, "processed_data.csv")
    df_processed.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-path', type=str, required=True)
    parser.add_argument('--processed-data-output-path', type=str, required=True)
    args = parser.parse_args()

    run_etl(args.data_path, args.processed_data_output_path)