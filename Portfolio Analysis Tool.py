# Stage 1: Functions for Calculations
# Install API library (yfinance) and fetch current prices for each ticker
import yfinance as yf
import numpy as np
import pandas as pd

risk_free_rate = 4.6 # US Government bond yield (4.6%) (May 2026)

# Cost basis = the total amount of cash you actually spent.
def calculate_cost_basis(shares, purchase_price):
        cost_basis = shares * purchase_price
        return cost_basis
    
# Current value = how much your position is worth TODAY.
def calculate_current_value(shares, current_price):
    current_value = shares * current_price
    return current_value

# Gain/loss = current value - cost basis
def calculate_gain_loss(current_value, cost_basis):
    gain_loss = current_value - cost_basis
    return gain_loss

# Return % = (gain/loss ÷ cost basis) × 100
def calculate_return_percent(gain_loss, cost_basis):
    if cost_basis == 0:
        return 0
    return_percent = (gain_loss / cost_basis) * 100
    return return_percent


def calculate_volatility(ticker):  # NEW FUNCTION
    stock = yf.Ticker(ticker)
    history = stock.history(period="1y")
    closing_prices = history['Close']
    daily_returns = closing_prices.pct_change() * 100
    volatility = daily_returns.std() * np.sqrt(252)  # Annualize volatility
    return volatility

def calculate_sharpe_ratio(ticker, risk_free_rate=4.6):
    stock = yf.Ticker(ticker)
    history = stock.history(period="1y")
    closing_prices = history['Close']
    daily_returns = closing_prices.pct_change().dropna()
    annual_return = daily_returns.mean() * 252 * 100
    annual_volatility = daily_returns.std() * np.sqrt(252) * 100
    sharpe_ratio = (
        (annual_return - risk_free_rate)
        / annual_volatility
        if annual_volatility > 0 else 0)
    return sharpe_ratio

def analyse_position(position):
    ticker = position["ticker"]
    shares = position["shares"]
    purchase_price = position["purchase_price"]
    current_price = position["current_price"]
    #call functions
    cost_basis = calculate_cost_basis(shares, purchase_price)
    current_value = calculate_current_value(shares, current_price)
    gain_loss = calculate_gain_loss(current_value, cost_basis)
    return_percent = calculate_return_percent(gain_loss, cost_basis)
    volatility = calculate_volatility(ticker)
    sharpe_ratio = calculate_sharpe_ratio(ticker, risk_free_rate)
    
    
    return {"ticker": ticker, "cost_basis": cost_basis, "current_value": current_value, "gain_loss": gain_loss, "return_percent": return_percent, "volatility": volatility, "sharpe_ratio": sharpe_ratio}

while True:
    try:
        number_of_positions = int(input("Enter the number of positions in your portfolio: "))
        
        if number_of_positions <= 0:
            print("Please enter a valid number of positions.")
            continue
        elif number_of_positions > 10:
            print("Please enter a reasonable number of positions (1 to 10).")
            continue
        
        break  # Exit loop if valid
    
    except ValueError:
        print("That's not a number!")

portfolio = []

for i in range(number_of_positions):
    ticker = input(f"Enter ticker for position {i+1}: ").strip().upper()
    shares = int(input(f"Enter number of shares for {ticker}: "))
    currency = input("Enter currency symbol ($ for USD, ₹ for INR): ")
    purchase_price = float(input(f"Enter purchase price for {ticker}: "))
  
    try:
        stock = yf.Ticker(ticker)
        current_price = stock.info['currentPrice']
        print(f"Fetched {ticker}: {currency}{current_price:.2f}")
    except:
        print(f"Error: Could not fetch {ticker}")
        continue # Skip to next iteration if fetch fails
    position = {"ticker": ticker, "shares": shares, "purchase_price": purchase_price, "current_price": current_price}
    portfolio.append(position)

print ()

#TABLE FORMAT
print ()
print("=" * 90)
print("              PORTFOLIO ANALYSIS TABLE   ")
print("=" * 90)
print(f"{'Ticker':<8} {'Invested':<12} {'Current Value':<15} {'Gain/Loss':<15} {'Return %':<10} {'Volatility':<12} {'Weight':<10}")
print("=" * 90)

total_cost_basis = 0
total_current_value = 0
total_gain_loss = 0
total_volatility = 0  # NEW: Initialize total volatility

