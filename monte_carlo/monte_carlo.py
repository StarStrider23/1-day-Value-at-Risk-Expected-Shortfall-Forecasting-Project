import numpy as np

class MonteCarlo:

    def __init__(self, data, distribution_model, drift_model, volatility_model, steps=1, n_sim=10000):
        self.data = data
        self.distribution_model = distribution_model
        self.drift_model = drift_model
        self.volatility_model = volatility_model 
        self.steps = steps
        self.n_sim = n_sim
        self.dt = 1/steps
        self.returns = np.log(data/data.shift(1)).dropna()

    def fit(self, market=None, rf_rate=None):
        self.drift_model.drift(self.returns, market, rf_rate)
        self.volatility_model.volatility(self.returns)

    def forecast_var_es(self, data, alpha=0.99):
        mu = self.drift_model.get_drift()
        sigma = self.volatility_model.get_volatility()

        n_assets = data.shape[1]

        if n_assets == 1:
            S = np.zeros((self.steps+1, self.n_sim))
            S[0, :] = data.iloc[-1]
            for i in range(1, self.steps+1):
                Z = self.distribution_model.get_distribution(self.returns, self.n_sim, 1)
                S[i, :] = (
                            S[i-1, :] * np.exp((mu[i-1] - 0.5 * sigma[i-1]**2) * 
                                              self.dt + sigma[i-1] * np.sqrt(self.dt) * Z)
                            )

            returns_paths = (S[-1] - S[0]) / S[0]

        else:
            S = np.zeros((self.steps+1, self.n_sim, n_assets))
            for i in range(n_assets):
                S[0, :, i] = data.iloc[-1].iloc[i]

            cov_matrix = self.returns.cov()
            low_triang = np.linalg.cholesky(cov_matrix)

            for i in range(1, self.steps+1):
                Z = self.distribution_model.get_distribution(self.returns, self.n_sim, n_assets)
                eps = low_triang @ Z
                for j in range(n_assets): 
                    S[i, :, j] = (
                                    S[i-1, :, j] * np.exp((mu[j] - 0.5 * sigma[j]**2) * 
                                                        self.dt + np.sqrt(self.dt) * eps[j])
                                )

            weights = np.array([1/n_assets] * n_assets)
            portfolio = np.sum(S * weights, axis=2)

            returns_paths = (portfolio[-1] - portfolio[0]) / portfolio[0]

        var = float(np.percentile(returns_paths, 100 * (1 - alpha)))
        es = float(np.mean(returns_paths[returns_paths <= var]))

        return var, es