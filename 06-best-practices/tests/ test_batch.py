import pandas as pd
from datetime import datetime

def read_data(filename):
    return pd.read_parquet(filename)

def prepare_data(df, categorical):
    df = df.copy()
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df
def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

def test_prepare_data():
    data = [
        (None, None, dt(1, 1), dt(1, 10)),          # duration = 9 min
        (1, 1, dt(1, 2), dt(1, 10)),                # duration = 8 min
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),       # duration = 59 min
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),           # duration = 1441 min (filtered out)
    ]
    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)
    categorical = ['PULocationID', 'DOLocationID']

    actual = prepare_data(df, categorical)

    expected_data = [
        {'PULocationID': '-1', 'DOLocationID': '-1', 'duration': 9.0},
        {'PULocationID': '1',  'DOLocationID': '1',  'duration': 8.0},
        {'PULocationID': '1',  'DOLocationID': '-1', 'duration': 59.0},
    ]
    expected = pd.DataFrame(expected_data)

    # Only compare relevant columns
    assert actual[categorical + ['duration']].reset_index(drop=True).to_dict(orient='records') == expected.to_dict(orient='records')