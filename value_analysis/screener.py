"""Stock screener based on value investing principles."""
from typing import List, Dict, Optional
import pandas as pd
from .analysis import ValueAnalyzer

class ValueScreener:
    def __init__(self, api_key: Optional[str] = None):
        self.analyzer = ValueAnalyzer(api_key)
    
    def screen_stocks(self, symbols: List[str], criteria: Dict) -> pd.DataFrame:
        """Screen stocks based on value investing criteria."""
        results = []
        
        for symbol in symbols:
            try:
                analysis = self.analyzer.analyze_stock(symbol)
                if self._meets_criteria(analysis, criteria):
                    results.append(self._format_result(symbol, analysis))
            except Exception as e:
                print(f"Error analyzing {symbol}: {str(e)}")
        
        return pd.DataFrame(results)
    
    def _meets_criteria(self, analysis: Dict, criteria: Dict) -> bool:
        """Check if stock meets screening criteria."""
        metrics = analysis['fundamental_metrics']
        growth = analysis['growth_metrics']
        
        return all([
            metrics['pe_ratio'] <= criteria.get('max_pe', float('inf')),
            metrics['pb_ratio'] <= criteria.get('max_pb', float('inf')),
            metrics['debt_to_equity'] <= criteria.get('max_debt_to_equity', float('inf')),
            metrics['roe'] >= criteria.get('min_roe', 0),
            growth['revenue_growth'] >= criteria.get('min_revenue_growth', 0),
            growth['earnings_growth'] >= criteria.get('min_earnings_growth', 0)
        ])
    
    def _format_result(self, symbol: str, analysis: Dict) -> Dict:
        """Format analysis results for DataFrame."""
        metrics = analysis['fundamental_metrics']
        growth = analysis['growth_metrics']
        
        return {
            'Symbol': symbol,
            'P/E Ratio': metrics['pe_ratio'],
            'P/B Ratio': metrics['pb_ratio'],
            'Debt/Equity': metrics['debt_to_equity'],
            'ROE (%)': metrics['roe'],
            'Revenue Growth (%)': growth['revenue_growth'] * 100,
            'Earnings Growth (%)': growth['earnings_growth'] * 100,
            'Competitive Position': analysis['competitive_analysis']['assessment']
        }