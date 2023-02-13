# Week 2 Notes

- prefect deployment build flows/03_deployments/parameterized_flow.py:etl_parent_flow -n "Parameterized ETL" -o ./deployments/etl_parent_flow.yaml

- prefect deployment apply ./deployments/etl_parent_flow-deployment.yaml

- prefect deployment build flows/04_homework/q1_etl_web_to_gcs.py:etl_parent_flow -n "ETL with Cron" -o deployments/q1_etl_parent_flow.yaml --cron "0 5 1 * *"

- prefect deployment apply ./deployments/q1_etl_parent_flow-deployment.yaml

- prefect deployment build flows/04_homework/q3_etl_gcs_to_bq.py:etl_parent_flow -n "ETL Q3" -o deployments/q3_etl_gcs_to_bq.py.yaml --apply 

- prefect deployment build flows/04_homework/q3_etl_gcs_to_bq.py:etl_parent_flow -n "ETL Q4" -o deployments/q4_etl_gcs_to_bq.py.yaml -sb github/zoom-github --apply 