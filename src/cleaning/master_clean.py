import pandas as pd
import yaml
import glob
import os

def run_master_cleaning():
    # 1. Load config from the raw folder
    config_path = 'data/raw/meta.yaml'
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    target_cols = config['gold_standard_columns']
    processed_dir = 'data/processed'
    os.makedirs(processed_dir, exist_ok=True)

    # 2. Identify all CSVs
    raw_files = glob.glob('data/raw/*.csv')
    
    for file_path in raw_files:
        filename = os.path.basename(file_path)
        year_str = "".join(filter(str.isdigit, filename))[:4]
        
        # Skip 2015 and non-year files
        if not year_str or year_str == "2015":
            continue
            
        year = int(year_str)
        
        if year not in config['mappings']:
            print(f"Skipping {year}: No mapping found in meta.yaml")
            continue

        print(f"Cleaning {year}...")
        
        try:
            # Read and sanitize headers
            df = pd.read_csv(file_path, low_memory=False, encoding='latin1')
            df.columns = df.columns.str.strip()
        except Exception as e:
            print(f"Error reading {year}: {e}")
            continue
        
        # 3. Apply Mapping
        mapping = config['mappings'][year]
        rename_map = {v: k for k, v in mapping.items() if v is not None}
        df = df.rename(columns=rename_map)
        
        # 4. Standardize Columns
        df['year'] = year
        for col in target_cols:
            if col not in df.columns:
                df[col] = None

        # 5. Original Quality Filter (60% completeness)
        df['trust_score'] = df[target_cols].notnull().mean(axis=1)
        min_trust = config['quality_settings']['min_completeness_pct'] # 0.60
        
        df_cleaned = df[df['trust_score'] >= min_trust].copy()

        # 6. Save as high-speed Parquet
        output_file = os.path.join(processed_dir, f"{year}_cleaned.parquet")
        df_cleaned[target_cols + ['trust_score']].to_parquet(output_file, index=False)
        
        print(f"Saved {len(df_cleaned)} high-quality rows for {year}")

if __name__ == "__main__":
    run_master_cleaning()