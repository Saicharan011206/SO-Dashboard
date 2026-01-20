import duckdb
import pandas as pd

def get_salary_trends():
    con = duckdb.connect('data/database/stackoverflow.db', read_only=True)
    
    query = """
    SELECT 
        year,
        ROUND(median(salary_numeric), 2) as median_salary_usd,
        COUNT(salary_numeric) as response_count
    FROM (
        SELECT 
            year, 
            TRY_CAST(salary_usd AS DOUBLE) as salary_numeric 
        FROM survey_data
    )
    WHERE salary_numeric IS NOT NULL 
      AND salary_numeric > 1000 
      AND salary_numeric < 1000000
    GROUP BY year
    ORDER BY year ASC;
    """
    
    try:
        df = con.execute(query).df()
    finally:
        con.close()
    
    return df

if __name__ == "__main__":
    results = get_salary_trends()
    print(results)