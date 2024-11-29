import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_stock_data(ticker_list, period='5y'):
    """Fetch historical stock data for given tickers."""
    data = {}
    for ticker in ticker_list:
        try:
            stock = yf.Ticker(ticker)
            data[ticker] = stock.history(period=period)
        except Exception as e:
            print(f'Error fetching data for {ticker}: {e}')
    return data

def get_key_metrics(ticker_list):
    """Get key value investing metrics for stocks."""
    metrics = []
    for ticker in ticker_list:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            metrics.append({
                'Symbol': ticker,
                'P/E Ratio': info.get('forwardPE', None),
                'P/B Ratio': info.get('priceToBook', None),
                'Debt/Equity': info.get('debtToEquity', None),
                'ROE': info.get('returnOnEquity', None),
                'Profit Margin': info.get('profitMargins', None),
                'Dividend Yield': info.get('dividendYield', None)
            })
        except Exception as e:
            print(f'Error fetching metrics for {ticker}: {e}')
    return pd.DataFrame(metrics)

def main():
    # Value stocks based on search results
    tickers = ['AAPL', 'BAC', 'KO', 'CVX', 'OXY']
    
    # Fetch and save data
    historical_data = fetch_stock_data(tickers)
    metrics = get_key_metrics(tickers)
    
    # Save to CSV
    metrics.to_csv('value_metrics.csv', index=False)
    for ticker, data in historical_data.items():
        data.to_csv(f'historical_{ticker}.csv')

if __name__ == '__main__':
    main()