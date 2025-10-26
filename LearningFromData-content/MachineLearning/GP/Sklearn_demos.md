(sec:SklearnDemos)=
# Scikit-learn demo notebooks

The [Gaussian Process for Machine Learning](https://scikit-learn.org/stable/auto_examples/gaussian_process/index.html) page on the [scikit-learn website](https://scikit-learn.org/stable/index.html) is a great source of code and documentation and examples for GPs.

Here we have adapted their demonstration notebooks for:
* [](./BUQ/plot_gpr_noisy_targets.ipynb). Compares noise-free (interpolation) and noisy (regression) for a one-dimensional function (which can be easily changed). An RBF kernel is the default, but this is exchangeable for any of the standard sklearn kernels. A maximum likelihood fit determines the hyperparameters (so it might fail to find a good solution, but the hyperparameter values are given so this can be diagnosed). 
* [](./BUQ/plot_gpr_prior_posterior.ipynb). This example illustrates the prior and posterior of the Scikit-learn class `GaussianProcessRegressor` with different kernels. Mean, standard deviation, and 5 samples are shown for both prior and posterior distributions.  