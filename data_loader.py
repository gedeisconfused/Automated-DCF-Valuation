import pandas as pd

def load_data(excel_file):
    """
    Loads data from an Excel file.
    
    Expects two sheets:
    
    1. **Assumptions**  
       Must have two columns: 'Parameter' and 'Value'.  
       Example:
       | Parameter             | Value   |
       |-----------------------|---------|
       | discount_rate         | 0.10    |
       | terminal_growth_rate  | 0.02    |
       | net_debt              | 5000000 |
    
    2. **Projections**  
       Must include the columns: Year, Revenue, EBITDA, Depreciation, CapEx, Change in NWC.
    
    :param excel_file: Path to the Excel file.
    :return: Tuple (assumptions, projections_df)
    """
    # Load assumptions
    assumptions_df = pd.read_excel(excel_file, sheet_name='Assumptions')
    assumptions = {}
    for index, row in assumptions_df.iterrows():
        param = row['Parameter']
        value = row['Value']
        assumptions[param] = value

    # Load projections
    projections_df = pd.read_excel(excel_file, sheet_name='Projections')
    return assumptions, projections_df
