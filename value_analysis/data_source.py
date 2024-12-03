"""Data source integration for financial data retrieval."""
from typing import Dict, List, Optional
import pandas as pd
import yfinance as yf

class DataSource:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        
    def get_stock_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Retrieve stock data from Yahoo Finance."""
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(start=start_date, end=end_date)
            return data
        except Exception as e:
            raise Exception(f'Error fetching data for {symbol}: {str(e)}')
            
    def get_financial_statements(self, symbol: str) -> Dict[str, pd.DataFrame]:
        """Retrieve financial statements for a company."""
        try:
            stock = yf.Ticker(symbol)
            return {
                'income_statement': stock.financials,
                'balance_sheet': stock.balance_sheet,
                'cash_flow': stock.cashflow
            }
        except Exception as e:
            raise Exception(f'Error fetching financials for {symbol}: {str(e)}')