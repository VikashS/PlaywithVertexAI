# pipelines/fraud_pipeline.py
import os
from kfp import dsl
from kfp.v2 import compiler

# Define the path to components relative to this script
COMPONENTS_DIR = os.path.dirname(__file__) + '/components'

# Load components from their YAML files
common_etl_op = dsl.load_component_from_file(f'{COMPONENTS_DIR}/common_etl_component.yaml')
train_op = dsl.load_component_from_file(f'{COMPONENTS_DIR}/train_component.yaml')
predict_op = dsl.load_component_from_file(f'{COMPONENTS_DIR}/predict_component.yaml')
final_train_op = dsl.load_component_from_file(f'{COMPONENTS_DIR}/final_train_component.yaml')


@dsl.pipeline(
    name='fraud-detection-pipeline',
    description='A complex pipeline with parallel training and a final model.'
)
def fraud_pipeline(
        project_id: str,
        location: str,
        raw_data_gcs_path: str
):
    # 1. Common ETL
    etl_task = common_etl_op(
        input_data_path=raw_data_gcs_path
    )

    # 2. Parallel Training & Prediction
    predictions_outputs = []
    for i in range(2):  # Example for 2 parallel models
        train_task = train_op(
            data_path=etl_task.outputs['processed_data_output_path']
        ).set_display_name(f'Parallel-Train-{i + 1}')

        predict_task = predict_op(
            model_path=train_task.outputs['model_output_path'],
            data_path=etl_task.outputs['processed_data_output_path']
        ).set_display_name(f'Parallel-Predict-{i + 1}')

        predictions_outputs.append(predict_task.outputs['predictions_output_path'])

    # 3. Final Model Training (using outputs of previous predictions)
    final_train_task = final_train_op(
        prediction_inputs=predictions_outputs  # KFP automatically handles passing the list
    )

    # 4. Final Prediction
    final_predict_task = predict_op(
        model_path=final_train_task.outputs['final_model_path'],
        data_path=etl_task.outputs['processed_data_output_path']
    )


if __name__ == '__main__':
    compiler.Compiler().compile(
        pipeline_func=fraud_pipeline,
        package_path='fraud_pipeline.json'  # This will be created in the root directory
    )
    print("Pipeline compiled to fraud_pipeline.json")