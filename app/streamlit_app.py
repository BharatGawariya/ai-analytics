# app/streamlit_app.py
import streamlit as st
import pandas as pd
from src.data_cleaning import load_data, basic_cleaning
from src.features import aggregate_sales
from src.forecasting import train_prophet, forecast_prophet, save_model
from src.insights import build_prompt_for_llm
import os


st.set_page_config(page_title='Aspri AI - Sales Forecast', layout='wide')


st.title('Aspri Spirits - AI Sales Forecast & Insights')


uploaded = st.file_uploader('Upload sales CSV (date,brand,segment,region,channel,sales,units)')


if uploaded is not None:
df = pd.read_csv(uploaded, parse_dates=['date'])
df = basic_cleaning(df)
st.write('Raw data sample', df.head())


# Aggregation
group_cols = st.multiselect('Group by (choose none for total)', ['brand','segment','region','channel'], default=['segment'])
freq = st.selectbox('Forecast frequency', ['MS','M'], index=0)
df_agg = aggregate_sales(df, freq='MS', group_cols=group_cols)
st.write('Aggregated sample', df_agg.head())


# choose series
if len(group_cols) > 0:
sel = st.selectbox('Select series', df_agg[group_cols].drop_duplicates().astype(str).apply(lambda row: ' | '.join(row.values), axis=1))
match = df_agg[group_cols].drop_duplicates().astype(str).apply(lambda row: ' | '.join(row.values), axis=1)
idx = match[match==sel].index[0]
sel_vals = df_agg[group_cols].drop_duplicates().iloc[idx].to_dict()
df_series = df_agg.copy()
for k,v in sel_vals.items():
df_series = df_series[df_series[k]==v]
else:
df_series = df_agg


st.write('Series preview', df_series.head())


periods = st.number_input('Forecast periods (months)', min_value=1, max_value=36, value=6)
if st.button('Run Prophet Forecast'):
with st.spinner('Training Prophet...'):
m = train_prophet(df_series.reset_index(drop=True))
fcst = forecast_prophet(m, periods=periods)
save_model(m, name='prophet_model.pkl')
st.success('Forecast ready')
st.write(fcst.tail(periods))


if st.button('Generate Report (PPTX)'):
st.info('Report generation not implemented in this demo. See scripts in src/ to wire python-pptx report generation.')


else:
st.info('Upload a CSV to proceed. Use sample_sales.csv as a template.')
