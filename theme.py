"""Visual language for the fraud dashboard."""
from __future__ import annotations

import os
import textwrap

import streamlit as st

CREAM = "#17201A"
DIM = "#556057"
FAINT = "#7A847B"
INK = "#FFFFFF"
CARD = "#FFFFFF"
CARD_2 = "#F2F4EE"
LINE = "#DCE2D7"
AMBER = "#B45309"
GOLD = "#CA8A04"
ROSE = "#BE3A3A"
TEAL = "#0F766E"
BLUE = "#2563EB"
GREEN = "#15803D"
PURPLE = "#7C3AED"

OVERNIGHT = [22, 23, 0, 1, 2, 3, 4, 5, 6]
DAYTIME = list(range(7, 22))
AMOUNT_ORDER = [
    "₦0–₦1,000",
    "₦1,001–₦5,000",
    "₦5,001–₦10,000",
    "₦10,001–₦50,000",
    "₦50,001–₦100,000",
    "Above ₦100,000",
]
CHANNEL_ORDER = ["mobile", "pos", "atm", "web", "ussd", "branch", "agent"]
CHANNEL_COLORS = {
    "mobile": AMBER,
    "pos": ROSE,
    "atm": GOLD,
    "web": BLUE,
    "ussd": TEAL,
    "branch": GREEN,
    "agent": PURPLE,
}
TYPE_COLORS = {"credit": BLUE, "debit": AMBER}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&family=Space+Mono:wght@400;700&display=swap');

:root {
  --cream: #17201A;
  --dim: #556057;
  --faint: #7A847B;
  --ink: #FFFFFF;
  --card: #FFFFFF;
  --card2: #F2F4EE;
  --line: #DCE2D7;
  --amber: #B45309;
  --gold: #CA8A04;
  --rose: #BE3A3A;
  --teal: #0F766E;
  --blue: #2563EB;
}

html, body, .stApp {
  background:
    radial-gradient(1100px 560px at 12% -8%, rgba(180,83,9,0.05), transparent 62%),
    radial-gradient(900px 520px at 102% 2%, rgba(190,58,58,0.035), transparent 58%),
    #F6F7F3;
}

.stApp { color: var(--cream); }
header[data-testid="stHeader"],
div[data-testid="stHeader"] { background: transparent !important; }
footer { visibility: hidden; }
#MainMenu, [data-testid="stMainMenu"], [data-testid="stAppDeployButton"] { display: none !important; }
div.block-container {
  max-width: 1440px;
  padding-top: 1.6rem;
  padding-bottom: 3rem;
}

h1, h2, h3, h4 {
  font-family: 'Space Grotesk', sans-serif;
  color: var(--cream);
  letter-spacing: -0.035em;
}

p, li, div { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }

/* ---------------------------------------------------------------- sidebar */
section[data-testid="stSidebar"] {
  background: #FFFFFF;
  border-right: 1px solid var(--line);
}
section[data-testid="stSidebar"] > div { padding-top: 1.2rem; }
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
  color: var(--dim);
  font-size: 12px;
  line-height: 1.55;
}
section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] p {
  font-family: 'Space Mono', monospace;
  font-size: 9.5px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--dim);
}
section[data-testid="stSidebar"] button {
  background: #F4F6F1;
  border: 1px solid var(--line);
  color: var(--cream);
  border-radius: 10px;
  font-family: 'Space Mono', monospace;
  font-size: 10px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
section[data-testid="stSidebar"] button:hover {
  border-color: var(--amber);
  color: var(--amber);
  background: #EEF2EA;
}
span[data-baseweb="tag"] {
  background: #F0F3EC !important;
  color: var(--cream) !important;
  border: 1px solid #D6DDD1 !important;
  border-radius: 6px !important;
  font-size: 10.5px !important;
}
section[data-testid="stSidebar"] .st-key-channels label[data-testid="stWidgetLabel"] p,
section[data-testid="stSidebar"] .st-key-types label[data-testid="stWidgetLabel"] p,
section[data-testid="stSidebar"] .st-key-amounts label[data-testid="stWidgetLabel"] p { font-size: 10.5px; }
.st-key-channels span[data-baseweb="tag"],
.st-key-types span[data-baseweb="tag"],
.st-key-amounts span[data-baseweb="tag"] { font-size: 12px !important; }
.st-key-channels div[data-baseweb="select"],
.st-key-types div[data-baseweb="select"],
.st-key-amounts div[data-baseweb="select"] { font-size: 12px; }
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
  background: #FFFFFF !important;
  border-color: var(--line) !important;
  border-radius: 10px !important;
}
div[data-testid="stSidebar"] hr { border-color: var(--line); }

