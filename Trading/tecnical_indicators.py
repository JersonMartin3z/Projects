import numpy as np
from stocktrends import Renko
import copy


######## ----------------------------------------------------------- ##########
# Calcular la rentabilidad de la estrategia
def CAGR(DF, x):
    "function to calculate the Cumulative Annual Growth Rate of a trading strategy"
    df = DF.copy()
    df["cum_return"] = (1 + df["ret"]).cumprod()
    n = len(df)/(252 * x)
    CAGR = (df["cum_return"].tolist()[-1])**(1/n) - 1
    return CAGR


def volatility(DF, x):
    "function to calculate annualized volatility of a trading strategy"
    df = DF.copy()
    vol = df["ret"].std() * np.sqrt(252 * x)
    return vol

def sharpe(DF, rf):
    df =  DF.copy()
    sr = (CAGR(df) - 0.03)/volatility(df)
    return sr

##### RENKO ######
def renko_DF(DF, DF2, n=20, atr_period=120):
    # Función para calcular el ATR
    def ATR_RENKO(DF, n):
        df = DF.copy()
        df['H-L'] = df['High'] - df['Low']
        df['H-PC'] = df['High'] - df['Adj Close'].shift(1)
        df['L-PC'] = df['Low'] - df['Adj Close'].shift(1)
        df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)
        df['ATR'] = df['TR'].ewm(span=n, min_periods=n).mean()
        return df['ATR']
    
    # Copiar los DataFrames
    df = DF.copy()
    df_2 = DF2.copy()
    
    # Aplicar los pasos específicos para df
    df.drop('Close', axis=1, inplace=True)
    df.reset_index(inplace=True)
    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    
    # Calcular el tamaño del ladrillo de Renko
    brick_size = 3 * round(ATR_RENKO(df_2, atr_period).iloc[-1], 0)
    
    # Crear objeto Renko y obtener los datos OHLC
    renko = Renko(df)
    renko.brick_size = brick_size
    renko_df = renko.get_ohlc_data()
    
    return renko_df


######## ----------------------------------------------------------- ##########
def ATR(DF, n =20):
    df = DF.copy()
    df['H-L'] = df['High'] - df['Low']
    df['H-PC'] = df['High'] - df['Adj Close'].shift(1)
    df['L-PC'] = df['High'] - df['Adj Close'].shift(1)
    df['TR'] = df[['H-L','H-PC','L-PC']].max(axis=1,skipna = False)
    df['ATR'] = df['TR'].rolling(n).mean()
    #df['ATR'] = df['TR'].ewm(com=n, min_periods=n).mean()
    return df['ATR']

