"""Charts for the fraud dashboard. All figures are built from the notebook aggregates."""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from theme import (
    AMBER,
    AMOUNT_ORDER,
    BLUE,
    CHANNEL_COLORS,
    CREAM,
    DIM,
    FAINT,
    GOLD,
    INK,
    LINE,
    OVERNIGHT,
    ROSE,
    TYPE_COLORS,
    fmt_ngn,
)


def aggregate(df: pd.DataFrame, by: str) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=[by, "total", "fraud", "total_amount", "fraud_amount", "rate"])
    out = (
        df.groupby(by, observed=True)
        .agg(
            total=("total_transactions", "sum"),
            fraud=("fraud_transactions", "sum"),
            total_amount=("total_amount", "sum"),
            fraud_amount=("fraud_amount", "sum"),
        )
        .reset_index()
    )
    out["rate"] = np.where(out["total"] > 0, out["fraud"] / out["total"] * 100, 0.0)
    return out


def style_figure(
    fig: go.Figure,
    height: int = 340,
    x_title: str = "",
    y_title: str = "",
    margin_r: int = 16,
    showlegend: bool = False,
    x_range=None,
    y_range=None,
) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=8, r=margin_r, t=12, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=DIM, size=11),
        hoverlabel=dict(bgcolor="#1B1F16", bordercolor="#3A4030", font=dict(color=CREAM, size=11)),
        showlegend=showlegend,
        hovermode="closest",
        bargap=0.28,
    )
    fig.update_xaxes(
        title_text=x_title,
        gridcolor="#24281F",
        zeroline=False,
        linecolor=LINE,
        tickfont=dict(size=10, color=DIM),
        title_font=dict(size=10, color=FAINT),
        automargin=True,
    )
    fig.update_yaxes(
        title_text=y_title,
        gridcolor="#24281F",
        zeroline=False,
        linecolor=LINE,
        tickfont=dict(size=10, color=DIM),
        title_font=dict(size=10, color=FAINT),
        automargin=True,
    )
    if x_range is not None:
        fig.update_xaxes(range=x_range)
    if y_range is not None:
        fig.update_yaxes(range=y_range)
    return fig


def hour_figure(df: pd.DataFrame) -> go.Figure:
    h = aggregate(df, "hour").set_index("hour").reindex(range(24), fill_value=0).reset_index()
    h["rate"] = np.where(h["total"] > 0, h["fraud"] / h["total"] * 100, 0.0)
    colors = [ROSE if int(x) in OVERNIGHT else "rgba(91,141,239,0.62)" for x in h["hour"]]
    custom = np.stack([h["total"], h["fraud"]], axis=-1)
    fig = go.Figure(
        go.Bar(
            x=h["hour"],
            y=h["rate"],
            marker_color=colors,
            marker_line_width=0,
            customdata=custom,
            hovertemplate=(
                "<b>%{x}:00</b><br>"
                "Fraud rate %{y:.2f}%<br>"
                "%{customdata[0]:,.0f} transactions<br>"
                "%{customdata[1]:,.0f} frauds<extra></extra>"
            ),
        )
    )
    fig.add_vrect(x0=21.5, x1=23.5, fillcolor=ROSE, opacity=0.055, line_width=0)
    fig.add_vrect(x0=-0.5, x1=6.5, fillcolor=ROSE, opacity=0.055, line_width=0)
    fig.update_xaxes(
        tickmode="array",
        tickvals=list(range(24)),
        ticktext=[f"{i:02d}" for i in range(24)],
        title_text="hour of day",
    )
    fig.update_yaxes(title_text="fraud rate (%)")
    ymax = float(h["rate"].max()) if len(h) else 0.0
    return style_figure(fig, 386, y_range=[0, max(0.02, ymax * 1.16)])


def month_figure(df: pd.DataFrame, month_list: list[str]) -> go.Figure:
    m = aggregate(df, "month")
    m["month"] = m["month"].astype(str)
    m = m.set_index("month").reindex(month_list, fill_value=0).reset_index()
    m["rate"] = np.where(m["total"] > 0, m["fraud"] / m["total"] * 100, 0.0)
    labels = pd.to_datetime(m["month"] + "-01").dt.strftime("%b %y").tolist()
    custom = np.stack([m["total"], m["fraud"], m["fraud_amount"] / 1e6], axis=-1)
    fig = go.Figure(
        go.Scatter(
            x=m["month"],
            y=m["rate"],
            mode="lines+markers",
            line=dict(color=AMBER, width=2.2, shape="linear"),
            marker=dict(size=6, color=AMBER, line=dict(color=INK, width=1.4)),
            fill="tozeroy",
            fillcolor="rgba(255,182,39,0.055)",
            customdata=custom,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Fraud rate %{y:.3f}%<br>"
                "%{customdata[0]:,.0f} transactions<br>"
                "%{customdata[1]:,.0f} frauds<br>"
                "₦%{customdata[2]:.1f}M lost<extra></extra>"
            ),
        )
    )
    step = 2 if len(m) > 14 else 1
    fig.update_xaxes(
        tickmode="array",
        tickvals=m["month"].tolist()[::step],
        ticktext=labels[::step],
        tickangle=-45,
        title_text="",
    )
    fig.update_yaxes(title_text="fraud rate (%)")
    ymax = float(m["rate"].max()) if len(m) else 0.0
    y_range = [0, 1.0] if ymax <= 1.2 else [0, ymax * 1.18]
    return style_figure(fig, 326, y_range=y_range)


