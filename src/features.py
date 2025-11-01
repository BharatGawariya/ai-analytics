# src/features.py
import pandas as pd


def create_time_features(df: pd.DataFrame, date_col='date') -> pd.DataFrame:
df = df.copy()
df['month'] = df[date_col].dt.month
df['year'] = df[date_col].dt.year
df['quarter'] = df[date_col].dt.quarter
df['month_start'] = df[date_col].dt.is_month_start.astype(int)
return df


# Simple aggregation helper
def aggregate_sales(df: pd.DataFrame, freq='MS', group_cols=None) -> pd.DataFrame:
if group_cols is None:
group_cols = []
df_agg = (df
.groupby(group_cols + [pd.Grouper(key='date', freq=freq)])
.agg({'sales':'sum','units':'sum'})
.reset_index())
return df_agg
