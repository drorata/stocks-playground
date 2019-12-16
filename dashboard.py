import streamlit as st
import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr

yf.pdr_override()  # <== that's all it takes :-)

"""
# Tickers Tracking

by Dror Atariah ([LinkedIn](https://www.linkedin.com/in/atariah/) / [GitHub](https://github.com/drorata))
"""

start_date = st.text_input("Start date (YYYY-MM-DD):", "2018-10-10")
end_date = st.text_input("End date (YYYY-MM-DD):", "2019-10-10")
tickers = st.text_input("Ticker(s), separated by commas:", "C001.DE, FB2A.DE")
tickers = [x.strip() for x in tickers.split(",")]

tickers_data = {
    ticker: pdr.get_data_yahoo(ticker, start=start_date, end=end_date)[
        ["Open", "Close"]
    ]
    for ticker in tickers
}

changes = {
    ticker: 100
    * (tickers_data[ticker] - (tickers_data[ticker]).iloc[0])
    / (tickers_data[ticker]).iloc[0]
    for ticker in tickers_data.keys()
}


res = []
for key in tickers_data.keys():
    data = changes[key]["Open"]
    data.name = key
    res.append(data)

df = pd.DataFrame(res).transpose()
df.index.name = "index"
st.line_chart(df)

df
