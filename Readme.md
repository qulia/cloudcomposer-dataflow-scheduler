# Cloud Composer Dataflow Scheduling

Automating Dataflow job scheduling with Cloud Composer/Airflow. Read more at: .

Folder structure:

- [airflow](airflow) folder contains the creator DAG which registers batch DAGs with Airflow. The controller DAG updates
  the variable with schedule config to be used by creator DAG in the next scan.

- [cloud-functions](cloud-functions) folder contains the logic to externally trigger the DAG upon Cloud Storage bucket's
  create/update event. Schedule configs like [schedule.json](example/schedule.json) is pushed to the bucket, which
  triggers the cloud function.

- [example](example) folder contains an end to end example on how to provision GCP resources and scheduling with a
  single command and JSON file. It illustrates how to pass in runtime parameters and configuration to the jobs. 
