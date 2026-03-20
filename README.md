# Quantitative Finance Projects

### 1. Gold Lookahead Bug Strategy
Backtests a gold ETF signal strategy that appears to generate 291% CAGR. However, the result is fictional because the signal uses today's price to place a trade that needed to happen yesterday.

**Stack:** Python, NumPy, yfinance, Matplotlib, Pandas

**Result:**
Strategy (Flawed): 344.5% CAGR
TGLDX Buy & Hold: 8.7% CAGR

### 2. Gold Mean-Reversion Strategy
Applies statistical arbitrage to the GLD/TGLDX price ratio using a 60-day rolling z-score, going long when the ratio is stretched and flat when it normalises. Documents why mean-reversion is the wrong model for miners vs physical gold, because the two diverge for years at a time, not days.

**Stack:** Python, NumPy, yfinance, Matplotlib, Pandas

**Result:**
Strategy (Flawed): 25.0% CAGR
TGLDX Buy & Hold: 8.7% CAGR
