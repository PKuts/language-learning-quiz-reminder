import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import tempfile
from data.loader import load_dictionary, save_dictionary

def create_sample_df():
    return pd.DataFrame({
        "German": ["der Hund", "die Katze"],
        "Ukrainian": ["собака", "кіт"],
        "Example": ["Der Hund bellt.", "Die Katze schläft."],
        "Date": ["2025-06-01", "2025-06-02"],
    })

def test_excel_load_and_save():
    df_original = create_sample_df()

    with tempfile.TemporaryDirectory() as tmp_dir:
        excel_path = os.path.join(tmp_dir, "test_dictionary.xlsx")
        config = {
            "data_source": "excel",
            "excel_path": excel_path
        }

        save_dictionary(df_original, config)
        assert os.path.exists(excel_path), "Excel file not saved"

        df_loaded = load_dictionary(config)
        pd.testing.assert_frame_equal(df_original, df_loaded)

def test_sqlite_load_and_save():
    df_original = create_sample_df()

    with tempfile.TemporaryDirectory() as tmp_dir:
        sqlite_path = os.path.join(tmp_dir, "test_dictionary.db")
        config = {
            "data_source": "sqlite",
            "sqlite_path": sqlite_path
        }

        save_dictionary(df_original, config)
        assert os.path.exists(sqlite_path), "SQLite file not saved"

        df_loaded = load_dictionary(config)
        pd.testing.assert_frame_equal(df_original, df_loaded)