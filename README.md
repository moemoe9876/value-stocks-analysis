# Value Stocks Analyzer

Python toolkit for analyzing value stocks using Warren Buffett's investment principles.

## Files

- `stock_data.py`: Fetches historical prices and financial metrics
- `analysis.py`: Calculates returns and risk metrics
- `value_screener.py`: Implements Buffett's value criteria
- `requirements.txt`: Lists required Python packages

## Setup and Usage

```bash
git clone https://github.com/moemoe9876/value-stocks-analysis.git
cd value-stocks-analysis
pip install -r requirements.txt

# Run in sequence:
python stock_data.py
python analysis.py
python value_screener.py
```

## Features

- Fetches data using yfinance API
- Analyzes key metrics (P/E, P/B, ROE)
- Calculates returns and volatility
- Generates performance visualizations
- Scores stocks based on Buffett criteria

## Disclaimer

For educational purposes only. Do your own research before investing.