# 1-day Value-at-Risk & Expected Shortfall Forecasting

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

It should also be mentioned that the dataset spaned approximately four years of daily observations (2022-01-01 to 2026-03-31), of which the last 1000 trading days were used for backtesting.

## Background

Since the project involves a number of advanced financial models, 

### Student's t-distribution

The Student’s t-distribution is widely used for statistical inference when dealing with small sample sizes and unknown population variance. Unlike the normal distribution, it has heavier tails, which makes it more robust to extreme observations. The t-statistic is defined as:

$$ t = (\bar{X}_{n} - \mu) \frac{\sqrt{n}}{\sigma_{n}} $$

where $\bar{X}_{n}$ is the sample mean of size $n$, $\sigma_{n}$ is the sample standard deviation and $\mu$ is the population mean. The shape of the distribution depends on the degrees of freedom $\nu \coloneq (n−1)$ and it converges to the normal distribution as the sample size increases, i.e. $$. It is commonly applied in hypothesis testing and confidence interval estimation.

## Structure

The models folder contains the distribution, drift and volatility model definitions. The monte_carlo folder includes the Monte Carlo simulation engine file. The test folder contains the file test.py that implements the Kupiec and Christoffersen tests. Finally, main.py ties everything together and executes the workflow.

## Results 

Results are averaged across 10 simulation runs to reduce Monte Carlo variability and provide more robust performance estimates.

### Single-asset (MSFT)

All models produced 7/1000 violations. The Kupiec and Christoffersen tests yielded 1.001 and 0.0989 respectively.  

Historical VaR = -0.0438  

| Model                                            | VaR Mean | VaR % Mean | VaR Median | VaR Min | VaR Max | VaR Std |
| ------------------------------------------------ | -------- | ---------- | ---------- | ------- | ------- | ------- |
| Normal, Constant drift, Constant volatility      | -0.0392  | 10.54      | -0.0393    | -0.0400 | -0.0377 | 0.0006  |
| Student's t, Constant drift, Constant volatility | -0.0430  | 1.68       | -0.0434    | -0.0438 | -0.0417 | 0.0008  |
| Normal, CAPM, Constant volatility                | -0.0390  | 10.98      | -0.0389    | -0.0400 | -0.0384 | 0.0005  |
| Student's t, CAPM, Constant volatility           | -0.0442  | 2.67       | -0.0440    | -0.0467 | -0.0418 | 0.0014  |
| Normal, Constant drift, GARCH(1,1)               | -0.0406  | 7.31       | -0.0405    | -0.0412 | -0.0400 | 0.0003  |
| Student's t, Constant drift, GARCH(1,1)          | -0.0459  | 5.35       | -0.0460    | -0.0474 | -0.0427 | 0.0014  |
| Normal, CAPM, GARCH(1,1)                         | -0.0407  | 7.10       | -0.0406    | -0.0417 | -0.0398 | 0.0006  |
| Student's t, CAPM, GARCH(1,1)                    | -0.0455  | 4.73       | -0.0456    | -0.0484 | -0.0423 | 0.0018  |
  
Historical ES = -0.0593  

| Model                                            | ES Mean | ES % Mean | ES Median | ES Min  | ES Max  | ES Std |
| ------------------------------------------------ | ------- | --------- | --------- | ------- | ------- | ------ |
| Normal, Constant drift, Constant volatility      | -0.0450 | 24.21     | -0.0450   | -0.0466 | -0.0440 | 0.0007 |
| Student's t, Constant drift, Constant volatility | -0.0584 | 3.49      | -0.0576   | -0.0633 | -0.0556 | 0.0022 |
| Normal, CAPM, Constant volatility                | -0.0448 | 24.47     | -0.0449   | -0.0459 | -0.0442 | 0.0006 |
| Student's t, CAPM, Constant volatility           | -0.0592 | 3.27      | -0.0589   | -0.0637 | -0.0563 | 0.0023 |
| Normal, Constant drift, GARCH(1,1)               | -0.0463 | 22.03     | -0.0464   | -0.0474 | -0.0448 | 0.0007 |
| Student's t, Constant drift, GARCH(1,1)          | -0.0620 | 5.62      | -0.0625   | -0.0683 | -0.0559 | 0.0032 |
| Normal, CAPM, GARCH(1,1)                         | -0.0462 | 22.09     | -0.0461   | -0.0476 | -0.0453 | 0.0006 |
| Student's t, CAPM, GARCH(1,1)                    | -0.0623 | 6.17      | -0.0613   | -0.0700 | -0.0568 | 0.0041 |
  
<img width="1200" height="600" alt="Figure_1" src="https://github.com/user-attachments/assets/c8d067ec-bf9e-4868-9a29-5b2fa020bb6a" />
(Note: For ease of visual interpretation, VaR and ES are plotted in absolute terms (i.e., reported as positive values), although they represent potential losses.)

### Multi-asset (MSFT, AAPL and GOOGL)

Historical VaR = -0.0417  