for position in portfolio:
    analysis = analyse_position(position)
    ticker = analysis['ticker']
    cost_basis = analysis['cost_basis']
    current_value = analysis['current_value']
    gain_loss = analysis['gain_loss']
    return_percent = analysis['return_percent']
    volatility = analysis['volatility']
    sharpe_ratio = analysis['sharpe_ratio']
    total_volatility += volatility  # NEW: Calculate volatility for each stock
    total_cost_basis += cost_basis
    total_current_value += current_value
    total_gain_loss += gain_loss
    total_return = (total_gain_loss / total_cost_basis) * 100 if total_cost_basis > 0 else 0
    avg_volatility = total_volatility / number_of_positions if number_of_positions > 0 else 0

for position in portfolio:
    analysis = analyse_position(position)
    ticker=analysis['ticker']
    cost_basis=analysis['cost_basis']
    current_value=analysis['current_value']
    gain_loss=analysis['gain_loss']
    return_percent=analysis['return_percent']
    volatility=analysis['volatility']
    weight=(current_value/total_current_value)*100 if total_current_value > 0 else 0

    
    
    print(f"{ticker:<12} {currency}{cost_basis:<11.2f} {currency}{current_value:<14.2f} {currency}{gain_loss:<14.2f} {return_percent:<5.2f}%  {volatility:<5.2f}%  {weight:<5.2f}%")  # NEW: Print volatility for each stock
    print("=" * 90)



print("             PORTFOLIO OVERVIEW")
print("=" * 90)
print(f"Total invested:    {currency}{total_cost_basis:>10.2f}")
print(f"Current value:     {currency}{total_current_value:>10.2f}")
print(f"Total gain/loss:   {currency}{total_gain_loss:>10.2f}")
print(f"Portfolio return:  {total_return:>10.2f}%")
print(f"Avg. volatility:   {avg_volatility:>10.2f}%")
print(f"Sharpe Ratio:               {sharpe_ratio:.2f}")  # NEW: Sharpe Ratio
print(f"For every 1% of risk, you earn {sharpe_ratio:.2f}% of excess return")  # NEW: Sharpe Ratio interpretation

# Further analysis

# RETURN ANALYSIS

if total_return < -20:
    print("Portfolio has experienced severe capital erosion.")

elif total_return < 0:
    print("Portfolio is operating at a net loss.")

elif total_return < 8:
    print("Portfolio returns are below long-term equity market averages.")

elif total_return < 15:
    print("Portfolio is delivering healthy market-level returns.")

elif total_return < 25:
    print("Portfolio is outperforming broader market benchmarks.")

else:
    print("Portfolio is generating exceptionally high returns.")


# VOLATILITY ANALYSIS

if avg_volatility < 10:
    print("Portfolio volatility is very low.")

elif avg_volatility < 20:
    print("Portfolio volatility is within conservative ranges.")

elif avg_volatility < 35:
    print("Portfolio exhibits moderate market risk.")

elif avg_volatility < 50:
    print("Portfolio volatility is elevated.")

else:
    print("Portfolio is highly volatile and risk-intensive.")


# SHARPE RATIO ANALYSIS

if sharpe_ratio < 0:
    print("Portfolio is underperforming relative to the risk-free rate.")

elif sharpe_ratio < 1:
    print("Risk-adjusted returns are below institutional standards.")

elif sharpe_ratio < 1.5:
    print("Portfolio demonstrates acceptable risk-adjusted performance.")

elif sharpe_ratio < 2:
    print("Portfolio exhibits strong risk-adjusted returns.")

elif sharpe_ratio < 3:
    print("Portfolio risk efficiency is excellent.")

else:
    print("Portfolio risk-adjusted performance is exceptionally rare.")


# COMBINED ANALYSIS

if total_return > 20 and sharpe_ratio > 1.5:
    print("High returns have been achieved efficiently relative to risk.")

elif total_return > 20 and sharpe_ratio < 1:
    print("Strong returns are being driven by elevated risk exposure.")

elif total_return < 0 and sharpe_ratio < 0:
    print("Portfolio is producing negative returns with poor risk efficiency.")

elif avg_volatility > 40 and sharpe_ratio < 1:
    print("Portfolio risk profile may be excessive relative to returns.")

elif avg_volatility < 15 and sharpe_ratio > 1.5:
    print("Portfolio demonstrates efficient defensive positioning.")

else:
    print("Portfolio metrics remain within standard market ranges.")


    

 