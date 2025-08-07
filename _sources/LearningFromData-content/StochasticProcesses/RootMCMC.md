(sec:RootMCMC)=
# Overview of Part III: Sampling

We have already seem examples of the sampling of PDFs in previous chapters. Here we look in depth at Markov chain Monte Carlo (MCMC), which is the workhorse of sampling methods. We will give an overview of both the theory and practice, considering first the Random Walk Metropolis-Hastings algorithm and then other more efficient samplers.

Chapters in this part:
* {ref}`sec:StochasticProcesses` has a general introduction to random processes plus various examples (e.g., Poisson distribution) to set up for more detailed MCMC background. 
* {ref}`sec:OverviewMCMC` has a detailed introduction to Markov chains and then MCMC, followed by demonstrations.
* {ref}`sec:Advanced_MCMC` looks at convergence tests and other diagnostics.
* {ref}`sec:OtherSamplers` describes Hamiltonian Monte Carlo and other alternatives to Metropolis-Hastings, plus an introduction to PyMC.
