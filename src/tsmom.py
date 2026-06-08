import numpy as np
import pandas as pd

def tsmom(price_range, vol_lookback,
          target_vol, lookback_range):
    '''Compute daily portfolio returns based on signals'''

    price_range = price_range.asfreq("B") # align all to be business days
    perct_changes = price_range.pct_change() # %changes

    # list of DFs
    signals = [np.sign(price_range / price_range.shift(k) - 1.0) for k in lookback_range]

    # avg signal
    sum_hrzt, count_no_hrzt = None, None
    for signal in signals:
        if sum_hrzt is None: # first iteration
            sum_hrzt = signal # initialise sum with the first signal df
            count_no_hrzt = signal.notna().astype(int) # count no of signals across
        else: # subsequent iterations
            sum_hrzt = sum_hrzt.add(signal, fill_value=0) # resulting NaN become 0
            count_no_hrzt = count_no_hrzt.add(signal.notna().astype(int), fill_value=0) 
            # count no of signals across, any NaN become 0

    avg_sig = sum_hrzt.div(count_no_hrzt.replace(0, np.nan)) # div to find avgs

    ### normalising weights ###
    daily_vol = perct_changes.rolling(vol_lookback).std()
    ann_vol = daily_vol * np.sqrt(252)
    weights = (avg_sig / ann_vol).replace([np.inf, -np.inf], np.nan)
    weekly_rebal_weights = weights.resample("W-FRI").last().ffill() # rebal to fri weight
    daily_rebal_weights = weekly_rebal_weights.reindex(perct_changes.index).ffill() 
    # expand fri weight to subsequent week

    sum_weights = daily_rebal_weights.abs().sum(axis=1).replace(0, np.nan)
    # summing up absol weights across each etf

    norm_weights = daily_rebal_weights.div(sum_weights, axis=0).fillna(0.0)
    # dividing to obtain normalised weights, to cater to some ETFs existing before others
    
    ### ex ante vol targeting ###
    port_vol_daily = np.sqrt((norm_weights.pow(2) * daily_vol.pow(2)).sum(axis=1))
    #ignore cov term, use diagonal approx (use only each asset's own var)

    k = (target_vol / np.sqrt(252)) / port_vol_daily
    # scale factor k for forecast to hit target vol

    k = k.replace([np.inf, -np.inf], np.nan).fillna(1.0)
    # replace infs with NaNs then with 1.0

    scaled_weights = norm_weights.mul(k, axis=0)
    # apply k to weight vector 

    port_rets = (scaled_weights.shift(1) * perct_changes).sum(axis=1).fillna(0.0)
    # use D_t-1 weights for D_1 to avoid clairvoyance
    
    return port_rets