| Model                                            | VaR Mean | VaR % Mean | VaR Median | VaR Min | VaR Max | VaR Std |
| ------------------------------------------------ | -------- | ---------- | ---------- | ------- | ------- | ------- |
| Normal, Constant drift, Constant volatility      | -0.0355  | 14.82      | -0.0356    | -0.0360 | -0.0349 | 0.0003  |
| Student's t, Constant drift, Constant volatility | -0.0563  | 34.94      | -0.0565    | -0.0590 | -0.0531 | 0.0016  |
| Normal, CAPM, Constant volatility                | -0.0350  | 15.99      | -0.0349    | -0.0364 | -0.0345 | 0.0005  |
| Student's t, CAPM, Constant volatility           | -0.0558  | 33.71      | -0.0558    | -0.0575 | -0.0542 | 0.0010  |
| Normal, Constant drift, GARCH(1,1)               | -0.0354  | 15.13      | -0.0357    | -0.0365 | -0.0340 | 0.0008  |
| Student's t, Constant drift, GARCH(1,1)          | -0.0568  | 36.26      | -0.0573    | -0.0588 | -0.0541 | 0.0016  |
| Normal, CAPM, GARCH(1,1)                         | -0.0352  | 15.59      | -0.0353    | -0.0359 | -0.0344 | 0.0005  |
| Student's t, CAPM, GARCH(1,1)                    | -0.0560  | 34.33      | -0.0559    | -0.0595 | -0.0533 | 0.0019  |
  
Historical ES = -0.0491  

| Model                                            | ES Mean  | ES % Mean | ES Median | ES Min  | ES Max  | ES Std  |
| ------------------------------------------------ | -------- | --------- | --------- | ------- | ------- | ------- |
| Normal, Constant drift, Constant volatility      | -0.0407  | 17.18     | -0.0406   | -0.0412 | -0.0402 | 0.0004  |
| Student's t, Constant drift, Constant volatility | -0.0757  | 54.19     | -0.0766   | -0.0788 | -0.0702 | 0.0030  |
| Normal, CAPM, Constant volatility                | -0.0403  | 17.87     | -0.0403   | -0.0415 | -0.0393 | 0.0007  |
| Student's t, CAPM, Constant volatility           | -0.0768  | 56.53     | -0.0762   | -0.0815 | -0.0738 | 0.0025  |
| Normal, Constant drift, GARCH(1,1)               | -0.0403  | 17.96     | -0.0405   | -0.0419 | -0.0390 | 0.0009  |
| Student's t, Constant drift, GARCH(1,1)          | -0.0765  | 55.83     | -0.0772   | -0.0810 | -0.0721 | 0.0026  |
| Normal, CAPM, GARCH(1,1)                         | -0.0406  | 17.40     | -0.0404   | -0.0416 | -0.0394 | 0.0006  |
| Student's t, CAPM, GARCH(1,1)                    | -0.0759  | 54.58     | -0.0750   | -0.0807 | -0.0726 | 0.0026  |
  
<img width="1200" height="600" alt="Figure_2" src="https://github.com/user-attachments/assets/724c5f94-c410-4670-a160-84687b0eba63" />
(Note: For ease of visual interpretation, VaR and ES are plotted in absolute terms (i.e., reported as positive values), although they represent potential losses.)


## Discussion

The results reveal a clear and somewhat non-trivial pattern in the performance of the different models. For the single-asset case, models based on the Student’s t-distribution consistently produce more accurate estimates of both VaR and ES compared to their normal counterparts. This is particularly evident for Expected Shortfall, where the normal distribution significantly underestimates tail risk. This finding aligns with well-known stylized facts in financial markets, namely that individual asset returns exhibit fat tails and extreme events occur more frequently than predicted by the normal distribution.

However, this pattern reverses in the multi-asset portfolio setting. In contrast to the single-asset results, models based on the Student’s t-distribution systematically overestimate risk, producing VaR and ES values that deviate substantially from historical benchmarks. Instead, models assuming normally distributed returns provide more accurate and stable estimates for the diversified portfolio, although they still exhibit a tendency to underestimate risk to a moderate extent. This difference can be explained by the effect of diversification: when combining multiple assets, idiosyncratic extreme events tend to offset each other, leading to a distribution of portfolio returns that is closer to normal. As a result, heavy-tailed assumptions appropriate at the individual asset level may become overly conservative when applied to an aggregated portfolio, suggesting that extreme tail behavior is largely idiosyncratic and diversifiable, while some degree of tail risk remains even after diversification.

Across both settings, the inclusion of CAPM-based drift and GARCH(1,1) volatility does not lead to consistent improvements in forecasting performance. While these models are theoretically more sophisticated and capture important financial phenomena such as time-varying volatility and systematic risk exposure, their benefits appear limited in the context of unconditional 1-day risk forecasting. In practice, the additional estimation complexity may introduce noise that offsets their theoretical advantages.

