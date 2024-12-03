"""Example of generating analysis reports."""
from value_analysis import ValueAnalyzer, ValueReport

def main():
    # Analyze stock
    analyzer = ValueAnalyzer()
    analysis = analyzer.analyze_stock('AAPL')
    
    # Create report
    report = ValueReport(analysis)
    
    # Generate different report formats
    report.generate_html_report('reports/analysis_report.html')
    report.generate_excel_report('reports/analysis_report.xlsx')
    
    # Print summary to console
    print(report.visualizer.create_summary_report(analysis))

if __name__ == '__main__':
    main()