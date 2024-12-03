# Value Stocks Analysis

A Python package for analyzing value stocks using Warren Buffett's investment principles. This tool helps identify undervalued companies with strong fundamentals and competitive advantages.

## Features

- Core Value Investing Metrics
  - Price-to-Earnings (P/E) Ratio
  - Price-to-Book (P/B) Ratio
  - Debt-to-Equity Ratio
  - Return on Equity (ROE)
  - Free Cash Flow Analysis
  - Operating Margin Trend

- Data Integration
  - Yahoo Finance API integration
  - Historical data analysis
  - Financial statements analysis
  - Real-time price data

- Backtesting Framework
  - Strategy testing
  - Performance metrics
  - Risk analysis
  - Portfolio simulation

- Visualization and Reporting
  - Interactive charts
  - PDF reports
  - Excel exports
  - HTML reports

## Installation

```bash
# Clone the repository
git clone https://github.com/moemoe9876/value-stocks-analysis.git

# Navigate to the project directory
cd value-stocks-analysis

# Install the package
pip install -e .
```

## Quick Start

```python
from value_analysis import ValueAnalyzer, ValueScreener

# Analyze a single stock
analyzer = ValueAnalyzer()
analysis = analyzer.analyze_stock('AAPL')

# Screen multiple stocks
screener = ValueScreener()
criteria = {
    'max_pe': 15,
    'max_pb': 1.5,
    'min_roe': 15
}
results = screener.screen_stocks(['AAPL', 'MSFT', 'GOOGL'], criteria)
```

## Documentation

Detailed documentation is available in the `/docs` directory:
- [Installation Guide](docs/installation.md)
- [Usage Guide](docs/usage.md)
- [API Reference](docs/api_reference.md)

## Testing

Run the test suite:
```bash
pytest tests/
```

## Examples

Check out the examples directory for sample scripts:
- Stock analysis example
- Screening example
- Backtesting example
- Report generation example

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
