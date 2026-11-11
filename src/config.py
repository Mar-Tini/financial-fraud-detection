from pathlib import Path
import yaml # type: ignore 
from src.utils.paths import CONFIG_DIR,  DATA_CONFIG, MODEL_CONFIG

def load_config():
    
    with open(CONFIG_DIR /  DATA_CONFIG , 'r', encoding='utf-8') as file:
        data_config = yaml.safe_load(file)
    
    with open(CONFIG_DIR /  MODEL_CONFIG , 'r', encoding='utf-8') as file:
        model_config = yaml.safe_load(file)
            
    return data_config, model_config