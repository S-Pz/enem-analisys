from load_data import loadDataEnem, loadDataPib

RAW_ENEM_PATH = "../../data/raw/microdados-enem-2023.csv"
RAW_PIB_PATH = "../../data/raw/pib-dos-municipios-2010-2023.xlsx"

PROCESSED_ENEM_PATH = "../../data/processed/enem_2023_limpo.parquet"
PROCESSED_PIB_PATH = "../../data/processed/pib_2023_limpo.parquet"

def extrair_dados():
    print("1. Extraindo dados...")
    df_enem = loadDataEnem(RAW_ENEM_PATH)
    df_pib = loadDataPib(RAW_PIB_PATH)
    return df_enem, df_pib

def transformar_dados(df_enem, df_pib):
    print("2.Transformando dados...")
    df_enem = df_enem.dropna(subset=['TP_ESCOLA'])
    df_enem = df_enem[df_enem['IN_TREINEIRO'] != 1]
    
    mapa_regioes = {
        'N': ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO'],
        'NE': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
        'CO': ['DF', 'GO', 'MT', 'MS'],
        'SE': ['ES', 'MG', 'RJ', 'SP'],
        'S': ['PR', 'RS', 'SC']
    }
    
    def definir_regiao(uf):
        for regiao, estados in mapa_regioes.items():
            if uf in estados: return regiao
        return None

    df_enem['REGIAO'] = df_enem['SG_UF_PROVA'].apply(definir_regiao)
    df_enem['TP_ESCOLA'] = df_enem['TP_ESCOLA'].astype(int).map({1: 'Não Responderam', 2: 'Pública', 3: 'Privada'})
    df_enem['TP_SEXO'] = df_enem['TP_SEXO'].map({'M': 'Masculino', 'F': 'Feminino'})
    
    faixa_salarial = {
        "A": 0, "B": 1320, "C": 1980, "D": 2640, "E": 3300,
        "F": 3960, "G": 5280, "H": 6600, "I": 7920, "J": 9240,
        "K": 10560, "L": 11880, "M": 13200, "N": 15840,
        "O": 19800, "P": 26400, "Q": 30000 
    }
    df_enem['RENDA_MEDIA'] = df_enem['Q006'].map(faixa_salarial)

    df_pib = df_pib[df_pib['Ano'] == 2023]
    
    return df_enem, df_pib

def carregar_dados(df_enem, df_pib):
    print("3. Salvando dados...")
    
    df_enem.to_parquet(PROCESSED_ENEM_PATH, index=False)
    df_pib.to_parquet(PROCESSED_PIB_PATH, index=False)
    
if __name__ == "__main__":
    df_e, df_p = extrair_dados()
    df_e_limpo, df_p_limpo = transformar_dados(df_e, df_p)
    carregar_dados(df_e_limpo, df_p_limpo)