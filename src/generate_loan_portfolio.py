import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def generate_loan_portfolio(n_loans: int = 1000, random_seed: int = 42) -> pd.DataFrame:
    """
    Generate a synthetic loan portfolio for credit risk analysis.

    Columns include PD, LGD, EAD, LTV, provisions, etc.
    """
    rng = np.random.default_rng(random_seed)

    # Basic IDs
    loan_id = np.arange(1, n_loans + 1)
    borrower_id = rng.integers(1, n_loans // 2 + 1, size=n_loans)  # some borrowers have multiple loans

    # Segments and countries
    segments = np.array(["Retail", "SME", "Corporate"])
    segment = rng.choice(segments, size=n_loans, p=[0.5, 0.3, 0.2])

    countries = np.array(["DE", "FR", "IT", "ES", "NL"])
    country = rng.choice(countries, size=n_loans)

    # Dates: origination in last 5 years, maturity 1–10 years after origination
    today = datetime(2025, 1, 1)
    origination_offset_days = rng.integers(0, 5 * 365, size=n_loans)
    origination_date = np.array([today - timedelta(days=int(d)) for d in origination_offset_days])

    maturity_offset_years = rng.integers(1, 10, size=n_loans)
    maturity_date = np.array([
        od + timedelta(days=int(y * 365)) for od, y in zip(origination_date, maturity_offset_years)
    ])

    # Currency: mostly EUR
    currencies = np.array(["EUR", "USD", "GBP"])
    currency = rng.choice(currencies, size=n_loans, p=[0.8, 0.15, 0.05])

    # Interest rates: slightly different by segment
    base_rate = 0.02  # 2%
    spread_retail = rng.normal(0.02, 0.005, size=n_loans)   # 2% ± 0.5%
    spread_sme = rng.normal(0.03, 0.007, size=n_loans)      # 3% ± 0.7%
    spread_corp = rng.normal(0.015, 0.004, size=n_loans)    # 1.5% ± 0.4%

    interest_rate = np.empty(n_loans)
    interest_rate[segment == "Retail"] = base_rate + spread_retail[segment == "Retail"]
    interest_rate[segment == "SME"] = base_rate + spread_sme[segment == "SME"]
    interest_rate[segment == "Corporate"] = base_rate + spread_corp[segment == "Corporate"]

    # PD: different ranges per segment (in 0–1)
    pd_retail = rng.beta(a=1.5, b=40, size=n_loans)      # mostly below 5%
    pd_sme = rng.beta(a=2.0, b=25, size=n_loans)         # slightly higher
    pd_corp = rng.beta(a=1.2, b=35, size=n_loans)

    pd_1y = np.empty(n_loans)
    pd_1y[segment == "Retail"] = pd_retail[segment == "Retail"]
    pd_1y[segment == "SME"] = pd_sme[segment == "SME"]
    pd_1y[segment == "Corporate"] = pd_corp[segment == "Corporate"]

    # LGD: typically between 20% and 70%
    lgd = rng.uniform(0.2, 0.7, size=n_loans)

    # EAD: lognormal-like exposure in currency units
    ead = np.exp(rng.normal(10, 1.0, size=n_loans))  # around exp(10) ~ 22k, but wide range

    # Collateral & LTV (some loans unsecured: collateral_value = 0)
    has_collateral = rng.choice([0, 1], size=n_loans, p=[0.3, 0.7])

    # Target LTV distribution: Retail lower, SME medium, Corporate higher variability
    ltv_target = np.empty(n_loans)
    ltv_target[segment == "Retail"] = rng.uniform(0.3, 0.8, size=(segment == "Retail").sum())
    ltv_target[segment == "SME"] = rng.uniform(0.4, 0.9, size=(segment == "SME").sum())
    ltv_target[segment == "Corporate"] = rng.uniform(0.2, 0.9, size=(segment == "Corporate").sum())

    collateral_value = np.zeros(n_loans)
    collateral_value[has_collateral == 1] = ead[has_collateral == 1] / ltv_target[has_collateral == 1]

    # Compute LTV; if no collateral, set NaN
    ltv = np.full(n_loans, np.nan)
    mask_coll = collateral_value > 0
    ltv[mask_coll] = ead[mask_coll] / collateral_value[mask_coll]

    # Defaults: Bernoulli with pd_1y as probability
    is_default = rng.binomial(1, pd_1y)

    # Initialize default_date as a pandas datetime Series filled with NaT
    default_date = pd.Series([pd.NaT] * n_loans, dtype="datetime64[ns]")

    # Populate default dates only for defaulted loans
    default_indices = np.where(is_default == 1)[0]
    for idx in default_indices:
        start = origination_date[idx]
        end = min(today, maturity_date[idx])
        if end <= start:
            default_date[idx] = pd.NaT
        else:
            delta_days = (end - start).days
            offset = rng.integers(0, delta_days + 1)
            default_date[idx] = start + timedelta(days=int(offset))

    # Convert to numpy at the end if desired (not required)
    default_date = default_date.to_numpy()

    # Days past due: higher if defaulted
    days_past_due = np.zeros(n_loans, dtype=int)
    days_past_due[is_default == 1] = rng.integers(90, 361, size=(is_default == 1).sum())
    days_past_due[is_default == 0] = rng.integers(0, 30, size=(is_default == 0).sum())

    # Provisions: roughly EL with some noise (for Coverage Ratio analysis)
    expected_loss = pd_1y * lgd * ead
    provision_amount = expected_loss * rng.uniform(0.8, 1.2, size=n_loans)

    # Internal rating: map PD buckets to ratings
    rating_bins = [0.0, 0.005, 0.01, 0.02, 0.05, 1.0]
    rating_labels = ["AAA", "AA", "A", "BBB", "BB/B"]
    internal_rating = pd.cut(pd_1y, bins=rating_bins, labels=rating_labels, include_lowest=True)
    
    
    df = pd.DataFrame(
        {
            "loan_id": loan_id,
            "borrower_id": borrower_id,
            "segment": segment,
            "country": country,
            "origination_date": origination_date,
            "maturity_date": maturity_date,
            "currency": currency,
            "interest_rate": interest_rate,
            "pd_1y": pd_1y,
            "lgd": lgd,
            "ead": ead,
            "collateral_value": collateral_value,
            "ltv": ltv,
            "is_default": is_default,
            "default_date": default_date,
            "days_past_due": days_past_due,
            "provision_amount": provision_amount,
            "internal_rating": internal_rating,
        }
    )

    # Ensure all date fields are pure dates (no time component)
    df["origination_date"] = pd.to_datetime(df["origination_date"]).dt.date
    df["maturity_date"] = pd.to_datetime(df["maturity_date"]).dt.date
    df["default_date"] = pd.to_datetime(df["default_date"]).dt.date
    return df


def main():
    DATA_DIR.mkdir(exist_ok=True)

    df = generate_loan_portfolio(n_loans=1000, random_seed=42)

    # Save to CSV and Excel
    csv_path = DATA_DIR / "loan_portfolio.csv"
    xlsx_path = DATA_DIR / "loan_portfolio.xlsx"

    df.to_csv(csv_path, index=False)
    df.to_excel(xlsx_path, index=False)

    print(f"Saved loan portfolio to:\n- {csv_path}\n- {xlsx_path}")


if __name__ == "__main__":
    main()