def channel_figure(df: pd.DataFrame) -> go.Figure:
    ch = aggregate(df, "channel")
    ch["channel"] = ch["channel"].astype(str)
    ch = ch.sort_values("fraud_amount", ascending=False)
    sizes = ch["fraud"].astype(float).clip(lower=1)
    sizeref = 2.0 * float(sizes.max()) / (42 ** 2) if len(sizes) else 1.0
    colors = [CHANNEL_COLORS.get(c, AMBER) for c in ch["channel"]]
    custom = np.stack([ch["fraud"], ch["total"], ch["fraud_amount"] / 1e6], axis=-1)
    fig = go.Figure(
        go.Scatter(
            x=ch["rate"],
            y=ch["fraud_amount"] / 1e6,
            mode="markers+text",
            text=ch["channel"],
            textposition="top center",
            textfont=dict(size=10, color=CREAM, family="Space Mono"),
            cliponaxis=False,
            marker=dict(
                size=sizes,
                sizemode="area",
                sizeref=sizeref,
                sizemin=9,
                color=colors,
                line=dict(color=INK, width=1.5),
                opacity=0.92,
            ),
            customdata=custom,
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Fraud rate %{x:.3f}%<br>"
                "₦%{y:.1f}M fraud value<br>"
                "%{customdata[0]:,.0f} frauds on %{customdata[1]:,.0f} transactions<extra></extra>"
            ),
        )
    )
    fig.update_xaxes(title_text="fraud rate (%)")
    fig.update_yaxes(title_text="fraud value (₦m)")
    ymax = float((ch["fraud_amount"] / 1e6).max()) if len(ch) else 0.0
    return style_figure(fig, 438, margin_r=24, y_range=[0, max(1.0, ymax * 1.22)])


def state_rate_figure(df: pd.DataFrame) -> go.Figure:
    s = aggregate(df, "location_state")
    s["location_state"] = s["location_state"].astype(str)
    s = s.sort_values(["rate", "total"], ascending=[False, False]).head(10)
    s = s.sort_values("rate", ascending=True)
    custom = np.stack([s["total"], s["fraud"], s["fraud_amount"] / 1e6], axis=-1)
    fig = go.Figure(
        go.Bar(
            x=s["rate"],
            y=s["location_state"],
            orientation="h",
            marker_color=ROSE,
            marker_line_width=0,
            text=[f"{v:.2f}%" for v in s["rate"]],
            textposition="outside",
            textfont=dict(size=9, color=CREAM, family="Space Mono"),
            cliponaxis=False,
            customdata=custom,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Fraud rate %{x:.3f}%<br>"
                "%{customdata[1]:,.0f} frauds on %{customdata[0]:,.0f} transactions<br>"
                "₦%{customdata[2]:.1f}M lost<extra></extra>"
            ),
        )
    )
    fig.update_xaxes(title_text="fraud rate (%)")
    fig.update_yaxes(title_text="")
    xmax = float(s["rate"].max()) if len(s) else 1.0
    return style_figure(fig, 392, margin_r=58, x_range=[0, max(0.1, xmax * 1.28)])


def state_value_figure(df: pd.DataFrame) -> go.Figure:
    s = aggregate(df, "location_state")
    s["location_state"] = s["location_state"].astype(str)
    s = s.sort_values(["rate", "total"], ascending=[False, False]).head(10)
    s = s.sort_values("fraud_amount", ascending=True)
    custom = np.stack([s["rate"], s["total"], s["fraud"]], axis=-1)
    fig = go.Figure(
        go.Bar(
            x=s["fraud_amount"] / 1e6,
            y=s["location_state"],
            orientation="h",
            marker_color=GOLD,
            marker_line_width=0,
            text=[fmt_ngn(v) for v in s["fraud_amount"]],
            textposition="outside",
            textfont=dict(size=9, color=CREAM, family="Space Mono"),
            cliponaxis=False,
            customdata=custom,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "₦%{x:.1f}M lost<br>"
                "Fraud rate %{customdata[0]:.3f}%<br>"
                "%{customdata[2]:,.0f} frauds on %{customdata[1]:,.0f} transactions<extra></extra>"
            ),
        )
    )
    fig.update_xaxes(title_text="fraud value (₦m)")
    fig.update_yaxes(title_text="")
    xmax = float((s["fraud_amount"] / 1e6).max()) if len(s) else 1.0
    return style_figure(fig, 392, margin_r=64, x_range=[0, max(1.0, xmax * 1.3)])


