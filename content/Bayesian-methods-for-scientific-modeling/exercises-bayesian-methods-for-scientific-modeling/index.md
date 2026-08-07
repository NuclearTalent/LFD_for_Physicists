(ch:PartIExercises)=
# Problems for Part I

In this chapter we collect various hands-on problems to build intuition or gain practice in the basics of Bayesian inference. You will further explore PDFs and parameter estimation, and you will get a first exposure to Monte Carlo sampling.

* [](./problem-exploring-PDFs.ipynb) has a series of tasks to play with plots of probability density functions (PDFs) using the scipy.stats and numpy libraries.

* [](./problem-gaussian-mean-and-variance.ipynb) takes a look at a simple parameter-estimation problem, namely estimating the mean and the variance of a normal distribution that is associated with a collection of random variables. The exercise develops a Bayesian approach to this problem and shows how it reduces to standard frequentist estimators for a particular choice of prior.

* [](./problem-radioactive-lighthouse-problem.ipynb) explores a variation on a classic problem from Gull, which entails identifying the location of a hidden radioactive source using a Bayesian approach.

* The goal of [](./problem-amplitude-of-a-signal-in-the-presence-of-background.ipynb) is to estimate the amplitude of a signal when there is background. The notebook considers a limiting case where the background is flat, so it is completely specified by its magnitude, and the signal is known to be a Gaussian with unknown amplitude but (at least initially) known position (mean) and width (standard deviation). This exercise can be considered a first exposure to an experimental design problem.

* [](./problem-fitting-a-straight-line-i.ipynb) is a simple Bayesian parameter estimation example in the context of the familiar problem of fitting a straight line to noisy data.

The final exercises introduce the use of Markov Chain Monte Carlo (MCMC) sampling in basic parameter estimation problems, but in a black-box mode. This first exposure to MCMC is focused on the visualization and interpretation of sampled posteriors, without delving into the details of how the MCMC algorithm that creates them works. Those latter details are explored in {ref}`sec:RootMCMC`, which develops intuition, provides technical details, and introduces diagnostics for troubleshooting and validation.

* [](./problem-gaussian-noise-and-averages-ii.ipynb) revisits the problem considered in [](./problem-gaussian-mean-and-variance.ipynb) but now determines the posterior via MCMC sampling. 

* [](./problem-2d-radioactive-lighthouse-location-using-mcmc.ipynb) revisits [](./problem-radioactive-lighthouse-problem.ipynb) with a more complex goal (identifying the location of the lighthouse in two dimensions) that is carried out using MCMC sampling.

* [](./problem-fitting-a-straight-line-ii.ipynb) extends the straight-line parameter estimation problem by considering marginalizing over nuisance parameters and error propagation while using MCMC sampling.

* {ref}`exercise:GaussianLighthouseCompare` is a brief exercise highlighting the commonality of sampling problems using MCMC.

