# 1-day Value-at-Risk & Expected Shortfall Forecasting Project

Project by Alexsey Chernichenko

## Project Goal

This project implements a single- and multi-asset risk framework. It utilises different distributions (Normal and Student’s t-distribution), drifts (constant and CAPM-based drift) and volatilities (constant and
GARCH(1,1) volatility modelling), and Monte Carlo simulation to estimate 1-day Value-at-Risk (VaR) and Expected Shortfall (ES) at the 99th percentile for one or multiple assets (using the Cholesky decomposition). Models are validated using the Kupiec and Christoffersen tests, and their predictions are compared with historical VaR/ES to evaluate performance.

## Methodology & Models

The project is based on a Monte Carlo simulation framework for forecasting 1-day risk measures. Asset returns are modeled using Geometric Brownian Motion (GBM), which assumes that returns follow a stochastic process with a drift and a volatility component. Within this framework, different assumptions are tested to evaluate their impact on risk estimation.

First, two alternative distributional assumptions for returns are considered: the Normal distribution, which is standard in many financial models but underestimates extreme events and the Student’s t-distribution, which captures heavy tails and is therefore more suitable for modeling large market moves.

Second, the drift component is modeled in two ways. A constant drift assumes a fixed expected return over time, while a CAPM-based drift incorporates systematic market risk by linking expected returns to a market factor.

Third, volatility is modeled either as constant or using a GARCH(1,1) process, which allows volatility to evolve over time and capture clustering effects commonly observed in financial markets.

While the single-asset portfolio included only one share of MSFT, for the multi-asset part, the portfolio was chosen to be consisting of GOOGL, MSFT and AAPL (with equal weights). Correlated asset returns are generated using Cholesky decomposition of the covariance matrix, ensuring that simulated paths preserve the empirical correlation structure between assets.

Finally, model performance is evaluated through backtesting on the single-asset case. The Kupiec test is used to assess whether the frequency of VaR violations matches the expected confidence level, while the Christoffersen test evaluates whether violations occur independently over time, i.e., without clustering.

It should also be mentioned that the dataset spaned approximately four years of daily observations, of which the last 1000 days were used for backtesting.

## Structure

The models folder contains the distribution, drift and volatility model definitions. The monte_carlo folder includes the Monte Carlo simulation engine file. The test folder contains the file test.py that implements the Kupiec and Christoffersen tests. Finally, main.py ties everything together and executes the workflow.

## Results 

Results are averaged across 10 simulation runs to reduce Monte Carlo variability and provide more robust performance estimates.

### Single-asset (MSFT)

Historical VaR = -0.0438

| Model                                            | VaR Mean | VaR % Mean | VaR Median | VaR Min | VaR Max | VaR Std |
| ------------------------------------------------ | -------- | ---------- | ---------- | ------- | ------- | ------- |
| Normal, Constant drift, Constant volatility      | -0.0389  | 11.2       | -0.0391    | -0.0400 | -0.0378 | 0.0007  |
| Student's t, Constant drift, Constant volatility | -0.0442  | 2.7        | -0.0437    | -0.0465 | -0.0426 | 0.0014  |
| Normal, CAPM, Constant volatility                | -0.0386  | 11.8       | -0.0387    | -0.0400 | -0.0372 | 0.0008  |
| Student's t, CAPM, Constant volatility           | -0.0442  | 2.7        | -0.0437    | -0.0472 | -0.0420 | 0.0015  |
| Normal, Constant drift, GARCH(1,1)               | -0.0410  | 6.4        | -0.0409    | -0.0418 | -0.0404 | 0.0004  |
| Student's t, Constant drift, GARCH(1,1)          | -0.0464  | 6.0        | -0.0466    | -0.0498 | -0.0438 | 0.0018  |
| Normal, CAPM, GARCH(1,1)                         | -0.0414  | 5.5        | -0.0413    | -0.0427 | -0.0401 | 0.0008  |
| Student's t, CAPM, GARCH(1,1)                    | -0.0454  | 3.9        | -0.0454    | -0.0480 | -0.0433 | 0.0011  |

Historical ES = -0.0593

| Model                                            | ES Mean | ES % Mean | ES Median | ES Min  | ES Max  | ES Std |
| ------------------------------------------------ | ------- | --------- | --------- | ------- | ------- | ------ |
| Normal, Constant drift, Constant volatility      | -0.0447 | 24.7      | -0.0449   | -0.0458 | -0.0433 | 0.0008 |
| Student's t, Constant drift, Constant volatility | -0.0597 | 3.5       | -0.0597   | -0.0632 | -0.0561 | 0.0024 |
| Normal, CAPM, Constant volatility                | -0.0441 | 25.7      | -0.0443   | -0.0452 | -0.0421 | 0.0011 |
| Student's t, CAPM, Constant volatility           | -0.0603 | 3.8       | -0.0598   | -0.0666 | -0.0537 | 0.0031 |
| Normal, Constant drift, GARCH(1,1)               | -0.0471 | 20.6      | -0.0472   | -0.0479 | -0.0463 | 0.0005 |
| Student's t, Constant drift, GARCH(1,1)          | -0.0621 | 5.1       | -0.0622   | -0.0660 | -0.0582 | 0.0022 |
| Normal, CAPM, GARCH(1,1)                         | -0.0469 | 20.9      | -0.0470   | -0.0483 | -0.0454 | 0.0010 |
| Student's t, CAPM, GARCH(1,1)                    | -0.0610 | 3.7       | -0.0609   | -0.0649 | -0.0584 | 0.0023 |


