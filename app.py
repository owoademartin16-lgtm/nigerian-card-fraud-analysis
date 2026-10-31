"""Streamlit dashboard for the Nigerian card-fraud case study.

The app reads compact aggregates built from the same cleaned dataset used in
`Nigerian Banking Card Transactions.ipynb`. It does not re-clean or impute rows.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

import charts as ch
from theme import (
    AMBER,
    AMOUNT_ORDER,
    BLUE,
    CHANNEL_COLORS,
    CHANNEL_ORDER,
    CREAM,
    CSS,
    DAYTIME,
    DIM,
    FAINT,
    GOLD,
    OVERNIGHT,
    ROSE,
    TEAL,
    chart_card,
    fmt_ngn,
    kpi_card,
    md,
    rec_card,
    section,
)

st.set_page_config(
    page_title="Fraud Intelligence · Nigerian Banking",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"


@st.cache_data(show_spinner=False)
def load_data():
    cube = pd.read_parquet(DATA / "fraud_cube.parquet")
    headline = json.loads((DATA / "headline.json").read_text(encoding="utf-8"))
    day = pd.read_csv(DATA / "day_summary.csv")
    cat = pd.read_csv(DATA / "category_summary.csv", dtype={"merchant_category_code": "string"})

    months = sorted(str(x) for x in cube["month"].cat.categories)
    all_states = [str(x) for x in cube["location_state"].cat.categories]
    channel_categories = [str(x) for x in cube["channel"].cat.categories]
    available_channels = [c for c in CHANNEL_ORDER if c in channel_categories]
    available_channels.extend(c for c in channel_categories if c not in available_channels)
    month_labels = {m: pd.to_datetime(m + "-01").strftime("%b %y") for m in months}

    return cube, headline, day, cat, months, all_states, available_channels, month_labels


st.markdown(CSS, unsafe_allow_html=True)

try:
    cube, headline, day, cat, months, all_states, available_channels, MONTH_LABELS = load_data()
except FileNotFoundError:
    st.error("Dashboard data is missing. Run `python prepare_dashboard_data.py` first.")
    st.stop()


# ---------------------------------------------------------------- sidebar
with st.sidebar:
    md("""
    <div class="side-brand">
      <div class="brand-mark">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFB627"
             stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 3l7 3v6c0 4.4-3 7.3-7 9-4-1.7-7-4.6-7-9V6l7-3z"/>
          <path d="M9 12l2 2 4-4"/>
        </svg>
      </div>
      <div>
        <div class="brand-name">FRAUD / RISK</div>
        <div class="brand-sub">Nigerian retail banking</div>
      </div>
    </div>
    """)

    md('<div class="side-section">01 · window</div>')
    start_month = st.selectbox(
        "From",
        months,
        index=0,
        format_func=lambda m: MONTH_LABELS[m],
        key="start_month",
    )
    end_month = st.selectbox(
        "To",
        months,
        index=len(months) - 1,
        format_func=lambda m: MONTH_LABELS[m],
        key="end_month",
    )
    start_month, end_month = sorted([start_month, end_month])
    month_list = [m for m in months if start_month <= m <= end_month]

    time_window = st.radio(
        "Time window",
        ["All day", "Overnight", "Daytime", "Custom"],
        index=0,
        key="time_window",
        help="Overnight is 22:00 to 06:59. Daytime is 07:00 to 21:59.",
    )
    if time_window == "Custom":
        custom_hours = st.slider("Hour range", 0, 23, (0, 23), key="custom_hours")
        hours = list(range(custom_hours[0], custom_hours[1] + 1))
    elif time_window == "Overnight":
        hours = OVERNIGHT
    elif time_window == "Daytime":
        hours = DAYTIME
    else:
        hours = list(range(24))
    st.caption("Overnight 22:00–06:59 · Daytime 07:00–21:59")

    md('<div class="side-section">02 · segment</div>')
    channels = st.multiselect(
        "Channel",
        available_channels,
        default=available_channels,
        key="channels",
    )
    states = st.multiselect(
        "State",
        all_states,
        default=[],
        placeholder="All 37 states",
        key="states",
    )
    types = st.multiselect(
        "Transaction type",
        ["credit", "debit"],
        default=["credit", "debit"],
        key="types",
    )
    st.caption("Leave state empty to include every state.")

    md('<div class="side-section">03 · size</div>')
    amounts = st.multiselect(
        "Amount band",
        AMOUNT_ORDER,
        default=AMOUNT_ORDER,
        key="amounts",
    )

    def reset_filters() -> None:
        st.session_state["start_month"] = months[0]
        st.session_state["end_month"] = months[-1]
        st.session_state["time_window"] = "All day"
        st.session_state["custom_hours"] = (0, 23)
        st.session_state["channels"] = list(available_channels)
        st.session_state["states"] = []
        st.session_state["types"] = ["credit", "debit"]
        st.session_state["amounts"] = list(AMOUNT_ORDER)

    st.button("Reset filters", on_click=reset_filters, width="stretch")

    md(f"""
    <div class="side-note">
      <div class="note-title">DATA NOTE</div>
      <p>5,000,000 transactions, Jan 2023 to Dec 2024. Public dataset. Figures describe this book, not national fraud incidence.</p>
      <p>Cards and interactive charts follow the filters. Day-of-week and merchant-category views are full-period context.</p>
    </div>
    """)


# ---------------------------------------------------------------- hero
md("""
<div class="hero">
  <div class="kicker">case study · nigerian retail banking · 2023–2024</div>
  <h1>Fraud runs on the <span class="accent">night shift</span>.</h1>
  <p class="lede">
    Nigeria's retail banks processed <strong>5,000,000 transactions worth ₦328.11 billion</strong>
    between January 2023 and December 2024. <strong>40,000</strong> were fraudulent, worth
    <strong>₦2.66 billion</strong>. The sharpest pattern is not the calendar, the channel or the
    ticket size. It is the clock: <strong>99.1%</strong> of fraud happens between 22:00 and 06:59.
  </p>
  <div class="hero-tags">
    <span class="hero-tag"><b>5.0M</b> transactions</span>
    <span class="hero-tag"><b>40,000</b> frauds</span>
    <span class="hero-tag"><b>0.80%</b> fraud rate</span>
    <span class="hero-tag"><b>₦2.66B</b> fraud value</span>
    <span class="hero-tag">Jan 2023 – Dec 2024</span>
  </div>
