"""Example of backtesting a value investing strategy."""
from value_analysis import Backtester
from value_analysis.data_source import DataSource

def value_strategy(data):
    """Define a simple value investing strategy."""
    return {
        'buy': data['pe_ratio'] < 15 and data['pb_ratio'] < 1.5,
        'position_size': 1.0 if data['pe_ratio'] < 15 else 0.0
    }

def main():
    # Get historical data
    data_source = DataSource()
    stock_data = data_source.get_stock_data('AAPL', '2020-01-01', '2023-12-31')
    
    # Initialize backtester
    backtester = Backtester(stock_data)
    
    # Run backtest
    results = backtester.run_backtest(
        strategy=value_strategy,
        start_date='2020-01-01',
        end_date='2023-12-31'
    )
    
    # Print results
    print('Backtest Results:')
    print(f"Total Return: {results['total_return']:.2%}")
    print(f"Max Drawdown: {results['max_drawdown']:.2%}")
    print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")

if __name__ == '__main__':
    main()