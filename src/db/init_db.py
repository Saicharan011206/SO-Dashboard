import duckdb
import os
import pandas as pd
def create_unified_db():
    #1.Paths
    db_dir='data/database'
    os.makedirs(db_dir, exist_ok=True)
    db_path=os.path.join(db_dir,'stackoverflow.db')
    #2.Connect to DuckDB
    con=duckdb.connect(db_path)
    print("Connected to DuckDB at",db_path)
    #3.Create Single Table from CSVs
    con.execute("""
        CREATE OR REPLACE TABLE survey_data AS
        SELECT * FROM read_parquet('data/processed/*.parquet',union_by_name=True)
    """)
    print("Created table 'survey_data' from Parquet files.")
    print("Final row counts per year:")
    report=con.execute("""
        SELECT year,COUNT(*) AS responses,ROUND(AVG(trust_score),3) as avg_quality
        FROM survey_data
        GROUP BY year
        ORDER BY year
    """).df()
    print(report.to_string(index=False))
    con.close()
if __name__=="__main__":
    create_unified_db()
    """Creates a unified DuckDB database from processed Parquet survey data."""