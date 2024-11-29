import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Union
import time
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='value_stocks.log'
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

def retry_api_call(func, max_retries: int = 3, delay: int = 1):
    """Decorator for retrying API calls."""
    def wrapper(*args, **kwargs):
        for i in range(max_retries):
            try:
                return func(*args, **kwargs)
            except requests.exceptions.RequestException as e:
                if i == max_retries - 1:
                    logger.error(f"API call failed after {max_retries} attempts: {str(e)}")
                    raise
                logger.warning(f"API call failed, retrying ({i + 1}/{max_retries})")
                time.sleep(delay * (i + 1))
    return wrapper

def validate_metrics_data(metrics_df: pd.DataFrame) -> bool:
    """Validate the metrics DataFrame."""
    required_columns = ['Ticker', 'P/E Ratio', 'P/B Ratio', 'Debt/Equity', 
                       'ROE', 'Profit Margin', 'Dividend Yield']
    
    # Check required columns
    missing_cols = [col for col in required_columns if col not in metrics_df.columns]
    if missing_cols:
        logger.error(f"Missing required columns: {missing_cols}")
        return False
    
    # Check for null values
    null_counts = metrics_df[required_columns].isnull().sum()
    if null_counts.any():
        logger.warning(f"Null values found in columns: \n{null_counts[null_counts > 0]}")
    
    return True

def buffett_criteria(metrics_df: pd.DataFrame) -> pd.DataFrame:
    """Apply Warren Buffett's investment criteria with validation."""
    if not validate_metrics_data(metrics_df):
        raise ValueError("Invalid metrics data")

    criteria = {
        'P/E Ratio': lambda x: x < 15,  # Reasonable P/E ratio
        'P/B Ratio': lambda x: x < 3,   # Reasonable P/B ratio
        'Debt/Equity': lambda x: x < 0.5,  # Low debt
        'ROE': lambda x: x > 0.15,  # Strong return on equity
        'Profit Margin': lambda x: x > 0.1,  # Good profit margins
        'Dividend Yield': lambda x: x > 0.02  # Dividend paying
    }
    
    scores = pd.DataFrame(index=metrics_df.index)
    
    for criterion, condition in criteria.items():
        if criterion in metrics_df.columns:
            scores[criterion] = metrics_df[criterion].apply(
                lambda x: 1 if pd.notnull(x) and condition(x) else 0
            )
        else:
            logger.warning(f"Missing criterion: {criterion}")
            scores[criterion] = 0
    
    scores['Total Score'] = scores.sum(axis=1)
    return scores

def handle_missing_data(df: pd.DataFrame, columns: List[str], 
                       fill_method: str = 'mean') -> pd.DataFrame:
    """Handle missing data in DataFrame."""
    df = df.copy()
    for col in columns:
        if col in df.columns:
            null_count = df[col].isnull().sum()
            if null_count > 0:
                logger.warning(f"Found {null_count} null values in {col}")
                if fill_method == 'mean':
                    df[col].fillna(df[col].mean(), inplace=True)
                elif fill_method == 'median':
                    df[col].fillna(df[col].median(), inplace=True)
                elif fill_method == 'zero':
                    df[col].fillna(0, inplace=True)
    return df

def main():
    try:
        logger.info("Starting value screening process")
        
        # Load metrics with validation
        try:
            value_metrics = pd.read_csv('value_metrics.csv')
            performance_metrics = pd.read_csv('performance_metrics.csv')
        except FileNotFoundError as e:
            logger.error(f"Required CSV file not found: {str(e)}")
            raise
        
        # Validate and handle missing data
        value_metrics = handle_missing_data(
            value_metrics, 
            ['P/E Ratio', 'P/B Ratio', 'Debt/Equity', 'ROE', 'Profit Margin', 'Dividend Yield']
        )
        
        # Ensure consistent column naming
        value_metrics = value_metrics.rename(columns={'Symbol': 'Ticker'})
        
        # Validate tickers
        invalid_tickers = [ticker for ticker in value_metrics['Ticker'] 
                          if not validate_ticker(ticker)]
        if invalid_tickers:
            logger.warning(f"Found invalid tickers: {invalid_tickers}")
        
        # Apply Buffett criteria
        try:
            scores = buffett_criteria(value_metrics)
        except ValueError as e:
            logger.error(f"Error in Buffett criteria calculation: {str(e)}")
            raise
        
        # Combine metrics with proper error handling
        try:
            final_analysis = pd.merge(
                value_metrics,
                performance_metrics,
                on='Ticker',
                how='inner'
            )
            final_analysis['Buffett Score'] = scores['Total Score']
        except Exception as e:
            logger.error(f"Error merging datasets: {str(e)}")
            raise
        
        # Save results
        try:
            final_analysis.to_csv('final_analysis.csv', index=False)
            logger.info("Analysis completed successfully")
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")
            raise
        
        # Print summary
        print('\nTop Value Stocks by Buffett Criteria:')
        print(final_analysis.sort_values('Buffett Score', ascending=False))
        
    except Exception as e:
        logger.error(f"Error in value screening: {str(e)}")
        raise

if __name__ == '__main__':
    main()