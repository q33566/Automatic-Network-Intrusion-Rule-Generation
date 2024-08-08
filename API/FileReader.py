import pickle
import pandas as pd
from typing import Any, Union
import os

def read_pkl(file_path: str) -> Union[Any, pd.DataFrame]:
    with open(file_path, "rb") as f:
        data = pickle.load(f)
    return data

def read_csv(file_path: str) -> pd.DataFrame:
    data = pd.read_csv(file_path)
    return data

def read_file_as_dataframe(file_path: str) -> pd.DataFrame:
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension == '.csv':
        return pd.read_csv(file_path)
    elif file_extension == '.pkl':
        return pd.read_pickle(file_path)
    elif file_extension == '.txt':
        return pd.read_excel
    else:
        raise ValueError(f"Unsupported file type: {file_extension}, please provide a .csv or .pkl file, or you can modify this function to support other file types.")

def read_generated_regex(file_path: str) -> list:
    data = pd.read_csv(file_path, usecols=[0],header=None,encoding='ISO-8859-1', skip_blank_lines=False)
    #data = data.dropna()
    return data.iloc[:, 0].tolist()
    
def read_generated_regex_from_directory(directory_path: str) -> dict:
    
    def strip_txt(file_path: str) -> list:
        with open(file_path, 'r') as file :
            return [line.strip() for line in file]
    
    sid_to_generated_regex: dict = {}
    files = os.listdir(directory_path)
    for file in files:
        if file.endswith(".txt"):
            sid = os.path.splitext(file)[0]
            if sid in sid_to_generated_regex:
                sid_to_generated_regex[sid].append(strip_txt(os.path.join(directory_path, file)))
            else:
                sid_to_generated_regex[sid] = strip_txt(os.path.join(directory_path, file))
    return sid_to_generated_regex