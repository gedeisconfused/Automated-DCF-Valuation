# Automated Discounted Cash Flow (DCF) Valuation Tool
An attempt at combining my finance + python knowledge. 

This project automates the process of building a **Discounted Cash Flow (DCF)** model using **Python**. It reads a company’s financial data and assumptions from an Excel file, computes free cash flows, terminal value, and ultimately the **enterprise** and **equity** values.

Is it oversimplified? Probably. Does it work? I think so...

---

## **Project Structure**

dcf_project/

├── main.py                  *Main script to run the DCF analysis*

├── dcf_calculator.py        *Module containing the DCF calculation logic*

├── data_loader.py           *Module for loading and parsing Excel data*

├── requirements.txt         *Python dependencies*

├── README.md                *Project overview and instructions*

├── sample_data.xlsx         *Sample Excel file with DCF inputs (see below)*

└── .gitignore               *Git ignore file*

---

## **Excel File Format (sample_data.xlsx)**

The Excel file should contain **two sheets**:

### **1. Assumptions**

This sheet must include two columns: **Parameter** and **Value**. For example:

| Parameter             | Value    |
|-----------------------|----------|
| discount_rate         | **0.10** |
| terminal_growth_rate  | **0.02** |
| net_debt              | **5000000** |

### **2. Projections**

This sheet must include the following columns:

| Year | Revenue  | EBITDA  | Depreciation | CapEx  | Change in NWC |
|------|----------|---------|--------------|--------|---------------|
| 2024 | 10000000 | 2000000 | 500000       | 300000 | 200000        |
| 2025 | 11000000 | 2200000 | 550000       | 330000 | 220000        |
| 2026 | 12100000 | 2420000 | 605000       | 363000 | 242000        |
| 2027 | 13310000 | 2662000 | 665500       | 399300 | 266200        |
| 2028 | 14641000 | 2928200 | 732050       | 439230 | 292820        |

> **Note:** Free Cash Flow (FCF) is automatically computed as:  
> **FCF = EBITDA - Depreciation - CapEx - Change in NWC**

---

## **Setup Instructions**

1. **Clone or Download the Repository:**
   ```bash
   git clone <repository_url>
   cd dcf_project

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare Your Excel File:**
   - Use the provided `sample_data.xlsx` or create your own following the format above.

4. **Run the DCF Analysis:**
   ```bash
   python main.py sample_data.xlsx --output dcf_results.xlsx
   ```
   - Replace `sample_data.xlsx` with your Excel file if necessary.
   - The results will be printed in the console and saved to `dcf_results.xlsx`.