.side-brand { display: flex; align-items: center; gap: 11px; margin: -48px 0 1.4rem 0; }
.brand-mark {
  width: 38px; height: 38px; border-radius: 11px;
  display: grid; place-items: center;
  background: linear-gradient(145deg, rgba(180,83,9,0.10), rgba(190,58,58,0.06));
  border: 1px solid rgba(180,83,9,0.24);
}
.brand-name {
  font-family: 'Space Mono', monospace; font-size: 11px; font-weight: 700;
  letter-spacing: 0.12em; color: var(--cream);
}
.brand-sub { font-size: 10.5px; color: var(--faint); margin-top: 2px; }

.side-section {
  font-family: 'Space Mono', monospace; font-size: 9px; letter-spacing: 0.16em;
  text-transform: uppercase; color: var(--amber);
  margin: 1.4rem 0 0.55rem 0; padding-top: 0.9rem;
  border-top: 1px solid var(--line);
}
.side-note {
  margin-top: 1.4rem; padding: 12px 13px; border-radius: 12px;
  background: #F7F8F4; border: 1px solid var(--line);
}
.side-note .note-title {
  font-family: 'Space Mono', monospace; font-size: 9px; letter-spacing: 0.14em;
  text-transform: uppercase; color: var(--gold); margin-bottom: 6px;
}
.side-note p { font-size: 10.8px !important; line-height: 1.5 !important; color: var(--faint) !important; margin: 0 0 7px 0; }
.side-note p:last-child { margin-bottom: 0; }

