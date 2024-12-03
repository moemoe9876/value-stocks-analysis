"""Example usage of the value stocks analysis package."""
from value_analysis import ValueAnalyzer, ValueScreener

def analyze_single_stock():
    # Initialize analyzer
    analyzer = ValueAnalyzer()
    
    # Analyze a single stock
    analysis = analyzer.analyze_stock('AAPL')
    
    # Print results
    print(f"Analysis Results for {analysis['symbol']}:")
    print("\nFundamental Metrics:")
    for metric, value in analysis['fundamental_metrics'].items():
        print(f"{metric}: {value:.2f}")
    
    print("\nGrowth Metrics:")
    for metric, value in analysis['growth_metrics'].items():
        print(f"{metric}: {value:.2%}")
    
    print("\nCompetitive Analysis:")
    print(analysis['competitive_analysis']['assessment'])

def screen_multiple_stocks():
    # Initialize screener
    screener = ValueScreener()
    
    # Define screening criteria
    criteria = {
        'max_pe': 15,
        'max_pb': 1.5,
        'max_debt_to_equity': 1.0,
        'min_roe': 15,
        'min_revenue_growth': 0.10,
        'min_earnings_growth': 0.15
    }
    
    # Screen stocks
    stocks_to_screen = ['AAPL', 'MSFT', 'GOOGL', 'BRK-B', 'KO']
    results = screener.screen_stocks(stocks_to_screen, criteria)
    
    # Print results
    print("\nScreening Results:")
    print(results.to_string())

if __name__ == '__main__':
    print("Analyzing Single Stock:")
    analyze_single_stock()
    
    print("\nScreening Multiple Stocks:")
    screen_multiple_stocks()