---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:bayesian-bias-variance)=
# A Bayesian view of bias and variance

In the previous sections we built up Bayesian linear regression using a normal likelihood {eq}`eq:BayesianLinearRegression:normal_iid_likelihood` and a Gaussian prior {eq}`eq:BayesianLinearRegression:gaussian_iid_prior`. The resulting posterior is also Gaussian {eq}`eq:BayesianLinearRegression:posterior_pars_with_iid_gaussian_prior`, with mean $\tilde{\parsLR}$ and covariance $\tildecovparsLR$. A very broad prior recovers the least-squares optimum $\optparsLR$ as the posterior mode, while an informative prior pulls the parameters towards the prior mean.

In this section we look at what that pull does to *predictions*, and we use it to introduce two issues that will be central when we discuss model validation for Machine learning in Part IV ({numref}`sec:ModelValidation`): a model can be too simple or too flexible for the data at hand, and the two failure modes look very different. The Bayesian and the frequentist descriptions of this differ in one respect that is worth being clear about from the start.

```{admonition} Fixing parameters and varying data, or fixing data and varying parameters
:class: tip
The frequentist analysis of an estimator imagines a fixed, true parameter vector $\parsLR_\mathrm{true}$ and asks how a fitted quantity would scatter if the experiment were repeated with fresh noise, over data sets that were never collected. Bayesian inference does the opposite: it fixes the one data set we actually have and treats $\parsLR$ as the uncertain quantity. Both are legitimate views. They just lead to different questions and different answers, and it is easy to confuse them.
```

## Model complexity: underfitting and overfitting

Consider the polynomial data-generating process from the addendum of {numref}`sec:BayesianLinearRegression`: a cubic function with random coefficients, measured at $N_d=10$ points with noise $\sigmares = 1$. We fit it with polynomials of degree 1, 3 and 9; note that the degree-9 model has $N_p = N_d$ parameters. The figure below demonstrates two different data fitting scenarios.

* *Top row:* ordinary least squares, repeated for five independent noisy data sets from the same data-generating process. Each fit is a single curve, a point estimate; the spread among the five curves shows how much that estimate depends on which data set we happened to get.
* *Bottom row:* Bayesian linear regression with a broad Gaussian prior, $\sigma_{\paraLR}=10$, applied to *one* data set. The result is a distribution over curves, summarised by the posterior predictive mean and its $2\sigma$ band.

```{code-cell} python3
:tags: [hide-input]

import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(seed=35)

# --- data-generating process, as in the addendum of BLR-I ---------------
def data_generating_process_reality(model_type, rng=rng, **kwargs):
    if model_type == 'polynomial':
        true_params = rng.uniform(low=-5.0, high=5, size=(kwargs['poldeg']+1,))
        def process(params, xdata):
            return np.polynomial.polynomial.polyval(xdata, params)
    return process, true_params, model_type

def data_generating_process_measurement(process, params, xdata,
                                        sigma_error=0.5, rng=rng):
    ydata = process(params, xdata)
    error = rng.normal(0, sigma_error, len(xdata)).reshape(-1, 1)
    return ydata + error, sigma_error*np.ones(len(xdata)).reshape(-1,)

reality, true_params, _ = data_generating_process_reality('polynomial', poldeg=3)

Nd = 10; sigma_e = 1.0; sigma_b = 10.0
xmin, xmax = -1, 1
x_meas = np.linspace(xmin, xmax, Nd).reshape(-1, 1)
x_grid = np.linspace(xmin, xmax, 200).reshape(-1, 1)
y_true = reality(true_params, x_grid)

# --- OLS and BLR for a polynomial design matrix ---------------------------
def design(x, poldeg):
    return np.vander(x.ravel(), poldeg+1, increasing=True)

def ols_fit(X, y):
    return np.linalg.lstsq(X, y, rcond=None)[0]

def blr_fit(X, y, sigma_e, sigma_b):
    prec = X.T @ X / sigma_e**2 + np.eye(X.shape[1]) / sigma_b**2
    cov = np.linalg.inv(prec)
    mean = cov @ X.T @ y / sigma_e**2
    return mean, cov

degrees = [1, 3, 9]
n_resample = 5
fig, axes = plt.subplots(2, 3, figsize=(11, 6.2), sharex=True, sharey=True)

# top row: OLS point estimates from several resampled data sets
datasets = [data_generating_process_measurement(reality, true_params, x_meas,
                                                sigma_error=sigma_e)[0]
            for _ in range(n_resample)]
for ax, deg in zip(axes[0], degrees):
    Xg = design(x_grid, deg); Xm = design(x_meas, deg)
    for y in datasets:
        beta = ols_fit(Xm, y)
        ax.plot(x_grid, Xg @ beta, color='C0', lw=1.2, alpha=0.8)
    ax.plot(x_grid, y_true, 'k--', lw=1.5)
    ax.set_title(f'polynomial degree {deg}')

# bottom row: BLR posterior predictive from ONE data set
y_one = datasets[0]
for ax, deg in zip(axes[1], degrees):
    Xg = design(x_grid, deg); Xm = design(x_meas, deg)
    mean, cov = blr_fit(Xm, y_one, sigma_e, sigma_b)
    mu = (Xg @ mean).ravel()
    sd_epi = np.sqrt(np.einsum('ij,jk,ik->i', Xg, cov, Xg))   # parameter uncertainty
    sd_tot = np.sqrt(sd_epi**2 + sigma_e**2)                     # + measurement noise
    ax.fill_between(x_grid.ravel(), mu-2*sd_tot, mu+2*sd_tot, color='C1', alpha=0.15, lw=0)
    ax.fill_between(x_grid.ravel(), mu-2*sd_epi, mu+2*sd_epi, color='C1', alpha=0.45, lw=0)
    ax.plot(x_grid, mu, color='C1', lw=1.5)
    ax.errorbar(x_meas.ravel(), y_one.ravel(), yerr=sigma_e, fmt='o', color='k', ms=4, lw=1)
    ax.plot(x_grid, y_true, 'k--', lw=1.5)

axes[0, 0].set_ylabel('OLS fits,\n5 different data sets')
axes[1, 0].set_ylabel('BLR posterior predictive,\none data set')
for ax in axes[1]:
    ax.set_xlabel('$x$')
axes[0, 0].set_ylim(y_true.min()-3, y_true.max()+3)
fig.tight_layout();
```

