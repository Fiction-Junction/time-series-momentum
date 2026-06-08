from src.data import load_data
from src.plotting import plotting
from src.rolling_oos_backtest import rolling
from src.benchmark import benchmark_strat

etf_folder = 'data/ETFs'
data = load_data(etf_folder)

### PARAMETERS ###  
lookback_days = [63, 126, 252] # 3M, 6M, 12M
VOL_LOOKBACK = 63 # 3 months
TARGET_VOL = 0.1
PAD_DAYS = max(lookback_days) + VOL_LOOKBACK # min for 1st OOS day
TRAIN_YEARS = 3    
TEST_YEARS = 1 

# TSMOM strategy
tsmom_returns, dates, count = rolling(data, TRAIN_YEARS, TEST_YEARS,
                  TARGET_VOL, VOL_LOOKBACK,
                  lookback_days, PAD_DAYS)

# Benchmark strategy (no rolling walk-forward needed)
benchmark_returns = benchmark_strat(data, dates)

# Plot comparison
plotting(tsmom_returns, benchmark_returns, count)
