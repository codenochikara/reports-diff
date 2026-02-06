import pandas as pd

from config import COLUMNS


def load_excel(path):
    df = pd.read_excel(path)
    df = df[COLUMNS]
    return df
