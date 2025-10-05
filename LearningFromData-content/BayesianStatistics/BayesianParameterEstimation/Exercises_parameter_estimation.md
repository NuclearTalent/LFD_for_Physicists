# Exercises for Part I

In this chapter we collect various exercises to build intuition or gain practice in the basics of Bayesian inference, particularly parameter estimation.

* {ref}`exercise:CheckingSumProduct`. Practice applying the sum and product rules (and their consequences: marginalization, Bayes' theorem, conditional independence) using a simple and intuitive frequentist example. 

* {ref}`exercise:MedicalExample`. Practice on translating English statements into probability notation and then applying the Bayesian rules.

* [](./parameter_estimation_Gaussian_noise.ipynb) takes a look at a simple parameter-estimation problem, namely estimating the mean and the variance of a normal distribution that is associated with a collection of random variables. The exercise develops a Bayesian approach to this problem and shows how it reduces to standard frequentist estimators for a particular choice of prior.

* [](./radioactive_lighthouse_exercise.ipynb) explores a variation on a classic problem from Gull, which entails identifying the location of a hidden radioactive source using a Bayesian approach.

* The goal of [](./amplitude_in_presence_of_background.ipynb) is to estimate the amplitude of a signal when there is background. The notebook considers a limiting case where the background is flat, so it is completely specified by its magnitude, and the signal is known to be a Gaussian with unknown amplitude but (at least initially) known position (mean) and width (standard deviation). This exercise can be considered a first exposure to an experimental design problem.

* [](./parameter_estimation_fitting_straight_line_I.ipynb) is a simple Bayesian parameter estimation example in the context of the familiar problem of fitting a straight line to noisy data.

The final exercises introduce the use of Markov Chain Monte Carlo (MCMC) sampling in basic parameter estimation problems, but in a black-box mode. This first exposure to MCMC is focused on the visualization and interpretation of sampled posteriors, without delving into the details of how the MCMC algorithm that creates them works. Those latter details are explored in {ref}`sec:RootMCMC`, which develops intuition, provides technical details, and introduces diagnostics for troubleshooting and validation.

* [](../../StochasticProcesses/BUQ/parameter_estimation_Gaussian_noise-2.ipynb) revisits the problem considered in [](./parameter_estimation_Gaussian_noise.ipynb) but now determines the posterior via MCMC sampling. 

* [](../../StochasticProcesses/BUQ/Assignment_extending_radioactive_lighthouse.ipynb) revisits [](./radioactive_lighthouse_exercise.ipynb) with a more complex goal (identifying the location of the lighthouse in two dimensions) that is carried out using MCMC sampling.

* [](./parameter_estimation_fitting_straight_line_II.ipynb) extends the straight-line parameter estimation problem by considering marginalizing over nuisance parameters and error propagation while using MCMC sampling.


