"""Tests for value investing metrics."""
import pytest
import pandas as pd
from value_analysis.metrics import ValueMetrics

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'price': [100.0],
        'eps': [5.0],
        'book_value': [50.0],
        'total_debt': [1000.0],
        'total_equity': [2000.0]
    })

def test_pe_ratio(sample_data):
    metrics = ValueMetrics(sample_data)
    pe = metrics.calculate_pe_ratio(100.0, 5.0)
    assert pe == 20.0

def test_pb_ratio(sample_data):
    metrics = ValueMetrics(sample_data)
    pb = metrics.calculate_pb_ratio(100.0, 50.0)
    assert pb == 2.0

def test_debt_to_equity(sample_data):
    metrics = ValueMetrics(sample_data)
    de = metrics.calculate_debt_to_equity(1000.0, 2000.0)
    assert de == 0.5