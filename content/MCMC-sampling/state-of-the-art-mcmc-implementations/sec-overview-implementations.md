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

(sec:overview-implementations)=
# Overview: individual sampling libraries and full probabilistic packages

Here we present an (incomplete) list of state-of-the-art MCMC implementations and packages that are available in Python (and often other languages). Several demo notebooks follow in subsequent sections.

## Individual libraries for MCMC sampling

```{admonition} emcee:
  [emcee](https://emcee.readthedocs.io/en/latest/) {cite}`Foreman_Mackey_2013` is an MIT licensed pure-Python implementation of Goodman & Weare’s [Affine Invariant Markov chain Monte Carlo (MCMC) Ensemble sampler](http://msp.berkeley.edu/camcos/2010/5-1/p04.xhtml) {cite}`Goodman2010`
  ```


```{admonition} pocoMC:
  [pocoMC](https://pocomc.readthedocs.io/en/latest/)
  From the documentation: 
  * `pocoMC` is a Python package for fast Bayesian posterior and model evidence estimation. 
  * It leverages the Preconditioned Monte Carlo (PMC) algorithm, offering significant speed improvements over traditional methods like MCMC and Nested Sampling. 
  * Ideal for large-scale scientific problems with expensive likelihood evaluations, non-linear correlations, and multimodality, pocoMC provides efficient and scalable posterior sampling and model evidence estimation. 
  * Widely used in cosmology and astronomy, `pocoMC` is user-friendly, flexible, and actively maintained."
  ```


```{admonition} zeus:
  [zeus](https://zeus-mcmc.readthedocs.io/en/latest/) is a Python implementation of the Ensemble Slice Sampling method. From the documentation: 
  * Fast & Robust Bayesian Inference,
  * Efficient Markov Chain Monte Carlo (MCMC),
  * Black-box inference, no hand-tuning,
  * Excellent performance in terms of autocorrelation time and convergence rate,
  * Scale to multiple CPUs without any extra effort,
  * Automated Convergence diagnostics. 
  ```


  
```{admonition} PyMultiNest:
  [PyMultiNest](https://johannesbuchner.github.io/PyMultiNest/) interacts with [MultiNest](https://github.com/farhanferoz/MultiNest) {cite}`Feroz2009`, a Nested Sampling Monte Carlo library.
  ```


```{admonition} ptemcee
  [ptemcee](https://github.com/willvousden/ptemcee)
  From the documentation: "`ptemcee`, pronounced "tem-cee", is fork of Daniel Foreman-Mackey's emcee to implement parallel tempering more robustly. As far as possible, it is designed as a drop-in replacement for emcee. If you're trying to characterise awkward, multi-modal probability distributions, then `ptemcee` is your friend.
"
  This repository is archived (frozen) and unmaintained.
  ```

  
## Full packages for inference (including sampling)

```{admonition} PyMC:
  [PyMC](https://docs.pymc.io/) is a Python package for Bayesian statistical modeling and probabilistic machine learning which focuses on advanced Markov chain Monte Carlo and variational fitting algorithms.
  ```
  
```{admonition} PyStan:
  [PyStan](https://pystan.readthedocs.io/en/latest/) provides an interface to [Stan](http://mc-stan.org/), a package for Bayesian inference using the No-U-Turn sampler, a variant of Hamiltonian Monte Carlo.
  ```

```{admonition} Bilby:
  [Bilby](https://bilby-dev.github.io/bilby/) is a Bayesian inference library. From the documentation: "The aim of bilby is to provide a user-friendly interface to perform parameter estimation. It is primarily designed and built for inference of compact binary coalescence events in interferometric data, but it can also be used for more general problems." Bilby provides a common interface to a wide range of samplers, including all of those listed in the first section above.
