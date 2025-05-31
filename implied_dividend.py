import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calculate_implied_dividend(spot, futures, r, T):
    """
    Calculate implied dividend yield q from spot and futures prices.
    
    Parameters:
        spot (float or np.array): spot price(s)
        futures (float or np.array): futures price(s)
        r (float): risk-free rate (annual)
        T (float): time to maturity (in years)
        
    Returns:
        implied dividend yield q (float or np.array)
    """
    # To avoid division by zero or log of zero
    with np.errstate(divide='ignore', invalid='ignore'):
        q = r - np.log(futures / spot) / T
    return q

def detect_mispricing(df, maturity_days):
    """
    Detect mispricing as difference between implied dividend and forecast dividend.
    
    Args:
        df (pd.DataFrame): DataFrame with columns ['Spot', 'F_<maturity>d', 'RiskFreeRate', 'DivForecast']
        maturity_days (int): Days to futures expiry
        
    Returns:
        df_extended (pd.DataFrame): Original df with new columns:
          - 'ImpliedDiv_<maturity>d'
          - 'Mispricing_<maturity>d' (implied dividend - forecast dividend)
    """
    T = maturity_days / 252  # Convert days to years (trading days)
    implied_div_col = f'ImpliedDiv_{maturity_days}d'
    mispricing_col = f'Mispricing_{maturity_days}d'

    df[implied_div_col] = calculate_implied_dividend(df['Spot'], df[f'F_{maturity_days}d'], df['RiskFreeRate'], T)
    df[mispricing_col] = df[implied_div_col] - df['DivForecast']
    
    return df

def plot_implied_vs_forecast(df, maturity_days):
    implied_div_col = f'ImpliedDiv_{maturity_days}d'
    
    plt.figure(figsize=(12,6))
    plt.plot(df['Day'], df['DivForecast'], label='Forecast Dividend Yield', linestyle='--')
    plt.plot(df['Day'], df[implied_div_col], label='Implied Dividend Yield', alpha=0.8)
    plt.xlabel('Day')
    plt.ylabel('Dividend Yield')
    plt.title(f'Implied vs Forecast Dividend Yield ({maturity_days}d Futures)')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_mispricing(df, maturity_days):
    mispricing_col = f'Mispricing_{maturity_days}d'
    
    plt.figure(figsize=(12,6))
    plt.plot(df['Day'], df[mispricing_col], label='Dividend Mispricing')
    plt.axhline(0, color='red', linestyle='--')
    plt.xlabel('Day')
    plt.ylabel('Implied Dividend - Forecast Dividend')
    plt.title(f'Dividend Mispricing Detection ({maturity_days}d Futures)')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    # Load the mock data generated on Day 1
    df = pd.read_csv('/Users/sohailwaquee/Documents/delta one mispricing/data/mock_market_data.csv')
    
    # Choose a maturity to analyze
    maturity = 20  # 20 days (1 month futures)
    
    # Calculate implied dividend and mispricing
    df = detect_mispricing(df, maturity)
    
    # Plot results
    plot_implied_vs_forecast(df, maturity)
    plot_mispricing(df, maturity)

    df.to_csv('/Users/sohailwaquee/Documents/delta one mispricing/data/mock_market_data.csv', index=False)
    print("Updated DataFrame with implied dividend and mispricing saved.")
