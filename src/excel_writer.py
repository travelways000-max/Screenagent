import os
import pandas as pd
from datetime import datetime
from config import EXCEL_FILE


def save_to_excel(data_dict):
    """Append extracted data to Excel file. Creates file if missing."""
    # Remove internal fields
    clean = {k: v for k, v in data_dict.items() if not k.startswith('_')}

    df_new = pd.DataFrame([clean])

    if os.path.exists(EXCEL_FILE):
        df_old = pd.read_excel(EXCEL_FILE)
        df_combined = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.to_excel(EXCEL_FILE, index=False)
    print(f"✅ Saved to {EXCEL_FILE} | Total rows: {len(df_combined)}")
    return EXCEL_FILE


def view_all_data():
    """Show all data collected so far."""
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        print(f"\n📊 Total records: {len(df)}")
        print(df.to_string())
    else:
        print("No data yet.")
