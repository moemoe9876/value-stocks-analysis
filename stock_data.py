import yfinance as yf
import pandas as pd
import logging
from typing import Dict, List
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='stock_data.log'
)
logger = logging.getLogger(__name__)

def validate_ticker(ticker: str) -> bool:
    """Validate if a ticker symbol is valid."""
    if not isinstance(ticker, str):
        return False
    if not ticker.isalnum():
        return False
    if len(ticker) > 5 or len(ticker) < 1:
        return False
    return True

def retry_api_call(max_retries: int = 3):
    """Decorator for retrying API calls."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        logger.error(f"API call failed after {max_retries} attempts: {str(e)}")
                        raise
                    logger.warning(f"API call failed, retrying ({attempt + 1}/{max_retries})")
            return None
        return wrapper
    return decorator

@retry_api_call(max_retries=3)
def fetch_stock_data(ticker_list: List[str], period: str = '5y') -> Dict[str, pd.DataFrame]:
    """Fetch historical stock data for given tickers."""
    data = {}
    for ticker in ticker_list:
        if not validate_ticker(ticker):
            logger.warning(f"Invalid ticker format: {ticker}")
            continue
            
        try:
            logger.info(f"Fetching data for {ticker}")
            stock = yf.Ticker(ticker)
            data[ticker] = stock.history(period=period)
            if data[ticker].empty:
                logger.warning(f"No data retrieved for {ticker}")
        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {str(e)}")
    return data

@retry_api_call(max_retries=3)
def get_key_metrics(ticker_list: List[str]) -> pd.DataFrame:
    """Get key value investing metrics for stocks."""
    metrics = []
    for ticker in ticker_list:
        if not validate_ticker(ticker):
            logger.warning(f"Invalid ticker format: {ticker}")
            continue
            
        try:
            logger.info(f"Fetching metrics for {ticker}")
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Validate required fields
            required_fields = ['forwardPE', 'priceToBook', 'debtToEquity', 
                             'returnOnEquity', 'profitMargins', 'dividendYield']
            missing_fields = [field for field in required_fields 
                            if field not in info or info[field] is None]
            
            if missing_fields:
                logger.warning(f"Missing fields for {ticker}: {missing_fields}")
            
            metrics.append({
                'Symbol': ticker,
                'P/E Ratio': info.get('forwardPE'),
                'P/B Ratio': info.get('priceToBook'),
                'Debt/Equity': info.get('debtToEquity'),
                'ROE': info.get('returnOnEquity'),
                'Profit Margin': info.get('profitMargins'),
                'Dividend Yield': info.get('dividendYield')
            })
        except Exception as e:
            logger.error(f"Error fetching metrics for {ticker}: {str(e)}")
    
    df = pd.DataFrame(metrics)
    
    # Handle missing values
    for col in df.columns:
        if df[col].isnull().any():
            logger.warning(f"Found {df[col].isnull().sum()} null values in {col}")
            if col != 'Symbol':
                df[col] = df[col].fillna(df[col].mean())
    
    return df

def main():
    try:
        logger.info("Starting data collection process")
        
        # Value stocks based on search results
        tickers = ['AAPL', 'BAC', 'KO', 'CVX', 'OXY']
        
        # Validate tickers
        invalid_tickers = [ticker for ticker in tickers if not validate_ticker(ticker)]
        if invalid_tickers:
            logger.error(f"Invalid tickers found: {invalid_tickers}")
            tickers = [ticker for ticker in tickers if validate_ticker(ticker)]
        
        # Fetch and save data
        historical_data = fetch_stock_data(tickers)
        metrics = get_key_metrics(tickers)
        
        # Save to CSV
        try:
            metrics.to_csv('value_metrics.csv', index=False)
            logger.info("Successfully saved value metrics")
            
            for ticker, data in historical_data.items():
                data.to_csv(f'historical_{ticker}.csv')
                logger.info(f"Successfully saved historical data for {ticker}")
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            raise
            
        logger.info("Data collection process completed successfully")
        
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        raise

if __name__ == '__main__':
    main()