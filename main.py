import json
import streamlit as st
import openai
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

open.api_key = open('API_KEY','r').read()

def get_stock_price(ticker):
    return str(yf.Ticker(ticker).history(period='1y').iloc[-1].Close)

def calculate_SMA(ticker,window):
    data = yf.Ticker(ticker).history(period='1y').Close
    return str(data.rolling(window=window).mean().iloc[-1])
def calculate_EMA(ticker,window):
    data = yf.Ticker(ticker).history(period='1y').Close
    return str(data.ewm(span=window,adjust=False).mean().iloc[-1])

def calculate_RSI(ticker,window):
    data = yf.Ticker(ticker).history(period="1y").Close
    delta=data.diff()
    up=delta.clip(lower=0)
    down=-1*delta.clip(upper=0)
    ema_up=up.ewm(com=14-1,adjust=False).mean()
    ema_down = down.ewm(com=14 - 1, adjust=False).mean()
    rs = ema_up / ema_down
    return str(100 - (100 / (1 + rs)).iloc[-1])

def calculate_MACD(ticker):
    data = yf.Ticker(ticker).history(period="1y").close()
    short_EMA = data.ewm(span=12,adjust=False).mean()
    long_EMA = data.ewm(span=26, adjust=False).mean()

    MACD = short_EMA - long_EMA
    signal = MACD.ewm(span=9,adjust=False).mean()
    MACD_histogram = MACD-signal

    return f'{MACD[-1]},{signal[-1]},{MACD_histogram[-1]}'
def plot_stock_price(ticker):
    data = yf.Ticker(ticker).history(period="1y")
    plt.figure(figure=(10,5))
    plt.plot(data.index,data.Close)
    plt.title('{ticker} Stock Price Over Last Year')
    plt.xlabel('Date')
    plt.ylabel('Stock Price($)')
    plt.grid(True)
    plt.savefig('stock_price.png')
    plt.close()


functions = [
    {
        'name': 'get_stock_price',
        'description':'gets the latest stock price given the ticker symbol of a company.',
        'parameters': {
            'type':'object',
            'properties':{
                'ticker':{
                    'type':'string',
                    'description':'The stock ticker symbol for a company(for example AAPl for apple)'
                }
            },
            'required':['ticker']
        }

    },
    {
        "name":"calculate_SMA",
        "description":"calculates the simple moving average for a given stock ticker and a window.",
        "parameters":{
            "type":"object",
            "properties":{
                "ticker":{
                    "type":"string",
                    "description":"The stock ticker symbol for a company",
                },
                "window":{
                    "type":"integer",
                    "description":"the timeframe to consider when calculating the SMA"

                }
            },
            "required":['ticker','window'],
        },
    },
    {
        "name":"calculate_EMA",
        "description":"calculates the exponential moving average for a given stock ticker and a window.",
        "parameters":{
            "type":"object",
            "properties":{
                "ticker":{
                    "type":"string",
                    "description":"The stock ticker symbol for a company",
                },
                "window":{
                    "type":"integer",
                    "description":"the timeframe to consider when calculating the EMA"

                }
            },
            "required":['ticker','window'],
        },
    },
    {
        "name":"calculate_RSI",
        "description":"calculates the RSI  for a given stock ticker",
        "parameters":{
            "type":"object",
            "properties":{
                "ticker":{
                    "type":"string",
                    "description":"The stock ticker symbol for a company",
                },

            },
            "required":['ticker'],
        },
    },
    {
        "name": "calculate_MACD",
        "description": "calculates the MACD  for a given stock ticker and a short and long window.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol for a company",
                },

            },
            "required": ['ticker'],
        },
    },
    {
        "name": "plot_stock_price",
        "description": "plot  the stock price  for the last year given the ticker symbol of a company",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol for a company",
                },

            },
            "required": ['ticker'],

        },
    },
]

available_functions ={
    'get_stock_price': get_stock_price,
    'calculate_SMA': calculate_SMA,
    'calculate_EMA': calculate_EMA,
    'calculate_MACD': calculate_MACD,
    'calculate_RSI': calculate_RSI,
    'plot_stock_price': plot_stock_price
}
