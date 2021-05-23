# Stocks Playground

Check out the deployed app here: [salty-harbor-10851](https://salty-harbor-10851.herokuapp.com/). Feedback is welcomed!

## Motivation

The initial motivation of this dashboard was to compare the value changes of financial assets.
I was not able to find exactly what I wanted, so I wrote it.
Thanks to [Streamlit](https://www.streamlit.io/) this was amazingly easy and fun!
The data source is [Yahoo finance](https://finance.yahoo.com/) and the data is extracted using [`yfinance`](https://github.com/ranaroussi/yfinance).

## Running locally

### Virtual environment

In the project's root run:

```bash
conda conda env create -f environment.yml
```

### Install dependencies

Next, use `pip`:

```bash
pip install -r requirements.txt
```

### Run the application

```bash
streamlit run dashboard.py
```

## Deploy to `heroku`

```bash
git push heroku master
```
