import numpy as np
from scipy.optimize import minimize 

class Constant_Volatility:

    def volatility(self, data, steps=1):
        self.const_vol = data.std().values
    
    def get_volatility(self):
        return self.const_vol
    
class GARCH11_Volatility:

    def fit(self, data):
        self.epsilon = data - np.mean(data)
        self.epsilon = 100 * self.epsilon 
        self.variance = np.var(self.epsilon)

        init_params = [1e-6, 0.05, 0.9]  

        res = minimize(
            self._log_likelihood,
            init_params,
            method='L-BFGS-B'
            )

        self.omega, self.alpha, self.beta = res.x[0]/100**2, res.x[1], res.x[2] 

    def _log_likelihood(self, params):
        omega, alpha, beta = params

        if (alpha + beta >= 1 - 1e-6) or (alpha < 0) or (beta < 0) or (omega < 0):
            return 1e10

        variance = np.zeros(len(self.epsilon))
        variance[0] = omega / (1 - alpha - beta + 1e-6)

        for i in range(1, len(self.epsilon)):
            variance[i] = (
                omega +
                alpha * self.epsilon.iloc[i-1]**2 +
                beta * variance[i-1]
            )

        logL = -0.5 * np.sum(
            np.log(2 * np.pi) +
            np.log(variance) +
            self.epsilon**2 / variance
        )

        return -logL

    def volatility(self, data, steps=1):
        self.std = []

        for j in range(data.shape[1]):

            self.fit(data[data.columns.values[j]])

            variance = np.zeros(steps+1)
            variance[0] = self.omega/(1 - self.alpha - self.beta + 1e-6)
        
            for i in range(1, steps+1):
                variance[i] = (
                                self.omega + 
                                self.alpha * (self.epsilon.iloc[i-1]/100)**2 + 
                                self.beta * variance[i-1]
                            ) 
                
                self.std.append(float(np.sqrt(variance[i])))

    def get_volatility(self):
        return self.std
    