def amount_figure(df: pd.DataFrame) -> go.Figure:
    a = aggregate(df, "amount_group")
    a["amount_group"] = a["amount_group"].astype(str)
    a = a.set_index("amount_group").reindex(AMOUNT_ORDER, fill_value=0).reset_index()
    a["rate"] = np.where(a["total"] > 0, a["fraud"] / a["total"] * 100, 0.0)
    custom = np.stack([a["total"], a["fraud"]], axis=-1)
    fig = go.Figure(
        go.Bar(
            x=a["rate"],
            y=a["amount_group"],
            orientation="h",
            marker_color="rgba(78,205,196,0.78)",
            marker_line_width=0,
            text=[f"{v:.2f}%" for v in a["rate"]],
            textposition="outside",
            textfont=dict(size=8.5, color=CREAM, family="Space Mono"),
            cliponaxis=False,
            customdata=custom,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Fraud rate %{x:.3f}%<br>"
                "%{customdata[0]:,.0f} transactions<br>"
                "%{customdata[1]:,.0f} frauds<extra></extra>"
            ),
        )
    )
    fig.update_xaxes(title_text="fraud rate (%)")
    fig.update_yaxes(title_text="", tickfont=dict(size=8.5, color=DIM))
    xmax = float(a["rate"].max()) if len(a) else 0.0
    return style_figure(fig, 292, margin_r=48, x_range=[0, max(1.0, xmax * 1.35)])


def type_figure(df: pd.DataFrame) -> go.Figure:
    t = aggregate(df, "transaction_type")
    t["transaction_type"] = t["transaction_type"].astype(str)
    t = t.set_index("transaction_type").reindex(["credit", "debit"]).dropna().reset_index()
    colors = [TYPE_COLORS.get(x, AMBER) for x in t["transaction_type"]]
    custom = np.stack([t["total"], t["fraud"], t["fraud_amount"] / 1e6], axis=-1)
    fig = go.Figure(
        go.Bar(
            x=t["transaction_type"],
            y=t["rate"],
            marker_color=colors,
            marker_line_width=0,
            text=[f"{v:.3f}%" for v in t["rate"]],
            textposition="outside",
            textfont=dict(size=9, color=CREAM, family="Space Mono"),
            cliponaxis=False,
            customdata=custom,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Fraud rate %{y:.3f}%<br>"
                "%{customdata[0]:,.0f} transactions<br>"
                "%{customdata[1]:,.0f} frauds<br>"
                "₦%{customdata[2]:.1f}M lost<extra></extra>"
            ),
        )
    )
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="fraud rate (%)")
    ymax = float(t["rate"].max()) if len(t) else 0.0
    return style_figure(fig, 292, y_range=[0, max(1.0, ymax * 1.35)])


def day_figure(day: pd.DataFrame) -> go.Figure:
    d = day.copy()
    custom = np.stack([d["total_transactions"], d["fraud_transactions"]], axis=-1)
    fig = go.Figure(
        go.Bar(
            x=d["day_of_week"],
            y=d["fraud_rate_pct"],
            marker_color="rgba(91,141,239,0.72)",
            marker_line_width=0,
            text=[f"{v:.2f}%" for v in d["fraud_rate_pct"]],
            textposition="outside",
            textfont=dict(size=8.5, color=CREAM, family="Space Mono"),
            cliponaxis=False,
            customdata=custom,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Fraud rate %{y:.3f}%<br>"
                "%{customdata[0]:,.0f} transactions<br>"
                "%{customdata[1]:,.0f} frauds<extra></extra>"
            ),
        )
    )
    fig.update_xaxes(tickangle=-18, tickfont=dict(size=8.5, color=DIM), title_text="")
    fig.update_yaxes(title_text="fraud rate (%)")
    return style_figure(fig, 292, y_range=[0, 1.0])


def overnight_donut(night_share: float) -> go.Figure:
    share = max(0.0, min(100.0, night_share))
    fig = go.Figure(
        go.Pie(
            labels=["night", "day"],
            values=[share, max(0.01, 100 - share)],
            hole=0.74,
            sort=False,
            direction="clockwise",
            marker=dict(colors=[ROSE, "#262B1E"], line=dict(color=INK, width=2)),
            textinfo="none",
            hoverinfo="skip",
        )
    )
    fig.add_annotation(
        text=f"<b>{share:.1f}%</b><br><span style='font-size:10px;color:{DIM}'>at night</span>",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(family="Space Grotesk, sans-serif", size=30, color=CREAM),
        align="center",
    )
    fig.update_layout(
        height=244,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )
    return fig
