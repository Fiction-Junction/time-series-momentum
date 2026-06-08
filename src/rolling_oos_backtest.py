import pandas as pd
from pandas.tseries.offsets import BDay
from src.tsmom import tsmom

def rolling(data, train_years, test_years, target_vol,
            vol_lookback, lookback_range, padding):
    '''
    Conserves data with 3 training years and 1 testing year 
    Runs TSMOM strat on each padded window
    Returns concatenated OOS period returns, dates, count
    '''

    prices = pd.DataFrame(data).asfreq("B").ffill()
    idx = prices.index
    roll_over = idx[0]
    oos_res = []
    oos_dates = []
    oos_count = 0

    while True:
        train_start = roll_over
        train_end = train_start + pd.DateOffset(years=train_years) - pd.DateOffset(days=1)
        test_start = train_end + pd.DateOffset(days=1)
        test_end = test_start + pd.DateOffset(years=test_years) - pd.DateOffset(days=1)
        if test_end > idx[-1]:
            break

        # padding so day-1 of OOS has valid momentum/vol
        start_with_pad = test_start - BDay(padding)
        start_with_pad= max(start_with_pad, idx[0]) # in case padding exceeds first available date
        pad_window = prices.loc[start_with_pad:test_end]

        # ensure ETF has sufficient OOS dates
        pre_hist = pad_window.loc[start_with_pad : (test_start - BDay(1))]
        valid_etf = []
        for col in pad_window.columns:
            if pre_hist[col].notna().sum() >= padding: 
                valid_etf.append(col)
        
        if len(valid_etf) < 2: # immediate rollover if insufficient etf
            roll_over = train_start + pd.DateOffset(years=1)
            oos_count += test_years
            continue

        pad_window = pad_window[valid_etf] # filter only for valid etf with padded window
        res = tsmom(pad_window, vol_lookback, target_vol, lookback_range)
        oos_window = res.loc[test_start:test_end]
        oos_res.append(oos_window)
        oos_dates.extend(oos_window.index.tolist())

        roll_over = train_start + pd.DateOffset(years=1) # roll to next window by one year
        oos_count += test_years

    total_returns = pd.concat(oos_res).sort_index()
    return total_returns, oos_dates, oos_count