All models produced 7/1000 violations. The Kupiec and Christoffersen tests yielded 1.001 and 0.0989 respectively.

### Multi-asset (MSFT, AAPL and GOOGL)

Historical VaR = -0.0417

| Model | Mean ES | Mean VaR% | Median | Standard deviation | Min | Max |
|---|---|---|---|---|---|---|
| Normal, const drift & volatility |  | | | | |	|
| t, const drift & volatility | | | | | |	|
| Normal, CAPM & const volatility | | | | | | |
| t, CAPM & const volatility | | | | | | |
| Normal, const drift & GARCH	| | | | | |	|
| t, const drift & GARCH | | | | | | |
| Normal, CAPM & GARCH | | | | | | |
| t, CAPM & GARCH	| | | | | |	|

Historical ES = -0.0491

| Model | Mean | Mean ES% | Median | Standard deviation | Min | Max |
|---|---|---|---|---|---|---|
| Normal, const drift & volatility |  | | | | |	|
| t, const drift & volatility | | | | | |	|
| Normal, CAPM & const volatility | | | | | | |
| t, CAPM & const volatility | | | | | | |
| Normal, const drift & GARCH	| | | | | |	|
| t, const drift & GARCH | | | | | | |
| Normal, CAPM & GARCH | | | | | | |
| t, CAPM & GARCH	| | | | | |	|


## Discussion

The results reveal a clear and somewhat non-trivial pattern in the performance of the different models. For the single-asset case, models based on the Student’s t-distribution consistently produce more accurate estimates of both VaR and ES compared to their normal counterparts. This is particularly evident for Expected Shortfall, where the normal distribution significantly underestimates tail risk. This finding aligns with well-known stylized facts in financial markets, namely that individual asset returns exhibit fat tails and extreme events occur more frequently than predicted by the normal distribution.

However, this pattern reverses in the multi-asset portfolio setting. In contrast to the single-asset results, models based on the Student’s t-distribution systematically overestimate risk, producing VaR and ES values that deviate substantially from historical benchmarks. Instead, models assuming normally distributed returns provide more accurate and stable estimates for the diversified portfolio.

This difference can be explained by the effect of diversification. When combining multiple assets, idiosyncratic extreme events tend to offset each other, leading to a distribution of portfolio returns that is closer to normal. As a result, heavy-tailed assumptions that are appropriate at the individual asset level may become overly conservative when applied to an aggregated portfolio. This suggests that heavy-tailed behavior is largely idiosyncratic and diversifiable.

Across both settings, the inclusion of CAPM-based drift and GARCH(1,1) volatility does not lead to consistent improvements in forecasting performance. While these models are theoretically more sophisticated and capture important financial phenomena such as time-varying volatility and systematic risk exposure, their benefits appear limited in the context of unconditional 1-day risk forecasting. In practice, the additional estimation complexity may introduce noise that offsets their theoretical advantages.

Finally, the backtesting results for the single asset indicate that all models produce an acceptable number of VaR violations and pass both the Kupiec and Christoffersen tests. In particular, every model produced only 7 violations out of 1000 observations, which makes up less than 1%. This suggests that, despite differences in accuracy, the models are statistically adequate in terms of coverage and independence of violations. However, these tests alone are not sufficient to distinguish between models, as they do not capture the magnitude of tail losses, which is better reflected in the ES metric.

One could probably notice the fact that all the models produced identical results for Kupiec and Christoffersen tests. For 1-day 99th percentile VaR over 1000 days, the number of expected violations is very small, so many models produce nearly identical violating days. As a result, Kupiec and Christoffersen tests give similar statistics, which reflects the sparsity of extreme events rather than an implementation error. This was confirmed by backtesting the models at the 95th percentile, which then gave different results for each of the models. 

Overall, the findings highlight that model selection should be driven by the specific application and level of aggregation. While heavy-tailed distributions are essential for accurately modeling individual asset risk, simpler models may be more appropriate for diversified portfolios, where extreme risks are naturally mitigated.

## Outlook

This project focuses on 1-day ahead risk forecasting, but the framework can be naturally extended to multi-day (n-day) VaR and Expected Shortfall.

For models based on constant volatility, such as standard Geometric Brownian Motion with normally distributed returns, multi-day risk measures can be approximated using the square-root-of-time rule, where volatility (and therefore VaR and ES) scales with √n. This approach relies on the assumption of independent and identically distributed returns.

However, this scaling does not apply to GARCH-type models, where volatility evolves over time and depends on past shocks. In such models, returns are heteroskedastic and serially dependent, meaning that future risk cannot be obtained through simple scaling. Instead, multi-day forecasts require iterative simulation or recursive volatility forecasting, which significantly increases computational complexity.
