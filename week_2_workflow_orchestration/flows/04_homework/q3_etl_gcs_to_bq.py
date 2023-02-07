from pathlib import Path

import pandas as pd
from prefect import flow, task
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket


@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    file_name = f'{color}_tripdata_{year}-{month:02}.parquet' 
    path =f"./data/{color}/{file_name}" 
    gcs_path = f"opt/prefect/{path}"
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"./data/")
    
    return Path(file_name).absolute()


@task()
def transform(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)
    print(f"pre: missing passenger count: {df['passenger_count'].isna().sum()}")
    # df["passenger_count"].fillna(0, inplace=True)
    # print(f"post: missing passenger count: {df['passenger_count'].isna().sum()}")
    return df


@task()
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BiqQuery"""

    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")

    df.to_gbq(
        destination_table="dezoomcamp.rides",
        project_id="pacific-card-374422",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )


@flow()
def etl_gcs_to_bq(color: str, year: int, month: int):
    """Main ETL flow to load data into Big Query"""
    # color = "yellow"
    # year = 2021
    # month = 1

    path = extract_from_gcs(color, year, month)
    df = transform(path)
    write_bq(df)


@flow(log_prints=True)
def etl_parent_flow(
    colors: list[str] = ["yellow"],  years: list[int] = [2021], months: list[int] = [1, 2]
):
    print(f'current location is {Path.cwd()}')
    for color in colors:
        for year in years:
            for month in months:
                etl_gcs_to_bq(color, year, month)


if __name__ == "__main__":
    colors = ["yellow"]
    months = [2,3]
    years = [2019]
    etl_parent_flow(colors, years, months)