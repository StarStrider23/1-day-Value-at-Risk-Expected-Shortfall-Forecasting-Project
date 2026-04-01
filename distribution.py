import numpy as np
import scipy as sp
import scipy.stats as stats

class Normal_Distribution:

    def get_distribution(self, returns, n_sim, n_assets=1):
        returns = None
        N = np.random.normal(0, 1, size=(n_assets, n_sim))
        return N
    

class t_Distribution:

    def __init__(self, df=4):
        self.df = df

    def get_distribution(self, returns, n_sim, n_assets=1):
        residuals = (returns - np.mean(returns))/np.std(returns, axis=0)
        residuals_flat = residuals.values.flatten()
        self.df, _, _ = stats.t.fit(residuals_flat)
        if n_assets==1:
            t = sp.stats.t.rvs(df=self.df, size=(1, n_sim))/np.sqrt(self.df/(self.df-2))
            return t
        else:
            Z = np.random.normal(size=(n_assets, n_sim))
            chi = np.random.chisquare(self.df, size=n_sim)
            scaling = np.sqrt(self.df/chi)
            t = Z * scaling
            return t
