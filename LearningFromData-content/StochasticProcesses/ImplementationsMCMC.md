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

(sec:ImplementationsMCMC)=
# State-of-the-art MCMC implementations

Here is an (incomplete) list of state-of-the-art MCMC implementations and packages that are available in Python (and often other languages)

```{admonition} emcee:
  [emcee](https://emcee.readthedocs.io/en/latest/) {cite}`Foreman_Mackey_2013` is an MIT licensed pure-Python implementation of Goodman & Weare’s [Affine Invariant Markov chain Monte Carlo (MCMC) Ensemble sampler](http://msp.berkeley.edu/camcos/2010/5-1/p04.xhtml) {cite}`Goodman2010`
  ```
  
```{admonition} PyMC3:
  [PyMC3](https://docs.pymc.io/) is a Python package for Bayesian statistical modeling and probabilistic machine learning which focuses on advanced Markov chain Monte Carlo and variational fitting algorithms.
  ```
  
```{admonition} PyStan:
  [PyStan](https://pystan.readthedocs.io/en/latest/) provides an interface to [Stan](http://mc-stan.org/), a package for Bayesian inference using the No-U-Turn sampler, a variant of Hamiltonian Monte Carlo.
  ```
  
```{admonition} PyMultiNest:
  [PyMultiNest](https://johannesbuchner.github.io/PyMultiNest/) interacts with [MultiNest](https://github.com/farhanferoz/MultiNest) {cite}`Feroz2009`, a Nested Sampling Monte Carlo library.
  ```
