# src/forecasting.py
from prophet import Prophet
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')




def train_prophet(df: pd.DataFrame, target_col='sales'):
# df must have columns: date, sales, and any grouping aggregated as single series
df_prophet = df.rename(columns={'date':'ds', target_col:'y'})[['ds','y']]
m = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
m.fit(df_prophet)
return m




def forecast_prophet(model, periods=6, freq='M'):
future = model.make_future_dataframe(periods=periods, freq=freq)
fcst = model.predict(future)
return fcst[['ds','yhat','yhat_lower','yhat_upper']]




# XGBoost time-series framing (simple lag features)


def create_lag_features(df, lags=[1,2,3,12]):
df = df.copy().sort_values('date')
for lag in lags:
df[f'lag_{lag}'] = df['sales'].shift(lag)
df = df.dropna().reset_index(drop=True)
return df




def train_xgboost(df):
df_feat = create_lag_features(df)
X = df_feat[[c for c in df_feat.columns if c.startswith('lag_')]]
y = df_feat['sales']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
model = XGBRegressor(n_estimators=200)
model.fit(X_train, y_train)
preds = model.predict(X_test)
print('XGB MAE:', mean_absolute_error(y_test, preds))
return model




def save_model(obj, name='model.pkl'):
os.makedirs(MODEL_DIR, exist_ok=True)
path = os.path.join(MODEL_DIR, name)
joblib.dump(obj, path)
return path




def load_model(name='model.pkl'):
path = os.path.join(MODEL_DIR, name)
return joblib.load(path)