</div>
""")

if not channels or not types or not amounts:
    st.warning("Choose at least one channel, transaction type and amount band to see the dashboard.")
    st.stop()

mask = (
    cube["month"].isin(month_list)
    & cube["hour"].isin(hours)
    & cube["channel"].isin(channels)
    & cube["transaction_type"].isin(types)
    & cube["amount_group"].isin(amounts)
)
if states:
    mask &= cube["location_state"].isin(states)
f = cube.loc[mask]

segment_mask = (
    cube["month"].isin(month_list)
    & cube["channel"].isin(channels)
    & cube["transaction_type"].isin(types)
    & cube["amount_group"].isin(amounts)
)
if states:
    segment_mask &= cube["location_state"].isin(states)
segment = cube.loc[segment_mask]

if f.empty or int(f["total_transactions"].sum()) == 0:
    st.warning("No transactions match this combination. Widen the month, time or segment filters.")
    st.stop()

total = int(f["total_transactions"].sum())
fraud = int(f["fraud_transactions"].sum())
total_value = float(f["total_amount"].sum())
fraud_value = float(f["fraud_amount"].sum())
rate = fraud / total * 100 if total else 0.0
value_share = fraud_value / total_value * 100 if total_value else 0.0
avg_fraud = fraud_value / fraud if fraud else 0.0
avg_legit = (total_value - fraud_value) / (total - fraud) if total > fraud else 0.0

night_segment = segment[segment["hour"].isin(OVERNIGHT)]
day_segment = segment[~segment["hour"].isin(OVERNIGHT)]
night_fraud = int(night_segment["fraud_transactions"].sum())
day_fraud = int(day_segment["fraud_transactions"].sum())
night_total = night_fraud + day_fraud
night_share = night_fraud / night_total * 100 if night_total else 0.0
night_volume_share = (
    night_segment["total_transactions"].sum() / segment["total_transactions"].sum() * 100
    if segment["total_transactions"].sum()
    else 0.0
)

is_filtered = not (
    start_month == months[0]
    and end_month == months[-1]
    and time_window == "All day"
    and set(channels) == set(available_channels)
    and not states
    and set(types) == {"credit", "debit"}
    and set(amounts) == set(AMOUNT_ORDER)
)
book_rate = float(headline["fraud_rate_pct"])

# ---------------------------------------------------------------- overview
pill_class = "view-pill" if is_filtered else "view-pill quiet"
pill_text = "Filtered view" if is_filtered else "Full book"
md(f"""
<div class="view-bar">
  <span class="{pill_class}">{pill_text}</span>
  <span><b>{total:,}</b> transactions</span><span class="view-sep">·</span>
  <span><b>{fraud:,}</b> frauds</span><span class="view-sep">·</span>
  <span><b>{rate:.2f}%</b> fraud rate</span>
