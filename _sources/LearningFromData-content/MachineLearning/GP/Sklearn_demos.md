(sec:SklearnDemos)=
# Scikit-learn demo notebooks

The [Gaussian Process for Machine Learning](https://scikit-learn.org/stable/auto_examples/gaussian_process/index.html) page on the [scikit-learn website](https://scikit-learn.org/stable/index.html) is a great source of code and documentation and examples for GPs.

Here we have adapted their demonstration notebooks for:
* [](./sklearn/plot_gpr_noisy_targets.ipynb). Compares noise-free (interpolation) and noisy (regression) for a one-dimensional function (which can be easily changed). An RBF kernel is the default, but this is exchangeable for any of the standard sklearn kernels. A maximum likelihood fit determines the hyperparameters (so it might fail to find a good solution, but the hyperparameter values are given so this can be diagnosed). 
* [](./sklearn/plot_gpr_prior_posterior.ipynb). This example illustrates the prior and posterior of the Scikit-learn class `GaussianProcessRegressor` with different kernels. Mean, standard deviation, and 5 samples are shown for both prior and posterior distributions.  

We also have additional demo notebooks 
* [](./sklearn/demo-GaussianProcesses-sklearn.ipynb), which builds an RBF-based kernel (with signal scale and noise term), fits the GP on a subset (e.g., every 3rd point), predicts mean and uncertainty on a target grid or the full input, plots mean ±2σ and data, and computes simple validation metrics.

* [](./sklearn/exercise_GP_sklearn.ipynb), which build RBF kernels with signal variance and length-scale, fit GaussianProcessRegressor with a white-noise term, predict posterior mean and uncertainty, plot mean ±2σ and data, examine setting hyperparameters explicitly vs. optimizing by LML.

* [](./sklearn/Gaussian_processes_exercises_sklearn.ipynb), which build RBF kernels and visualize samples, fit a GP to 1D data (train/test split), plot the posterior mean and ±2σ band, apply the workflow to a small dataset.

