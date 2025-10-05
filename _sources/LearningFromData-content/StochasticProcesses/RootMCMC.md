(sec:RootMCMC)=
# Overview of Part III: Sampling

We have already seem examples of the sampling of PDFs in previous chapters. Here we look in depth at Markov chain Monte Carlo (MCMC), which is the workhorse of sampling methods. We will give an overview of both the theory and practice, considering first the Random Walk Metropolis-Hastings algorithm and then other more efficient samplers.

Chapters in this part:
* {ref}`sec:IntuitionMCMC` gives a general motivation for MCMC, builds intuition through visualizations and analogies to statistical mechanics, introduces the Metropolis-Hastings algorithm, and provides some basic examples, such as an application to Poisson processes.

* {ref}`sec:TechnicalDetailsMCMC` provides formal and detailed discussion on stochastic processes in general, Markov chains, and MCMC.

* {ref}`sec:Advanced_MCMC` looks at MCMC in practice, with convergence tests and other diagnostics.

* {ref}`sec:OtherSamplers` describes Hamiltonian Monte Carlo (HMC) and other alternatives to Metropolis-Hastings in theory and in practice.
