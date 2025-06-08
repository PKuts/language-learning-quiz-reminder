import pandas as pd
import sqlite3
import importlib
import os
#import boto3


def load_dictionary(config):
    source = config["data_source"]

    if source == "excel":
        file_path = config["excel_path"]
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Excel file not found at: {file_path}")
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip()
        return df

    elif source == "sqlite":
        db_path = config["sqlite_path"]
        if not os.path.exists(db_path):
            print(f"SQLite database not found at: {db_path}")
            print("Initializing default database...")

            # Run init_sqlite.py dynamically
            import subprocess
            init_path = os.path.join(os.path.dirname(__file__), "init_sqlite.py")
            subprocess.run(["python", init_path], check=True)
            if not os.path.exists(db_path):
                raise FileNotFoundError(f"Failed to create SQLite database at: {db_path}")

        
        
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM dictionary", conn)
        conn.close()
        return df

    # elif source == "aws_s3":
    #     s3 = boto3.client("s3", region_name=config["aws_s3"]["region"])
    #     bucket = config["aws_s3"]["bucket_name"]
    #     key = config["aws_s3"]["object_key"]
    #     local_path = "/tmp/dictionary.xlsx"
    #     s3.download_file(bucket, key, local_path)
    #     df = pd.read_excel(local_path)
    #     df.columns = df.columns.str.strip()
    #     return df

    else:
        raise ValueError(f"Unsupported data source: {source}")
    

def save_dictionary(df, config):
    source = config["data_source"]

    if source == "excel":
        df.to_excel(config["excel_path"], index=False)

    elif source == "sqlite":
        import sqlite3
        conn = sqlite3.connect(config["sqlite_path"])
        df.to_sql("dictionary", conn, if_exists="replace", index=False)
        conn.close()

    # elif source == "aws_s3":
    #     #import boto3
    #     import io
    #     buffer = io.BytesIO()
    #     df.to_excel(buffer, index=False)
    #     buffer.seek(0)

        # s3 = boto3.client("s3", region_name=config["aws_s3"]["region"])
        # s3.upload_fileobj(buffer, config["aws_s3"]["bucket_name"], config["aws_s3"]["object_key"])

    else:
        raise ValueError(f"Unsupported data source: {source}")