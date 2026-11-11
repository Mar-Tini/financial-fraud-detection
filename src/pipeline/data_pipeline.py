from src.data.load import load_data 
from src.data.preprocess import preprocessing_data 
from src.data.cleaning import clear_data 
from pathlib import Path  
from src.config import load_config
from src.data.preprocess import save_preprocessor
def run_pipeline():  
    # -- Load configuration --
    data_config, model_condif = load_config()
    
    # -- Load data --                    
    df = load_data(data_config['data']['raw'])
    print('\n# -- Loading data ok --')
    
    # -- Cleaning data --
    df = clear_data(df, data_config['data']['remouve_columns'] )
    print('\n# -- Cleaning data ok --')
    
    
    output_data = Path(data_config['data']['interim'])
    output_data.parent.mkdir(parents=True,  exist_ok=True)
    
    
    
    df.to_csv(output_data , index=False, encoding='utf-8')
    print(f'\n# -- Data save to {output_data} --')
    
    # -- Preprocessing data --
    train_data, validation_data, test_data, encoder = preprocessing_data(df, data_config['data'])
    
    
    save_preprocessor(encoder, data_config['data']['preprocessing'])
    
    print('\n# -- Preprocessing ok --')
    

if __name__ == '__main__': 
    run_pipeline()
    
    