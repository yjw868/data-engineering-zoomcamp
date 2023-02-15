from pathlib import Path
from random import randint

import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket

# data map to /opt/prefect in docker container
loc = Path(__file__).parents[1] / "data"

@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    # if randint(0, 1) > 0:
    #     raise Exception

    df = pd.read_csv(dataset_url)
    return df


@task(log_prints=True)
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df.astype({
        'VendorID' : 	'Int64',
        'tpep_pickup_datetime' : 	'datetime64[ns]',
        'tpep_dropoff_datetime' : 	'datetime64[ns]',
        'passenger_count' : 	'Int64',
        'trip_distance' : 	'float64',
        'PULocationID' : 	'Int64',
        'DOLocationID' : 	'Int64',
        'RatecodeID' : 	'Int64',
        'store_and_fwd_flag' : 	'string',
        'payment_type' : 	'Int64',
        'fare_amount' : 	'float64',
        'extra' : 	'float64',
        'mta_tax' : 	'float64',
        'improvement_surcharge' : 	'float64',
        'tip_amount' : 	'float64',
        'tolls_amount' : 	'float64',
        'total_amount' : 	'float64',
        'congestion_surcharge' : 	'float64'
    })
    # return df


@task(log_prints=True)
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    parent = Path(f"{loc}/{color}")
    if not Path.is_dir(parent):
        parent.mkdir(parents=True, exist_ok=False)
        
    path = Path(f"{parent}/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")
    print(f"path is {path}")
    return path


@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    to_path = Path('data') / path.parent.name / path.name
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.upload_from_path(from_path=path, to_path=to_path)
    return


@flow()
def etl_web_to_gcs(retries=18) -> None:
    """The main ETL function"""
    color = "yellow"
    year = 2019
    months = range(1, 13)
    
    for month in months:
        dataset_file = f"{color}_tripdata_{year}-{month:02}"
        dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

        df = fetch(dataset_url)
        df_clean = clean(df)
        path = write_local(df_clean, color, dataset_file)
        # write_gcs(path)


if __name__ == "__main__":
    etl_web_to_gcs()