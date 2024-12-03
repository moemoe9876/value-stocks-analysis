"""Visualization tools for value stock analysis."""
from typing import Dict, List
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class ValueVisualizer:
    @staticmethod
    def plot_fundamental_metrics(analysis: Dict) -> plt.Figure:
        """Create bar plot of fundamental metrics."""
        metrics = analysis['fundamental_metrics']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        metrics_df = pd.DataFrame(list(metrics.items()), columns=['Metric', 'Value'])
        
        sns.barplot(data=metrics_df, x='Metric', y='Value', ax=ax)
        ax.set_title(f"Fundamental Metrics for {analysis['symbol']}")
        ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_growth_trends(financials: Dict[str, pd.DataFrame]) -> plt.Figure:
        """Plot revenue and earnings growth trends."""
        income_stmt = financials['income_statement']
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(income_stmt.index, income_stmt['Total Revenue'],
                label='Revenue', marker='o')
        ax.plot(income_stmt.index, income_stmt['Net Income'],
                label='Net Income', marker='o')
        
        ax.set_title('Revenue and Earnings Growth Trends')
        ax.legend()
        ax.grid(True)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_efficiency_metrics(analysis: Dict) -> plt.Figure:
        """Create radar plot of efficiency metrics."""
        metrics = analysis['efficiency_metrics']
        
        # Prepare data
        categories = list(metrics.keys())
        values = list(metrics.values())
        
        # Create radar plot
        angles = [n / float(len(categories)) * 2 * np.pi for n in range(len(categories))]
        values += values[:1]
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        ax.plot(angles, values)
        ax.fill(angles, values, alpha=0.25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        
        plt.title('Efficiency Metrics')
        return fig
    
    @staticmethod
    def create_summary_report(analysis: Dict) -> str:
        """Create a text-based summary report of the analysis."""
        report = [f"Value Stock Analysis Report for {analysis['symbol']}\n"]
        
        # Fundamental Metrics
        report.append("\nFundamental Metrics:")
        for metric, value in analysis['fundamental_metrics'].items():
            report.append(f"{metric}: {value:.2f}")
        
        # Growth Metrics
        report.append("\nGrowth Metrics:")
        for metric, value in analysis['growth_metrics'].items():
            report.append(f"{metric}: {value:.2%}")
        
        # Efficiency Metrics
        report.append("\nEfficiency Metrics:")
        for metric, value in analysis['efficiency_metrics'].items():
            report.append(f"{metric}: {value:.2f}")
        
        # Competitive Analysis
        report.append("\nCompetitive Analysis:")
        report.append(analysis['competitive_analysis']['assessment'])
        
        return '\n'.join(report)
