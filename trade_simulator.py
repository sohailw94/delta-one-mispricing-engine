import pandas as pd
import matplotlib.pyplot as plt

def generate_trade_signals(df, maturity_days, entry_threshold=0.005):
    """
    Generate long/short futures signals based on dividend mispricing.

    Args:
        df (DataFrame): Contains 'Mispricing_<maturity>d' column.
        maturity_days (int): Futures maturity.
        entry_threshold (float): Threshold above which to enter trades.

    Returns:
        DataFrame with 'Signal' column:
            +1 = long future (div underpriced)
            -1 = short future (div overpriced)
             0 = no trade
    """
    mispricing_col = f'Mispricing_{maturity_days}d'
    signal_col = f'Signal_{maturity_days}d'

    df[signal_col] = 0
    df.loc[df[mispricing_col] > entry_threshold, signal_col] = -1  # short future
    df.loc[df[mispricing_col] < -entry_threshold, signal_col] = +1  # long future
    
    return df

def simulate_pnl(df, maturity_days, hold_period=5):
    """
    Simulate PnL for each signal assuming constant holding period.
    
    Args:
        df (DataFrame): Should already have 'Signal' column.
        maturity_days (int): Futures maturity.
        hold_period (int): How many days we hold the position.

    Returns:
        DataFrame with PnL columns added.
    """
    signal_col = f'Signal_{maturity_days}d'
    future_col = f'F_{maturity_days}d'
    pnl_col = f'PnL_{maturity_days}d'
    
    df[pnl_col] = 0.0
    positions = []

    for i in range(len(df) - hold_period):
        signal = df.at[i, signal_col]
        if signal != 0:
            entry_price = df.at[i, future_col]
            exit_price = df.at[i + hold_period, future_col]
            pnl = signal * (exit_price - entry_price)
            df.at[i + hold_period, pnl_col] = pnl  # PnL realized at exit day
            positions.append((i, signal, entry_price, exit_price, pnl))
    
    return df, positions

def summarize_pnl(df, maturity_days):
    pnl_col = f'PnL_{maturity_days}d'
    realized_pnl = df[pnl_col][df[pnl_col] != 0]
    summary = {
        'Total PnL': realized_pnl.sum(),
        'Average PnL per trade': realized_pnl.mean(),
        'Number of trades': len(realized_pnl),
        'Hit ratio': (realized_pnl > 0).sum() / len(realized_pnl) if len(realized_pnl) else 0
    }
    return summary

def plot_cumulative_pnl(df, maturity_days):
    pnl_col = f'PnL_{maturity_days}d'
    df['CumulativePnL'] = df[pnl_col].cumsum()

    plt.figure(figsize=(12,6))
    plt.plot(df['Day'], df['CumulativePnL'], label='Cumulative PnL', color='blue')
    plt.axhline(0, color='black', linestyle='--')
    plt.title(f'Cumulative PnL Curve ({maturity_days}d Futures)')
    plt.xlabel('Day')
    plt.ylabel('PnL')
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_drawdown(df, maturity_days):
    cumulative = df[f'PnL_{maturity_days}d'].cumsum()
    rolling_max = cumulative.cummax()
    drawdown = cumulative - rolling_max

    plt.figure(figsize=(12,6))
    plt.plot(df['Day'], drawdown, label='Drawdown', color='red')
    plt.title(f'Drawdown Curve ({maturity_days}d Futures)')
    plt.xlabel('Day')
    plt.ylabel('Drawdown')
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    # Load data with mispricing
    df = pd.read_csv('/Users/sohailwaquee/Documents/delta one mispricing/data/mock_market_data.csv')
    
    maturity = 20
    df = generate_trade_signals(df, maturity, entry_threshold=0.005)
    df, trades = simulate_pnl(df, maturity, hold_period=5)
    
    summary = summarize_pnl(df, maturity)
    print("PnL Summary:")
    for k, v in summary.items():
        print(f"{k}: {v:.4f}")
    
    df.to_csv(f'/Users/sohailwaquee/Documents/delta one mispricing/data/trade_sim_results_{maturity}d.csv', index=False)
    
    plot_cumulative_pnl(df, maturity)
    plot_drawdown(df, maturity)
