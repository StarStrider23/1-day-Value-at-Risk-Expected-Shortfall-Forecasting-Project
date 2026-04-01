# 1-day Value-at-Risk & Expected Shortfall Forecasting Project

Project by Alexsey Chernichenko

## Project Goal

This project implements a single- and multi-asset risk framework. It utilises different distributions (Gaussian and Student’s t-distribution), drifts (constant and CAPM-based drift) and volatilities (constant and
GARCH(1,1) volatility modelling), and Monte Carlo simulation to estimate 1-day Value-at-Risk (VaR) and Expected Shortfall (ES) at the 99th percentile for one or multiple assets (using the Cholesky decomposition). Models are validated using the Kupiec and Christoffersen tests, and their predictions are compared with historical VaR/ES to evaluate performance.

## Methodology & Models

The project is based on a Monte Carlo simulation framework for forecasting 1-day risk measures. Asset returns are modeled using Geometric Brownian Motion (GBM), which assumes that returns follow a stochastic process with a drift and a volatility component. Within this framework, different assumptions are tested to evaluate their impact on risk estimation.

First, two alternative distributional assumptions for returns are considered: the Normal distribution, which is standard in many financial models but underestimates extreme events and the Student’s t-distribution, which captures heavy tails and is therefore more suitable for modeling large market moves.

Second, the drift component is modeled in two ways. A constant drift assumes a fixed expected return over time, while a CAPM-based drift incorporates systematic market risk by linking expected returns to a market factor.

Third, volatility is modeled either as constant or using a GARCH(1,1) process, which allows volatility to evolve over time and capture clustering effects commonly observed in financial markets.

While the single-asset portfolio included only one share of MSFT, for the multi-asset part, the portfolio was chosen to be consisting of GOOGL, MSFT and AAPL (with equal weights). Correlated asset returns are generated using Cholesky decomposition of the covariance matrix, ensuring that simulated paths preserve the empirical correlation structure between assets.

Finally, model performance is evaluated through backtesting on the single-asset case. The Kupiec test is used to assess whether the frequency of VaR violations matches the expected confidence level, while the Christoffersen test evaluates whether violations occur independently over time, i.e., without clustering.

## Results 

### Single-asset (MSFT)

