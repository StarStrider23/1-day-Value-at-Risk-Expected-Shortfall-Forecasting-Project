import yfinance as yf
import datetime as dt
import statistics as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from models.distribution import Normal_Distribution
from models.distribution import t_Distribution
from models.drift import Constant_Drift
from models.drift import CAPM_Drift
from models.volatility import Constant_Volatility
from models.volatility import GARCH11_Volatility
from monte_carlo.monte_carlo import MonteCarlo

import test.test as test

# Function that unifies all the required testing and validation 

def var_es_comparison(data, 
                      market_data, rf_data, days, 
                      *model, backtesting=True, 
                      steps=1, n_sim=10000):

    weights = [1/len(data.columns.values)] * len(data.columns.values)

    mc = MonteCarlo(data[:-1], *model, steps, n_sim)
    mc.fit(market_data[:-1], rf_data[:-1])
    var, es = mc.forecast_var_es(data[:-1])

    # Historical VaR and ES 
    var_hist, es_hist = test.historical_var_es(data, weights)

    var_hist = float(var_hist)
    es_hist = float(es_hist)

    var_percent = abs(100 * (1 - var/var_hist))
    es_percent = abs(100 * (1 - es/es_hist))

    results = [var, var_hist, var_percent, 
               es, es_hist, es_percent]

    if backtesting is True:

        data_backtesting = data[-days:]

        var_list = []
        for j in range(0, days):
            mc = MonteCarlo(data[:j-days], *model, steps, n_sim)
            mc.fit(market_data[:j-days], rf_data[:j-days])
            var, es = mc.forecast_var_es(data[:j-days])

            var_list.append(var)

        violations = test.compute_violations(data_backtesting, var_list[:-1])
        n_viol = int(sum(violations))
        sample_size = len(var_list)

        kupiec = test.kupiec_test(violations)

        christoffersen = test.christofferesen_test(violations)

        results.append(violations, n_viol, sample_size, kupiec, christoffersen)
    
    return results

# Print function

def print_results(results_list):
    results = {"VaR": results_list[0], 
               "Historical VaR": results_list[1], 
               "VaR percent difference": results_list[2],
               "ES": results_list[3], 
               "Historical ES": results_list[4],
               "ES percent difference": results_list[5],
                }
    if len(results_list) > 6:
        results["Violations"] = results_list[6]
        results["Sample size"] = results_list[7]
        results["Kupiec test"] = results_list[8]
        results["Christoffersen test"] = results_list[9]

    return results

# Full model validation of all models using single-asset portfolio

dist = {"Normal distribution": Normal_Distribution(), "Student's t-distribution": t_Distribution()}
drift = {"Constant drift": Constant_Drift(), "CAPM": CAPM_Drift()}
vol = {"Constant volatility": Constant_Volatility(), "GARCH(1, 1)" :GARCH11_Volatility()}

start_date = dt.datetime(2022, 1, 1)
end_date = dt.datetime.now() - dt.timedelta(1)

sample_days = 1000

asset = ['MSFT']

data = yf.download(asset, start_date, end_date)['Close']
market_data = yf.download('^GSPC', start_date, end_date)['Close']
rf_data = yf.download('^IRX', start_date, end_date)['Close']

for keys_vol, values_vol in vol.items():
    for keys_drift, values_drift in drift.items():
        for keys_dist, values_dist in dist.items():
            results_p1 = var_es_comparison(data, market_data, rf_data, 
                                sample_days, values_dist, values_drift, values_vol, 
                                backtesting=True, steps=1, n_sim=10000)
            out = print_results(results_p1)
            print(f"Model: {keys_dist}, {keys_drift} and {keys_vol}; the results are: {out}")
            print()
     
# Statistical analysis of the models when handling single-asset portfolio

stat_results_single = []

for vol_name, vol_val in vol.items():
    for drift_name, drift_val in drift.items():
        for dist_name, dist_val in dist.items():

            var, var_pct, es, es_pct = [], [], [], []

            for _ in range(10):
                res = var_es_comparison(
                    data, market_data, rf_data,
                    sample_days, dist_val, drift_val, vol_val,
                    backtesting=False, steps=1, n_sim=10000
                )

                var.append(res[0])
                var_pct.append(res[2])
                es.append(res[3])
                es_pct.append(res[5])

            stat_results_single.append({
                "model": f"{dist_name}, {drift_name} and {vol_name}",

                "VaR_mean": float(np.mean(var)),
                "VaR_std": float(np.std(var)),
                "VaR_min": float(min(var)),
                "VaR_max": float(max(var)),
                "VaR_median": float(st.median(var)),
                "VaR_pct_mean": float(np.mean(var_pct)),

                "ES_mean": float(np.mean(es)),
                "ES_std": float(np.std(es)),
                "ES_min": float(min(es)),
                "ES_max": float(max(es)),
                "ES_median": float(st.median(es)),
                "ES_pct_mean": float(np.mean(es_pct)),
            })
        print(stat_results_single)
        print()

