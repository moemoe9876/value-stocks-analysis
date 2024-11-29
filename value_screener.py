import pandas as pd
import numpy as np

def buffett_criteria(metrics_df):
    """Apply Warren Buffett's investment criteria."""
    criteria = {
        'P/E Ratio': lambda x: x < 15,  # Reasonable P/E ratio
        'P/B Ratio': lambda x: x < 3,   # Reasonable P/B ratio
        'Debt/Equity': lambda x: x < 0.5,  # Low debt
        'ROE': lambda x: x > 0.15,  # Strong return on equity
        'Profit Margin': lambda x: x > 0.1,  # Good profit margins
        'Dividend Yield': lambda x: x > 0.02  # Dividend paying
    }
    
    scores = pd.DataFrame(index=metrics_df.index)
    for criterion, condition in criteria.items():
        if criterion in metrics_df.columns:
            scores[criterion] = metrics_df[criterion].apply(
                lambda x: 1 if pd.notnull(x) and condition(x) else 0
            )
    
    scores['Total Score'] = scores.sum(axis=1)
    return scores

def main():
    try:
        # Load metrics
        value_metrics = pd.read_csv('value_metrics.csv')
        performance_metrics = pd.read_csv('performance_metrics.csv')
        
        # Ensure consistent column naming
        value_metrics = value_metrics.rename(columns={'Symbol': 'Ticker'})
        
        # Apply Buffett criteria
        scores = buffett_criteria(value_metrics)
        
        # Combine all metrics
        final_analysis = pd.merge(
            value_metrics,
            performance_metrics,
            on='Ticker',
            how='inner'  # Only keep stocks present in both datasets
        )
        final_analysis['Buffett Score'] = scores['Total Score']
        
        # Save results
        final_analysis.to_csv('final_analysis.csv', index=False)
        
        # Print summary
        print('\nTop Value Stocks by Buffett Criteria:')
        print(final_analysis.sort_values('Buffett Score', ascending=False))
        
    except Exception as e:
        print(f'Error in value screening: {e}')

if __name__ == '__main__':
    main()