"""Tests for value stock analysis."""
import pytest
import pandas as pd
from value_analysis.analysis import ValueAnalyzer

@pytest.fixture
def sample_financials():
    return {
        'income_statement': pd.DataFrame({
            'Total Revenue': [100000, 90000, 80000],
            'Operating Income': [20000, 18000, 15000],
            'Net Income': [15000, 13000, 10000],
            'EPS': [1.5, 1.3, 1.0]
        }),
        'balance_sheet': pd.DataFrame({
            'Total Assets': [200000, 180000, 160000],
            'Total Debt': [80000, 70000, 60000],
            'Total Stockholder Equity': [120000, 110000, 100000],
            'Book Value per Share': [12, 11, 10]
        })
    }

def test_analyze_stock(sample_financials, mocker):
    # Mock data source
    mocker.patch('value_analysis.data_source.DataSource.get_financial_statements',
                 return_value=sample_financials)
    mocker.patch('value_analysis.data_source.DataSource.get_latest_price',
                 return_value=30.0)
    
    analyzer = ValueAnalyzer()
    analysis = analyzer.analyze_stock('TEST')
    
    assert analysis['symbol'] == 'TEST'
    assert 'fundamental_metrics' in analysis
    assert 'growth_metrics' in analysis
    assert 'competitive_analysis' in analysis
    
    metrics = analysis['fundamental_metrics']
    assert metrics['pe_ratio'] == pytest.approx(20.0)
    assert metrics['roe'] > 0