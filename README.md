# Fraud Detection & Risk Mitigation in Nigerian Banking Transactions

Exploratory analysis of **5,000,000 Nigerian retail banking transactions** from January 2023 to December 2024, worth **₦328.11 billion** in processed value. The project combines the full analysis notebook and an interactive Streamlit dashboard in one repository. The goal is to show where card and transfer fraud concentrates and what a risk team should prioritise.

**Repository:** https://github.com/owoademartin16-lgtm/nigerian-card-fraud-analysis

## Repository layout

| Path | Description |
| --- | --- |
| `Nigerian Banking Card Transactions.ipynb` | Full exploratory analysis, from data loading and quality checks to fraud-rate charts by time, state, channel, merchant category, transaction type and amount band. |
| `app.py` | Streamlit dashboard entry point, sidebar filters and page layout. |
| `theme.py` | Main light visual system, CSS, KPI cards and Plotly styling. |
| `theme_dark.py` | Dark palette and CSS copy used by the optional dark dashboard. |
| `run_dark.sh` | Runs the same dashboard with the dark theme. |
| `charts.py` | Reusable Plotly figures built from the dashboard aggregates. |
| `data/fraud_cube.parquet` | 743,785-row pre-aggregated cube that powers the filtered dashboard views. |
| `data/day_summary.csv` | Full-period day-of-week context. |
| `data/category_summary.csv` | Full-period merchant-category context. |
| `data/headline.json` | Headline figures used to validate the dashboard against the notebook. |
| `prepare_dashboard_data.py` | Rebuilds the dashboard aggregates from the local Arrow cache of the cleaned dataset. |
| `requirements.txt` | Dashboard dependencies. |
| `runtime.txt` | Python version for Streamlit Community Cloud. |

## Dashboard

The dashboard reads `data/fraud_cube.parquet`, a compact aggregate built from the same cleaned dataset used in the notebook. No cleaning or imputation is repeated at runtime.

### Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The main app uses the light theme. The original dark theme is kept as a runnable copy:

```bash
./run_dark.sh
```

`run_dark.sh` sets `FRAUD_THEME=dark`, loads `theme_dark.py` and passes the dark Streamlit palette. The app, charts, filters and data are otherwise the same.

### Filters

The sidebar filters the month range, time window, channel, state, transaction type and amount band. The KPI cards and most charts follow the filters. The day-of-week and merchant-category views are full-period context.

### What the dashboard shows

- Animated KPI cards for transactions, fraud cases, fraud rate, fraud value and average fraud amount.
- Hourly and overnight concentration views.
- Monthly fraud-rate trend.
- Channel fraud-rate versus fraud-value bubble chart.
- A mobile and POS loss-mix card.
- State loss and state-rate views.
- Full-period day-of-week and merchant-category context.

### Deploy to Streamlit Community Cloud

1. Sign in at https://share.streamlit.io.
2. Create a new app from `owoademartin16-lgtm/nigerian-card-fraud-analysis`.
3. Select branch `main` and entry point `app.py`.
4. Deploy. The repository already includes `requirements.txt`, `runtime.txt` and `.streamlit/config.toml`.

## Notebook

The notebook covers:

- Loading the public Hugging Face dataset.
- Schema checks, null checks, duplicate checks and dtype downcasting.
- Time features for hour, day of week and month.
- Fraud exposure, fraud counts, fraud rates and fraud value.
- Fraud analysis by hour, day, month, state, LGA, channel, merchant category, transaction type and amount band.
- Matplotlib charts for the write-up.

To rerun the notebook, install the dashboard requirements first, then the notebook extras:

```bash
pip install -r requirements.txt
pip install jupyter datasets matplotlib scikit-learn
jupyter lab "Nigerian Banking Card Transactions.ipynb"
```

## Headline figures

| Measure | Value |
| --- | --- |
| Transactions analysed | 5,000,000 |
| Fraud cases | 40,000 (0.80%) |
| Fraud value | ₦2,660,513,024 (0.81%) |
| Fraud between 22:00 and 06:59 | 39,634 cases (99.1%) |
| Mobile + POS share of losses | ₦1.73bn (65.1%) |
| Highest fraud rate | Bayelsa, 1.134% |
| Highest fraud losses | Kaduna, ₦87.7M |

## What the analysis found

- **Fraud is flat everywhere except the clock.** Weekday rates sit between 0.78% and 0.81%, monthly rates between 0.765% and 0.847%, amount bands between 0.767% and 0.817%, and merchant categories between 0.799% and 0.835%.
- **The overnight window carries almost everything.** Nine hours, 22:00 through 06:59, hold 39,634 of the 40,000 fraud cases. That is 10.3% of transaction volume and 99.1% of the fraud.
- **Rate and value rank things differently.** Agent (0.847%) and branch (0.844%) have the highest rates, while mobile (₦939.4M) and POS (₦793.8M) carry the most money.
- **Bayelsa has the highest rate, Kaduna the biggest loss.** Bayelsa records 1.134% on 6,347 transactions; Kaduna loses ₦87.7M across 159,387.

## Data pipeline

1. The notebook loads the public dataset and applies the light cleaning steps described above.
2. `prepare_dashboard_data.py` reads the local Arrow cache of that cleaned data and writes the dashboard aggregates.
3. The Streamlit app reads only the aggregates, which keeps filter changes fast and avoids repeating the 5-million-row preparation at runtime.

To rebuild the aggregates from a different cache location:

```bash
python prepare_dashboard_data.py --arrow-dir /path/to/arrow/cache --out data
```

The script's default cache path is macOS-specific. Pass `--arrow-dir` when running it on another machine.

## Notebook charts

1. Fraud rate by hour of day
2. Fraud rate by day of week
3. Monthly fraud rate, January 2023 to December 2024
4. Fraud losses by channel
5. Top 10 states by fraud rate
6. Top 10 states by fraud losses

## Case study

Rendered write-up: https://owoademartinportfolio-seven.vercel.app/nigerian-card-fraud-analysis.html

## Data

Public dataset: https://huggingface.co/datasets/electricsheepafrica/nigerian-banking-retail-transactions

## Note

All figures describe this public dataset. They should not be read as a measured estimate of national fraud incidence.
