
# AI Analytics Blueprint


## Quickstart


1. Clone this repo
2. Create a Python environment (venv/conda)
3. `pip install -r requirements.txt`
4. Place your sales CSV in `data/sample_sales.csv` (or upload via app)
5. Run Streamlit: `streamlit run app/streamlit_app.py`


## Notes
- For LLM-powered written insights, set `OPENAI_API_KEY` or configure Hugging Face inference.
- Use `src/forecasting.py` to train models and save them to `models/`.
- Use `src/insights.py` as a prompt builder to feed to your chosen LLM.
