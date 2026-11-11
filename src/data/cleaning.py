import pandas as pd # type: ignore 

def clear_data(df: pd.DataFrame, remouve_columns) ->  pd.DataFrame : 
    
    # -- Remouve  duplicated -- 
    df = df.drop_duplicates()
    
    # -- Remouve impossible values --
    df  =  df[df['amount'] >= 0 ]
    
    # -- Remouve unwanted columns --     
    df = df.drop(remouve_columns ,  axis=1)
    
    return df 