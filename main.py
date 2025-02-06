import argparse
import sys
import os
import pandas as pd
from data_loader import load_data
from dcf_calculator import DCFCalculator

def main():
    parser = argparse.ArgumentParser(description="Automated DCF Valuation Script")
    parser.add_argument("excel_file", help="Path to the Excel file containing DCF data")
    parser.add_argument("--output", help="Path to output file (Excel)", default="dcf_output.xlsx")
    args = parser.parse_args()

    # Check if the Excel file exists
    if not os.path.exists(args.excel_file):
        print(f"Error: File {args.excel_file} does not exist.")
        sys.exit(1)

    # Load data from Excel
    assumptions, projections_df = load_data(args.excel_file)
    print("\n*** Loaded Assumptions ***")
    for key, value in assumptions.items():
        print(f"  {key}: **{value}**")

    print("\n*** Projections Data (first 5 rows) ***")
    print(projections_df.head())

    # Run the DCF calculation
    calculator = DCFCalculator(projections_df, assumptions)
    results = calculator.calculate()

    # Print DCF Results (numbers are shown in **bold**)
    print("\n*** DCF Valuation Results ***")
    print(f"Total Discounted FCF: **{results['discounted_fcf_total']:.2f}**")
    print(f"Terminal Value: **{results['terminal_value']:.2f}**")
    print(f"Discounted Terminal Value: **{results['terminal_value_discounted']:.2f}**")
    print(f"Enterprise Value: **{results['enterprise_value']:.2f}**")
    print(f"Equity Value (after subtracting Net Debt): **{results['equity_value']:.2f}**")

    # Save detailed projections with discounted FCFs to output Excel file
    with pd.ExcelWriter(args.output) as writer:
        results['projections'].to_excel(writer, index=False, sheet_name="Detailed_Projections")
        summary_df = pd.DataFrame({
            "Metric": ["Total Discounted FCF", "Terminal Value", "Discounted Terminal Value", "Enterprise Value", "Equity Value"],
            "Value": [results['discounted_fcf_total'], results['terminal_value'], results['terminal_value_discounted'], results['enterprise_value'], results['equity_value']]
        })
        summary_df.to_excel(writer, index=False, sheet_name="Summary")
    print(f"\nDetailed output saved to **{args.output}**.")

if __name__ == "__main__":
    main()