The backtesting results for the single asset indicate that all models produce an acceptable number of VaR violations and pass both the Kupiec and Christoffersen tests. In particular, every model produced only 7 violations out of 1000 observations, which is less than 1%. Notably, many models gave identical results in these tests. This reflects the sparsity of extreme events at the 99th percentile over 1000 days: when expected violations are few, different models often identify the same violating days. Testing at the 95th percentile confirms this explanation, producing distinct results across models. These observations highlight that while Kupiec and Christoffersen tests assess statistical adequacy in terms of coverage and independence, they may not sufficiently capture differences in tail magnitude, which are better reflected in the ES metric.

Finally, running multiple simulations enables the computation of summary statistics such as mean, standard deviation, and minimum/maximum values for both VaR and ES. These aggregated metrics provide a more robust picture of model performance than single-run results, mitigating the effects of sampling variability and highlighting differences between models in a statistically meaningful way.
Overall, the findings emphasize that model selection should consider both the aggregation level and the specific risk measure of interest. Heavy-tailed distributions are essential for accurately modeling individual asset risk, while simpler normal-based models may be preferable for diversified portfolios where extreme risks are naturally mitigated. Multi-run summary statistics further enhance the reliability and interpretability of the results, supporting informed decision-making in risk management.

## Model ranking

With that being said, let's rank the models based on their precision. The proposed way to rank the models is according to a simple aggregate error measure which is constructed based on the percentual deviation of model-implied risk measures from their historical counterparts. Specifically, for each model, the absolute percetage deviation of VaR and ES are summed:  

Score = |VaR % error| + |ES % error|  
  
Models are then ranked according to this score, with lower values indicating better overall performance. This approach avoids the need to impose arbitrary weighting schemes on VaR and ES, ensuring that the ranking remains transparent and reproducible.  

However, in practice, greater emphasis is typically placed on Expected Shortfall, as it captures tail risk beyond the VaR threshold and is preferred in regulatory frameworks such as Basel III. However, assigning an exact relative weight between VaR and ES is inherently subjective and difficult to justify empirically. To assess the sensitivity of the results, alternative specifications with higher weight assigned to ES were considered. These adjustments did not materially affect the ranking of models, suggesting that the conclusions are robust to reasonable variations in weighting.  

### Single-asset 

| Rank | Model                                            | VaR % | ES %  | Score |
|------|--------------------------------------------------|-------|-------|-------|
| 1    | Student's t, Constant drift, Constant volatility | 1.68  | 3.49  | 5.17  |
| 2    | Student's t, CAPM, Constant volatility           | 2.67  | 3.27  | 5.94  |
| 3    | Student's t, CAPM, GARCH(1,1)                    | 4.73  | 6.17  | 10.90 |
| 4    | Student's t, Constant drift, GARCH(1,1)          | 5.35  | 5.62  | 10.97 |
| 5    | Normal, CAPM, GARCH(1,1)                         | 7.10  | 22.09 | 29.19 |
| 6    | Normal, Constant drift, GARCH(1,1)               | 7.31  | 22.03 | 29.34 |      
| 7    | Normal, Constant drift, Constant volatility      | 10.54 | 24.21 | 34.75 |
| 8    | Normal, CAPM, Constant volatility                | 10.98 | 24.47 | 35.45 |

### Multi-asset

| Rank | Model                                            | VaR % | ES %  | Score |
|------|--------------------------------------------------|-------|-------|-------|
| 1    | Normal, Constant drift, Constant volatility      | 14.82 | 17.18 | 32.00 |
| 2    | Normal, CAPM, GARCH(1,1)                         | 15.59 | 17.40 | 32.99 |
| 3    | Normal, Constant drift, GARCH(1,1)               | 15.13 | 17.96 | 33.09 |
| 4    | Normal, CAPM, Constant volatility                | 15.99 | 17.87 | 33.86 |
| 5    | Student's t, CAPM, GARCH(1,1)                    | 34.33 | 54.58 | 88.91 |
| 6    | Student's t, Constant drift, Constant volatility | 34.94 | 54.19 | 89.13 |
| 7    | Student's t, CAPM, Constant volatility           | 33.71 | 56.53 | 90.24 |
| 8    | Student's t, Constant drift, GARCH(1,1)          | 36.26 | 55.83 | 92.09 |  

### Side comment
  
However, one thing should be added. In cases where differences in performance are marginal, there is little justification for favoring more complex models. According to the principle of parsimony, simpler models are generally preferable, as they achieve similar predictive accuracy with fewer assumptions, reduced estimation uncertainty and lower computional and implementation effort.

## Outlook

This project focuses on 1-day ahead risk forecasting, but the framework can be naturally extended to multi-day (n-day) VaR and Expected Shortfall.

For models based on constant volatility, such as standard Geometric Brownian Motion with normally distributed returns, multi-day risk measures can be approximated using the square-root-of-time rule, where volatility (and therefore VaR and ES) scales with √n. This approach relies on the assumption of independent and identically distributed returns.

However, this scaling does not apply to GARCH-type models, where volatility evolves over time and depends on past shocks. In such models, returns are heteroskedastic and serially dependent, meaning that future risk cannot be obtained through simple scaling. Instead, multi-day forecasts require iterative simulation or recursive volatility forecasting, which significantly increases computational complexity.
