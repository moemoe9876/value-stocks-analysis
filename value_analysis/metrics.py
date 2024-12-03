"""Core value investing metrics implementation based on Warren Buffett's principles."""
from typing import Dict, Union, Optional
import pandas as pd
import numpy as np

class ValueMetrics:
    def __init__(self, financial_data: pd.DataFrame):
        self.data = financial_data
        
    def calculate_pe_ratio(self, price: float, eps: float) -> float:
        if eps <= 0:
            return float('inf')
        return price / eps
        
    def calculate_pb_ratio(self, price: float, book_value: float) -> float:
        if book_value <= 0:
            return float('inf')
        return price / book_value
        
    def calculate_debt_to_equity(self, total_debt: float, total_equity: float) -> float:
        if total_equity <= 0:
            return float('inf')
        return total_debt / total_equity
        
    def calculate_roe(self, net_income: float, avg_equity: float) -> float:
        if avg_equity <= 0:
            return 0.0
        return (net_income / avg_equity) * 100