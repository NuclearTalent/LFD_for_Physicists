(sec:RootMCMC)=
# Overview of Part III: Sampling

```{epigraph}
> "Any one who considers arithmetical methods of producing random digits is, of course, in a state of sin."

-- John von Neumann (1951)
```

We have already seem examples of the sampling of PDFs in previous chapters. Here we look in depth at Markov chain Monte Carlo (MCMC), which is the workhorse of sampling methods. We will give an overview of both the theory and practice, considering first the Random Walk Metropolis-Hastings algorithm and then other more efficient samplers.

Chapters in this part:
* {ref}`sec:intuition-for-mcmc` gives a general motivation for MCMC sampling, builds intuition through visualizations and analogies to statistical mechanics, introduces the Metropolis-Hastings algorithm, and provides some basic examples, such as an application to Poisson processes.

* {ref}`sec:details-of-mcmc` provides formal and detailed discussion on stochastic processes in general, Markov chains, and Metropolis-Hastings MCMC.

* {ref}`sec:mcmc-in-practice` looks at MCMC in practice, with convergence tests and other diagnostics.

* {ref}`sec:advanced-sampling-algorithms` introduces a handful of useful and more advanced sampling algorithms such as Hamiltonian Monte Carlo (HMC), ensamble and slice sampling, parallel tempering, importance resampling, and nested sampling.

* {ref}`sec:state-of-the-art-mcmc-implementations` provides several demo notebooks for selected state-of-the-art implementations of advanced sampling algorithms.