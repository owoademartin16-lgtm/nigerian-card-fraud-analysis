# Fraud Detection & Risk Mitigation in Nigerian Banking Transactions

Exploratory analysis of **5,000,000 Nigerian retail banking transactions** from January 2023 to December 2024, worth **₦328.11 billion** in processed value. The goal: find where card and transfer fraud concentrates, and what a risk team should prioritise.

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

## Charts in the write-up

1. Fraud rate by hour of day
2. Fraud rate by day of week
3. Monthly fraud rate, January 2023 to December 2024
4. Fraud losses by channel
5. Top 10 states by fraud rate
6. Top 10 states by fraud losses

## Files

- `Nigerian Banking Card Transactions.ipynb`: the full exploratory analysis, including all outputs and figures.

## Case study

Rendered write-up: https://owoademartinportfolio-seven.vercel.app/nigerian-card-fraud-analysis.html

## Data

Public dataset: https://huggingface.co/datasets/electricsheepafrica/nigerian-banking-retail-transactions

## Note

All figures describe this public dataset. They should not be read as a measured estimate of national fraud incidence.
