import matplotlib.pyplot as plt
import numpy as np

def plotting(tsmom_returns, benchmark_returns, oos_count):
    '''Plots equity curves and drawdowns for TSMOM vs Benchmark'''

    # Calculate equity curves
    tsmom_equity = (1 + tsmom_returns).cumprod()
    benchmark_equity = (1 + benchmark_returns).cumprod()
    
    # Calculate drawdowns
    tsmom_dd = (tsmom_equity - tsmom_equity.expanding().max()) / tsmom_equity.expanding().max()
    benchmark_dd = (benchmark_equity - benchmark_equity.expanding().max()) / benchmark_equity.expanding().max()
    
    tsmom_max_dd = tsmom_dd.min()
    benchmark_max_dd = benchmark_dd.min()

    # Create subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

    # Equity curves
    tsmom_equity.plot(ax=ax1, title="TSMOM Strategy - Equity Curve", color="blue", label="TSMOM")
    ax1.set_ylabel("Growth of $1")
    ax1.set_xlabel("")
    ax1.grid(True, alpha=0.3)

    benchmark_equity.plot(ax=ax2, title="Equal-Weight Benchmark - Equity Curve", color="green", label="Benchmark")
    ax2.set_ylabel("Growth of $1")
    ax2.set_xlabel("")
    ax2.grid(True, alpha=0.3)
    
    # Share y-axis for equity curves
    ax2.set_ylim(ax1.get_ylim())

    # Drawdowns
    tsmom_dd.plot(ax=ax3, title="TSMOM - Drawdown", color="red", label="TSMOM DD")
    ax3.axhline(y=tsmom_max_dd, color='darkred', linestyle='--', label=f'Max DD: {tsmom_max_dd*100:.2f}%')
    ax3.set_ylabel("Drawdown (%)")
    ax3.set_xlabel("")
    ax3.legend(loc='center')
    ax3.grid(True, alpha=0.3)

    benchmark_dd.plot(ax=ax4, title="Equal-Weight Benchmark - Drawdown", color="orange", label="Benchmark DD")
    ax4.axhline(y=benchmark_max_dd, color='darkorange', linestyle='--', label=f'Max DD: {benchmark_max_dd*100:.2f}%')
    ax4.set_ylabel("Drawdown (%)")
    ax4.set_xlabel("")
    ax4.legend(loc='center left')
    ax4.grid(True, alpha=0.3)

    # Share y-axis for drawdowns
    ax3.set_ylim(ax4.get_ylim())

    plt.tight_layout()
    plt.savefig("plots.png", dpi=150, bbox_inches="tight")
    print("Plot saved to plots.png\n")

    # Print comparison stats    
    for name, returns, max_dd in [("TSMOM", tsmom_returns, tsmom_max_dd), 
                                    ("Equal-Weight Benchmark", benchmark_returns, benchmark_max_dd)]:
        ann_ret = returns.mean() * 252 * 100
        ann_vol = returns.std() * np.sqrt(252) * 100
        sharpe = 0 if ann_vol == 0 else (ann_ret / 100) / (ann_vol / 100)
        
        print(f"\n{name}:")
        print(f"    Annualised Return: {ann_ret:.2f}%")
        print(f"    Annualised Volatility: {ann_vol:.2f}%")
        print(f"    Sharpe Ratio: {sharpe:.4f}")
        print(f"    Maximum Drawdown: {max_dd*100:.2f}%")
    
    print(f"\nAccumulative out-of-sample years: {oos_count}")

    # plt.show()