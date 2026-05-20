# portfolio-analysis-tool
A Python-based Portfolio Analysis Tool with live market data integration using yfinance. Features portfolio returns, annualized volatility, Sharpe Ratio, position weighting, diversification analysis, and risk-adjusted performance insights through structured financial analytics.
Features

Live Price Fetching: Real-time stock prices from Yahoo Finance API
Core Metrics: Cost basis, current value, gain/loss, return percentage
Advanced Metrics:

Volatility: Annualized standard deviation of daily returns (how much your stock bounces around)
Sharpe Ratio: Risk-adjusted returns (how much excess return you get per unit of risk)
Position Weights: Percentage allocation of each stock in your portfolio
Diversification Analysis: Comments on portfolio concentration and diversification quality


Error Handling: Validates user input and handles API failures gracefully
Max 10 Positions: Prevents portfolio from becoming too complex to manage

Installation & Setup
Requirements

Python 3.7 or higher
macOS, Linux, or Windows

Step 1: Install Python libraries
bashpip install yfinance numpy pandas
Or, if you have multiple Python versions, use:
bash/usr/local/bin/python3 -m pip install yfinance numpy pandas
Step 2: Clone or download the repository
bashgit clone https://github.com/yourusername/portfolio-analysis-tool.git
cd portfolio-analysis-tool
Step 3: Run the tool
bashpython3 portfolio_analysis.py
Or:
bash/usr/local/bin/python3 portfolio_analysis.py

How to Use:
1. Enter your Portfolio details: ticker, currency symbol, number of shares and buy price.
2. View your portfolio analysis, the tool provides: Portfolio Table, Overview and Advanced Metrics alongside interpretation


Technical Details:
Libraries Used

yfinance: Fetches stock prices and historical data from Yahoo Finance
numpy: Calculates standard deviation and annualization
pandas: Handles time-series data (252 days of prices)

Annualization
Volatility and returns are annualized (converted to yearly figures):

Daily volatility × √252 = Annual volatility (252 trading days/year)
Daily returns × 252 = Annual returns

Risk-Free Rate
Defaults to 4.5% (approximate US Treasury yield). Adjust in code if rates change significantly.

Limitations & Future Improvements
Current Limitations

Maximum 10 positions (prevents analysis paralysis)
Only tracks unrealized gains (positions you still hold)
Sharpe Ratio assumes normal distribution of returns
No tax-loss harvesting or cost basis tracking for tax purposes
Does not consider currency conversion, foregin exchange calculation, currency is asked for format purposes, best used with only one currency.
