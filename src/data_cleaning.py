# src/data_cleaning.py
def load_data(path):
    df = pd.read_csv(path, parse_dates=['date'])
    return df

def basic_cleaning(df):
    df.columns = df.columns.str.strip().str.lower()
    df.dropna(subset=['sales'], inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    return df

