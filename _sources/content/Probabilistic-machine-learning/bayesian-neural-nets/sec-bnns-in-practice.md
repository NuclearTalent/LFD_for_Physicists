---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:bnns-in-practice)=
# Bayesian neural networks in practice
How can we compute the marginalization integral for neural networks with thousands of parameters?

In short, there are three different approaches:

1. **Sampling methods**, e.g. MCMC (this approach would be exact as the number of samples $\rightarrow \infty$);
2. **Deterministic approximate methods**, for example using Gaussian approximations with the Laplace method;
3. **Variational methods**.

The first two have been discussed previously in these notes in the general context of Bayesian inference. In the following, we will focus on the variational methods.

<!-- !split -->
## Variational inference for Bayesian neural networks

Bayesian neural networks differ from plain neural networks in that their weights are assigned a probability distribution instead of a single value or point estimate. These probability distributions describe the uncertainty in weights and can be used to estimate uncertainty in predictions. 

Unfortunately, full inference of the weight posterior $p(\boldsymbol{w} \lvert \mathcal{D})$ for neural networks is usually intractable due to the large dimensionality. Instead we can attempt to approximate the true posterior with a proxy distribution $q(\boldsymbol{w} \lvert \boldsymbol{\theta})$ with variational parameters that we want to estimate. 

Training a Bayesian neural network via variational inference implies learning the parameters of the proxy distribution rather than learning the real posterior.


This can be done by minimizing the [Kullback-Leibler divergence](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence) between $q(\boldsymbol{w} \lvert \boldsymbol{\theta})$ and the true posterior $p(\boldsymbol{w} \lvert \mathcal{D})$  w.r.t. $\boldsymbol{\theta}$.

The specific goal is then to replace $p(\boldsymbol{w} \lvert \mathcal{D})$, which we don't know, with the known proxy distribution $q(\boldsymbol{w} \lvert \boldsymbol{\theta}^*)$, where $\boldsymbol{\theta}^*$ is the optimal set of variational parameters. 

<!-- !split -->
### The Kullback-Leibler divergence

The KL divergence is a numeric measure of the difference between two distributions. For two probability distributions $q(\boldsymbol{w})$ and $p(\boldsymbol{w})$, the KL divergence in a continuous case,

$$
 D_\mathrm{KL}(q||p) = \int d \boldsymbol{w} q(\boldsymbol{w}) \log \frac{q(\boldsymbol{w})}{p(\boldsymbol{w})} \equiv \mathbb{E}_{q} \left[ \log \, q(\boldsymbol{w}) - \log \, p(\boldsymbol{w}) \right] 
$$ (eq:KL)

As we can see, the KL divergence corresponds to the expected log difference between two distributions with respect to distribution $q$. It is a non-negative quantity and it is equal to zero only when the two distributions are identical.

Intuitively there are three scenarios:
* if both $q$ and $p$ are high at the same positions, then we are succeeding;
* if $q$ is high where $p$ is low, we pay a price;
* if $q$ is low we don't care about $p$ (because of the expectation).

The divergence measure is not symmetric, i.e., $D_\mathrm{KL}(p||q) \neq D_\mathrm{KL}(q||p)$. In fact, it is possibly more natural to reverse the arguments and compute $D_\mathrm{KL}(p||q)$. However, we choose $\mathrm{KL}(q||p)$ so that we can take expectations with respect to the known $q(\boldsymbol{w})$ distribution. In addition, the minimization of this KL divergence will encourage the fit to concentrate on plausible parameters since

\begin{equation}
D_\mathrm{KL}(q||p) = \int d \boldsymbol{w} q(\boldsymbol{w}\lvert \boldsymbol{\theta}) \log \frac{q(\boldsymbol{w} \lvert \boldsymbol{\theta})}{p(\boldsymbol{w} \lvert \mathcal{D})} 
= -\int d \boldsymbol{w} q(\boldsymbol{w}\lvert \boldsymbol{\theta}) \log \, p(\boldsymbol{w} \lvert \mathcal{D}) + \int d \boldsymbol{w} q(\boldsymbol{w}\lvert \boldsymbol{\theta}) \log \, q(\boldsymbol{w} \lvert \boldsymbol{\theta}).
\end{equation}

To minimize the first term we have to avoid putting probability mass into regions of implausible parameters. To minimize the second term we have to maximize the entropy of the variational distribution $q$ as this term corresponds to its negative entropy.

<!-- !split -->
### Evidence Lower Bound

Let us rewrite the posterior pdf $p(\boldsymbol{w} \lvert \mathcal{D})$ using Bayes theorem

