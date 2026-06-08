import pandas as pd
import os

def load_data(filepath: str):
    """
    Load price data into dictionary while aligning to calendar
    """

    etf_dict = {}
    for file in os.listdir(filepath):
        name = os.path.splitext(file)[0]
        file_path = os.path.join(filepath, file)
        df = pd.read_csv(file_path, parse_dates=["Date"], index_col="Date") 
        etf_dict[name] = pd.to_numeric(df["Close"], errors="coerce")
    
    return etf_dict