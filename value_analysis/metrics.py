"""
Core value investing metrics implementation based on Warren Buffett's principles.
"""
from typing import Dict, Union, Optional
import pandas as pd
import numpy as np

class ValueMetrics:
    def __init__(self, financial_data: pd.DataFrame):
        """
        Initialize with financial data DataFrame containing required metrics.
        
        Args:
            financial_data (pd.DataFrame): DataFrame containing financial data
        """
        self.data = financial_data
        
    def calculate_pe_ratio(self, price: float, eps: float) -> float:
        """
        Calculate Price-to-Earnings ratio.
        
        Args:
            price (float): Current stock price
            eps (float): Earnings per share
            
        Returns:
            float: P/E ratio
        """
        if eps <= 0:
            return float('inf')
        return price / eps
        
    def calculate_pb_ratio(self, price: float, book_value: float) -> float:
        """
        Calculate Price-to-Book ratio.
        
        Args:
            price (float): Current stock price
            book_value (float): Book value per share
            
        Returns:
            float: P/B ratio
        """
        if book_value <= 0:
            return float('inf')
        return price / book_value
        
    def calculate_debt_to_equity(self, total_debt: float, total_equity: float) -> float:
        """
        Calculate Debt-to-Equity ratio.
        
        Args:
            total_debt (float): Total debt
            total_equity (float): Total shareholders' equity
            
        Returns:
            float: Debt-to-Equity ratio
        """
        if total_equity <= 0:
            return float('inf')
        return total_debt / total_equity
        
    def calculate_roe(self, net_income: float, avg_equity: float) -> float:
        """
        Calculate Return on Equity (ROE).
        
        Args:
            net_income (float): Net income
            avg_equity (float): Average shareholders' equity
            
        Returns:
            float: ROE as a percentage
        """
        if avg_equity <= 0:
            return 0.0
        return (net_income / avg_equity) * 100
        
    def calculate_free_cash_flow(self, operating_cash_flow: float, 
                               capital_expenditures: float) -> float:
        """
        Calculate Free Cash Flow.
        
        Args:
            operating_cash_flow (float): Operating cash flow
            capital_expenditures (float): Capital expenditures
            
        Returns:
            float: Free cash flow
        """
        return operating_cash_flow - capital_expenditures
        
    def calculate_operating_margin(self, operating_income: float, 
                                 revenue: float) -> float:
        """
        Calculate Operating Margin.
        
        Args:
            operating_income (float): Operating income
            revenue (float): Total revenue
            
        Returns:
            float: Operating margin as a percentage
        """
        if revenue <= 0:
            return 0.0
        return (operating_income / revenue) * 100
        
    def assess_competitive_advantage(self, 
                                   operating_margins: list,
                                   market_share: list,
                                   industry_margins: list) -> Dict[str, Union[float, str]]:
        """
        Assess competitive advantage period based on historical data.
        
        Args:
            operating_margins (list): Historical operating margins
            market_share (list): Historical market share
            industry_margins (list): Industry average operating margins
            
        Returns:
            Dict containing competitive advantage metrics
        """
        margin_trend = np.polyfit(range(len(operating_margins)), operating_margins, 1)[0]
        market_share_trend = np.polyfit(range(len(market_share)), market_share, 1)[0]
        
        advantage_score = 0
        if margin_trend > 0:
            advantage_score += 1
        if market_share_trend > 0:
            advantage_score += 1
        if np.mean(operating_margins) > np.mean(industry_margins):
            advantage_score += 1
            
        assessment = {
            'margin_trend': margin_trend,
            'market_share_trend': market_share_trend,
            'advantage_score': advantage_score,
            'assessment': self._get_advantage_assessment(advantage_score)
        }
        
        return assessment
        
    def _get_advantage_assessment(self, score: int) -> str:
        """
        Convert competitive advantage score to qualitative assessment.
        
        Args:
            score (int): Numerical advantage score
            
        Returns:
            str: Qualitative assessment
        """
        assessments = {
            0: "No sustainable competitive advantage",
            1: "Weak competitive advantage",
            2: "Moderate competitive advantage",
            3: "Strong competitive advantage"
        }
        return assessments.get(score, "Unknown")
