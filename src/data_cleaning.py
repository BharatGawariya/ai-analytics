# src/data_cleaning.py
import pandas as pd
from datetime import datetime


def load_data(path: str) -> pd.DataFrame:
df = pd.read_csv(path, parse_dates=['date'])
return df


def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
df = df.copy()
df['date'] = pd.to_datetime(df['date'])
# Fill missing values
numeric_cols = df.select_dtypes(include=['number']).columns
df[numeric_cols] = df[numeric_cols].fillna(0)
df['brand'] = df['brand'].fillna('Unknown')
df['segment'] = df['segment'].fillna('Unknown')
df['region'] = df['region'].fillna('Unknown')
df['channel'] = df['channel'].fillna('Unknown')
return df


if __name__ == '__main__':
df = load_data('../data/sample_sales.csv')
df = basic_cleaning(df)
print(df.head())
