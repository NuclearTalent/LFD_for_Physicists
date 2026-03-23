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

(sec:PyMC)=
# Using PyMC

[PyMC](https://www.pymc.io/welcome.html) is a _probabilistic programming library_ for Python. 
Let's quote from the [documentation](https://www.pymc.io/welcome.html): "PyMC strives to make Bayesian modeling as simple and painless as possible, allowing users to focus on their problem rather than the methods." 
The list of features are (taken directly from the documentation page):
* **Modern**: Includes state-of-the-art inference algorithms, including MCMC (NUTS) and variational inference (ADVI).
* **User friendly**: Write your models using friendly Python syntax. [Learn Bayesian modeling](https://www.pymc.io/projects/docs/en/latest/learn.html#) from the many [example notebooks](https://www.pymc.io/projects/examples/en/latest/gallery.html).
* **Fast**: Uses {doc}`PyTensor <pytensor:index>` as its computational backend to compile through C, Numba or JAX, [run your models on the GPU](https://www.pymc-labs.io/blog-posts/pymc-stan-benchmark/), and benefit from complex graph-optimizations.
* **Batteries included**: Includes probability distributions, Gaussian processes, ABC, SMC and much more. It integrates nicely with {doc}`ArviZ <arviz:index>` for visualizations and diagnostics, as well as {doc}`Bambi <bambi:index>` for high-level mixed-effect models.
* **Community focused**: Ask questions on [discourse](https://discourse.pymc.io), join [MeetUp events](https://meetup.com/pymc-online-meetup/), follow us on [Twitter](https://twitter.com/pymc_devs), and start [contributing](https://www.pymc.io/projects/docs/en/latest/contributing/index.html).

In this chapter, we provide a hands-on, active-learning introduction to PyMC.
