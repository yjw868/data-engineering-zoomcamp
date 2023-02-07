from pathlib import Path
from random import randint

import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket

loc =  "/opt/prefect/data"

@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    # if randint(0, 1) > 0:
    #     raise Exception

    df = pd.read_csv(dataset_url)
    return df


# @task(log_prints=True)
# def clean(df: pd.DataFrame) -> pd.DataFrame:
#     """Fix dtype issues"""
#     print(df.head(2))
#     print(f"columns: {df.dtypes}")
#     df.rename(columns={"lpep_pickup_datetime":"tpep_pickup_datetime",
#                        "lpep_dropoff_datetime":"tpep_dropoff_datetime"},
#             inplace=True)
#     df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
#     df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
#     print(df.head(2))
#     print(f"columns: {df.dtypes}")
#     print(f"rows: {len(df)}")
#     return df


@task()
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f"{loc}/{color}/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")
    return path


@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.upload_from_path(from_path=path, to_path="data")
    return


@flow()
def etl_web_to_gcs(year: int, month: int, color: str) -> None:
    """The main ETL function"""
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    # df_clean = clean(df)
    path = write_local(df, color, dataset_file)
    write_gcs(path)


@flow()
def etl_parent_flow(
    months: list[int] = [1, 2], years:list[int] = [2021], colors: list[str] = ["yellow"]
):
    for year in years:
        for color in colors:
            for month in months:
                etl_web_to_gcs(year, month, color)


if __name__ == "__main__":
    colors = ["green"]
    months = [11]
    years = [2020]
    # User below to generate the data for Q3
    # color = "yellow"
    # months = [2,3]
    # year = 2019
    etl_parent_flow(months, years, colors)
    
    


