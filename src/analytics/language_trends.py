import duckdb
import pandas as pd

def compare_languages(lang1, lang2):
    db_path = 'data/database/stackoverflow.db'
    con = duckdb.connect(db_path)
    
    query = """
    WITH expanded AS (
        SELECT 
            year, 
            unnest(string_split(languages_worked_with, ';')) AS language
        FROM survey_data
        WHERE languages_worked_with IS NOT NULL
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
    WHERE y.language IN (?, ?)
    ORDER BY y.year ASC;
    """
    
    df = con.execute(query, [lang1, lang2]).df()
    con.close()
    
    if df.empty:
        return "No data found."

    comparison = df.pivot(index='year', columns='language', values='market_share')
    comparison = comparison.fillna(0.0)
    
    return comparison

if __name__ == "__main__":
    first = input("Enter first language: ").strip()
    second = input("Enter second language: ").strip()
    
    results = compare_languages(first, second)
    print(results)