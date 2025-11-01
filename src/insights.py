# src/insights.py
import textwrap
from typing import List


# RULE-BASED INSIGHTS


def top_growth_segments(df, past_periods=3):
# expects aggregated monthly sales per segment
df = df.copy()
# compute pct change month over month
df['pct'] = df.groupby('segment')['sales'].pct_change()
recent = df.sort_values('date').groupby('segment').tail(past_periods)
summary = recent.groupby('segment')['pct'].mean().sort_values(ascending=False)
return summary.head(5)


# LLM-BASED INSIGHTS (prompt builder)


def build_prompt_for_llm(brand: str, top_findings: List[str], recent_trend_text: str) -> str:
prompt = f"""
You are an expert business analyst for Aspri Spirits. Write a concise (4-6 sentence) executive summary for the brand {brand} using the findings below.


Key findings:
{chr(10).join(['- '+s for s in top_findings])}


Recent Trend:
{recent_trend_text}


Output format:\n1) Headline\n2) 2-3 bullet key drivers\n3) 1 line recommended action\n
Keep the tone formal and concise.
"""
return textwrap.dedent(prompt)


# Example: a thin wrapper if using OpenAI


def call_openai_for_insight(openai_client, prompt: str):
# expects openai client imported and configured (openai)
completion = openai_client.ChatCompletion.create(
model='gpt-4o-mini',
messages=[{"role":"user","content":prompt}],
max_tokens=300
)
return completion['choices'][0]['message']['content']