The dashed line is the true cubic. In the bottom row the darker band is the $2\sigma$ uncertainty of the model prediction itself (from the posterior of $\parsLR$), the lighter band adds the measurement noise $\sigmares$.

Read the top row first. The straight lines (degree 1) agree closely with each other but are all wrong in the same way: the model is too simple to follow the data, and no amount of resampling will fix that. This is **underfitting**, and the systematic offset is what we will later call **bias**. The degree-9 fits show the opposite problem: each curve passes exactly through its own ten data points, but the curves differ wildly from one another because they are following the noise. This is **overfitting**, and the scatter between fits is what we will call **variance**. The cubic is a compromise: a little scatter, no systematic offset.

Now compare with the bottom row. The Bayesian analysis does not have several data sets to compare; it has one. Yet it displays the same information in a different form. For degree 1 the predictive band is narrow but misses the data: the model is confident and wrong. For degree 9 the band is widest where the OLS curves scatter most, near the edges and between data points, because those are the directions in parameter space that a single data set fails to pin down. Even the broad prior used here has tamed the wiggles that made the OLS fits so erratic, since it penalises large coefficients. What the frequentist reads off from imagined repetitions, the Bayesian reads off from the posterior width.

## What the predictive distribution contains

Recall from {numref}`sec:blr-workflow` that for a new input $\testinput$, with corresponding row $\widetilde{\dmat}$ of basis functions, the posterior predictive distribution {eq}`eq:BayesianLinearRegression:ppd_pdf` is normal,

$$
\pdf{\futuredata}{\data,\sigmares^2,I} = \mathcal{N}\left(
\widetilde{\dmat}\tilde{\parsLR}, \;\;
\sigmares^2 + \widetilde{\dmat}\,\tildecovparsLR\,\widetilde{\dmat}^T
\right).
$$ (eq:BayesianBiasVariance:ppd)

Its variance has two parts. The term $\sigmares^2$ is the noise of a future measurement (the lighter band in the figure); it is irreducible and does not shrink as we collect more data of the same quality. The term $\widetilde{\dmat}\tildecovparsLR\widetilde{\dmat}^T$ is our remaining uncertainty about $\parsLR$ (the darker band); it is a property of our state of knowledge and shrinks with more data. In machine-learning language these are called **aleatoric** and **epistemic** uncertainty. In the frequentist decomposition of Part IV, $\sigmares^2$ reappears as the irreducible noise term, while the variance term is the counterpart of the epistemic part. Bias has no counterpart in the posterior width: a model that is too simple can be confidently wrong, as the degree-1 panel shows.

## The prior as a regulariser

The prior width $\sigma_{\paraLR}$ is what kept the degree-9 model in the bottom row under control. Its effect can be stated in a form that a frequentist would recognise.

