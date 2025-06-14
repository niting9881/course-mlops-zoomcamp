import argparse
import pickle
import pandas as pd
import numpy as np
import os

categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df

def main(year, month):
    input_file = f'./dataset/yellow_tripdata_{year}-{month:02d}.parquet'
    output_file = f'./output/output_{year}-{month:02d}.parquet'
    model_file = './model/model.bin'

    with open(model_file, 'rb') as f_in:
        dv, model = pickle.load(f_in)

    df = read_data(input_file)
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)

    df['prediction'] = y_pred
    df['year'] = df.tpep_pickup_datetime.dt.year
    df['month'] = df.tpep_pickup_datetime.dt.month
    df['ride_id'] = df['year'].astype(str).str.zfill(4) + '/' + df['month'].astype(str).str.zfill(2) + '_' + df.index.astype('str')

    df_result = df[['ride_id', 'prediction']].copy()
    df_result.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )
    print(f"Predictions saved to {output_file}")
    print(f"Mean predicted duration: {np.mean(y_pred)}")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, required=True, help='Year of the data file')
    parser.add_argument('--month', type=int, required=True, help='Month of the data file')
    args = parser.parse_args()
    main(args.year, args.month)
    