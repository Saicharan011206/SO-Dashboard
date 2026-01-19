import duckdb
import pandas as pd
import os

def compare_languages(lang1, lang2):
    con = duckdb.connect('data/database/stackoverflow.db')
    
    # We use a f-string or parameter binding for the 'IN' clause
    query = f"""
    WITH expanded AS (
        SELECT year, unnest(string_split(languages_worked_with, ';')) AS language
        FROM survey_data
    ),
    yearly_counts AS (
        SELECT year, language, COUNT(*) AS mentions
        FROM expanded
        GROUP BY year, language
    ),
    totals AS (
        SELECT year, SUM(mentions) as total_mentions
        FROM yearly_counts
        GROUP BY year
    )
    SELECT 
        y.year, 
        y.language, 
        ROUND((y.mentions * 100.0) / t.total_mentions, 2) AS market_share
    FROM yearly_counts y
    JOIN totals t ON y.year = t.year
    WHERE y.language IN ('{lang1}', '{lang2}')
    ORDER BY y.year ASC;
    """
    
    df = con.execute(query).df()
    con.close()
    
    # Pivot for a clean comparison view
    comparison = df.pivot(index='year', columns='language', values='market_share')
    return comparison

if __name__ == "__main__":
    # Example: Comparing C++ and Rust
    l1 = input("Enter first language (e.g., C++): ")
    l2 = input("Enter second language (e.g., Rust): ")
    
    print(f"\nComparing {l1} vs {l2} Market Share (%):")
    print(compare_languages(l1, l2))