````{admonition} BLR with a Gaussian prior is ridge regression
:class: tip
Maximising the posterior {eq}`eq:BayesianLinearRegression:posterior_with_iid_gaussian_prior` is the same as minimising

$$
\left(\data-\dmat\parsLR\right)^T\left(\data-\dmat\parsLR\right) + \lambda\, \parsLR^T\parsLR,
\qquad
\lambda = \frac{\sigmares^2}{\sigma_{\paraLR}^2},
$$ (eq:BayesianBiasVariance:ridge)

which is the cost function of **ridge regression** (or Tikhonov regularization), with solution $\tilde{\parsLR} = (\dmat^T\dmat + \lambda\boldsymbol{1})^{-1}\dmat^T\data$. The regularization strength $\lambda$ that a frequentist would tune by cross-validation is here the ratio of residual variance to prior variance: a penalty otherwise introduced by hand is a statement of prior belief about the size of the parameters.
````

A tight prior ($\lambda$ large) pulls all coefficients towards zero and pushes the model towards underfitting; a broad prior ($\lambda \to 0$) returns the least-squares fit with all its scatter. The trade-off between the two failure modes is not removed by the Bayesian framework. What changes is how the balance point is chosen: rather than a tuning parameter fixed on held-out data, the prior width is a modelling assumption that can be stated, justified and criticised like any other. Another consequence is visible in the figure: since $\tildecovparsLR^{-1} = \covparsLR^{-1} + \sigma_{\paraLR}^{-2}\boldsymbol{1}$ is always invertible, BLR can fit a model with more parameters than data points, while OLS cannot.

## Looking ahead

In {numref}`sec:ModelValidation` we will make the top row of the figure quantitative: bias and variance will be defined as expectation values over repeated data sets, and the expected squared prediction error will be shown to decompose into bias$^2$ + variance + noise. Bayesian linear regression is a good test bed for that theorem, because the posterior mean $\tilde{\parsLR}$ is itself an estimator whose bias and variance can be computed in closed form. Readers who want to see this now can open the block below; everyone else can safely skip it until Part IV.

