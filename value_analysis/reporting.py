"""Reporting module for value stock analysis."""
from typing import Dict, Optional
from datetime import datetime
import pandas as pd
from .visualization import ValueVisualizer

class ValueReport:
    def __init__(self, analysis: Dict):
        self.analysis = analysis
        self.visualizer = ValueVisualizer()
    
    def generate_pdf_report(self, output_path: str) -> None:
        """Generate a PDF report with analysis and visualizations."""
        # Note: This would require additional PDF generation library
        pass
    
    def generate_excel_report(self, output_path: str) -> None:
        """Generate an Excel report with analysis data."""
        writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
        
        # Write fundamental metrics
        pd.DataFrame(self.analysis['fundamental_metrics'].items(),
                    columns=['Metric', 'Value']).to_excel(writer, sheet_name='Fundamentals')
        
        # Write growth metrics
        pd.DataFrame(self.analysis['growth_metrics'].items(),
                    columns=['Metric', 'Value']).to_excel(writer, sheet_name='Growth')
        
        # Write efficiency metrics
        pd.DataFrame(self.analysis['efficiency_metrics'].items(),
                    columns=['Metric', 'Value']).to_excel(writer, sheet_name='Efficiency')
        
        writer.save()
    
    def generate_html_report(self, output_path: str) -> None:
        """Generate an HTML report with analysis and interactive charts."""
        # Create HTML template with analysis data
        html_content = f"""
        <html>
        <head>
            <title>Value Stock Analysis - {self.analysis['symbol']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .metric {{ margin: 10px 0; }}
                .section {{ margin: 20px 0; }}
            </style>
        </head>
        <body>
            <h1>Value Stock Analysis Report</h1>
            <h2>{self.analysis['symbol']}</h2>
            <div class="section">
                <h3>Fundamental Metrics</h3>
                {self._metrics_to_html(self.analysis['fundamental_metrics'])}
            </div>
            <div class="section">
                <h3>Growth Metrics</h3>
                {self._metrics_to_html(self.analysis['growth_metrics'])}
            </div>
            <div class="section">
                <h3>Competitive Analysis</h3>
                <p>{self.analysis['competitive_analysis']['assessment']}</p>
            </div>
        </body>
        </html>
        """
        
        with open(output_path, 'w') as f:
            f.write(html_content)
    
    def _metrics_to_html(self, metrics: Dict) -> str:
        """Convert metrics dictionary to HTML format."""
        html = '<div class="metrics">'
        for metric, value in metrics.items():
            html += f'<div class="metric"><strong>{metric}:</strong> {value:.2f}</div>'
        html += '</div>'
        return html