</div>
""")

col1, col2, col3, col4, col5 = st.columns(5, gap="small")
with col1:
    md(kpi_card(
        "Transactions",
        f"{total:,}",
        "full book" if not is_filtered else f"of {headline['total_transactions']:,} in the book",
        AMBER,
    ))
with col2:
    md(kpi_card(
        "Fraud cases",
        f"{fraud:,}",
        f"{rate:.2f}% of selected transactions",
        ROSE,
    ))
with col3:
    md(kpi_card(
        "Fraud rate",
        f"{rate:.2f}%",
        f"book average {book_rate:.2f}%",
        GOLD,
    ))
with col4:
    md(kpi_card(
        "Fraud value",
        fmt_ngn(fraud_value),
        f"{value_share:.2f}% of selected value",
        TEAL,
    ))
with col5:
    md(kpi_card(
        "Avg fraud ticket",
        f"₦{avg_fraud:,.0f}",
        f"legit ticket ₦{avg_legit:,.0f}",
        BLUE,
    ))

# ---------------------------------------------------------------- the clock
section(
    "01 · the clock",
    "Fraud runs on the night shift.",
    "Nine hours, 22:00 through 06:59, hold <strong>39,634 of the 40,000 fraud cases</strong>. "
    "That is 10.3% of transaction volume and 99.1% of the fraud. Daylight is almost clean.",
)

left, right = st.columns([3, 2], gap="medium")
with left:
    chart_card(
        "Fraud rate by hour",
        "Rose bars are 22:00 to 06:59, where the rate jumps.",
        ch.hour_figure(f),
        "hour",
    )
with right:
    with st.container(border=True, key="night_card"):
        md("""
        <div class="chart-title">Night concentration</div>
        <div class="chart-sub">All hours in this slice, independent of the hour filter.</div>
        """)
        st.plotly_chart(
            ch.overnight_donut(night_share),
            width="stretch",
            theme=None,
            config={"displayModeBar": False, "responsive": True},
            key="night",
        )
        md(f"""
        <div class="insight-text" style="margin-top:-4px">
          <strong>{night_share:.1f}%</strong> of fraud falls in the nine-hour window,
          on <strong>{night_volume_share:.1f}%</strong> of transaction volume.
        </div>
        <div class="mini-list">
          <div class="mini-row"><span class="left"><span class="mini-dot" style="--dot:{ROSE}"></span>Night frauds</span><b>{night_fraud:,}</b></div>
          <div class="mini-row"><span class="left"><span class="mini-dot" style="--dot:{GOLD}"></span>Day frauds</span><b>{day_fraud:,}</b></div>
          <div class="mini-row"><span class="left"><span class="mini-dot" style="--dot:{BLUE}"></span>Night volume</span><b>{night_volume_share:.1f}%</b></div>
        </div>
        """)

chart_card(
    "Monthly fraud rate",
    "Selected slice. In the full book every month sits between 0.765% and 0.847%.",
    ch.month_figure(f, month_list),
    "month",
)

# ---------------------------------------------------------------- the money
section(
    "02 · the money",
    "Rate and value rank channels differently.",
    "Agent (0.847%) and branch (0.844%) have the highest rates. Mobile (₦939.4M) and POS "
    "(₦793.8M) carry <strong>65.1% of the money</strong>. Rate and value are different questions.",
)

ch_data = ch.aggregate(f, "channel")
ch_data["channel"] = ch_data["channel"].astype(str)
ch_data = ch_data.sort_values("fraud_amount", ascending=False)
mobile_pos = ch_data[ch_data["channel"].isin(["mobile", "pos"])]["fraud_amount"].sum()
mobile_pos_share = mobile_pos / fraud_value * 100 if fraud_value else 0.0
top_channels = ch_data.head(4)

left, right = st.columns([3, 2], gap="medium")
with left:
    chart_card(
        "Fraud rate vs fraud value",
        "Bubble size = fraud cases. Further right means a higher rate.",
        ch.channel_figure(f),
        "channel",
    )
with right:
    rows = "".join(
        f'<div class="mini-row"><span class="left">'
        f'<span class="mini-dot" style="--dot:{CHANNEL_COLORS.get(str(row.channel), AMBER)}"></span>'
        f'{row.channel}</span>'
        f'<span><b>{fmt_ngn(row.fraud_amount)}</b> '
        f'<span style="color:{FAINT}">· {row.rate:.2f}%</span></span></div>'
        for row in top_channels.itertuples()
    )
    with st.container(border=True, key="channel_insight_card"):
        md(f"""
        <div class="channel-insight-body">
          <div class="insight-kicker">where the money goes</div>
          <div class="insight-value">{mobile_pos_share:.1f}%</div>
          <div class="insight-text">
            of fraud value in this slice runs through <strong>mobile and POS</strong>.
          </div>
          <div class="insight-bar"><span style="width:{max(0, min(100, mobile_pos_share)):.1f}%"></span></div>
          <div class="mini-list">{rows}</div>
        </div>
        """)

# ---------------------------------------------------------------- the map
section(
    "03 · the map",
    "Small states lead the rate. Volume leads the loss.",
    "Bayelsa leads the rate at <strong>1.134%</strong> on 6,347 transactions. Kaduna carries "
    "the biggest loss among the high-rate states at <strong>₦87.7M</strong> on 159,387. "
    "Small bases move the rate; volume moves the loss.",
)

left, right = st.columns(2, gap="medium")
with left:
    chart_card(
        "Highest fraud rate by state",
        "Top 10 in the current slice. Read the count with the rate.",
        ch.state_rate_figure(f),
        "state_rate",
    )
with right:
    chart_card(
        "Fraud losses in the highest-rate states",
        "Top 10 by rate, ranked by fraud value. Kaduna carries the most among them.",
        ch.state_value_figure(f),
        "state_value",
    )

# ---------------------------------------------------------------- flat signals
section(
    "04 · the flat signals",
    "Everything else is noise.",
    "Weekday rates sit between 0.779% and 0.809%, amount bands between 0.767% and 0.817%, "
    "and merchant categories between 0.799% and 0.835%. None of them separates fraud the way "
    "the clock does.",
)

c1, c2, c3 = st.columns(3, gap="medium")
with c1:
    chart_card(
        "Amount band",
        "Full book: 0.767% to 0.817%. The bars barely move.",
        ch.amount_figure(f),
        "amount",
    )
with c2:
    chart_card(
        "Transaction type",
        "Credit vs debit. The full-book gap is 0.008 points.",
        ch.type_figure(f),
        "type",
    )
with c3:
    chart_card(
        "Day of week",
        'Full period. Every day sits between 0.779% and 0.809%. <span class="mini-pill">full period</span>',
        ch.day_figure(day),
        "day",
    )

with st.expander("Merchant category detail · full period"):
    md("""
    <div class="chart-sub" style="margin-bottom:10px">
      Top 10 merchant category codes by fraud rate. The full spread is 0.799% to 0.835%.
      Codes are raw MCC values from the dataset.
    </div>
    """)
    cat_view = cat.head(10).copy()
    cat_view["merchant_category_code"] = (
        cat_view["merchant_category_code"].fillna("No MCC").replace("", "No MCC")
    )
    cat_view["Transactions"] = cat_view["total_transactions"].map(lambda v: f"{v:,.0f}")
    cat_view["Frauds"] = cat_view["fraud_transactions"].map(lambda v: f"{v:,.0f}")
    cat_view["Fraud rate"] = cat_view["fraud_rate_pct"].map(lambda v: f"{v:.3f}%")
    cat_view = cat_view[["merchant_category_code", "Transactions", "Frauds", "Fraud rate"]]
    cat_view.columns = ["MCC", "Transactions", "Frauds", "Fraud rate"]
    st.dataframe(cat_view, hide_index=True, width="stretch")

# ---------------------------------------------------------------- playbook
section(
    "05 · the playbook",
    "Three moves for a risk team.",
    "The analysis points to a short list: put the night shift first, follow the money, and stop "
    "overfitting the calendar.",
)

r1, r2, r3 = st.columns(3, gap="medium")
with r1:
    md(rec_card(
        "01",
        "Put the night shift first",
        "22:00 to 06:59 holds 99.1% of fraud on 10.3% of volume. Move velocity, device and "
        "beneficiary checks into that window.",
        AMBER,
    ))
with r2:
    md(rec_card(
        "02",
        "Follow the money",
        "Mobile and POS carry 65.1% of losses. Agent and branch have the highest rates but small "
        "totals. Staff the queues that move the most value.",
        ROSE,
    ))
with r3:
    md(rec_card(
        "03",
        "Do not overfit the calendar",
        "Day, month, amount band and merchant category are flat. Rules that only reshuffle those "
        "dimensions add noise, not signal.",
        TEAL,
    ))

md("""
<div class="footer">
  <div class="fine">
    Source: 5,000,000 Nigerian retail banking transactions, January 2023 to December 2024.
    Figures are reproduced from the analysis notebook and describe this public dataset. They are
    not a measured estimate of national fraud incidence.
  </div>
  <div>
    <a href="https://github.com/owoademartin16-lgtm/nigerian-card-fraud-analysis" target="_blank" rel="noopener">GitHub</a>
    ·
    <a href="https://github.com/owoademartin16-lgtm/nigerian-card-fraud-analysis/blob/main/Nigerian%20Banking%20Card%20Transactions.ipynb" target="_blank" rel="noopener">Notebook</a>
    ·
    <a href="https://huggingface.co/datasets/electricsheepafrica/nigerian-banking-retail-transactions" target="_blank" rel="noopener">Dataset</a>
  </div>
</div>
""")
