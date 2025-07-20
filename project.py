import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Download data for given tickers
tickers = ['AAPL', 'MSFT', 'GOOGL']
start_date = '2022-01-01'
end_date = '2023-01-01'

for ticker in tickers:
    data = yf.download(ticker, start=start_date, end=end_date)
    data.to_csv(f"{ticker}.csv")
    print(f"Downloaded {ticker}.csv")

# Load and clean Close price data
prices = pd.DataFrame()

for ticker in tickers:
    df = pd.read_csv(f"{ticker}.csv", index_col=0, parse_dates=True)

    # Convert 'Close' column to numeric (handle strings, missing, etc.)
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    prices[ticker] = df['Close']

# Drop rows with any missing data
prices.dropna(inplace=True)

# Daily Returns
daily_returns = prices.pct_change().dropna()

# Volatility (standard deviation)
volatility = daily_returns.std()

# Moving Averages (50-day)
moving_avg = prices.rolling(window=50).mean()

# Plot closing prices
plt.figure(figsize=(12, 6))
for ticker in tickers:
    plt.plot(prices[ticker], label=ticker)
plt.title('Stock Closing Prices')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.show()

# Plot daily returns
plt.figure(figsize=(12, 6))
for ticker in tickers:
    plt.plot(daily_returns[ticker], label=ticker)
plt.title('Daily Returns')
plt.xlabel('Date')
plt.ylabel('Return')
plt.legend()
plt.grid(True)
plt.show()

# Print basic analysis
print("\nVolatility (Standard Deviation of Returns):")
print(volatility)

print("\nLatest 5-Day Moving Averages:")
print(moving_avg.tail())
