# Cybersecurity Threat Detection Dataset

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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


def clean_df(df):
    df_clean = df.copy()
    print("Cleaning dataset")
    print("="*50)

    #Removing duplicates
    if df_clean.duplicated().sum() > 0:
        dup_count = df_clean.duplicated().sum()
        df_clean = df_clean.drop_duplicates()
        print(f"Removed {dup_count} duplicate rows \n")

    #Handle missing values
    if df_clean.isnull().sum().sum() > 0:
        print("Handling missing values")
        print("=" * 50)

        numeric_cols = df_clean.select_dtypes(include=np.number).columns.tolist()
        for col in numeric_cols:
            if df_clean[col].isnull().any():
                fill_value = df_clean[col].median()
                df_clean[col] = df_clean[col].fillna(fill_value)
                print(f"{col}: Filled with median={fill_value}")

        if df_clean['url'].isnull().any():
            df_clean['url'] = df_clean['url'].fillna('')
            print("url: Filled with empty string")

        if df_clean['user_agent'].isnull().any():
            df_clean['user_agent'] = df_clean['user_agent'].fillna('Unknown')
            print("user_agent: Filled with 'Unknown'")

        cat_cols = ['src_ip', 'dst_ip', 'protocol', 'attack_type']
        for col in cat_cols:
            if col in df_clean.columns and df_clean[col].isnull().any():
                mode_val = df_clean[col].mode()[0] if len(df_clean[col].mode()) > 0 else 'Unknown'
                df_clean[col] = df_clean[col].fillna(mode_val)
                print(f"{col}: Filled with mode='{mode_val}'")
    else:
        print("No missing values detected - data is already clean!\n")

    final_missing = df_clean.isnull().sum().sum()
    print(f"Missing values: {final_missing}")
    return df_clean

raw_csv_path = 'data/raw/cybersecurity.csv'
df = pd.read_csv(raw_csv_path)
print_df_info(df)
missing_data = analyze_missing(df)
print(missing_data.to_string(index=False))
cleaned_df = clean_df(df)
cleaned_df.to_csv("data/processed/cybersecurity.csv", index=False)


