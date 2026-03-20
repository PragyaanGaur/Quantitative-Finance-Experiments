import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

START = "2019-01-01"
END   = "2024-12-31"

print("Downloading data...")
gld_raw  = yf.download("GLD",   start=START, end=END, auto_adjust=True, progress=False)
tgldx_raw = yf.download("TGLDX", start=START, end=END, auto_adjust=True, progress=False)

gld   = gld_raw["Close"].squeeze().dropna()
tgldx = tgldx_raw["Close"].squeeze().dropna()
close = pd.DataFrame({"GLD": gld, "TGLDX": tgldx}).dropna()

print(f"Range: {close.index[0].date()}  ->  {close.index[-1].date()}")

r_gld   = close["GLD"].pct_change()
r_tgldx = close["TGLDX"].pct_change()
signal  = (r_gld > 0).astype(float)
r_strat = (signal * r_tgldx).dropna()

def cagr(returns):
    r = returns.dropna()
    return (1 + r).prod() ** (252 / len(r)) - 1

print("\n  Strategy (Flawed) :", f"{cagr(r_strat):.1%} CAGR")
print("  TGLDX Buy & Hold  :", f"{cagr(r_tgldx):.1%} CAGR")

nav_s = (1 + r_strat).cumprod()
nav_t = (1 + r_tgldx.dropna()).cumprod()

plt.figure(figsize=(10, 5))
plt.plot(nav_s.index, nav_s, label="Strategy (Flawed)", color="gold", lw=2)
plt.plot(nav_t.index, nav_t, label="TGLDX Buy & Hold",  color="blue", lw=1.5, alpha=0.8)
plt.legend()
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.1f}x"))
plt.tight_layout()
plt.show()
