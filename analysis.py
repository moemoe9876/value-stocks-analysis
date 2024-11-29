import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_returns(data):
    """Calculate daily, monthly, and annual returns."""
    daily_returns = data['Close'].pct_change()
    monthly_returns = data['Close'].resample('M').last().pct_change()
    annual_returns = data['Close'].resample('Y').last().pct_change()
    return daily_returns, monthly_returns, annual_returns

def calculate_metrics(returns):
    """Calculate key investment metrics."""
    metrics = {
        'Annual Return': returns.mean() * 252,
        'Volatility': returns.std() * np.sqrt(252),
        'Sharpe Ratio': (returns.mean() * 252) / (returns.std() * np.sqrt(252)),
        'Max Drawdown': (returns.cumsum() - returns.cumsum().cummax()).min()
    }
    return metrics

def plot_performance(data, ticker):
    """Plot stock performance metrics."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Price trend
    ax1.plot(data.index, data['Close'])
    ax1.set_title(f'{ticker} Price History')
    ax1.set_ylabel('Price')
    
    # Returns distribution
    daily_returns = data['Close'].pct_change()
    sns.histplot(daily_returns.dropna(), ax=ax2, bins=50)
    ax2.set_title('Returns Distribution')
    
    plt.tight_layout()
    plt.savefig(f'{ticker}_analysis.png')
    plt.close()

def main():
    tickers = ['AAPL', 'BAC', 'KO', 'CVX', 'OXY']
    metrics_list = []
    
    for ticker in tickers:
        try:
            data = pd.read_csv(f'historical_{ticker}.csv', index_col=0, parse_dates=True)
            daily_returns, monthly_returns, annual_returns = calculate_returns(data)
            metrics = calculate_metrics(daily_returns)
            metrics['Ticker'] = ticker
            metrics_list.append(metrics)
            plot_performance(data, ticker)
        except Exception as e:
            print(f'Error analyzing {ticker}: {e}')
    
    # Save metrics
    metrics_df = pd.DataFrame(metrics_list)
    metrics_df.to_csv('performance_metrics.csv', index=False)

if __name__ == '__main__':
    main()