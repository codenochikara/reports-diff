import re

import pandas as pd


def normalize_text(value):
  if pd.isna(value):
    return ""
  value = str(value).strip()
  value = re.sub(r"\s+", " ", value)
  return value

def normalize_df(df):
  df = df.copy()
  for col in df.columns:
    df[col] = df[col].apply(normalize_text)
  return df
