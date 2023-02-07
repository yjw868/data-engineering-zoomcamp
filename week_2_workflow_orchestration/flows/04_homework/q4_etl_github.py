from prefect.deployments import Deployment
from prefect.filesystems import GitHub
from q3_etl_gcs_to_bq import etl_parent_flow

# github_block = GitHub.load("zoom-github")
# github_block.get_directory("https://github.com/yjw868/data-engineering-zoomcamp/tree/week_2/week_2_workflow_orchestration") # specify a subfolder of repo
# github_block.save("week_2_q4")



storage = GitHub.load("zoom-github")

deployment = Deployment.build_from_flow(
     flow=etl_parent_flow,
     name="zoom-github",
     storage=storage,
     entrypoint="week_2_workflow_orchestration/flows/04_homework/q3_etl_gcs_to_bq.py:etl_parent_flow") # specify a subfolder of repo

if __name__ == "__main__":
    deployment.apply()