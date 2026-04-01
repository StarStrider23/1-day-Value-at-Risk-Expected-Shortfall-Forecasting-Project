# 1-day Value-at-Risk & Expected Shortfall Forecasting Project

This project implements a single- and multi-asset risk framework. It utilises different distributions (Gaussian and Student’s t-distribution), drifts (constant and CAPM-based drift) and volatilities (constant and
GARCH volatility modelling), and Monte Carlo simulation to estimate 1-day Value-atRisk (VaR) and Expected Shortfall (ES) at the 99th percentile for one or multiple assets (using the Cholesky decomposition). Models are validated using the Kupiec and Christoffersen tests, and their predictions are compared with historical VaR/ES to evaluate performance.
