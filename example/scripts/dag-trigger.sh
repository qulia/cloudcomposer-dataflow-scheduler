#!/bin/bash

source _env/setup.sh
gsutil cp ../schedule.json gs://$SCHEDULE_CONFIG_BUCKET/schedule.json
