import pickle
import pandas as pd
def readPkl(file):
    with open(file, "rb") as f:
        data = pickle.load(f)
    return data

def readCsv(file):
    data = pd.read_csv(file)
    return data

def readGeneratedRegex(file) -> list:
    data = pd.read_csv(file, usecols=[0],header=None,encoding='ISO-8859-1', skip_blank_lines=False)
    #data = data.dropna()
    return data.iloc[:, 0].tolist()
    