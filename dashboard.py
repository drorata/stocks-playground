from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
from dateutil.relativedelta import relativedelta
from pandas_datareader import data as pdr

yf.pdr_override()  # <== that's all it takes :-)

"""
# Tickers Tracking

by Dror Atariah ([LinkedIn](https://www.linkedin.com/in/atariah/) / [GitHub](https://github.com/drorata/stocks-playground))
"""


metrics = ["Open", "Close", "High", "Low"]


@st.cache()
def load_data(start_date, end_date, tickers):
    return {
        ticker: pdr.get_data_yahoo(ticker, start=start_date, end=end_date)[metrics]
        for ticker in tickers
    }


start_date = st.sidebar.text_input(
    "Start date (YYYY-MM-DD):",
    (datetime.now() - relativedelta(years=2)).strftime("%Y-%m-%d"),
)
end_date = st.sidebar.text_input(
    "End date (YYYY-MM-DD):", datetime.now().strftime("%Y-%m-%d")
)
tickers = st.sidebar.text_input("Ticker(s), separated by commas:", "AAPL, AMZN, GOOGL")
if len(tickers) == 0:
    st.error("You must specify at least one ticker")
    raise st.ScriptRunner.StopException
tickers = [x.strip() for x in tickers.split(",")]

raw_tickers_data = load_data(start_date, end_date, tickers)
for ticker in tickers:
    if raw_tickers_data[ticker].empty:
        st.error(f"No data found for the ticker '{ticker}'")
        raise st.ScriptRunner.StopException

roll_types = ["Normal", "Exponential"]
roll_type = st.sidebar.radio("Averaging type", roll_types)

roll_avg_map = {"1 day": "1d", "7 days": "7d", "30 days": "30d", "120 days": "120d"}
roll_avg = st.sidebar.radio("Average rolling window of", list(roll_avg_map.keys()))

if roll_type not in roll_types:
    st.error("Something went wrong with the rolling type. Exiting")
    raise st.ScriptRunner.StopException

if roll_type == "Normal":
    tickers_data = {
        ticker: raw_tickers_data[ticker].rolling(roll_avg_map[roll_avg]).mean()
        for ticker in tickers
    }
if roll_type == "Exponential":
    tickers_data = {
        ticker: raw_tickers_data[ticker]
        .ewm(span=int(roll_avg_map[roll_avg][:-1]))
        .mean()
        for ticker in tickers
    }

changes = {
    ticker: 100
    * (tickers_data[ticker] - (tickers_data[ticker]).iloc[0])
    / (tickers_data[ticker]).iloc[0]
    for ticker in tickers_data.keys()
}


st.write(
    """## Change in percentage for all tickers

(Based on daily OPEN value)
"""
)
res = []
for key in tickers_data.keys():
    data = changes[key]["Open"]
    data.name = key
    res.append(data)
df = pd.DataFrame(res).transpose().reset_index()

st.plotly_chart(
    px.line(df, x="Date", y=tickers).update_layout(
        yaxis_title="% change", legend_title_text="Ticker"
    )
)

if st.checkbox("Show data"):
    st.write(df.set_index("Date"))

st.write("## Ticker behavior")
ticker = st.selectbox("Select ticker", tickers)
df = tickers_data[ticker].reset_index()

fig = go.Figure(
    data=[
        go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
        )
    ]
)
st.plotly_chart(fig)
