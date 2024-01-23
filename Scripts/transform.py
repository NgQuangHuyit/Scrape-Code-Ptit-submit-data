import pandas as pd


def transformMemoryUse(s):
    return int(s[:-2]) if not pd.isna(s) else s


def transformRunTime(time):
    return float(time[0:-1]) if not pd.isna(time) else time


def readRawData():
    df = pd.read_csv('Data/RawData/raw_data.csv')


def main():
    print('Transforming...')
    df = pd.read_csv('Data/RawData/raw_data.csv')
    df['memory'] = df['memory'].apply(transformMemoryUse)
    df['run_time'] = df['run_time'].apply(transformRunTime)
    df.to_csv('Data/TransformedData/clean_data.csv', index=False)
    print('Success')