def max_dd(DF):
    "function to calculate max drawdown"
    df = DF.copy()
    df["cum_return"] = (1 + df["ret"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    df["drawdown_pct"] = df["drawdown"]/df["cum_roll_max"]
    max_dd = df["drawdown_pct"].max()
    return max_dd


def creating_signals(DF, tickers, x):

    dict_tickers = copy.deepcopy(DF)
    tickers_signal = {}
    tickers_ret = {}

    for ticker in tickers:
        dict_tickers[ticker]["ATR"] = ATR(dict_tickers[ticker], x)
        dict_tickers[ticker]["roll_max_cp"] = dict_tickers[ticker]["High"].rolling(20).max()
        dict_tickers[ticker]["roll_min_cp"] = dict_tickers[ticker]["Low"].rolling(20).min()
        dict_tickers[ticker]["roll_max_vol"] = dict_tickers[ticker]["Volume"].rolling(20).max()
        dict_tickers[ticker].dropna(inplace=True)
        tickers_signal[ticker] = ""
        tickers_ret[ticker] = [0]
    
    return dict_tickers, tickers_signal, tickers_ret

'''
def CARG(DF, x=1):
    # calculo del rate anual de la estrategia diaria. ^ Con datos diarios. 
    df = DF.copy()
    df['daily_ret'] = df['Adj Close'].pct_change()
    df['cum_return'] = (1 + df['daily_ret']).cumprod()
    n = len(df)/252 * x
    CARG = (df['cum_return'].iloc[-1])**(1/n) - 1
    return CARG




####### Revisar
def max_dd(DF, period=14):
    df = DF.copy()
    
    # Calcular los retornos diarios como el cambio porcentual del precio de cierre ajustado
    df['return'] = df['Adj Close'].pct_change()
    
    # Calcular el retorno acumulado como el producto acumulativo de (1 + retorno diario)
    df['cum_return'] = (1 + df['return']).cumprod()
    
    # Calcular el máximo acumulado rodante de los retornos acumulados en el período especificado
    df['cum_roll_max'] = df['cum_return'].rolling(window=period, min_periods=1).max()
    
    # Calcular el drawdown como la diferencia entre el máximo acumulado y el retorno acumulado actual
    df['drawdown'] = df['cum_roll_max'] - df['cum_return']
    
    # Calcular el drawdown máximo relativo en el período especificado
    max_drawdown_relative = (df['drawdown'] / df['cum_roll_max']).max()
    
    return max_drawdown_relative



def volatility(DF):
    "Función para calcular la volatilidad anualizada de la estrategía"
    df = DF.copy()
    df['daily_ret'] =  DF['Adj Close'].pct_change()
    vol = df['daily_ret'].std() *  np.sqrt(252 * 24)
    return vol

def sharpe(DF, rf):
    df =  DF.copy()
    sr = (CARG(df) - 0.03)/volatility(df)
    return sr


def sortino(DF, rf):
    df =  DF.copy()
    df['return'] = df.pct_change()
    neg_return = np.where(df['return'] > 0, 0, df['return'])
    neg_vol = pd.Series(neg_return[neg_return!=0]).std() * np.sqrt(252 * 24)
    sortin =(CARG(df)/volatility(df))
    return sortin


def calmar(DF):
    df = DF.copy()
    calm = CARG(df)/max_dd(DF)
    return calm


'''
###########


def RSI (DF, n =14):
    df = DF.copy()
    df['change'] =  df['Adj Close'] - df['Adj Close'].shift(1)
    df['gain'] = np.where(df['change']>= 0,df['change'],0)
    df['loss'] = np.where(df['change']< 0, -1*df['change'],0)
    df['avgGain'] = df['gain'].ewm(alpha= 1/n, min_periods = n).mean()
    df['avgLoss'] = df['loss'].ewm(alpha= 1/n, min_periods = n).mean()
    df['rs'] =  df['avgGain']/df['avgLoss']
    df['rsi'] = 100 - (100/(1 +df['rs']))
    return df['rsi']



def ADX(DF, n=20):
    df = DF.copy()
    df['ATR'] = ATR(df, n)
    df['upmove'] = df['High'] - df['High'].shift(1)
    df['downmove'] = df['Low'].shift(1) - df['Low']
    df['+dm'] = np.where((df['upmove']>df['downmove']) & (df['upmove']>0),df['upmove'], 0)
    df['-dm'] = np.where((df['downmove']>df['upmove']) & (df['downmove']>0),df['downmove'], 0)
    df['+di'] = 100 * (df['+dm']/df['ATR']).ewm(span = n, min_periods = n).mean()
    df['-di'] = 100 * (df['-dm']/df['ATR']).ewm(span = n, min_periods = n).mean()    
   
    df['ADX'] = 100 * abs((df['+di'] - df['-di'])/(df['+di'] + df['-di'])).ewm(span = n, min_periods = n).mean()
    df['ADX'] = df['ADX'].fillna(0) 
    return df['ADX']
   

def Boll_Band (DF, n=14):
    df = DF.copy()
    df['MB'] = df['Adj Close'].rolling(n).mean()
    df['UB'] = df['MB'] + 2*df['Adj Close'].rolling(n).std(ddof = 0)
    df['LB'] = df['MB'] - 2*df['Adj Close'].rolling(n).std(ddof = 0)
    df['BB_Width'] = df["UB"] - df['LB']
    return df[['MB', 'UB', 'LB', 'BB_Width']]



def MACD (DF, a = 12, b = 26, c = 9):
    df =DF.copy()
    df['ma_fast'] = df['Adj Close'].ewm(span=a, min_periods= a).mean()
    df['ma_slow'] = df['Adj Close'].ewm(span=b, min_periods= b).mean()
    df['macd'] = df['ma_fast'] - df['ma_slow']
    df['signal'] = df['macd'].ewm(span=c, min_periods= c).mean()
    return  df.loc[:, ['macd', 'signal']]


