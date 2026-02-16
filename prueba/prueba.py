#!/usr/bin/env python3
"""
Convert all Excel (.xlsx and .xlsm) files in the current folder to CSV.
- All data is read as strings to preserve exact capitalization (e.g., "true"/"false").
- Empty cells are filled with "0" only for rows below a customizable threshold.
- Columns C, F, and M are removed.

Dependencies:
    pandas, openpyxl

Install with:
    pip install pandas openpyxl
"""

import os
import glob
import pandas as pd

# ===== CONFIGURATION – ADJUST THESE VALUES AS NEEDED =====
# Columns to drop – given as Excel column letters (case‑insensitive)
COLUMNS_TO_DROP = ['C', 'F', 'M']

# Only fill empty cells with "0" for rows whose Excel row number is GREATER than this value.
# Example: 19 → rows 20 and beyond are filled; rows 1‑19 remain empty (blank in CSV).
ROW_THRESHOLD = 19
# =========================================================

def excel_columns_to_indices(columns_letters):
    """
    Convert Excel column letters (e.g., 'A', 'B', 'AA') to zero‑based indices.
    Returns a list of indices.
    """
    indices = []
    for col in columns_letters:
        col = col.upper()
        index = 0
        for char in col:
            index = index * 26 + (ord(char) - ord('A') + 1)
        indices.append(index - 1)  # convert to zero‑based
    return indices

def drop_columns_by_letters(df, column_letters):
    """
    Drop columns from a DataFrame using Excel column letters.
    If a column letter is out of range, it is silently ignored.
    """
    total_cols = df.shape[1]
    indices_to_drop = excel_columns_to_indices(column_letters)
    valid_indices = [idx for idx in indices_to_drop if 0 <= idx < total_cols]

    if valid_indices:
        df.drop(df.columns[valid_indices], axis=1, inplace=True)
        print(f"  Dropped columns at positions: {valid_indices}")
    else:
        print("  No columns to drop (all requested columns out of range).")
    return df

def fill_empty_below_row(df, row_threshold_excel, fill_value="0"):
    """
    Fill empty (NaN) cells with fill_value only for rows
    whose Excel row number is greater than row_threshold_excel.
    (Excel row numbers start at 1.)
    """
    # Convert Excel row number to zero‑based index
    idx_threshold = row_threshold_excel - 1

    if idx_threshold < 0:
        # If threshold is less than 1, fill all rows
        df.fillna(fill_value, inplace=True)
    elif idx_threshold >= len(df):
        # If threshold is beyond the last row, nothing to fill
        pass
    else:
        # Fill only rows from idx_threshold onward
        df.iloc[idx_threshold:] = df.iloc[idx_threshold:].fillna(fill_value)
    return df

def convert_excel_to_csv(excel_path):
    """
    Convert all sheets of a given Excel file to CSV:
      1. Read all data as strings (preserves exact capitalization).
      2. Fill empty cells with "0" for rows below the threshold.
      3. Remove columns C, F, and M.
    """
    try:
        # Read all data as strings to avoid boolean conversion (true/false → True/False)
        excel_file = pd.ExcelFile(excel_path, engine='openpyxl')
        sheet_names = excel_file.sheet_names

        if not sheet_names:
            print(f"No sheets found in {excel_path}")
            return

        base_name = os.path.splitext(os.path.basename(excel_path))[0]

        for sheet in sheet_names:
            # dtype=str ensures every cell is read as a string, preserving case
            df = pd.read_excel(excel_file, sheet_name=sheet, dtype=str)

            # Step 1: Fill empty cells with "0" for rows below the threshold
            fill_empty_below_row(df, row_threshold_excel=ROW_THRESHOLD, fill_value="0")

            # Step 2: Drop the specified columns
            df = drop_columns_by_letters(df, COLUMNS_TO_DROP)

            # Save to CSV – all data are strings, so case remains as in Excel
            output_file = f"{base_name}_{sheet}.csv"
            output_file = output_file.replace('/', '_').replace('\\', '_')
            df.to_csv(output_file, index=False)
            print(f"Saved: {output_file} (columns after drop: {df.shape[1]})")

    except Exception as e:
        print(f"Error processing {excel_path}: {e}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Find both .xlsx and .xlsm files
    excel_files = glob.glob("*.xlsx") + glob.glob("*.xlsm")

    if not excel_files:
        print("No .xlsx or .xlsm files found in the current folder.")
        return

    for excel_file in excel_files:
        print(f"\nProcessing: {excel_file}")
        convert_excel_to_csv(excel_file)

if __name__ == "__main__":
    main()