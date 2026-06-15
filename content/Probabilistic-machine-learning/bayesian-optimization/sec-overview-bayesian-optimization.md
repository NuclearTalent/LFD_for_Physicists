---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:overview-bayesian-optimization)=
# Overview of Bayesian optimization

> An optimization algorithm for expensive black-box functions

Bayesian optimization provides a strategy for selecting a sequence of function queries.  This is an alternative to a gradient descent method, which relies on derivatives of the function to move toward a nearby local minimum.


This diagram from [Wikimedia Commons](https://creativecommons.org/licenses/by-sa/4.0) illustrates the sequential moves in Newton's method for finding a root, with a sequence of $x$ values: $x_0 \rightarrow x_1 \rightarrow x_2 \rightarrow \ldots$ that approach a nearby zero of the function.
<img width="256" alt="Newton method scheme" src="https://upload.wikimedia.org/wikipedia/commons/b/bb/Newton%E2%80%93Raphson_method.png">
If applied to the derivative of a function, this yields a sequential approximation to a local minimum or maximum. We seek a different way to construct this sequence.

There are two main components in the Bayesian optimization algorithm, which will each be contingent on what we call the data $\mathcal{D}$, which will be the previously evaluated pairs of $\theta$ and $f(\theta)$. 
1. A prior probabilistic pdf $p(f|\mathcal{D})$ for the objective function $f(\theta)$ given some data $\mathcal{D}$. The prior is often a Gaussian process (GP) or a GP emulator. This will be updated with every iteration. The GP acts as a *surrogate* for the actual objective function, which we can evaluate at any given $\theta$, but it is so expensive to do so that we don't know its structure a priori. The idea is that we will do Bayesian updating each iteration after confronting the surrogate model with actual data $f(\theta)$.  So we refine the posterior for $f$, which becomes the prior for the next iteration.
1. An acquisition function $\mathcal{A}(\theta|\mathcal{D})$ given some data $\mathcal{D}$. This is a heuristic that balances *exploration* against *exploitation* and determines where to evaluate the objective function $f(\theta)$ next. Explorative means that you evaluate points in a domain of $\theta$ where the prior pdf for $f$ has large uncertainty.  This enables the escape from local minima in $\theta$.  Exploitive means that you evaluate points in a domain of $\theta$ where the prior pdf for $f$ exhibits low mean values. (This zeroes in on a local minimum.) 

Pseudo-code for BayesOpt:
1. choose initial $\mathbf{\theta}^{(1)},\mathbf{\theta}^{(2)},\ldots \mathbf{\theta}^{(k)}$, where $k \geq 2$
1. evaluate the objective function $f(\mathbf{\theta})$ to obtain $y^{(i)}=f(\mathbf{\theta}^{(i)})$ for $i=1,\ldots,k$
1. initialize a data vector $\mathcal{D}_k = \left\{(\mathbf{\theta}^{(i)},y^{(i)})\right\}_{i=1}^k$
1. select a statistical model for $f(\mathbf{\theta})$ (for us some choice of GP kernel)
1. **for** {$n=k+1,k+2,\ldots$}
   1.    select $\mathbf{\theta}^{(n)}$ by optimizing (maximizing) the acquisition function
   1.    $\mathbf{\theta}^{(n)} = \underset{\mathbf{\theta}}{\text{arg max}}\, \mathcal{A}(\mathbf{\theta}|\mathcal{D}_{n-1})$
   1.    evaluate the objective function to obtain $y^{(n)}=f(\mathbf{\theta}^{(n)})$
   1.    augment the data vector $\mathcal{D}_n = \left\{\mathcal{D}_{n-1} , (\mathbf{\theta}^{(n)},y^{(n)})\right\}$
   1.    update the statistical model for $f(\mathbf{\theta})$
1. **end for**


Some remarks:
* Use a space-filling method such as LHS (Latin hypercube sampling) or Sobol (see references) for the initial $k$ evaluations.
* Use of a gaussian process, or a Gaussian emulator, for the statistical model of $f(\theta)$.
* The choice of aquisition function is the heart of BayesOpt. There are several possible choices; with different balance between exploration-exploitation.
   * Expected improvement
   * Lower confidence bound
* The update of the statistical model is an $\mathcal{O}(n^3)$ cost (if using a GP).
* At each iteration, *all* collected data points are used, thus we build on the full history of the optimization procedure.
* The stopping criterion might be a fixed computational budget that limits the number of function evaluations that can be made.

