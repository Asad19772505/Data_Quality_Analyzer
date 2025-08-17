import pandas as pd
import numpy as np

def data_quality_report(df, filename="data_quality_report.txt"):
    """
    Generate a comprehensive data quality report for any DataFrame
    """
    report = []
    report.append("DATA QUALITY REPORT")
    report.append("=" * 60)
    report.append(f"Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns\n")
    
    # Missing values analysis
    report.append("MISSING VALUES:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    missing_df = pd.DataFrame({"Missing Values": missing, "Percent": missing_pct})
    missing_df = missing_df[missing_df["Missing Values"] > 0]
    
    if missing_df.empty:
        report.append("  ✓ No missing values found\n")
    else:
        for col, row in missing_df.iterrows():
            report.append(f"  {col}: {row['Missing Values']} ({row['Percent']:.1f}%)")
        report.append("")

    # Duplicate rows
    duplicates = df.duplicated().sum()
    report.append(f"DUPLICATE ROWS: {duplicates}\n")
    
    # Data types summary
    report.append("DATA TYPES SUMMARY:")
    dtype_counts = df.dtypes.value_counts()
    for dtype, count in dtype_counts.items():
        cols = df.select_dtypes(include=[dtype]).columns.tolist()
        report.append(f"  {dtype}: {count} columns → {cols}")
    report.append("")
    
    # Numeric columns analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        report.append("NUMERIC OUTLIERS (IQR method):")
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)][col].count()
            if outliers > 0:
                pct = (outliers / len(df)) * 100
                report.append(f"  {col}: {outliers} potential outliers ({pct:.1f}%)")
        report.append("")
    
    # Save and print report
    report_text = "\n".join(report)
    with open(filename, 'w') as f:
        f.write(report_text)
    
    print(report_text)
    print(f"\nReport saved to: {filename}")


# Example usage:
# df = pd.read_csv("your_data.csv")
# data_quality_report(df)
``