`````{admonition} Advanced: bias and variance of the posterior mean
:class: dropdown

**The posterior mean as an estimator.** The Bayesian result of {numref}`sec:blr-workflow` is a distribution, not a number. But the posterior mean

$$
\tilde{\parsLR} = \tildecovparsLR \covparsLR^{-1} \optparsLR
\equiv \boldsymbol{S} \optparsLR,
\qquad
\boldsymbol{S} \equiv \tildecovparsLR \covparsLR^{-1}
= \boldsymbol{1} - \frac{\tildecovparsLR}{\sigma_{\paraLR}^2},
$$ (eq:BayesianBiasVariance:shrinkage)

*is* a number (a vector of them), and we are free to ask how it behaves under repeated sampling of $\data$. We call $\boldsymbol{S}$ the **shrinkage matrix**. Its second form follows from $\tildecovparsLR^{-1} = \covparsLR^{-1} + \sigma_{\paraLR}^{-2}\boldsymbol{1}$. As $\sigma_{\paraLR}\to\infty$, $\boldsymbol{S}\to\boldsymbol{1}$ and $\tilde{\parsLR}\to\optparsLR$. The shrinkage is not uniform: a direction the data constrain sharply is barely affected, while a direction the data say little about is pulled strongly towards the prior mean.

Now let the data be generated by the model itself with fixed but unknown $\parsLR_{\rm true}$,

$$
\data = \dmat\parsLR_{\rm true} + \residuals,
\qquad
\residuals \sim \mathcal{N}(\zeros, \sigmares^2\boldsymbol{1}),
$$ (eq:BayesianBiasVariance:truth)

and draw many data sets with $\dmat$ held fixed. The least-squares estimator {eq}`eq:BayesianLinearRegression:OLS_optimum_b` is unbiased with sampling covariance

$$
\expect{\optparsLR} = \parsLR_{\rm true},
\qquad
\var{\optparsLR} = \sigmares^2 \left(\dmat^T\dmat\right)^{-1} = \covparsLR ,
$$ (eq:BayesianBiasVariance:ols_sampling)

so the matrix $\covparsLR$ that entered {eq}`eq:BayesianLinearRegression:likelihood_hessian_b` as the *curvature of the log-likelihood* is also the *sampling covariance of the OLS estimator*. Applying $\boldsymbol{S}$ gives, for the posterior mean,

$$
\expect{\tilde{\parsLR}} = \boldsymbol{S}\,\parsLR_{\rm true},
\qquad
\var{\tilde{\parsLR}} = \boldsymbol{S}\covparsLR\boldsymbol{S}^T = \boldsymbol{S}\,\tildecovparsLR .
$$ (eq:BayesianBiasVariance:blr_sampling)

**Bias and variance of a prediction.** The quantity to get right at a test input is the noise-free value $\widetilde{\dmat}\parsLR_{\rm true}$, and our estimate is $\widetilde{\dmat}\tilde{\parsLR}$. From {eq}`eq:BayesianBiasVariance:blr_sampling` and {eq}`eq:BayesianBiasVariance:shrinkage`,

$$
\text{Bias}(\testinput) &= \widetilde{\dmat}\expect{\tilde{\parsLR}} - \widetilde{\dmat}\parsLR_{\rm true}
= -\frac{1}{\sigma_{\paraLR}^2}\,\widetilde{\dmat}\,\tildecovparsLR\,\parsLR_{\rm true}, \\
\text{Var}(\testinput) &= \widetilde{\dmat}\,\var{\tilde{\parsLR}}\,\widetilde{\dmat}^T
= \widetilde{\dmat}\,\boldsymbol{S}\,\tildecovparsLR\,\widetilde{\dmat}^T .
$$ (eq:BayesianBiasVariance:bias_var)

The bias is proportional to $1/\sigma_{\paraLR}^2$: it is the price of the prior and vanishes only in the uninformative limit. Comparing with a noisy future measurement $\testoutput = \widetilde{\dmat}\parsLR_{\rm true} + \epsilon$ adds one more term,

$$
\expect{\left(\testoutput - \widetilde{\dmat}\tilde{\parsLR}\right)^2}
= \underbrace{\text{Bias}(\testinput)^2 + \text{Var}(\testinput)}_{\text{reducible}}
\;+\; \underbrace{\sigmares^2}_{\text{irreducible}} ,
$$ (eq:BayesianBiasVariance:mse)

which is the decomposition derived in general in {numref}`sec:ModelValidation`. Underfitting is the bias-dominated regime ($\sigma_{\paraLR}$ small, $\boldsymbol{S}\to\zeros$); overfitting is the variance-dominated regime ($\sigma_{\paraLR}$ large, $N_p$ approaching $N_d$ so that $\covparsLR$ has large eigenvalues).

**Scalar illustration.** For a single parameter estimated from $N_d$ repeated measurements ($\dmat^T\dmat = N_d$) everything collapses to scalars,

$$
\covparsLR = \frac{\sigmares^2}{N_d},
\qquad
\tildecovparsLR = \left( \frac{N_d}{\sigmares^2} + \frac{1}{\sigma_{\paraLR}^2} \right)^{-1},
\qquad
S = \frac{N_d/\sigmares^2}{N_d/\sigmares^2 + 1/\sigma_{\paraLR}^2}.
$$ (eq:BayesianBiasVariance:scalar)

The code cell below plots Bias$^2$ and Var against the prior width for $N_d = 20$, $\sigmares = 1$, $\paraLR_{\rm true} = 2$. Bias$^2$+Var has its minimum at $\sigma_{\paraLR}^2 = \paraLR_{\rm true}^2$, exactly where the prior correctly describes the size of the parameter.
`````

```{code-cell} python3
:tags: [hide-input, hide-output]

import numpy as np
import matplotlib.pyplot as plt

sigma_e2 = 1.0      # residual variance
beta_true = 2.0     # true parameter
Nd = 20             # number of data

A = Nd / sigma_e2                     # 1 / Sigma_beta
sigma_b2 = np.logspace(-2, 3, 400)    # prior variance
B = 1.0 / sigma_b2

var_D    = A / (A + B)**2             # sampling variance of the posterior mean
bias2    = (B * beta_true)**2 / (A + B)**2
mse      = bias2 + var_D              # reducible part of the MSE

fig, ax = plt.subplots(figsize=(6, 4.4))
ax.plot(sigma_b2, bias2, lw=2, label=r'Bias$^2$')
ax.plot(sigma_b2, var_D, lw=2, label=r'Var$_\mathcal{D}[\tilde\beta]$ (sampling)')
ax.plot(sigma_b2, mse, 'k-', lw=1.4, label=r'Bias$^2$ + Var$_\mathcal{D}$')
ax.axvline(beta_true**2, color='gray', ls=':', lw=1)
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlabel(r'prior variance $\sigma_\beta^2$')
ax.set_ylabel('contribution to MSE')
ax.set_title('Bias-variance trade-off vs. prior width')
ax.legend(frameon=False, fontsize=8, loc='lower left')
fig.tight_layout();
```
