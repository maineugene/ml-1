# Cybersecurity Threat Detection Dataset

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

raw_csv_path = 'data/raw/cybersecurity.csv'
df = pd.read_csv(raw_csv_path)

def print_df_info(df):
    print("=" * 50)
    print(f"Shape: {df.shape}")
    print("=" * 50)
    print("Columns:")
    print(df.columns.tolist())
    print("=" * 50)
    print("Statistical description:")
    print(df.describe())
    print("=" * 50)
    print("First 5 rows:")
    print(df.head(5))
    print("=" * 50)
    print("Last 5 rows:")
    print(df.tail(5))
    print("=" * 50)

def analyze_missing(df):
    missing = df.isnull().sum()
    missing_percent = 100 * missing / len(df)
    missing_df = pd.DataFrame({
        'Column': df.columns,
        'Missing' : missing.values,
        'Percent' : missing_percent.values,
        'Dtype': df.dtypes.values
    })
    missing_df = missing_df[missing_df['Missing'] > 0]
    return missing_df

missing_data = analyze_missing(df)
print_df_info(df)
print(missing_data.to_string(index=False))
