---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:Bayesian-optimization)=
# Bayesian optimization


Let us first state an inconvenient fact about optimization:

> Global minimization is almost always intractable. In practice, we have to resort to local minimization:

$  \newcommand{\thetavec}{\boldsymbol{\theta}} $
For $f:\;\mathbf{R}^D \to \mathbf{R}$, with $\thetavec \in \Theta \subset \mathbf{R}^D$ and possibly subject to constraints $c(\thetavec) \leq 0$

Find point(s) $\thetavec_*$ for which

$$
f(\thetavec_*) \leq f(\thetavec),
$$

for all $\thetavec \in \Theta$ *close* to $\thetavec_*$. (Here $\thetavec$ are the parameters of the theoretical model.)

Nevertheless, we will often want to do the best we can toward global minimization.

$  \newcommand{\thetavec}{\boldsymbol{\theta}} $
Consider **expensive** objective functions, e.g.

$$
f(\theta) = \chi^2(\theta) \equiv \sum_{i=1}^N \frac{\left[ y_i^\mathrm{exp} - y_i^\mathrm{th}(\theta) \right]^2}{\sigma_i^2},
$$

where $y_i^\mathrm{th}(\theta)$ may be computationally costly to evaluate.  (The objective function is the function we want to minimize, such as a $\chi^2$ function.)  How shall we proceed?  Here we consider one strategy, Bayesian optimization, which has been used in the optimization of hyperparameters of deep neural networks.  It is not necessarily the best strategy (see comments at the end), but it is an option in our toolkit.

Selected references:
* Paper: [Bayesian optimization in ab initio nuclear physics](https://iopscience.iop.org/article/10.1088/1361-6471/ab2b14) by A. Ekström, C. Forssén et al.,  J. Phys. G: Nucl. Part. Phys. 46, 095101 (2019).
* Book: Jonas Mockus (2012). Bayesian approach to global optimization: theory and applications. Kluwer Academic.



