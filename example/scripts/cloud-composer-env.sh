#!/bin/bash

source _env/setup.sh

gcloud composer environments create $CLOUD_COMPOSER_ENVIRONMENT_NAME \
  --location $CLOUD_COMPOSER_ENVIRONMENT_LOCATION \
  --airflow-configs api-auth_backend=airflow.api.auth.backend.default

AIRFLOW_URL=$(gcloud composer environments describe $CLOUD_COMPOSER_ENVIRONMENT_NAME \
  --location $CLOUD_COMPOSER_ENVIRONMENT_LOCATION \
  --format='value(config.airflowUri)')

echo $AIRFLOW_URL
curl -v $AIRFLOW_URL 2>&1 >/dev/null | grep "location:"
