# delta-one-mispricing-engine

A Python-based quantitative trading project that models, detects, and trades dividend mispricing in equity futures using implied dividend yields derived from spot and futures prices.

---

## Project Overview

This project builds a **Delta-One mispricing detection and trading engine** leveraging the theoretical relationship between spot, futures, risk-free rates, and dividend yields:

- Simulates spot price paths with Geometric Brownian Motion (GBM)
- Generates mock futures prices based on spot prices and dividend yield forecasts
- Calculates **implied dividend yield** from futures prices and compares it to noisy forecast dividend yields
- Detects mispricing opportunities when implied dividends deviate significantly from forecasts
- Generates trading signals (long/short futures) based on mispricing thresholds
- Simulates trade P&L assuming fixed holding periods
- Provides performance analytics and visualization

---

## Key Concepts

- **Implied Dividend Yield (q):**  
  \( q = r - \frac{1}{T} \ln\left(\frac{F}{S}\right) \)  
  Where:  
  - \( F \) = futures price  
  - \( S \) = spot price  
  - \( r \) = risk-free rate  
  - \( T \) = time to maturity (in years)

- **Mispricing:** Difference between implied dividend yield and forecast dividend yield.

---

## Data Generation

- 60 trading days simulated (~3 months)
- Initial spot price: 100
- Annual drift: 5%
- Annual volatility: 20%
- Risk-free rate: 2%
- True dividend yield: 1.5% (with forecast noise std dev ~0.3%)
- Futures maturities: 20 days (1 month) and 60 days (3 months)

---

## Usage

1. Generate mock market data:  
   ```bash
   python generate_mock_data.py
   ```

2. Detect mispricing and plot results:  
   ```bash
   python detect_mispricing.py
   ```

3. Generate trade signals and simulate PnL:  
   ```bash
   python trade_simulation.py
   ```

---

## Performance Summary (20-day Futures, Entry Threshold 0.5%, Hold 5 days)

| Metric               | Value      |
|----------------------|------------|
| Total PnL            | 220.8906   |
| Average PnL per trade | 14.7260    |
| Number of trades     | 15         |
| Hit ratio            | 46.67%     |

*Interpretation:*  
Over 60 days, the strategy executed 15 trades, with an average profit of ~14.73 units per trade, achieving a total net profit of ~220.89 units. The hit ratio indicates that approximately 47% of trades were profitable, highlighting moderate accuracy balanced by substantial PnL per winning trade.

---

## Visualizations

- **Implied vs Forecast Dividend Yield:** Shows the daily comparison of implied and forecast dividend yields.
- **Dividend Mispricing:** Displays deviations indicating trading opportunities.
- **PnL over Time:** Illustrates realized profits and losses on simulated trades.

*(Plots generated using matplotlib, see Jupyter notebooks or scripts for details)*

---

## Next Steps

- Extend to multiple maturities and multiple underlying assets
- Incorporate transaction costs and slippage modeling
- Use real market data for live backtesting
- Optimize entry thresholds and holding periods with machine learning techniques
- Develop automated trading system with live data integration

---

## Requirements

- Python 3.8+
- numpy
- pandas
- matplotlib

Install dependencies:  
```bash
pip install numpy pandas matplotlib
```

---

## File Structure

```
/data
    mock_market_data.csv          # Generated mock market data
    trade_sim_results_20d.csv     # Simulated trade results
/generate_mock_data.py           # Script to generate mock data
/detect_mispricing.py            # Implied dividend and mispricing detection
/trade_simulation.py             # Trade signal generation and PnL simulation
/README.md                      # This file
```

---

## Author

Mohd Sohail Waquee  
Email: sohail.ayas123@gmail.com  
GitHub: [sohailw94](https://github.com/sohailw94/repositories)

---

Feel free to reach out for collaboration or questions!

---

*This project was developed as part of a Delta-One trading strategy exploration, focusing on dividend mispricing arbitrage.*
