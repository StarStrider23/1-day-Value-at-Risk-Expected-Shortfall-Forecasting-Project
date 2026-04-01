import yfinance as yf
import datetime as dt

from models.distribution import Normal_Distribution
from models.distribution import t_Distribution
from models.drift import Constant_Drift
from models.drift import CAPM_Drift
from models.volatility import Constant_Volatility
from models.volatility import GARCH11_Volatility
from monte_carlo import MonteCarlo

import risk

# A function that unifies all the required testing and validation 

def var_es_comparison(data, 
                      market_data, rf_data, days, 
                      *model, backtesting=True, 
                      tests=True, steps=1, n_sim=10000):

    weights = [1/len(data.columns.values)] * len(data.columns.values)

    mc = MonteCarlo(data[:-1], *model, steps, n_sim)
    mc.fit(market_data[:-1], rf_data[:-1])
    var, es = mc.forecast_var_es(data[:-1])

    # Historical VaR and ES 
    var_hist, es_hist = risk.historical_var_es(data, weights)

    var_hist = float(var_hist)
    es_hist = float(es_hist)

    var_percent = abs(100 * (1 - var/var_hist))
    es_percent = abs(100 * (1 - es/es_hist))

    results = {"VaR": var, 
               "Historical VaR": var_hist, 
               "VaR percent difference": var_percent,
               "ES": es, 
               "Historical ES": es_hist,
               "ES percent difference": es_percent,
                }

    if backtesting is True:

        data_backtesting = data[-days:]

        var_list = []
        for j in range(days):
            mc = MonteCarlo(data[:j-days], *model, steps, n_sim)
            mc.fit(market_data[:j-days], rf_data[:j-days])
            var, es = mc.forecast_var_es(data[:j-days])

            var_list.append(var)

        violations = risk.compute_violations(data_backtesting, var_list)
        results["Number of violations"] = int(sum(violations))
        results["Sample size"] = len(var_list)

    if backtesting is True and tests is True:
        # Kupiec test
        results["Kupiec test"] = risk.kupiec_test(violations)

        # Christoffersen test
        results["Christoffersen test"] = risk.christofferesen_test(violations)
    
    return results

# Full model validation of all models

dist = {"Normal distribution": Normal_Distribution(), "Student's t-distribution": t_Distribution()}
drift = {"Constant drift": Constant_Drift(), "CAPM": CAPM_Drift()}
vol = {"Constant volatility": Constant_Volatility(), "GARCH(1, 1)" :GARCH11_Volatility()}

start_date = dt.datetime(2022, 1, 1)
end_date = dt.datetime(2026, 1, 3)
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
                                backtesting=True, tests=True, steps=1, n_sim=10000)
            print(f"The results for the model with {keys_dist}, {keys_drift} and {keys_vol} are: {results_p1}")
            print()

# Multi asset precision of the models

multiple_assets = ['AAPL', 'GOOGL', 'MSFT']
data_mult = yf.download(multiple_assets, start_date, end_date)['Close']

for keys_vol, values_vol in vol.items():
    for keys_drift, values_drift in drift.items():
        for keys_dist, values_dist in dist.items():
            results_p2 = var_es_comparison(data, market_data, rf_data, 
                                sample_days, values_dist, values_drift, values_vol, 
                                backtesting=False, tests=False, steps=1, n_sim=10000)
            print(f"The results for the model with {keys_dist}, {keys_drift} and {keys_vol} are: {results_p2}")
            print()