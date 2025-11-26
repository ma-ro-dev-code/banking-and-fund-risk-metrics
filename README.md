# Synthetic Loan Portfolio – Credit Risk Analysis (PD, LGD, EAD, LTV, EL, Coverage, Stress Testing)

This repository contains a fully synthetic credit risk dataset and a series of Jupyter
notebooks demonstrating how core banking risk metrics are calculated, analyzed and visualized.
The project is designed as an educational, end-to-end example of how risk analysts and
regulatory reporting teams (IFRS 9 / Basel / Credit Risk) work with loan portfolio data.

All data is **100% synthetic**, generated in Python using controlled statistical distributions
(no real borrowers, no real bank data).

---

## 📂 Repository Structure

```
📁 notebooks/
│   ├── 01_credit_risk_metrics.ipynb
│   ├── 02_portfolio_concentration.ipynb        (coming soon)
│   └── 03_ifrs9_and_rating_migration.ipynb     (coming soon)

📁 data/
│   └── loan_portfolio.xlsx

📁 src/
│   └── generate_loan_portfolio.py

📄 README.md
📄 LICENSE
```
---

# 🎯 Project Overview

The goal of this project is to:

- simulate a realistic banking-style loan portfolio  
- compute key **credit risk metrics** (PD, LGD, EAD, LTV, Expected Loss)  
- analyze provisions, coverage ratio and stress scenarios  
- build modular notebooks for different aspects of credit risk  
- provide a clean, readable, educational reference for risk analysts

This repository is intended as a **learning resource**, a **portfolio project**, and a
**demonstration of analytical and reporting skills**.

---

# 📊 Dataset Description

The dataset `loan_portfolio.xlsx` represents a synthetic loan book with 1,000 loans.

Each record corresponds to a loan with attributes such as:

- borrower characteristics  
- segment (Retail / SME / Corporate)  
- country  
- origination & maturity dates  
- collateral value  
- exposure  
- rating and PD  
- LGD  
- default indicators  
- provisions

The dataset is generated using `src/generate_loan_portfolio.py`.

---

# 📘 Glossary of Credit Risk Metrics  
*(professional, clean definitions with formulas)*

This section explains all key credit risk metrics included in the dataset.  
Each metric is described as it would appear in a professional banking risk report.

---

## 1. Probability of Default (PD)

**Definition:**  
PD estimates the probability that a borrower will default within a horizon (here: **1 year**).

**Range:** 0–1 (0% to 100%)

**Meaning:**
- PD = 0.01 → 1% probability of default  
- PD = 0.10 → 10% probability  
- Higher PD = weaker credit quality  

**Formula (conceptual):**

**PD = Probability of default within 12 months**

In this synthetic dataset, PD is generated using beta distributions per segment.

---

## 2. Loss Given Default (LGD)

**Definition:**  
LGD measures the share of exposure that the bank loses **if** a default occurs.

**LGD = 1 - Recovery Rate**

**Typical range:** 20–70% for collateralised loans  
Higher LGD = lower recoveries.

In this dataset, LGD is drawn from a uniform distribution between 0.20 and 0.70.

---

## 3. Exposure at Default (EAD)

**Definition:**  
EAD represents the amount of exposure outstanding at the moment of default.

EAD = Exposure if the borrower defaults today  
(The amount the bank is exposed to at the moment of default)

It is the “size” of the risk.

Values are lognormally distributed to simulate realistic skewness.

---

## 4. Expected Loss (EL)

Core credit risk metric:

**Expected Loss = PD × LGD × EAD**

- EL per loan  
- EL per segment  
- total portfolio EL  
- EL as % of EAD  

Used in Basel and IFRS 9 frameworks.

---

## 5. Loan-to-Value (LTV)

**Definition:**  
LTV measures how well collateral covers the exposure:

**LTV = EAD / Collateral Value**

- LTV < 0.8 → well-collateralised  
- LTV ≈ 1.0 → borderline  
- LTV > 1.0 → under-collateralised (no collateral buffer)

In this synthetic dataset, no loans exceed 100% LTV, representing a conservative portfolio.

---

## 6. Default indicator & default date

- `is_default` = 1 if the loan is simulated to have defaulted  
- default dates are generated randomly within the loan lifetime for defaulted loans

---

## 7. Days Past Due (DPD)

DPD simulates how many days payments are overdue.

- Performing loans: 0–30 days  
- Defaulted loans: 90–360 days  

Used in IFRS 9 staging:
- Stage 1 → DPD < 30  
- Stage 2 → DPD ≥ 30  
- Stage 3 → default  

---

## 8. Internal Rating

Loans are mapped into buckets based on PD:

- AAA  
- AA  
- A  
- BBB  
- BB/B  

This enables rating-based analysis and migration matrices.

---

## 9. Provisions (loan loss allowances)

Synthetic provision amounts are modeled as:

**Provision ≈ Expected Loss × (0.8 - 1.2)**  
A simple band indicating that provisions are modeled as ±20% around EL.
This allows realistic **Coverage Ratio** analysis.

---

## 10. Coverage Ratio

Indicates whether a loan or segment has sufficient reserves:

**Coverage Ratio = Provision / Expected Loss**

- >1.0 → over-reserved  
- <1.0 → under-reserved  
- ≈1.0 → adequate  

A stress scenario (PD × 1.5, LGD × 1.2) illustrates provisioning adequacy under downturns.

---

# 📓 Notebook Overview

### 📘 **01_credit_risk_metrics.ipynb**  
Core analysis:

- PD, LGD, EAD distributions  
- EL per loan, per segment, portfolio-level  
- LTV buckets & interpretation  
- Provisions and Coverage Ratio  
- Stress testing (PD × 1.5, LGD × 1.2)  
- Professional commentary & conclusions

---

### 📘 **02_portfolio_concentration.ipynb** *(coming soon)*  
Includes:

- Borrower concentration  
- Top-10 exposures  
- Country exposure  
- Herfindahl-Hirschman Index (HHI)  
- Heatmaps  
- Interpretation

---

### 📘 **03_ifrs9_and_rating_migration.ipynb** *(coming soon)*  
Includes:

- Simple IFRS 9 staging (Stage 1 / 2 / 3)  
- DPD triggers  
- Synthetic rating transitions  
- Migration matrix  
- EL by stage  

---

# ▶️ How to Run

Requirements:

- Python 3.10+
- pandas  
- numpy  
- matplotlib  
- openpyxl  
- jupyter / VSCode notebook plugin

To generate new synthetic data:

python src/generate_loan_portfolio.py


To view analysis:

Open any notebook in `notebooks/` through VSCode or Jupyter Lab.

---

# ⚠️ Disclaimer

All data in this repository is **fully synthetic**.  
This project is for **educational, demonstrational and portfolio purposes only.**  
No real customer or bank data is used.

---

# Author
GitHub: `ma-ro-dev-code`