/* ---------------------------------------------------------------- hero */
.hero { padding: 0.5rem 0 0.4rem 0; }
.kicker {
  font-family: 'Space Mono', monospace; font-size: 10px; letter-spacing: 0.17em;
  text-transform: uppercase; color: var(--amber); margin-bottom: 14px;
}
.hero h1 {
  font-size: clamp(42px, 5.3vw, 72px);
  line-height: 0.96;
  margin: 0 0 16px 0;
  max-width: 980px;
}
.hero h1 .accent {
  background: linear-gradient(92deg, var(--amber), var(--rose) 70%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.hero .lede {
  max-width: 860px; color: var(--dim); font-size: 15.5px; line-height: 1.65;
  margin: 0 0 18px 0;
}
.hero .lede strong { color: var(--cream); font-weight: 600; }
.hero-tags { display: flex; flex-wrap: wrap; gap: 7px; margin-bottom: 6px; }
.hero-tag {
  font-family: 'Space Mono', monospace; font-size: 9.5px; letter-spacing: 0.04em;
  color: var(--dim); border: 1px solid var(--line); border-radius: 999px;
  padding: 5px 10px; background: rgba(255,255,255,0.75);
}
.hero-tag b { color: var(--cream); font-weight: 700; }

/* ---------------------------------------------------------------- view bar */
.view-bar {
  display: flex; align-items: center; flex-wrap: wrap; gap: 8px;
  margin: 18px 0 12px 0; padding-top: 12px; border-top: 1px solid var(--line);
  font-family: 'Space Mono', monospace; font-size: 10px; color: var(--faint);
}
.view-pill {
  color: var(--ink); background: var(--amber); border-radius: 999px;
  padding: 4px 9px; font-weight: 700; font-size: 9px; letter-spacing: 0.06em;
  text-transform: uppercase;
}
.view-pill.quiet { background: #E9EDE4; color: var(--dim); }
.view-sep { color: #B7C0B4; }
.view-bar b { color: var(--cream); font-weight: 700; }

/* ---------------------------------------------------------------- KPI cards */
.kpi-card {
  position: relative; overflow: hidden; height: 150px; min-height: 150px;
  display: flex; flex-direction: column;
  padding: 17px 17px 15px 17px;
  border: 1px solid var(--line); border-radius: 16px;
  background: linear-gradient(180deg, #FFFFFF 0%, #FBFCF9 100%);
  box-shadow: 0 8px 24px -22px rgba(23,32,26,0.45);
  transition: transform 220ms ease, border-color 220ms ease, box-shadow 220ms ease;
}
.kpi-card::before {
  content: ""; position: absolute; inset: 0 0 auto 0; height: 3px;
  background: var(--accent); opacity: 0.9;
}
.kpi-card::after {
  content: ""; position: absolute; width: 120px; height: 120px; right: -55px; top: -60px;
  background: radial-gradient(circle, var(--accent), transparent 68%);
  opacity: 0.12; transition: opacity 220ms ease;
}
.kpi-card:hover {
  transform: translateY(-5px) scale(1.008);
  border-color: var(--accent);
  box-shadow: 0 20px 44px -24px rgba(23,32,26,0.36), 0 0 0 1px rgba(255,255,255,0.8) inset;
}
.kpi-card:hover::after { opacity: 0.18; }
.kpi-head { display: flex; align-items: center; gap: 7px; margin-bottom: 8px; }
.kpi-dot {
  width: 6px; height: 6px; border-radius: 50%; background: var(--accent);
}
.kpi-label {
  font-family: 'Space Mono', monospace; font-size: 9px; letter-spacing: 0.13em;
  text-transform: uppercase; color: var(--dim);
}
.kpi-value {
  font-family: 'Space Grotesk', sans-serif; font-size: 27px; font-weight: 600;
  letter-spacing: -0.04em; color: var(--cream); line-height: 1.05;
}
.kpi-sub { margin-top: auto; padding-top: 9px; font-size: 10.5px; color: var(--faint); line-height: 1.35; }
.kpi-sub b { color: var(--dim); font-weight: 600; }

/* ---------------------------------------------------------------- sections */
.section-head { margin: 2.6rem 0 0.75rem 0; }
.section-kicker {
  font-family: 'Space Mono', monospace; font-size: 9.5px; letter-spacing: 0.16em;
  text-transform: uppercase; color: var(--amber); margin-bottom: 8px;
}
.section-head h2 {
  font-size: clamp(25px, 2.6vw, 36px); line-height: 1.05; margin: 0 0 8px 0;
}
.section-head p { max-width: 820px; color: var(--dim); font-size: 13.5px; line-height: 1.6; margin: 0; }
.section-head p strong { color: var(--cream); font-weight: 600; }

/* ---------------------------------------------------------------- chart cards */
div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chart-title),
div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .channel-insight-body) {
  background: linear-gradient(180deg, #FFFFFF 0%, #FBFCF9 100%) !important;
  border: 1px solid var(--line) !important;
  border-radius: 18px !important;
  padding: 6px 8px 2px 8px !important;
  box-shadow: 0 10px 30px -26px rgba(23,32,26,0.38) !important;
}
.st-key-hour_card,
.st-key-night_card {
  min-height: 480px;
}
.st-key-channel_card,
.st-key-channel_insight_card {
  min-height: 500px;
}
.chart-title {
  font-family: 'Space Grotesk', sans-serif; font-size: 15px; font-weight: 600;
  color: var(--cream); letter-spacing: -0.025em; margin: 4px 4px 0 4px;
}
.chart-sub {
  font-size: 11px; color: var(--faint); margin: 3px 4px 2px 4px; line-height: 1.4;
}
.chart-sub .mini-pill {
  display: inline-block; margin-left: 5px; padding: 2px 6px; border-radius: 999px;
  border: 1px solid var(--line); color: var(--dim); font-family: 'Space Mono', monospace;
  font-size: 8px; letter-spacing: 0.08em; text-transform: uppercase;
}

/* ---------------------------------------------------------------- insight cards */
.insight-card {
  height: 100%; min-height: 400px; display: flex; flex-direction: column;
  padding: 20px 20px 18px 20px; border-radius: 18px;
  border: 1px solid var(--line);
  background:
    radial-gradient(300px 180px at 100% 0%, rgba(180,83,9,0.07), transparent 65%),
    linear-gradient(180deg, #FFFFFF 0%, #FBFCF9 100%);
  transition: transform 220ms ease, border-color 220ms ease, box-shadow 220ms ease;
}
.insight-card:hover {
  transform: translateY(-4px);
  border-color: rgba(180,83,9,0.40);
  box-shadow: 0 20px 44px -28px rgba(23,32,26,0.40);
}
.insight-kicker {
  font-family: 'Space Mono', monospace; font-size: 9px; letter-spacing: 0.15em;
  text-transform: uppercase; color: var(--amber); margin-bottom: 10px;
}
.insight-text { color: var(--dim); font-size: 12.5px; line-height: 1.55; margin: 10px 0 14px 0; }
.insight-text strong { color: var(--cream); font-weight: 600; }
.channel-insight-body { min-height: 414px; display: flex; flex-direction: column; }
.st-key-channel_insight_card .channel-insight-body { min-height: 488px; }
.st-key-channel_insight_card .mini-row { font-size: 12.5px; }
.st-key-channel_insight_card .mini-row b { font-size: 11.5px; }

/* money split card */
.money-body { justify-content: space-between; }
.money-topline { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
.money-topline .insight-kicker { margin-bottom: 0; }
.money-scope {
  font-family: 'Space Mono', monospace; font-size: 8px; letter-spacing: 0.12em;
  text-transform: uppercase; color: var(--faint); border: 1px solid var(--line);
  border-radius: 999px; padding: 3px 7px; white-space: nowrap;
}
.money-hero { display: flex; align-items: center; gap: 22px; padding: 12px 0 4px 0; }
.money-gauge {
  width: 184px; height: 184px; flex: 0 0 184px; position: relative;
  border-radius: 50%;
  background: conic-gradient(
    var(--amber) 0 var(--mobile),
    var(--rose) var(--mobile) var(--total),
    #E6EAE2 var(--total) 100%
  );
}
.money-gauge::before {
  content: ""; position: absolute; inset: 15px; border-radius: 50%;
  background: #FFFFFF; border: 1px solid var(--line);
}
.money-gauge-core {
  position: absolute; inset: 15px; z-index: 1; display: flex; flex-direction: column;
  align-items: center; justify-content: center; text-align: center;
}
.money-gauge-value {
  font-family: 'Space Grotesk', sans-serif; font-size: 42px; font-weight: 600;
  letter-spacing: -0.06em; line-height: 0.9; color: var(--cream);
}
.money-gauge-value span { font-size: 19px; letter-spacing: -0.02em; color: var(--dim); margin-left: 1px; }
.money-gauge-label {
  margin-top: 7px; font-family: 'Space Mono', monospace; font-size: 8px;
  letter-spacing: 0.14em; text-transform: uppercase; color: var(--amber);
}
.money-copy { min-width: 0; flex: 1; }
.money-copy p { margin: 0 0 14px 0; color: var(--dim); font-size: 13px; line-height: 1.55; }
.money-copy p strong { color: var(--cream); font-weight: 600; }
.money-total {
  font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 600;
  letter-spacing: -0.04em; line-height: 1; color: var(--cream);
}
.money-total span {
  display: block; margin-top: 5px; font-family: 'Space Mono', monospace;
  font-size: 9px; font-weight: 400; letter-spacing: 0.08em; color: var(--faint);
  text-transform: uppercase;
}
.money-ledger { border-top: 1px solid var(--line); }
.money-row {
  display: grid; grid-template-columns: minmax(0, 1fr) auto auto; align-items: center;
  gap: 14px; min-height: 42px; padding: 9px 0;
  border-bottom: 1px solid rgba(220,226,215,0.90); font-size: 12px; color: var(--dim);
}
.money-row:last-child { border-bottom: 1px solid transparent; }
.money-name { display: flex; align-items: center; gap: 8px; min-width: 0; }
.money-name i {
  width: 7px; height: 7px; border-radius: 50%; background: var(--dot);
  flex: 0 0 auto;
}
.money-amount { font-family: 'Space Mono', monospace; font-size: 11.5px; color: var(--cream); white-space: nowrap; }
.money-share {
  font-family: 'Space Mono', monospace; font-size: 10px; color: var(--faint);
  min-width: 42px; text-align: right; white-space: nowrap;
}
.money-row-rest .money-name { color: var(--faint); }
.money-row-rest .money-amount { color: var(--dim); }
.money-foot {
  display: flex; align-items: center; justify-content: space-between; gap: 10px;
  padding-top: 10px; font-family: 'Space Mono', monospace; font-size: 8.5px;
  letter-spacing: 0.08em; text-transform: uppercase; color: var(--faint);
}
.money-foot b { color: var(--dim); font-weight: 400; }

.mini-list { margin-top: auto; border-top: 1px solid var(--line); padding-top: 2px; }
.st-key-night_card .mini-list { margin-top: 34px; }
.mini-row {
  display: flex; align-items: center; justify-content: space-between; gap: 10px;
  min-height: 27px; box-sizing: border-box;
  padding: 4px 0; border-bottom: 1px solid rgba(220,226,215,0.90);
  font-size: 11.5px; color: var(--dim);
}
.mini-row:last-child { border-bottom: 1px solid transparent; }
.mini-row .left { display: flex; align-items: center; gap: 7px; }
.mini-row > span:last-child { white-space: nowrap; flex-shrink: 0; }
.mini-dot { width: 5px; height: 5px; border-radius: 50%; background: var(--dot); }
.mini-row b {
  color: var(--cream); font-family: 'Space Mono', monospace; font-size: 10.5px;
  font-weight: 400; display: inline-flex; align-items: center; min-height: 18px;
}

/* ---------------------------------------------------------------- recommendation cards */
.rec-card {
  height: 100%; min-height: 196px; padding: 20px 19px 18px 19px;
  border: 1px solid var(--line); border-radius: 17px;
  background: linear-gradient(180deg, #FFFFFF 0%, #FBFCF9 100%);
  box-shadow: 0 8px 24px -24px rgba(23,32,26,0.42);
  transition: transform 220ms ease, border-color 220ms ease, box-shadow 220ms ease;
}
.rec-card:hover {
  transform: translateY(-4px); border-color: var(--accent);
  box-shadow: 0 18px 40px -28px rgba(23,32,26,0.38);
}
.rec-num {
  font-family: 'Space Mono', monospace; font-size: 10px; letter-spacing: 0.12em;
  color: var(--accent); margin-bottom: 14px;
}
.rec-card h3 { font-size: 18px; line-height: 1.2; margin: 0 0 8px 0; }
.rec-card p { margin: 0; color: var(--dim); font-size: 12px; line-height: 1.6; }

/* ---------------------------------------------------------------- footer */
.footer {
  margin-top: 3.2rem; padding-top: 18px; border-top: 1px solid var(--line);
  display: flex; flex-wrap: wrap; justify-content: space-between; gap: 12px;
  color: var(--faint); font-size: 10.5px; line-height: 1.6;
}
.footer a { color: var(--amber); text-decoration: none; border-bottom: 1px solid rgba(180,83,9,0.28); }
.footer a:hover { border-bottom-color: var(--amber); }
.footer .fine { max-width: 760px; }

/* ---------------------------------------------------------------- misc */
div[data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }
div[data-testid="stPlotlyChart"] { background: transparent; }
div[data-testid="stAlert"] { border-radius: 12px; }
::-webkit-scrollbar { width: 9px; height: 9px; }
::-webkit-scrollbar-track { background: #F0F2EC; }
::-webkit-scrollbar-thumb { background: #C8D0C2; border-radius: 999px; }

@media (max-width: 1300px) {
  div[data-testid="stHorizontalBlock"]:has(.kpi-card) {
    flex-wrap: wrap; row-gap: 0.6rem;
  }
  div[data-testid="stHorizontalBlock"]:has(.kpi-card) > div[data-testid="stColumn"],
  div[data-testid="stHorizontalBlock"]:has(.kpi-card) > div[data-testid="column"] {
    flex: 1 1 calc(33.333% - 0.75rem) !important;
    min-width: calc(33.333% - 0.75rem) !important;
    width: auto !important;
  }
}
@media (max-width: 1100px) {
  .hero h1 { font-size: 48px; }
  .hero .lede { font-size: 14px; }
  .kpi-value { font-size: 24px; }
  .insight-card { min-height: 0; }
  .channel-insight-body { min-height: 0; }
  div[data-testid="stHorizontalBlock"]:has(.chart-title),
  div[data-testid="stHorizontalBlock"]:has(.channel-insight-body),
  div[data-testid="stHorizontalBlock"]:has(.rec-card) {
    flex-wrap: wrap; row-gap: 0.75rem;
  }
  div[data-testid="stHorizontalBlock"]:has(.chart-title) > div[data-testid="stColumn"],
  div[data-testid="stHorizontalBlock"]:has(.chart-title) > div[data-testid="column"],
  div[data-testid="stHorizontalBlock"]:has(.channel-insight-body) > div[data-testid="stColumn"],
  div[data-testid="stHorizontalBlock"]:has(.channel-insight-body) > div[data-testid="column"],
  div[data-testid="stHorizontalBlock"]:has(.rec-card) > div[data-testid="stColumn"],
  div[data-testid="stHorizontalBlock"]:has(.rec-card) > div[data-testid="column"] {
    flex: 1 1 100% !important;
    min-width: 100% !important;
    width: 100% !important;
  }
}
@media (max-width: 1000px) {
  div[data-testid="stHorizontalBlock"]:has(.kpi-card) > div[data-testid="stColumn"],
  div[data-testid="stHorizontalBlock"]:has(.kpi-card) > div[data-testid="column"] {
    flex: 0 1 calc(50% - 0.5rem) !important;
    min-width: calc(50% - 0.5rem) !important;
  }
}
@media (max-width: 900px) {
  div.block-container { padding-top: 1rem; }
  .side-brand { margin-top: -56px; }
  .hero h1 { font-size: 40px; }
  .kpi-card { height: 150px; min-height: 150px; }
}
@media (max-width: 700px) {
  .kpi-card { height: 142px; min-height: 142px; }
  .money-hero { flex-direction: column; align-items: flex-start; gap: 16px; }
  .money-gauge { width: 154px; height: 154px; flex-basis: 154px; }
  .money-gauge-value { font-size: 35px; }
}
@media (min-width: 720px) and (max-width: 1100px) {
  div[data-testid="stHorizontalBlock"]:has(.st-key-amount_card) {
    flex-wrap: nowrap !important;
  }
  div[data-testid="stHorizontalBlock"]:has(.st-key-amount_card) > div[data-testid="stColumn"],
  div[data-testid="stHorizontalBlock"]:has(.st-key-amount_card) > div[data-testid="column"] {
    flex: 1 1 calc(50% - 0.5rem) !important;
    min-width: 0 !important;
    width: auto !important;
  }
}
</style>
"""


if os.getenv("FRAUD_THEME", "light").strip().lower() == "dark":
    from theme_dark import (
        AMBER,
        BLUE,
        CARD,
        CARD_2,
        CHANNEL_COLORS,
        CREAM,
        CSS,
        DIM,
        FAINT,
        GOLD,
        GREEN,
        INK,
        LINE,
        PURPLE,
        ROSE,
        TEAL,
        TYPE_COLORS,
    )


def md(html_text: str) -> None:
    st.markdown(textwrap.dedent(html_text).strip(), unsafe_allow_html=True)


def fmt_int(value: float) -> str:
    return f"{value:,.0f}"


def fmt_ngn(value: float) -> str:
    if value >= 1e9:
        return f"₦{value / 1e9:.2f}B"
    if value >= 1e6:
        return f"₦{value / 1e6:.1f}M"
    return f"₦{value:,.0f}"


def fmt_pct(value: float, digits: int = 2) -> str:
    return f"{value:.{digits}f}%"


def kpi_card(label: str, value: str, sub: str, accent: str) -> str:
    return f"""
    <div class="kpi-card" style="--accent:{accent}">
      <div class="kpi-head"><span class="kpi-dot"></span><span class="kpi-label">{label}</span></div>
      <div class="kpi-value">{value}</div>
      <div class="kpi-sub">{sub}</div>
    </div>
    """


def section(kicker: str, title: str, text: str) -> None:
    md(f"""
    <div class="section-head">
      <div class="section-kicker">{kicker}</div>
      <h2>{title}</h2>
      <p>{text}</p>
    </div>
    """)


def chart_card(title: str, subtitle: str, fig, key: str) -> None:
    with st.container(border=True, key=f"{key}_card"):
        md(f'<div class="chart-title">{title}</div><div class="chart-sub">{subtitle}</div>')
        st.plotly_chart(
            fig,
            theme=None,
            config={"displayModeBar": False, "responsive": True},
            key=key,
        )


def rec_card(number: str, title: str, text: str, accent: str) -> str:
    return f"""
    <div class="rec-card" style="--accent:{accent}">
      <div class="rec-num">{number}</div>
      <h3>{title}</h3>
      <p>{text}</p>
    </div>
    """
