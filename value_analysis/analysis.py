"""Comprehensive value stock analysis module."""
from typing import Dict, List, Optional
import pandas as pd
import numpy as np
from .metrics import ValueMetrics
from .data_source import DataSource

class ValueAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        self.data_source = DataSource(api_key)
        self.metrics = None

    def analyze_stock(self, symbol: str, years: int = 5) -> Dict:
        """Perform comprehensive value analysis on a stock."""
        # Get financial data
        financials = self.data_source.get_financial_statements(symbol)
        
        # Initialize metrics with income statement data
        self.metrics = ValueMetrics(financials['income_statement'])
        
        # Calculate key metrics
        analysis = {
            'symbol': symbol,
            'fundamental_metrics': self._calculate_fundamental_metrics(financials),
            'growth_metrics': self._calculate_growth_metrics(financials),
            'efficiency_metrics': self._calculate_efficiency_metrics(financials),
            'competitive_analysis': self._analyze_competitive_position(financials)
        }
        
        return analysis
    
    def _calculate_fundamental_metrics(self, financials: Dict[str, pd.DataFrame]) -> Dict:
        """Calculate fundamental value metrics."""
        latest_price = self.data_source.get_latest_price()
        latest_income = financials['income_statement'].iloc[0]
        latest_balance = financials['balance_sheet'].iloc[0]
        
        return {
            'pe_ratio': self.metrics.calculate_pe_ratio(latest_price, latest_income['EPS']),
            'pb_ratio': self.metrics.calculate_pb_ratio(latest_price, latest_balance['Book Value per Share']),
            'debt_to_equity': self.metrics.calculate_debt_to_equity(
                latest_balance['Total Debt'],
                latest_balance['Total Stockholder Equity']
            ),
            'roe': self.metrics.calculate_roe(
                latest_income['Net Income'],
                latest_balance['Total Stockholder Equity']
            )
        }
    
    def _calculate_growth_metrics(self, financials: Dict[str, pd.DataFrame]) -> Dict:
        """Calculate growth metrics over time."""
        income_stmt = financials['income_statement']
        
        revenue_growth = self._calculate_cagr(income_stmt['Total Revenue'])
        earnings_growth = self._calculate_cagr(income_stmt['Net Income'])
        
        return {
            'revenue_growth': revenue_growth,
            'earnings_growth': earnings_growth,
            'sustainable_growth_rate': earnings_growth * (1 - self._get_payout_ratio(income_stmt))
        }
    
    def _calculate_efficiency_metrics(self, financials: Dict[str, pd.DataFrame]) -> Dict:
        """Calculate operational efficiency metrics."""
        latest_income = financials['income_statement'].iloc[0]
        latest_balance = financials['balance_sheet'].iloc[0]
        
        return {
            'operating_margin': self.metrics.calculate_operating_margin(
                latest_income['Operating Income'],
                latest_income['Total Revenue']
            ),
            'asset_turnover': latest_income['Total Revenue'] / latest_balance['Total Assets'],
            'inventory_turnover': latest_income['Cost of Revenue'] / latest_balance['Inventory']
        }
    
    def _analyze_competitive_position(self, financials: Dict[str, pd.DataFrame]) -> Dict:
        """Analyze company's competitive position."""
        income_stmt = financials['income_statement']
        
        operating_margins = income_stmt['Operating Income'] / income_stmt['Total Revenue'] * 100
        market_share = [0] # Would need industry data for actual market share
        industry_margins = [0] # Would need industry data for comparison
        
        return self.metrics.assess_competitive_advantage(
            operating_margins.tolist(),
            market_share,
            industry_margins
        )
    
    def _calculate_cagr(self, series: pd.Series) -> float:
        """Calculate Compound Annual Growth Rate."""
        years = len(series) - 1
        if years > 0 and series.iloc[-1] > 0 and series.iloc[0] > 0:
            return (series.iloc[0] / series.iloc[-1]) ** (1/years) - 1
        return 0
    
    def _get_payout_ratio(self, income_stmt: pd.DataFrame) -> float:
        """Calculate dividend payout ratio."""
        if 'Dividends Paid' in income_stmt.columns and 'Net Income' in income_stmt.columns:
            latest = income_stmt.iloc[0]
            if latest['Net Income'] > 0:
                return abs(latest['Dividends Paid']) / latest['Net Income']
        return 0