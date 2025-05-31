import numpy as np
import pandas as pd

def generate_gbm_paths(S0, mu, sigma, T, N, seed=42):
    """
    Generate geometric Brownian motion paths.
    Args:
        S0: Initial price
        mu: Drift
        sigma: Volatility
        T: Total time (years)
        N: Number of steps
        seed: Random seed
    Returns:
        np.array of prices of length N+1
    """
    np.random.seed(seed)
    dt = T / N
    prices = [S0]
    for _ in range(N):
        Z = np.random.normal()
        dS = prices[-1] * (mu * dt + sigma * np.sqrt(dt) * Z)
        prices.append(prices[-1] + dS)
    return np.array(prices)

def generate_mock_data():
    """
    Generate mock spot, futures, rates and dividend forecasts.
    Saves to data/mock_market_data.csv
    """
    # Parameters
    S0 = 100.0           # Initial spot price
    mu = 0.05            # Annual drift
    sigma = 0.2          # Annual volatility
    T_days = 60          # 60 trading days (~3 months)
    N = T_days
    r = 0.02             # Annual risk-free rate (constant)
    div_yield_true = 0.015  # True annual dividend yield
    div_noise_std = 0.003    # Dividend forecast noise

    # Generate spot price path (daily steps)
    spot_prices = generate_gbm_paths(S0, mu, sigma, T_days, N)

    # Futures price calculation:
    # Futures = Spot * exp((r - q) * T)
    # We'll do futures prices for 1-month and 3-month maturities
    maturities = [20, 60]  # days
    futures_data = {}
    for days_to_expiry in maturities:
        T = days_to_expiry / 252  # Trading year convention
        # Add noise to dividend forecast
        div_forecast = div_yield_true + np.random.normal(0, div_noise_std, size=N+1)
        futures = spot_prices * np.exp((r - div_forecast) * T)
        futures_data[f'F_{days_to_expiry}d'] = futures

    # Construct DataFrame
    df = pd.DataFrame({
        'Day': np.arange(N+1),
        'Spot': spot_prices,
        'RiskFreeRate': r,
        'DivTrue': div_yield_true
    })

    for key, val in futures_data.items():
        df[key] = val

    # Dividend forecasts time series (with noise)
    df['DivForecast'] = div_yield_true + np.random.normal(0, div_noise_std, size=N+1)

    # Save CSV
    df.to_csv('/Users/sohailwaquee/Documents/delta one mispricing/data/mock_market_data.csv', index=False)
    print('Mock market data saved to data/mock_market_data.csv')

if __name__ == '__main__':
    generate_mock_data()
