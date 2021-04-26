from airflow import models
from airflow.providers.google.cloud.operators.dataflow import (
    DataflowTemplatedJobStartOperator,
)
from airflow.models import Variable
from datetime import datetime


def create_dag(
        dag_id,
        schedule_interval,
        job_name,
        template,
        environment,
        parameters,
        location):
    dag = models.DAG(
        dag_id,
        start_date=datetime.now(),
        schedule_interval=schedule_interval)
    with dag:
        start_template_job = DataflowTemplatedJobStartOperator(
            task_id="start-template-job",
            job_name=job_name,
            template=template,
            # https://cloud.google.com/dataflow/docs/reference/rest/v1b3/RuntimeEnvironment
            environment=environment,
            parameters=parameters,
            location=location,
            wait_until_finished=True,
        )
    return dag


schedule_conf = Variable.get("schedule_conf", deserialize_json=True, default_var={})
print(f"schedule_conf {schedule_conf}")

if 'schedules' in schedule_conf:
    schedules = schedule_conf["schedules"]

    for sched in schedules:
        globals()[sched['dag_id']] = create_dag(
            dag_id=sched['dag_id'],
            schedule_interval=sched['schedule_interval'],
            job_name=sched['job_name'],
            template=sched['template'],
            environment=sched['environment'],
            parameters=sched['parameters'],
            location=sched['location'],
        )





