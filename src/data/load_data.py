import chardet
import pandas as pd

def loadDataEnem(filePath):
    row_number = 500000
    with open(filePath,'rb') as f:
        result = chardet.detect(f.read(row_number))
    
    micro_dados_df = pd.read_csv(filePath, sep=';', nrows = row_number*2, encoding = result['encoding'])

    return micro_dados_df

def loadDataPib(filePath):
    pip_brasil_df = pd.read_excel(filePath)

    return pip_brasil_df