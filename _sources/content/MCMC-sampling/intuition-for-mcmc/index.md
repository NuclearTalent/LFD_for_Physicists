(sec:intuition-for-mcmc)=
# Intuition for MCMC

Intuition for Markov Chain Monte Carlo (MCMC) includes:

* {ref}`sec:WhyMCMC`, which identifies problems in Bayesian inference where MCMC is useful or necessary; addresses multi-dimensional integration in general and then using Monte Carlo specfically; discusses sampling from a PDF; and provides a lead-in to MCMC.
* {ref}`sec:BasicStructureMCMC`, lays out the Metropolis-Hastings algorithm; provides intuition for detailed balance and why the MH algorithm satisfies the conditions; and provides a visual demonstration that a possibly non-intuitive feature of MH, namely repeating configurations in the MC chain when a proposal is rejected, is actually essential.
* {ref}`sec:VisualizingMCMC` points to online javascript simulations that are invaluable for building intuition about how MCMC works (here for MH but later for Hamiltonian MC) and highlights some of the features from the simulations.
* {ref}`demo:mh-sampling-of-poisson` provides a full MH MCMC example to play with, prompted by a series of question.
* {ref}`demo:random-walk-and-sampling` is another example to build intuition about MH sampling; autocorrelation is introduced.

There will be lead-ins in various places in this chapter to more details presented in the subsequent chapters.