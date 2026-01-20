import duckdb
import pandas as pd

def get_remote_trends():
    con = duckdb.connect('data/database/stackoverflow.db', read_only=True)
    
    query = """
    SELECT year, remote_work, COUNT(*) as count
    FROM survey_data
    WHERE remote_work IS NOT NULL 
      AND year != 2020 -- Removing 2020 because OpSys isn't Remote Work
    GROUP BY 1, 2
    """
    df = con.execute(query).df()
    con.close()

    # Define a normalization map
    val_map = {
        'Remote': 'Remote',
        'Fully remote': 'Remote',
        'All or almost all the time (I\'m full-time remote)': 'Remote',
        '1.0': 'Remote', 
        'Full in-person': 'In-person',
        'In-person': 'In-person',
        'Never': 'In-person',
        '3.0': 'In-person',
        'Hybrid (some remote, some in-person)': 'Hybrid',
        'A few days each month': 'Hybrid',
        'About half the time': 'Hybrid',
        '2.0': 'Hybrid'
    }

    # Apply the map and group again
    df['remote_clean'] = df['remote_work'].map(val_map).fillna('Other')
    
    # Calculate percentages on the cleaned data
    final = df.groupby(['year', 'remote_clean'])['count'].sum().reset_index()
    final['percentage'] = final.groupby('year')['count'].transform(lambda x: (x / x.sum() * 100).round(2))
    
    return final.sort_values(['year', 'percentage'], ascending=[True, False])

if __name__ == "__main__":
    print(get_remote_trends()[['year', 'remote_clean', 'percentage']])