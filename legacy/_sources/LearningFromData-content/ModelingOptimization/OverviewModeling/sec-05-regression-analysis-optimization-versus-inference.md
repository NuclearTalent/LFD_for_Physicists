# Regression analysis: optimization versus inference

Assuming that we have access to $N_d$ instances of data corresponding to measured responses $\{ \output_1, \output_2, \ldots \output_{N_d} \}$ and the corresponding values for the independent variable $\{ \inputt_1, \inputt_2, \ldots \inputt_{N_d} \}$. Let us define a *cost function* $C(\pars)$ that quantifies how well our model $\model{\pars}{\inputt}$ reproduces the training data,

\begin{equation}
C(\pars) = \sum_{i=1}^{N_d} \frac{(\output_i - \model{\pars}{\inputt_i})^2}{\sigma_i^2},
\end{equation}

where we have introduced some scaling parameters $\{ \sigma_i \}_{i=1}^{N_d}$ to produce 
a dimensionless value. Let us stress that the choice of cost function is by no means unique and we will offer both pragmatic and statistical perspectives on this later on.

The most common approach to regression analysis is to *optimize* the model parameters. The goal is then to find

$$
\pars^* = \mathop{\mathrm{arg} \min}_{\pars\in \mathbb{R}^p} \, C(\pars).
$$ (eq:OverviewModeling:Optimization)

We note that this task is an optimization problem that can become challenging when the model is non-linear and the parameter dimension $p$ is large. We will discuss gradient-descent-based optimization methods in {numref}`sec:MathematicalOptimization`: {ref}`sec:MathematicalOptimization`.

The optimization approach to regression will provide limited information on the model precision. It is also prone to overfitting and other issues of high-dimensional parameter volumes. In the **Bayesian inference** part we will therefore formulate regression as an inductive inference problem, with rigorous handling of uncertainties. See in particular {numref}`sec:BayesianLinearRegression`: {ref}`sec:BayesianLinearRegression`.

