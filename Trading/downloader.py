from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf 

def download_stock_data(tickers, days=60, interval='1d'):
    ticker_data = {}
    end_date = datetime.today()  # end_date siempre es la fecha actual

    start_date = end_date - timedelta(days=days)  # Calculamos start_date basado en los días proporcionados

    for ticker in tickers:
        try:
            if interval == '5m':
                # Ajustar fechas para intervalo de 5 minutos
                end_date_adjusted = end_date
                start_date_adjusted = end_date_adjusted - timedelta(days=days)  # Ajuste de días
                print(f"Descargando datos desde {start_date_adjusted.date()} hasta {end_date_adjusted.date()} para {ticker}...")

                # Descargar datos en intervalos de 7 días (ejemplo)
                all_data = pd.DataFrame()
                current_date = end_date_adjusted
                while current_date >= start_date_adjusted:
                    next_date = current_date - timedelta(days=7)
                    weekly_data = yf.download(ticker, start=next_date, end=current_date, interval=interval)
                    all_data = pd.concat([all_data, weekly_data])
                    current_date = next_date

                all_data.dropna(how='any', inplace=True)
                ticker_data[ticker] = all_data.sort_index()

            else:
                # Descargar datos según el intervalo y fechas especificadas
                data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
                data.dropna(how='any', inplace=True)
                ticker_data[ticker] = data

            print(f'Descargando datos para {ticker}')

        except Exception as e:
            print(f'Error al descargar datos para {ticker}: {str(e)}')

    return ticker_data