df_single = pd.DataFrame(stat_results_single)

models = [
     "N-CD-CV", "t-CD-CV", "N-CAPM-CV", "t-CAPM-CV",
     "N-CD-GARCH", "t-CD-GARCH", "N-CAPM-GARCH", "t-CAPM-GARCH"
     ]

x = np.arange(len(models))
width = 0.35

historical_var = -var_es_comparison(data, market_data, rf_data, 
                                 sample_days, Normal_Distribution(), 
                                 Constant_Drift(), Constant_Volatility(), 
                                 backtesting=False, steps=1, n_sim=1)[1]

historical_es = -var_es_comparison(data, market_data, rf_data, 
                                 sample_days, Normal_Distribution(), 
                                 Constant_Drift(), Constant_Volatility(), 
                                 backtesting=False, steps=1, n_sim=1)[4]

plt.figure(figsize=(12,6))

plt.bar(x - width/2, -df_single["VaR_mean"], 
            width, color='b', yerr=df_single["VaR_std"], 
            capsize=10, label="Single Asset VaR")
plt.bar(x + width/2, -df_single["ES_mean"],
            width, color='r', yerr=df_single["ES_std"], 
            capsize=10, label="Single Asset ES")

plt.axhline(y=historical_var, alpha=0.5, color='c', linestyle='--', linewidth=2, label='Historical VaR')
plt.axhline(y=historical_es, alpha=0.5, color='m', linestyle='--', linewidth=2, label='Historical ES')

plt.xticks(x, models, rotation=20)
plt.ylabel("VaR and ES")
plt.title(f"VaR and ES Comparison Across Models for a Single-Asset Portfolio ({asset})")
plt.legend()

plt.tight_layout()
plt.show()

# Statistical analysis of models when handling multi-asset portfolio

multiple_assets = ['AAPL', 'GOOGL', 'MSFT']
data_mult = yf.download(multiple_assets, start_date, end_date)['Close']

stat_results_mult = []

for vol_name, vol_val in vol.items():
    for drift_name, drift_val in drift.items():
        for dist_name, dist_val in dist.items():

            var, var_pct, es, es_pct = [], [], [], []

            for _ in range(10):
                res = var_es_comparison(
                    data, market_data, rf_data,
                    sample_days, dist_val, drift_val, vol_val,
                    backtesting=False, steps=1, n_sim=10000
                )

                var.append(res[0])
                var_pct.append(res[2])
                es.append(res[3])
                es_pct.append(res[5])

            stat_results_mult.append({
                "model": f"{dist_name}, {drift_name} and {vol_name}",

                "VaR_mean": float(np.mean(var)),
                "VaR_std": float(np.std(var)),
                "VaR_min": float(min(var)),
                "VaR_max": float(max(var)),
                "VaR_median": float(st.median(var)),
                "VaR_pct_mean": float(np.mean(var_pct)),

                "ES_mean": float(np.mean(es)),
                "ES_std": float(np.std(es)),
                "ES_min": float(min(es)),
                "ES_max": float(max(es)),
                "ES_median": float(st.median(es)),
                "ES_pct_mean": float(np.mean(es_pct)),
            })
        print(stat_results_mult)
        print()

df_mult = pd.DataFrame(stat_results_mult)

x = np.arange(len(models))
width = 0.35

historical_var_mult = -var_es_comparison(data_mult, market_data, rf_data, 
                                 sample_days, Normal_Distribution(), 
                                 Constant_Drift(), Constant_Volatility(), 
                                 backtesting=False, steps=1, n_sim=1)[1]

historical_es_mult = -var_es_comparison(data_mult, market_data, rf_data, 
                                 sample_days, Normal_Distribution(), 
                                 Constant_Drift(), Constant_Volatility(), 
                                 backtesting=False, steps=1, n_sim=1)[4]

plt.figure(figsize=(12,6))

plt.bar(x - width/2, -df_mult["VaR_mean"], 
            width, color='b', yerr=df_mult["VaR_std"], 
            capsize=10, label="Single Asset VaR")
plt.bar(x + width/2, -df_mult["ES_mean"],
            width, color='r', yerr=df_mult["ES_std"], 
            capsize=10, label="Single Asset ES")

plt.axhline(y=historical_var_mult, alpha=0.5, color='c', linestyle='--', linewidth=2, label='Historical VaR')
plt.axhline(y=historical_es_mult, alpha=0.5, color='m', linestyle='--', linewidth=2, label='Historical ES')

plt.xticks(x, models, rotation=20)
plt.ylabel("VaR and ES")
plt.title(f"VaR and ES Comparison Across Models for a Multi-Asset Portfolio ({multiple_assets})")
plt.legend()

plt.tight_layout()
plt.show()