import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

SIGNAL  = "GLD"
VEHICLE = "TGLDX"
START   = "2016-01-01"
END     = "2024-12-31"
WINDOW  = 60

print("Downloading data...")
gld_raw   = yf.download(SIGNAL,  start=START, end=END, auto_adjust=True, progress=False)
tgldx_raw = yf.download(VEHICLE, start=START, end=END, auto_adjust=True, progress=False)

gld   = gld_raw["Close"].squeeze().dropna()
tgldx = tgldx_raw["Close"].squeeze().dropna()
close = pd.DataFrame({SIGNAL: gld, VEHICLE: tgldx}).dropna()

print(f"Range: {close.index[0].date()}  ->  {close.index[-1].date()}")

ratio   = close[SIGNAL] / close[VEHICLE]
r_mean  = ratio.rolling(WINDOW).mean()
r_std   = ratio.rolling(WINDOW).std()
z_score = (ratio - r_mean) / r_std

position = pd.Series(0.0, index=close.index)
position[z_score > 2.0]   =  1.0
position[z_score < -2.0]  = -1.0
position[abs(z_score) < 0.5] = 0.0

position = position.replace(0.0, np.nan).ffill().fillna(0.0)

r_tgldx = close[VEHICLE].pct_change()
r_strat = (position.shift(1) * r_tgldx).dropna()

def cagr(returns):
    r = returns.dropna()
    return (1 + r).prod() ** (252 / len(r)) - 1

print("\n Strategy (Flawed) :", f"{cagr(r_strat):.1%} CAGR")
print(f"  {VEHICLE} Buy & Hold      :", f"{cagr(r_tgldx):.1%} CAGR")

nav_s = (1 + r_strat).cumprod()
nav_t = (1 + r_tgldx.dropna()).cumprod()

plt.figure(figsize=(10, 5))
plt.plot(nav_s.index, nav_s, label="Strategy (Flawed)", color="gold", lw=2)
plt.plot(nav_t.index, nav_t, label=f"{VEHICLE} Buy & Hold",  color="blue", lw=1.5, alpha=0.8)
plt.legend()
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.1f}x"))
plt.tight_layout()
plt.show()
