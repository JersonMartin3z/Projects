import pandas as pd

def converts_to_float(df): 
    # Seleccionar las columnas específicas
    cols = ['price', 'change', 'change_%']
    for col in cols:
        df[col] = df[col].apply(lambda x: float(x.replace('.', '').replace(',', '.').replace("%", "")))
        df[col] = df[col].round(2)
    return df

def convert_units(df):
    # Seleccionar las columnas específicas
    cols = ['market_cap', 'vol_total', 'vol_last_24', 'vol_t_last_24', 'vol_circ']
    def convert(value):
        
        if value[-1] == 'T':
            return float(value[:-1].replace(',', '')) * 1e12  # Multiplicar por 1 trillion
        elif value[-1] == 'B':
            return float(value[:-1].replace(',', '')) * 1e9   # Multiplicar por 1 billion
        elif value[-1] == 'M':
            return float(value[:-1].replace(',', '')) * 1e6   # Multiplicar por 1 million
        else:
            return float(value.replace(',', ''))  

    for col in cols:
        df[col] = df[col].apply(convert)
    return df

def selection_currency(DF, n = 5):
    df = DF.copy()

    cryptos = df.sort_values(by=['market_cap', 'change_%'], ascending= False).head(n)
    list = list(cryptos['symbol'])

    return list

