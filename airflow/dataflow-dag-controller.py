from airflow import models
from airflow.operators.bash_operator import BashOperator
from airflow.operators import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

with models.DAG(
        "gcp_dataflow_template_scheduler",
        start_date=days_ago(1),
        schedule_interval=None
) as dag_runner:
    # Print the received dag_run configuration.
    # The DAG run configuration contains information about the
    # Cloud Storage object change.
    print_content = BashOperator(
        task_id='print_gcs_info',
        bash_command="echo Triggered from GCF: {{ dag_run.conf }}",
        dag=dag_runner)


    def set_schedules(**kwargs):
        schedule_conf = kwargs['dag_run'].conf
        Variable.set("schedule_conf", schedule_conf, serialize_json=True)


    update_schedule_var = PythonOperator(
        task_id='update_schedule_var',
        python_callable=set_schedules,
        dag=dag_runner,
        provide_context=True)
    print_content >> update_schedule_var
