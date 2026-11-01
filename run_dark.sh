#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

FRAUD_THEME=dark exec python3 -m streamlit run app.py \
  --theme.base dark \
  --theme.primaryColor "#FFB627" \
  --theme.backgroundColor "#0B0D09" \
  --theme.secondaryBackgroundColor "#141710" \
  --theme.textColor "#F1EDDD"
