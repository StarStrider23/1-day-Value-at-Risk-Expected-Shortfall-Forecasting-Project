import numpy as np

class Constant_Drift:

    def drift(self, data, market, rf_rate):
        self.const_drift = data.mean().values
    
    def get_drift(self):
        return self.const_drift
    
class CAPM_Drift:

    def drift(self, data, market, rf_rate):
        daily_returns_market = np.log(market/market.shift(1)).dropna()
        rf = np.mean(rf_rate/100)
        cov_matrix = np.cov(np.hstack([data, daily_returns_market]), rowvar=False)
        beta_coef = cov_matrix[:-1, -1] / cov_matrix[-1, -1] 

        self.CAPM_drift = rf/252 + beta_coef * (np.mean(data) - rf/252)

    def get_drift(self):
        return self.CAPM_drift