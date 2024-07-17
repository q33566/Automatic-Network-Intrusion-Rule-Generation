import pickle
import pandas as pd
def readPkl(file):
    with open(file, "rb") as f:
        data = pickle.load(f)
    return data

def readCsv(file):
    data = pd.read_csv(file)
    return data