\begin{align*}
D_\mathrm{KL}(q||p) &= \int d \boldsymbol{w} q(\boldsymbol{w}\lvert \boldsymbol{\theta}) \left[ \log \, q(\boldsymbol{w}\lvert \boldsymbol{\theta})  - p( \mathcal{D} \lvert \boldsymbol{w}) - p(\boldsymbol{w}) + p(\mathcal{D}) \right] \\
&= \mathbb{E}_{q} \left[ \log \, q(\boldsymbol{w} \lvert \boldsymbol{\theta}) \right]
- \mathbb{E}_{q} \left[ \log \, p(\mathcal{D} \lvert \boldsymbol{w}) \right]
- \mathbb{E}_{q} \left[ \log \, p(\boldsymbol{w}) \right]
+ \log \, p(\mathcal{D}).
\end{align*}

Note that the logarithm of the last term has no dependence on $\boldsymbol{w}$ and the integration of $q$ will just give one since it should be a properly normalized pdf. This term is then the log marginal likelihood (or model evidence). Furthermore, since the KL divergence on the left hand side is bounded from below by zero we get the **Evidence Lower Bound** (ELBO)

$$
\log \, p(\mathcal{D}) \ge 
- \mathbb{E}_{q} \left[ \log \, q(\boldsymbol{w} \lvert \boldsymbol{\theta}) \right]
+ \mathbb{E}_{q} \left[ \log \, p(\mathcal{D} \lvert \boldsymbol{w}) \right]
+ \mathbb{E}_{q} \left[ \log \, p(\boldsymbol{w}) \right]
\equiv J_\mathrm{ELBO}(\boldsymbol{\theta})
$$ (eq:elbo)

Variational inference was originally inspired by work in statistical physics, and with that analogy, $-J_\mathrm{ELBO}(\boldsymbol{\theta})$ is also called the **variational free energy** and sometimes denoted $\mathcal{F}(\mathcal{D},\boldsymbol{\theta})$.

The task at hand is therefore to find the set of parameters $\boldsymbol{\theta}^*$ that maximizes $J_\mathrm{ELBO}(\boldsymbol{\theta})$. The hardest term to evaluate is obviously the expectation of the log-likelihood

\begin{equation}

\mathbb{E}_{q} \left[ \log \, p(\mathcal{D} \lvert \boldsymbol{w}) \right]
= \sum_{i=1}^N \mathbb{E}_{q} \left[ \log \, p( y^{(i)} \lvert \boldsymbol{x}^{(i)}, \boldsymbol{w}) \right].

\end{equation}

This problem constitutes a new and active area of research in machine learning and it permeates well with the overarching theme of this course. We will end by giving two pointers to further readings on this subject.

