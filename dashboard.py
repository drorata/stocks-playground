from datetime import datetime

import holoviews as hv
import pandas as pd
import streamlit as st
import yfinance as yf
from dateutil.relativedelta import relativedelta
from pandas_datareader import data as pdr

hv.extension("bokeh")


yf.pdr_override()  # <== that's all it takes :-)

"""
# Tickers Tracking

by Dror Atariah ([LinkedIn](https://www.linkedin.com/in/atariah/) / [GitHub](https://github.com/drorata/stocks-playground))
"""


@st.cache()
def load_data(start_date, end_date, tickers):
    return {
        ticker: pdr.get_data_yahoo(ticker, start=start_date, end=end_date)[
            ["Open", "Close", "High", "Low"]
        ]
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

df = pd.DataFrame(res).transpose().reset_index()
plt = hv.render(
    hv.Overlay(
        [
            hv.Curve(df, "Date", ticker, label=ticker).opts(
                width=700, height=300, tools=["hover"]
            )
            for ticker in tickers
        ]
    ).opts(legend_position="top_left"),
)
plt.yaxis.axis_label = "%"
st.bokeh_chart(plt)

if st.checkbox("Show data"):
    st.write(df.set_index("Date"))
