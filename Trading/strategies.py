import pandas as pd
import numpy as np

### estrategía basica de coger aquellas que van bien y elimnar aquellas que van mal
def pflio(DF,m,x):
    """Returns cumulative portfolio return
    DF = dataframe with monthly return info for all stocks
    m = number of stock in the portfolio
    x = number of underperforming stocks to be removed from portfolio monthly"""
    df = DF.copy()
    portfolio = []
    monthly_ret = [0]
    for i in range(len(df)):
        if len(portfolio) > 0:
            monthly_ret.append(df[portfolio].iloc[i,:].mean())
            bad_stocks = df[portfolio].iloc[i,:].sort_values(ascending=True)[:x].index.values.tolist()
            portfolio = [t for t in portfolio if t not in bad_stocks]
        fill = m - len(portfolio)

         # restar de todos los activos aquellos que han tenido peor performance
        new_picks = df.iloc[i,:].sort_values(ascending=False)[:fill].index.values.tolist()
        #new_picks = df[[t for t in top_10 if t not in portfolio]].iloc[i, :].sort_values(ascending = False)[:fill].index.values.tolist()
        portfolio = portfolio + new_picks
        #print(portfolio)
    monthly_ret_df = pd.DataFrame(np.array(monthly_ret),columns=["ret"])
    return monthly_ret_df

def strategy_signal(x, tickers, tickers_signal, tickers_ret):

    ohlc_dict = x
    tickers_signal = tickers_signal
    tickers_ret = tickers_ret

    for ticker in tickers:
        print("calculating returns for ",ticker)
        for i in range(1,len(ohlc_dict[ticker])):
            if tickers_signal[ticker] == "":
                tickers_ret[ticker].append(0)
                if ohlc_dict[ticker]["High"][i]>=ohlc_dict[ticker]["roll_max_cp"][i] and \
                ohlc_dict[ticker]["Volume"][i]>1.5*ohlc_dict[ticker]["roll_max_vol"][i-1]:
                    tickers_signal[ticker] = "Buy"
                elif ohlc_dict[ticker]["Low"][i]<=ohlc_dict[ticker]["roll_min_cp"][i] and \
                ohlc_dict[ticker]["Volume"][i]>1.5*ohlc_dict[ticker]["roll_max_vol"][i-1]:
                    tickers_signal[ticker] = "Sell"
            
            ### entender con palabras claras
            elif tickers_signal[ticker] == "Buy":
                if ohlc_dict[ticker]["Low"][i]<ohlc_dict[ticker]["Close"][i-1] - ohlc_dict[ticker]["ATR"][i-1]:
                    tickers_signal[ticker] = ""
                    tickers_ret[ticker].append(((ohlc_dict[ticker]["Close"][i-1] - ohlc_dict[ticker]["ATR"][i-1])/ohlc_dict[ticker]["Close"][i-1])-1)
                elif ohlc_dict[ticker]["Low"][i]<=ohlc_dict[ticker]["roll_min_cp"][i] and \
                ohlc_dict[ticker]["Volume"][i]>1.5*ohlc_dict[ticker]["roll_max_vol"][i-1]:
                    tickers_signal[ticker] = "Sell"
                    tickers_ret[ticker].append((ohlc_dict[ticker]["Close"][i]/ohlc_dict[ticker]["Close"][i-1])-1)
                else:
                    tickers_ret[ticker].append((ohlc_dict[ticker]["Close"][i]/ohlc_dict[ticker]["Close"][i-1])-1)
                    
            elif tickers_signal[ticker] == "Sell":
                if ohlc_dict[ticker]["High"][i]>ohlc_dict[ticker]["Close"][i-1] + ohlc_dict[ticker]["ATR"][i-1]:
                    tickers_signal[ticker] = ""
                    tickers_ret[ticker].append((ohlc_dict[ticker]["Close"][i-1]/(ohlc_dict[ticker]["Close"][i-1] + ohlc_dict[ticker]["ATR"][i-1]))-1)
                elif ohlc_dict[ticker]["High"][i]>=ohlc_dict[ticker]["roll_max_cp"][i] and \
                ohlc_dict[ticker]["Volume"][i]>1.5*ohlc_dict[ticker]["roll_max_vol"][i-1]:
                    tickers_signal[ticker] = "Buy"
                    tickers_ret[ticker].append((ohlc_dict[ticker]["Close"][i-1]/ohlc_dict[ticker]["Close"][i])-1)
                else:
                    tickers_ret[ticker].append((ohlc_dict[ticker]["Close"][i-1]/ohlc_dict[ticker]["Close"][i])-1)
                    
        ohlc_dict[ticker]["ret"] = np.array(tickers_ret[ticker])
    
    return ohlc_dict