<!-- !split -->
## Bayesian neural networks in PyMC3
In the demonstration notebook of this lecture, it is shown how to use Variational Inference in PyMC3 to fit a simple Bayesian Neural Network. That implementation is based on the **Automatic Differentation Variational Inference** (ADVI) approach, described e.g. in [Automatic Variational Inference in Stan](https://arxiv.org/abs/1506.03431) {cite}`Kucukelbir2015`.

<!-- ![<p><em>The training of the Bayesian binary classifier, that employs ADVI implemented in `pymc3`, corresponds to modifying the variational distribution's hyperparameters in order to maximize the Evidence Lower Bound (ELBO).</em></p>](../assets/ADVI-classifier_ELBO.png) -->

```{figure} ../assets/ADVI-classifier_ELBO.png
:name: fig-ADVI-classifier_ELBO

The training of the Bayesian binary classifier, that employs ADVI implemented in pymc3, corresponds to modifying the variational distribution's hyperparameters in order to maximize the Evidence Lower Bound (ELBO).
```

<!-- ![<p><em>The predictions for a Bayesian binary classifier that has been learning using ADVI implemented in `pymc3`. The mean (left panel) and standard deviation (right panel) of the binary classifier's label predictions are shown.</em></p>](../assets/ADVI-classifier.png) -->

```{figure} ../assets/ADVI-classifier.png
:name: fig-ADVI-classifier

The predictions for a Bayesian binary classifier that has been learning using ADVI implemented in `pymc3`. The mean (left panel) and standard deviation (right panel) of the binary classifier's label predictions are shown.
```

See also 
* Kucukelbir, A., Tran, D., Ranganath, R., Gelman, A., and Blei, D. M. (2016). *Automatic Differentiation Variational Inference*. arXiv: [1603.00788](https://arxiv.org/abs/1603.00788).

<!-- !split -->
## Bayes by Backprop

The well-cited paper paper: [Weight Uncertainty in Neural Networks](https://arxiv.org/abs/1505.05424) (*Bayes by Backprop*) {cite}`Blundell2015` has been well described in the [blog entry](http://krasserm.github.io/2019/03/14/bayesian-neural-networks/) by Martin Krasser. The main points of this blog entry are reproduced below with some modifications and some adjustments of notation. 

All three terms in equation {eq}`eq:elbo` are expectations w.r.t. the variational distribution $q(\boldsymbol{w} \lvert \boldsymbol{\theta})$. In this paper they use the variational free energy $\mathcal{F}(\mathcal{D},\boldsymbol{\theta}) \equiv -J_\mathrm{ELBO}(\boldsymbol{\theta})$ as a cost function (since it should be *minimized*). This quantity can be approximated by drawing [Monte Carlo](https://en.wikipedia.org/wiki/Monte_Carlo_method) samples $\boldsymbol{w}^{(i)}$ from $q(\boldsymbol{w} \lvert \boldsymbol{\theta})$.

$$
\mathcal{F}(\mathcal{D},\boldsymbol{\theta}) \approx {1 \over N} \sum_{i=1}^N \left[
\log \, q(\boldsymbol{w}^{(i)} \lvert \boldsymbol{\theta}) -
\log \, p(\boldsymbol{w}^{(i)}) -
\log \, p(\mathcal{D} \lvert \boldsymbol{w}^{(i)})\right]
$$ (eq:VariationalFreeEnergy)

In the example used in the blog post, they use a Gaussian distribution for the variational posterior, parameterized by $\boldsymbol{\theta} = (\boldsymbol{\mu}, \boldsymbol{\sigma})$ where $\boldsymbol{\mu}$ is the mean vector of the distribution and $\boldsymbol{\sigma}$ the standard deviation vector. The elements of $\boldsymbol{\sigma}$ are the elements of a diagonal covariance matrix which means that weights are assumed to be uncorrelated. Instead of parameterizing the neural network with weights $\boldsymbol{w}$ directly, it is parameterized with $\boldsymbol{\mu}$ and $\boldsymbol{\sigma}$ and therefore the number of parameters are doubled compared to a plain neural network.

<!-- !split -->
### Network training

A training iteration consists of a forward-pass and and backward-pass. During a forward pass a single sample is drawn from the variational posterior distribution. It is used to evaluate the approximate cost function defined by equation {eq}`eq:VariationalFreeEnergy`. The first two terms of the cost function are data-independent and can be evaluated layer-wise, the last term is data-dependent and is evaluated at the end of the forward-pass. During a backward-pass, gradients of $\boldsymbol{\mu}$ and $\boldsymbol{\sigma}$ are calculated via backpropagation so that their values can be updated by an optimizer.

Since a forward pass involves a stochastic sampling step we have to apply the so-called *re-parameterization trick* for backpropagation to work. The trick is to sample from a parameter-free distribution and then transform the sampled $\boldsymbol{\epsilon}$ with a deterministic function $t(\boldsymbol{\mu}, \boldsymbol{\sigma}, \boldsymbol{\epsilon})$ for which a gradient can be defined. In the blog post they choose $\boldsymbol{\epsilon}$ to be drawn from a standard normal distribution i.e. $\boldsymbol{\epsilon} \sim \mathcal{N}(\boldsymbol{0}, \boldsymbol{I})$ and the function $t$ is taken to be $t(\boldsymbol{\mu}, \boldsymbol{\sigma}, \boldsymbol{\epsilon}) = \boldsymbol{\mu} + \boldsymbol{\sigma} \odot \boldsymbol{\epsilon}$, i.e., it shifts the sample by mean $\boldsymbol{\mu}$ and scales it with $\boldsymbol{\sigma}$ where $\odot$ is element-wise multiplication.

For numerical stability the network is parametrized with $\boldsymbol{\rho}$ instead of $\boldsymbol{\sigma}$ and $\boldsymbol{\rho}$ is transformed with the softplus function to obtain $\boldsymbol{\sigma} = \log(1 + \exp(\boldsymbol{\rho}))$. This ensures that $\boldsymbol{\sigma}$ is always positive. As prior, a scale mixture of two Gaussians is used $p(\boldsymbol{w}) = \pi \mathcal{N}(\boldsymbol{w} \lvert 0,\sigma_1^2) + (1 - \pi) \mathcal{N}(\boldsymbol{w} \lvert 0,\sigma_2^2)$ where $\sigma_1$, $\sigma_2$ and $\pi$ are shared parameters. Their values are learned during training (which is in contrast to the paper where a fixed prior is used).

See Martin Krasser's [blog entry](http://krasserm.github.io/2019/03/14/bayesian-neural-networks/) for results and further details.

