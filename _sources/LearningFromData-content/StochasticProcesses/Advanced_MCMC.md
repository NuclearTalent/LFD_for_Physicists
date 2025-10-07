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

(sec:Advanced_MCMC)=
# Markov Chain Monte Carlo in practice

Here we look at aspects of using MCMC in actual analyses, particularly including MCMC diagnostics.


:::{admonition} Summary points from [arXiv:1710.06068](https://arxiv.org/abs/1710.06068)
* Observations from  ["Data Analysis Recipes: Using Markov Chain Monte Carlo"](https://arxiv.org/abs/1710.06068) by David Hogg and Daniel Foreman-Mackey.
    * Both are computational astrophysicists (or cosmologists or astronomers)
    * DFM wrote `emcee`.
    * Highly experienced in physics scenarios, highly opinionated, but not statisticians (although they interact with statisticians).

* MCMC is good for *sampling*, but not optimizing. If you want to find the modes of distributions, use an optimizer instead.
* For MCMC, you only have to calculate *ratios* of pdfs (as seen from the algorithm).
     * $\Lra$ don't need analytic normalized pdfs
     * $\Lra$ great for sampling posterior pdfs

$$
  p(\thetavec|D) = \frac{1}{Z} p(D|\thetavec)p(\thetavec)
$$     

* Getting $Z$ is really difficult because you need *global* information. (Cf. $Z$ and partition function in statistical mechanics.)

* MCMC is extremely easy to implement, without requiring derivatives or integrals of the function (but see later discussion of HMC).

* Success means a histogram of the samples looks like the pdf.

* Sampling for expectation values works even though we don't know $Z$; we just need the set of $\{\thetavec_k\}$.

$$\begin{align}
  E_{p(\thetavec)}[\thetavec] &\approx \frac{1}{N}\sum_{k=1}^{N}\thetavec_k \\
  E_{p(\thetavec)}[g(\thetavec)] &\approx \frac{1}{N}\sum_{k=1}^{N}g(\thetavec_k)
  \longrightarrow
  \frac{\int d\thetavec\, g(\thetavec)f(\thetavec)}{\int d\thetavec\, f(\thetavec)}
\end{align}$$

$\qquad$ where $f(\thetavec) = Z\, p(\thetavec)$ is unnormalized.

* Nuisance parameters are very easy to marginalize over: just drop that column in every $\theta_k$.

* Autocorrelation is important to monitor and one can tune (e.g., Metropolis step size) to minimize it. More on this later.

* How do you know when to stop? Heuristics and diagnostics to come!
* See the paper for practical advice on initialization and burn-in is given by Hogg and Foreman-Mackey.

**Figures to make every time you run MCMC (following Hogg and Foreman-Mackey sect. 9)**

* Trace plots
    * The burn-in length can be seen; lets you identify problems with model or sampler; qualitative judge of convergence.
    * Use convergence diagnostic such as Gelman-Rubin.

* Corner plots
    * If you have a $D$-dimensional parameter space, plot all $D$ diagonal and all ${D\choose 2}$ joint histograms to show low-level covariances and non-linearities.
    * "... they are remarkable for locating expected and unexpected parameter relationships, and often invaluable for suggesting re-parameterizations and transformation that simplify your problem."

* Posterior predictive plots 
    * Take $K$ random samples from your chain, plot the prediction each sample makes for the data and over-plot the observed data.
    * "This plot gives a qualitative sense of how well the model fits the data and it can identify problems with sampling or convergence."

:::