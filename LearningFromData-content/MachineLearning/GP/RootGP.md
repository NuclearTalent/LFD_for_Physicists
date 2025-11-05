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

(sec:RootGP)=
# Overview of Gaussian processes

In this chapter we introduce and demonstrate Gaussian processes (GPs).

Good references for GPs are [*Gaussian processes for machine learning*](http://www.gaussianprocess.org/gpml/chapters/) by Rasmussen and William; [*The Kernel Cookbook*](https://www.cs.toronto.edu/~duvenaud/cookbook/) by Duvenaud; Chapter 21 of [*Bayesian Data Analysis, 3rd Edition*](http://www.stat.columbia.edu/~gelman/book/BDA3.pdf) by Gelman et al.; 
and Melendez et al., [Phys. Rev. C **100**, 044001 (2019)](https://journals.aps.org/prc/abstract/10.1103/PhysRevC.100.044001), [arXiv:1904.10581](https://arxiv.org/abs/1904.10581).


The sections here are:
* {ref}`sec:GPIntuition`, which points to several websites with Gaussian process visualizations and tasks to build intuition;
* {ref}`sec:BasicInfoGPs`, which places GPs in the context of stochastic processes and provides a first exposure to the mathematical form of GPs and its use for interpolation and regression;
* {ref}`sec:GaussianProcesses`, which distinguishes parametric and non-parametric inference
* {ref}`sec:SklearnDemos` uses demonstrations with a popular library (scikit-learn); 



    
