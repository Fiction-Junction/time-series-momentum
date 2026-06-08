import pandas as pd

def benchmark_strat(data, date_range):
    """
    Equal-weighted buy-and-hold benchmark strategy.
    No timing, no signals, no volatility weighting.
    """
    prices_df = pd.DataFrame(data).asfreq("B").ffill()
    
    # Equal weights across all ETFs
    weights = pd.DataFrame(
        1.0 / len(prices_df.columns),
        index=prices_df.index,
        columns=prices_df.columns
    )
    
    # Calculate daily returns
    perct_changes = prices_df.pct_change()
    
    # Portfolio returns: equal-weighted sum
    port_rets = (weights * perct_changes).sum(axis=1).fillna(0.0)
    port_rets = port_rets.loc[port_rets.index.isin(date_range)] # filter for relevant dates
    
    return port_rets