---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---
# Special case: Gaussian process

{{ sub_extra_tif385_admonition }}

The joint density function for a multivariate normal distribution was presented in Eq. {eq}`eq:Statistics:multivariate-normal-PDF` for $\boldsymbol{x} = (x_1, x_2, \ldots, x_k)$ corresponding to random variables $X_1, X_2, \ldots X_k$. This normal distribution is completely determined by its mean vector, $\boldsymbol{\mu}$, and covariance matrix, $\boldsymbol{\Sigma}$, where elements $\mu_i = \expect{X_i}$ and $\Sigma_{ij} = \cov{X_i}{X_j}$.

The multivariate normal distribution has the remarkable property that all marginal and conditional distributions are normal, and specified by the corresponding subsets of the mean vector and covariance matrix. 

A Gaussian process extends the multivariate normal distribution to a stochastic process with a continuous time index $T$.

```{prf:definition} Gaussian process
:label: definition:gaussian-process

A Gaussian process $(X(t))_{t \geq 0}$ is a stochastic process with a continuous-time index $t \in [0,\infty)$ if each finite-dimensional vector of random variables 

$$
X(t_1), X(t_2), \ldots, X(t_k)
$$ 

has a multivariate distribution for $0 \leq t_1 < \ldots < t_k$.

A Gaussian process is completely determined by its *mean function* $\mu(X(t))$ and *covariance function* $C(X(s), X(t))$ for $s, t \geq 0$.

```  

A Gaussian process is stationary if the mean function $\mu(X(t))$ is constant for all $t$ and if the covariance function fulfils $C(X(s), X(t)) = C(X(s+h), X(t+h))$ with $h \geq 0$. Note that stationarity is not a requirement for a Gaussian process.

