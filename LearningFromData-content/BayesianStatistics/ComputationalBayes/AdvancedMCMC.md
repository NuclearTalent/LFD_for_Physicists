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

```{math}

\newcommand\pos{\boldsymbol{x}}
\newcommand\mom{\boldsymbol{p}}
\newcommand\mass{\mathcal{M}}
```

(sec:AdvancedMCMC)=
# Advanced Markov chain Monte Carlo sampling

```{epigraph}
> "Why walk when you can flow."

-- Richard McElreath
```

MCMC sampling is notoriously difficult to validate. In this chapter we will discuss some common convergence tests. Furthermore, we will consider two very useful sampling methods: Hamiltonian Monte Carlo and Sampling/Importance Resampling. Hamiltonian Monte Carlo is used in [Stan](https://mc-stan.org/), which is a state-of-the-art platform for statistical modeling and high-performance statistical computation. Sampling/Importance Resampling is mot a Markov chain method, but can be very useful for posterior updates and when working with a finite set of samples.

(sec:AdvancedMCMC:Convergence)=
## Convergence tests for MCMC sampling
MCMC sampling can go wrong in (at least) three ways:

1. No convergence---The limiting distribution is not reached.
1. Pseudoconvergence---The chain seems stationary, but the limiting distribution is not reached.
1. Highly correlated samples---Not really wrong, but inefficient.

There is no unique solution to such problems, but they are typically adressed in three ways:

1. Design the simulation runs for monitoring of convergence. In particular, run multiple sequences of the Markov chains with starting points dispersed over the sampling space. This is hard in high dimensions.
1. Monitor the convergence of individual sampling dimensions, as well as predictied quantities of interest, by comparing variations within and between the different sequences. Here you are looking for stationarity (the running means are stable) and mixing (different sequences are sampling the same distribution). The Gelman-Rubin test (see below) is devised for this purpose.
1. Unacceptably inefficient sampling (too low acceptance rate) implies that the algorithm must be adjusted, or that an altogether different sampling algorithm should be used.

The diagnostics that will be discussed below are all univariate. They work perfectly when there is only one parameter to estimate. In fact, most convergence tests are performed with univariate diagnostics applied to each sampling dimension one by one. 

### Variance of the mean
Consider the sampling variance of a parameter mean value

$$
\var{\bar\para} = \frac{\var{\para}}{N},
$$ (eq:AdvancedMCMC:sampling-variance)

where $N$ is the length of the chain. This quantity is capturing the simulation error of the mean rather than the underlying uncertainty of the parameter $\para$. We can visualize this by examining the moving average of our parameter trace. The trace is the sequence as a function of iteration number. 

### Autocorrelation
A challenge when doing MCMC sampling is that the collected samples can be *correlated*. This can be tested by computing the *autocorrelation function* and extracting the correlation time for a chain of samples.

Say that $X$ is an array of $N$ samples numbered by the index $t$. Then $X_{+h}$ is a shifted version of $X$ with elements $X_{t+h}$. The integer $h$ is called the *lag*. Since we have a finite number of samples, the array $X_{+h}$ will be $h$ elements shorter than $X$. 

Furthermore, $\bar{X}$ is the average value of $X$.

We can then define the autocorrelation function $\rho(h)$ from the list of samples. 

$$
\rho(h) = \frac{\sum_{t=0}^{N-h-1} \left[ (X_t - \bar{X}) (X_{t+h} - \bar{X})\right]}
{\sqrt{ \sum_{t=0}^{N-h-1} (X_t - \bar{X})^2 } \sqrt{ \sum_{t=0}^{N-h-1} (X_{t+h} - \bar{X})^2 }}
$$ (eq:AdvancedMCMC:autocorrelation-time)

The summation is carried out over the subset of samples that overlap. The autocorrelation is the overlap (scalar product) of the chain of samples (the trace) with a copy of itself shifted by the lag, as a function of the lag. If the lag is short so that nearby samples are close to each other (and have not moved very far) the product of these two vectors is large. If samples are independent, you will have both positive and negative numbers in the overlap that cancel each other.

The typical example of a highly correlated chain is a random walk with a too short proposal step length. 

It is often observed that $\rho(h)$ is roughly exponential so that we can define an autocorrelation time $\tau_\mathrm{a}$ according to $\rho(h) \sim \exp(-h/\tau_\mathrm{a})$.

The integrated autocorrelation time is

$$
\tau = 1 + 2 \lim_{N \to \infty} \sum_{h=1}^N \rho(h).
$$

With autocorrelated samples, the sampling variance {eq}`eq:AdvancedMCMC:sampling-variance` becomes

$$
\var{\bar\para} = \tau \frac{\var{\para}}{N},
$$ (eq:AdvancedMCMC:sampling-variance-autocorrelated)

with $\tau \gg 1$ for highly correlated samples. This motivates us to define the effective sample size (ESS) as

$$
\text{ESS} = N / \tau.
$$

To keep ESS high, we must collect many samples and keep the autocorrelation time small.

### The Gelman-Rubin test
The Gelman-Rubin diagnostic was constructed to test for stationarity and mixing of different Markov chain sequences {cite}`Gelman:1992`.

```{prf:algorithm} The Gelman-Rubin diagnostic
:label: algorithm:AdvancedMCMC:gelman-rubin

1. Collect $M>1$ sequences (chains) of length $2N$.
2. Discard the first $N$ draws of each sequence, leaving the last $N$ iterations in the chain.
3. Calculate the within and between chain variance.
   - Within chain variance:
   
     $$
     W = \frac{1}{M}\sum_{j=1}^M s_j^2 
     $$
     
     where $s_j^2$ is the variance of each chain (after throwing out the first $N$ draws).
   - Between chain variance:
   
     $$
     B = \frac{N}{M-1} \sum_{j=1}^M (\bar{\para} - \bar{\bar{\para}})^2
     $$
    
    where $\bar{\bar{\para}}$ is the mean of each of the M means.
4. Calculate the estimated variance of $\theta$ as the weighted sum of between and within chain variance.

$$
\widehat{\var{\para}} = \left ( 1 - \frac{1}{N}\right ) W + \frac{1}{N}B
$$

5. Calculate the potential scale reduction factor.

$$
\hat{R} = \sqrt{\frac{\widehat{\var{\para}}}{W}}
$$

```

We want the $\hat{R}$ number to be close to 1 since this would indicate that the between chain variance is small.  And a small chain variance means that both chains are mixing around the stationary distribution.  Gelman and Rubin {cite}`Gelman:1992` showed that stationarity has certainly not been achieved when $\hat{R}$ is greater than 1.1 or 1.2.

(sec:AdvancedMCMC:HMC)=
## Hamiltonian Monte Carlo

The Hamiltonian Monte Carlo Method (HMC) is a Metropolis method that uses gradient information to reduce the random-walk behavior and to collect effectively independent samples. It was introduced in lattice QCD by Duane et al. {cite}`Duane:1987de`and was originally named Hybrid Monte Carlo as they were combining molecular dynamics with the Metropolis MCMC algorithm. A very good and detailed review of HMC is written by Radford Neal and is contained in the Handbook of Markov Chain Monte Carlo {cite}`brooks2011handbook`.

In HMC, the state space $\pos$ is augmented by a conjugate momentum $\mom$. Note that $\pos$ will be the model parameters $\pars$ in our applications but here we will stick to $\pos,\mom$ to make the connection with Hamiltonian dynamics explicit. Let us define a *Hamiltonian*

$$
H(\pos,\mom) = K(\mom) + U(\pos),
$$ (eq:AdvancedMCMC:hamiltonian)

where the kinetic energy function $K(\mom)$ is a design choice while the potential energy function $U(\pos)$ will be defined as minus the log probability of the density that we wish to sample

$$
\begin{aligned}
  K(\mom) &= \frac{1}{2} \mom^T \mass^{-1} \mom, \\
  U(\pos) &= -\ln\left( \p{\pos} \right),
\end{aligned}
$$ (eq:AdvancedMCMC:kinetic-potential)

where $\mass$ is a user-defined mass matrix (positive definite and symmetric) and where we use $\p{\pos}$ to denote the PDF that we want to sample. It could for example be a posterior distribution for some model parameters. 

We can link $H(\pos,\mom)$ to a probability distribution for $(\pos,\mom)$ using the canonical Boltzmann distribution

\begin{equation}
\p{\pos,\mom} = \frac{1}{Z} \exp\left( \frac{-H(\pos,\mom)}{T}\right),
\end{equation}

where $Z$ is the normalization and $T$ is a temperature (here serving to render the exponents dimensionless). Let us set $T=1$ and use the expressions {eq}`eq:AdvancedMCMC:kinetic-potential` to obtain the separable joint distribution

$$
\p{\pos,\mom} \propto \p{\pos} \exp \left( \frac{\mom^T \mass^{-1} \mom}{2} \right).
$$ (eq:AdvancedMCMC:joint-distribution)

Since we will use the Metropolis ratio during sampling, the normalization factor becomes irrelevant. The joint distribution is a produce of two (independent) distributions, the one for $\mom$ becomes a Gaussian with our design choices and the one for $\pos$ is the one that we are seeking. If we manage to efficiently sample from $\p{\pos,\mom}$ then we can just ignore the $\mom$ samples and  we will be left with samples from $\p{\pos}$.

How do we sample from $\p{\pos,\mom}$? Well, naturally we simulate Hamiltonian dynamics for a finite period of time. For Metropolis updates, using a proposal found by Hamiltonian dynamics, the acceptance probability will be one since $H$ is kept invariant. Unfortunately, we will only be able to solve Hamilton's equations approximately and in practice we might not end up with perfect energy conservation.

Apart from energy conservation, two additional key properties of Hamiltonian dynamics---in the context of using it for MCMC sampling---are that it is time reversibile and that it preserves the volume in $(\pos,\mom)$-space (a result known as Liouville's theorem).

Hamilton's equations are

$$
\begin{aligned}
\frac{d x_i}{d t} &= \frac{\partial H}{\partial p_i} = \left( \mass^{-1}\mom\right)_i\\
\frac{d p_i}{d t} &= -\frac{\partial H}{\partial x_i} = \frac{\partial \ln(\p{\pos})}{\partial x_i}.
\end{aligned}
$$ (eq:AdvancedMCMC:hamiltons-equations)

Every HMC iteration begins with a sample of the momentum $\mom$ and continues with the integration of Hamilton's equations for some total time $t$ before the final Metropolis update and the (likely) acceptance of the new position.

In order to maintain energy conservation it is important to simulate the Hamiltonian dynamics using a short time step and to perform the integration such that the accumulation of numerical errors is avoided. The standard method in HMC is known as leapfrog integration and is a symplectic integrator where the discretization error for each time step is equally likely to be positive and negative, thus helping to preserve the total energy throughout the simulation. Leapfrog integration works as an update of the momentum with half a time step, followed by a full step for the position (using the new values for the momentum variables), and finally another half time step for the momentum using the newly updated position variables.

```{prf:algorithm} The Hamiltonian Monte Carlo method
:label: algorithm:AdvancedMCMC:HMC
HMC can be used to sample from continuous distributions pn $\mathbb{R}^d$ for which both the density and the partial derivatives of the log of the density can be evaluated.
1. In the first step, new values for the momentum variables $\mom$ are randomly drawn from their Gaussian distribution (independently of the current values of the position variables). The result is a state $(\pos_i,\mom_i)$.
2. In the second step, a Metropolis update is performed, simulating Hamiltonian dynamics to propose a new state. 
   - Starting at the current state $(\pos_i,\mom_i)$, Hamilton's equations are integrated for $L$ timesteps of length $\varepsilon$ using the leapfrog method (or some other reversible method that preserves volume). 
   - The momentum variable at the end of this $L$-step trajectory are then negated, giving a proposed state $(\pos^*_i,\mom^*_i)$. The negation is is needed to make the Metropolis proposal symmetric, but does not matter in practice since $K(-\mom) = K(\mom)$ and the momentum will be replaced before it is used again.
   - The proposed state is accepted as the new state $(\pos_{i+1},\mom_{i+1})$ with probability
   
     $$
     \min\left( 1, -\exp(-H(\pos^*_i,\mom^*_i)) +H\exp(-H(\pos_i,\mom_i)) \right).
     $$
     
     Otherwise, the new state is a copy of the current state. 
```


For succesful application of HMC there are three hyperparameters that need to be tuned by the user:

1. The mass matrix $\mass$;
2. The integration timestep $\varepsilon$;
3. The number of timesteps $L$.

The MontePython implementation of HMC, by Isak Svensson, was published in Ref. {cite}`Svensson:2021lzs` and is publicly available at: https://github.com/svisak/montepython.git

More advanced versions, such as the No-U-Turn Samplers (NUTS) {cite}`hoffman2014no`, are also available and aims to simplify the process of tuning the hyperparameters.

(sec:AdvancedMCMC:SIR)=
## Sampling / Importance Resampling

```{note}
This chapter is reproduced (with some adjustments) from *Bayesian probability updates using sampling/importance resampling: Applications in nuclear theory* by Weiguang Jiang and Christian Forssén in Front. in Phys., 10:1058809, 2022 {cite}`Jiang:2022off` (with permission).
```

The use of MCMC in the statistical analysis of complex computer models typically requires massive computations. There are certainly situations where MCMC sampling is not ideal, or even becomes infeasible:

1. When the posterior is conditioned on some calibration data for which the model evaluations are very costly. Then a limited number of full likelihood evaluations can be afforded and the MCMC sampling becomes less likely to converge.
1. Bayesian posterior updates in which calibration data is added in several different stages. This typically requires that the MCMC sampling must be carried out repeatedly from scratch.
1. Model checking where the sensitivity to prior assignments is being explored. This is a second example of posterior updating.
1. The prediction of target observables for which model evaluations become very costly and the handling of a large number of MCMC samples becomes infeasible.

These are situations where one might want to use the Sampling/Importance Resampling (S/IR) method {cite}`Smith:1992aa,Bernardo:2006`, which can exploit the previous results of model evaluations to allow posterior probability updates at a much smaller computational cost compared to the full MCMC method. 

### Brief review of the method
The basic idea of S/IR is to utilize the inherent duality between samples and the density (probability distribution) from which they were generated {cite}`Smith:1992aa`. This duality offers an opportunity to indirectly recreate a density (that might be hard to compute) from samples that are easy to obtain. 

Let us consider a target density $h(\pars)$. This could be a posterior PDF $\pdf{\pars}{\data, I}$. Instead of attempting to directly collect samples from $h(\pars)$, as would be the goal in MCMC approaches, the S/IR method uses a detour. We first obtain samples from a simple (even analytic) density $g(\pars)$. We then resample from this finite set using a resampling algorithm to approximately recreate samples from the target density $h(\pars)$. There are (at least) two different resampling methods. In this paper we only focus on one of them called weighted bootstrap (more details of resampling methods can be found in Refs. {cite}`Rubin:1988, Smith:1992aa`).

Assuming we are interested in the target density $h(\pars)=f(\pars)\,/\int\! f(\pars)\,\mathrm{d}\pars$, the procedure of resampling via weighted bootstrap can be summarized as follows:

```{prf:algorithm} The Sampling/Importance Resampling method
:label: algorithm:AdvancedMCMC:SIR

1. Generate the set $\{ \pars_i\}_{i=1}^n$ of samples from a sampling density $g(\pars)$.
1. Calculate $\omega_i=f(\pars_i)\,/\,g(\pars_i)$ for the $n$ samples and define importance weights as: $q_i=\omega_i~/\sum_{j=1}^n \omega_j$.
1. Draw $N$ new samples $\{ \optpars_i\}_{i=1}^N$ from the discrete distribution $\{ \pars_i \}_{i=1}^n$ with probability mass $q_i$ on $\pars_i$.
1. The set of samples $\{ \optpars_i \}_{i=1}^N $ will then be approximately distributed according to the target density $h(\pars)$.
```

Intuitively, the distribution of $\optpars$ should be good approximation of $h(\pars)$ when $n$ is large enough. Here we justify this claim via the cumulative distribution function of $\optpara$ (for the one-dimensional case)

$$
\begin{aligned}
\rm{pr}(\optpara\leq a) &= \sum\limits_{i=1}^n q_i \cdot H(a-\para_i) 
= \frac{ \frac{1}{n}\sum\limits_{i=1}^n \omega_i \cdot H(a-\para_i)}{ \frac{1}{n}\sum\limits_{i=1}^n \omega_i} \\
& \xrightarrow[n \rightarrow \infty]{} \frac{\mathbb{E}_g\left[ \frac{f(\para)}{g(\para)} \cdot H(a-\para) \right]}{\mathbb{E}_g\left[\frac{f(\para)}{g(\para)}\right]}
= \frac{\int^{a}_{-\infty}f(\para)\,d\para}{\int^{\infty}_{-\infty}f(\para)\,d\para}= \int^{a}_{-\infty}h(\para)\,d\para ,
\end{aligned} 
$$ (eq:AdvancedMCMC:cdf)

with $\mathbb{E}_g[X(\para)]=\int^{\infty}_{-\infty} X(\para) g(\para)\,d\para$ the expectation value of $X(\para)$ with respect to $g(\para)$, and $H$ Heaviside step function such that

$$
   H(a-\para) = \begin{cases}
      1 & \text{if}\ \para \leq a, \\
      0 & \text{if}\ \para > a .
\end{cases}
$$ (eq:AdvancedMCMC:Heaviside)

The above resampling method can be applied to generate samples from the posterior PDF $h(\pars)=\rm{pr}(\pars|\mathcal{D})$ in a Bayesian analysis. It remains to choose a sampling distribution, $g(\pars)$, which in principle could be any continuous density distribution. However, recall that $h(\pars)$ can be expressed in terms of an unnormalized distribution $f(\pars)$, and using Bayes' theorem we can set $f(\pars)=\mathcal{L}(\pars)\pdf{\pars}{I}$. Thus, choosing the prior $\pdf{\pars}{I}$ as the sampling distribution $g(\pars)$ we find that the importance weights are expressed in terms of the likelihood, $q_i = \mathcal{L}(\pars_i)/ \sum_{j=1}^n \mathcal{L}(\pars_j)$. Assuming that it is simple to collect samples from the prior, the costly operation will be the evaluation of $\mathcal{L}(\pars_i)$. Here we make the side remark that an effective and computationally cost-saving approximation can be made if we manage to perform a pre-screening to identify (and ignore) samples that will give a very small importance weight. We also note that the above choice of $g(\pars)=\rm{pr}(\pars)$ is purely for simplicity and one can perform importance resampling with any $g(\pars)$.

````{prf:example} Illustration of S/IR
Let us follow the above procedure in a simple example of S/IR to illustrate how to get samples from a posterior distribution. We consider a two-dimensional parametric model with $\pars = (\para_1$, $\para_2)$. Given data $\mathcal{D}$ obtained under the model we have:

$$
  \pdf{\para_1,\para_2}{\data} = \frac{ \mathcal{L}(\para_1,\para_2)\pdf{\para_1,\para_2}{I}}{\iint \mathcal{L}(\para_1,\para_2) \pdf{\para_1,\para_2}{I} \, d\para_1 d\para_2}.
$$ (eq:AdvancedMCMC:example_1)

For simplicity and illustration, the joint prior distribution for $\para_1$, $\para_2$ is set to be uniform over the unit square as shown in {numref}`fig:AdvancedMCMC:SIR`a. In this example we also assume that the data $\data$ likelihood is described by a multivariate Student-t distribution 

$$
  \mathcal{L}(\para_1,\para_2) = 
\frac{\Gamma[(\nu+p)/2]}{\Gamma(\nu/2)\nu^{p/2}\pi^{p/2}|\boldsymbol{\Sigma}|^{1/2}}\left[ {1+\frac{1}{\nu}(\pars-\boldsymbol{\mu})^{T}\boldsymbol{\Sigma}^{-1}(\pars-\boldsymbol{\mu})} \right]^{-(\mu+p)/2},
$$ (eq:AdvancedMCMC:student-t)

where the dimension $p=2$, the degrees of freedom $\nu=2$, the mean vector $\boldsymbol{\mu} = (0.2, 0.5)$ and the scale matrix $\boldsymbol\Sigma=[[0.02, 0.005], [0.005, 0.02]]$.

The importance weights $q_i$ are then computed for $n=2000$ samples drawn from the prior (these prior samples are shown in {numref}`fig:AdvancedMCMC:SIR`a). The resulting histogram of importance weights is shown in {numref}`fig:AdvancedMCMC:SIR`b. Here the weights have been rescaled as $\tilde{q}_i=q_i/\max(\{ q \})$ such that the sample with the largest probability mass corresponds to 1 in the histogram. We also define the effective number of samples, $n_\mathrm{eff}$, as the sum of rescaled importance weights, $n_\mathrm{eff} = \sum_{i=1}^n \tilde{q}_i$. Finally, in {numref}`fig:AdvancedMCMC:SIR`c we show $N=20,000$ new samples $\{ \optpars_i \}_{i=1}^N$ that are drawn from the prior samples $\{ \pars_i\}_{i=1}^n$ according to the probability mass $q_i$ for each $\pars_i$. The blue and green contour lines represent (68\% and 90\%) credible regions for the resampled distribution and for the Student-t distribution, respectively. This result demonstrates that the samples generated by the S/IR method give a very good approximation of the target posterior distribution. 

```{figure} ./figs/SIR_corner_plot.png
---
width: 800px
name: fig:AdvancedMCMC:SIR
---
Illustration of S/IR procedures. **a**. Samples $\{ \pars\}_{i=1}^n$ from a uniform prior in a unit square ($n=2000$ samples are shown). **b**. Histogram of rescaled importance weights $\tilde{q}_i=q_i/\max(\{q\})$ where $q_i= \mathcal{L}(\pars_i)/ \sum_{j=1}^n \mathcal{L}(\pars_j)$ with $\mathcal{L}(\pars)$ as in Eq. {eq}`eq:AdvancedMCMC:student-t`. The number of effective samples is $n_\mathrm{eff}=214.6$. Note that the samples are drawn from a unit square and that the tail of the target distribution is not covered. **c**. Samples $\{ \optpars\}_{i=1}^N$ of the posterior (blue dots with 10\% opacity) resampled from the prior samples with probability mass $q_i$. The contour lines for the $68\%$ and $90\%$ credible regions of the posterior samples (blue dashed) are shown and compared with those of the exact bivariate target distribution (green solid). Summary histograms of the marginal distributions for $\para_1$ and $\para_2$ are shown in the top and right subplots.
```

````

### S/IR limitations
While the S/IR approach might provide a useful alternative to full MCMC sampling, there are some important limitations. In particular, users should be mindful of the effective number of samples. The more complex the likelihood function, the less effective is the use of a sampling distribution.

Unfortunately one can also envision more difficult scenarios in which S/IR could fail without any clear signatures. For example, if the prior has a very small overlap with the posterior there is a risk that many prior samples get a similar importance weight (such that the number of effective samples is large) but that one has missed the most interesting region. Prior knowledge of the posterior landscape is very useful to avoid possible failure scenarios that might not be signaled by the number of effective samples.
