class DCFCalculator:
    def __init__(self, projections_df, assumptions):
        """
        Initializes the DCFCalculator.
        
        :param projections_df: DataFrame containing forecast projections.
               Expected columns: Year, Revenue, EBITDA, Depreciation, CapEx, Change in NWC.
        :param assumptions: Dictionary with keys:
               - 'discount_rate': e.g. **0.10** for **10%**
               - 'terminal_growth_rate': e.g. **0.02** for **2%**
               - 'net_debt': e.g. **5000000** (optional)
        """
        self.projections_df = projections_df.copy()
        self.assumptions = assumptions
        self.discount_rate = assumptions.get('discount_rate', 0.10)
        self.terminal_growth_rate = assumptions.get('terminal_growth_rate', 0.02)
        self.net_debt = assumptions.get('net_debt', 0)

        # Compute Free Cash Flow (FCF) if not provided:
        # **FCF = EBITDA - Depreciation - CapEx - Change in NWC**
        if 'FCF' not in self.projections_df.columns:
            self.projections_df['FCF'] = (
                self.projections_df['EBITDA'] -
                self.projections_df['Depreciation'] -
                self.projections_df['CapEx'] -
                self.projections_df['Change in NWC']
            )

    def calculate(self):
        """
        Performs the DCF calculation.
        
        :return: A dictionary with:
                 - discounted_fcf_total: Sum of discounted free cash flows.
                 - terminal_value: Calculated terminal value.
                 - terminal_value_discounted: Terminal value discounted to present.
                 - enterprise_value: Sum of discounted FCFs and discounted terminal value.
                 - equity_value: Enterprise value minus net debt.
                 - projections: Detailed DataFrame with discounted FCFs.
        """
        results = {}
        discounted_fcf = []
        n_years = self.projections_df.shape[0]

        # Discount each year's FCF
        for idx, row in self.projections_df.iterrows():
            t = idx + 1  # Assuming first row corresponds to t=1
            fcf = row['FCF']
            discounted_value = fcf / ((1 + self.discount_rate) ** t)
            discounted_fcf.append(discounted_value)
            self.projections_df.loc[idx, 'Discounted_FCF'] = discounted_value

        total_dcf = sum(discounted_fcf)
        results['discounted_fcf_total'] = total_dcf

        # Terminal Value calculation using the Gordon Growth Model:
        last_year_fcf = self.projections_df.iloc[-1]['FCF']
        terminal_value = (last_year_fcf * (1 + self.terminal_growth_rate)) / (self.discount_rate - self.terminal_growth_rate)
        terminal_value_discounted = terminal_value / ((1 + self.discount_rate) ** n_years)
        results['terminal_value'] = terminal_value
        results['terminal_value_discounted'] = terminal_value_discounted

        # Enterprise Value = Sum of discounted FCFs + discounted Terminal Value
        enterprise_value = total_dcf + terminal_value_discounted
        results['enterprise_value'] = enterprise_value

        # Equity Value = Enterprise Value - Net Debt
        equity_value = enterprise_value - self.net_debt
        results['equity_value'] = equity_value

        results['projections'] = self.projections_df
        return results
