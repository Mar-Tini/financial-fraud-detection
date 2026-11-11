import pandas as pd  # type: ignore 
from pathlib import Path 

ROOT_DIR = Path(__file__).resolve().parents[2]

def load_data(path_data: str) -> pd.DataFrame:

    path_file = ROOT_DIR / path_data 

    if not path_file.exists(): 
        raise FileNotFoundError(f'# -- File not found : {path_file}--')
    
    if path_file.suffix == '.csv': 
        dataset = pd.read_csv(path_file)
        
        df = dataset.copy()
    elif path_file.suffix == '.parquet':
        dataset = pd.read_parquet(path_file)
        
        df = dataset.copy()
        
    else: 
        raise ValueError(f'# -- Unsupported file format: {path_file} --')
    
    return df