# Value Stocks Analysis

Python toolkit for analyzing value stocks using Warren Buffett's investment principles.

## Features

- Historical data fetching using yfinance
- Key metrics calculation (P/E, P/B, ROE, etc.)
- Performance analysis (returns, volatility, Sharpe ratio)
- Value screening based on Buffett's criteria
- Visualization of price trends and returns

## Scripts

`stock_data.py`
- Fetches historical prices and financial metrics
- Saves data to CSV files for analysis

`analysis.py`
- Calculates returns and risk metrics
- Generates performance visualizations
- Computes Sharpe ratios and drawdowns

`value_screener.py`
- Implements Buffett's value criteria
- Scores stocks based on fundamental metrics
- Produces final analysis report

## Installation

```bash
git clone https://github.com/moemoe9876/value-stocks-analysis.git
cd value-stocks-analysis
pip install -r requirements.txt
```

## Usage

Run scripts in sequence:
```bash
python stock_data.py
python analysis.py
python value_screener.py
```

## Metrics

- Price ratios (P/E, P/B)
- Financial health (Debt/Equity)
- Profitability (ROE, Margins)
- Risk metrics (Volatility, Drawdown)
- Returns (Daily, Monthly, Annual)

## Disclaimer

For educational purposes only. Conduct thorough research before making investment decisions.