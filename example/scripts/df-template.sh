#!/bin/bash


source _env/setup.sh

gsutil mb gs://$ARTIFACTS_BUCKET
gsutil mb gs://$RESULTS_BUCKET
gsutil mb gs://$DATAFLOW_TEMPLATES_BUCKET

FILE_PATH=../Appender.py
TEMPLATE_NAME=Appender_V1

echo "$PROJECT_ID $BUCKET_NAME"

# create template
python $FILE_PATH \
    --project=$PROJECT_ID \
    --runner=DataflowRunner \
    --input_path=gs://dataflow-samples/shakespeare/kinglear.txt \
    --output_path=gs://$RESULTS_BUCKET/out \
    --staging_location gs://$ARTIFACTS_BUCKET/staging \
    --temp_location gs://$ARTIFACTS_BUCKET/temp \
    --template_location gs://$DATAFLOW_TEMPLATES_BUCKET/$TEMPLATE_NAME


