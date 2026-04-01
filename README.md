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

Historical VaR = -0.0438, historical ES = -0.0593

| Model | VaR	| VaR % diff  |	ES  |	ES % diff |
|---|---|---|---|---|
| Normal, const drift & volatility | -0.0396 | 9.6% |	-0.0451 | 23.9% |
| t, const drift & volatility | -0.0425 | 3.0% | -0.0571  |	3.8% |
| Normal, CAPM & const volatility |	-0.0391 |	10.7% |	-0.0450 |	24.1% |
| t, CAPM & const volatility | -0.0444 | 1.4%	| -0.0617 |	4.0% |
| Normal, const drift & GARCH	| -0.0406 |	7.3% |	-0.0464 |	21.8% |
| t, const drift & GARCH | -0.0464 |	5.9% |	-0.0613 |	3.3% |
| Normal, CAPM & GARCH | -0.0404 |	7.8% |	-0.0459 |	22.2% |
| t, CAPM & GARCH	| -0.0473 |	8.1% | -0.0624 | 5.2% |

### Multi-asset (MSFT, AAPL and GOOGL)

Historical VaR = -0.0417, historical ES = -0.0491

| Model | VaR	| VaR % diff  |	ES  |	ES % diff |
|---|---|---|---|---|
|Normal, const drift & volatility | -0.0347 |	16.9% |	-0.0401 |	18.2% |
|Student-t, const drift & volatility |	-0.0543 |	30.0%	| -0.0690 |	40.6% |
|Normal, CAPM & const volatility |	-0.0357 |	14.4% |	-0.0406 |	17.3% |
|t, CAPM & const volatility	-0.0562 |	34.7% |	-0.0782 |	59.2% |
|Normal, const drift & GARCH |	-0.0356 |	14.6% |	-0.0406 |	17.3% |
|t, const drift & GARCH	-0.0556 |	33.3% |	-0.0764 |	55.7% |
|Normal, CAPM & GARCH	-0.0352 |	15.8%	| -0.0410 |	16.4% |
|t, CAPM & GARCH |	-0.0564 |	35.2% |	-0.0750 |	52.7% |

## Discussion

The results reveal a clear and somewhat non-trivial pattern in the performance of the different models. For the single-asset case, models based on the Student’s t-distribution consistently produce more accurate estimates of both VaR and ES compared to their normal counterparts. This is particularly evident for Expected Shortfall, where the normal distribution significantly underestimates tail risk. This finding aligns with well-known stylized facts in financial markets, namely that individual asset returns exhibit fat tails and extreme events occur more frequently than predicted by the normal distribution.

However, this pattern reverses in the multi-asset portfolio setting. In contrast to the single-asset results, models based on the Student’s t-distribution systematically overestimate risk, producing VaR and ES values that deviate substantially from historical benchmarks. Instead, models assuming normally distributed returns provide more accurate and stable estimates for the diversified portfolio.

This difference can be explained by the effect of diversification. When combining multiple assets, idiosyncratic extreme events tend to offset each other, leading to a distribution of portfolio returns that is closer to normal. As a result, heavy-tailed assumptions that are appropriate at the individual asset level may become overly conservative when applied to an aggregated portfolio. This suggests that heavy-tailed behavior is largely idiosyncratic and diversifiable.

Across both settings, the inclusion of CAPM-based drift and GARCH(1,1) volatility does not lead to consistent improvements in forecasting performance. While these models are theoretically more sophisticated and capture important financial phenomena such as time-varying volatility and systematic risk exposure, their benefits appear limited in the context of unconditional 1-day risk forecasting. In practice, the additional estimation complexity may introduce noise that offsets their theoretical advantages.

Finally, the backtesting results for the single asset indicate that all models produce an acceptable number of VaR violations and pass both the Kupiec and Christoffersen tests. In particular, every model produced only 7 violations out of 1000 observations, which makes up less than 1 percent. This suggests that, despite differences in accuracy, the models are statistically adequate in terms of coverage and independence of violations. However, these tests alone are not sufficient to distinguish between models, as they do not capture the magnitude of tail losses, which is better reflected in the ES metric.

Overall, the findings highlight that model selection should be driven by the specific application and level of aggregation. While heavy-tailed distributions are essential for accurately modeling individual asset risk, simpler models may be more appropriate for diversified portfolios, where extreme risks are naturally mitigated.

## Outlook

This project focuses on 1-day ahead risk forecasting, but the framework can be naturally extended to multi-day (n-day) VaR and Expected Shortfall.

For models based on constant volatility, such as standard Geometric Brownian Motion with normally distributed returns, multi-day risk measures can be approximated using the square-root-of-time rule, where volatility (and therefore VaR and ES) scales with √n. This approach relies on the assumption of independent and identically distributed returns.

However, this scaling does not apply to GARCH-type models, where volatility evolves over time and depends on past shocks. In such models, returns are heteroskedastic and serially dependent, meaning that future risk cannot be obtained through simple scaling. Instead, multi-day forecasts require iterative simulation or recursive volatility forecasting, which significantly increases computational complexity.
