import requests
import pandas as pd
import json
from secret_configs import api_key
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Float
from sqlalchemy.engine import URL
from sqlalchemy.dialects import postgresql
from secret_configs import db_user, db_password, db_server_name, db_database_name

# Defining Functions (Extract)

def extract(
        api_key:str,
        start_date:str,
        end_date:str,
        symbols:str,
        base:str
    )->pd.DataFrame:
    """
    Extract time series currency data from foreign exchange API.
    - start_date: Beginning day of extract
    - end_date: Final day of extraction
    - base: Base currency
    - symbols: What currencies you wish to convert 'base' against - Three digit currency code seperate by comma
    """
    url = f"https://api.apilayer.com/exchangerates_data/timeseries?start_date={start_date}&end_date={end_date}&symbols={symbols}&base={base}"

    payload = {}
    headers= {
    "apikey": api_key
    }

    response = requests.request("GET", url, headers=headers, data = payload)

    status_code = response.status_code
    result = response.json()
    return result

# Defining Functions (Transformation)

def transform(result:dict)->pd.DataFrame:
    """
    Transform dictionary output from API
    """
    # Flattening JSON 'rates' only column
    df_currency_five = pd.json_normalize(result['rates'].values())

    # Other transformations
    df_currency_dates = pd.DataFrame.from_dict(result)
    df_currency_dates = df_currency_dates.reset_index()
    df_currency_dates['index'] = pd.to_datetime(df_currency_dates["index"]).dt.strftime('%d-%m-%Y')
    df_currency_dates = df_currency_dates.rename(columns={"index":"date"})
    df_currency_dates = df_currency_dates[["date","base"]]

    # Joining of two seperate DataFrames
    df_currency = pd.merge(df_currency_dates, df_currency_five, left_index=True, right_index=True)
    return df_currency

# Defining Functions (Load to Postgres)

def load(df_currency)->bool:
    connection_url = URL.create(
    drivername = "postgresql+pg8000",
    username = db_user,
    password = db_password,
    host = db_server_name, 
    port = 5432,
    database = db_database_name)
    # Creating connection
    engine = create_engine(connection_url)
    df_currency.to_sql("2022_aud_exchange_rate", engine, if_exists="replace")

# Combining the ETL functions

def pipeline():
    #Extract component
    extract(api_key=api_key, start_date="2022-01-01", end_date="2022-12-31", symbols="USD,EUR,GBP,CAD,HKD", base="AUD")
    x = extract(api_key=api_key, start_date="2022-01-01", end_date="2022-12-31", symbols="USD,EUR,GBP,CAD,HKD", base="AUD")
    #Transform component
    transform(x)
    y = transform(x)
    #Load component
    load(y)

    return True

if __name__ == "__main__":
    if pipeline():
        print("success!")

