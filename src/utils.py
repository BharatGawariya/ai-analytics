# src/utils.py
import pandas as pd
import os
from datetime import datetime




def ensure_dirs():
for d in ['models','reports']:
os.makedirs(d, exist_ok=True)




def save_forecast_to_excel(df, path='reports/forecast.xlsx'):
df.to_excel(path, index=False)
return path




def simple_eval(y_true, y_pred):
import numpy as np
mae = float((abs(y_true - y_pred)).mean())
mape = float((abs((y_true - y_pred)/y_true)).mean()) if (y_true!=0).all() else None
return {'mae': mae, 'mape': mape}
