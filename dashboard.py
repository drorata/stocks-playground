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


start_date = st.text_input(
    "Start date (YYYY-MM-DD):",
    (datetime.now() - relativedelta(years=2)).strftime("%Y-%m-%d"),
)
end_date = st.text_input("End date (YYYY-MM-DD):", datetime.now().strftime("%Y-%m-%d"))
tickers = st.text_input("Ticker(s), separated by commas:", "AAPL, AMZN, GOOGL")
tickers = [x.strip() for x in tickers.split(",")]

tickers_data = load_data(start_date, end_date, tickers)

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
roll_avg = st.radio("Averaging", ["Day", "7 days", "30 days"])
roll_avg_map = {"Day": "1d", "7 days": "7d", "30 days": "30d"}
df = pd.DataFrame(res).transpose().rolling(roll_avg_map[roll_avg]).mean().reset_index()

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
