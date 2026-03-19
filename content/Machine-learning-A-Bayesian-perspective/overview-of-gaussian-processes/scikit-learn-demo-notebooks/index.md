(sec:SklearnDemos)=
# Scikit-learn demo notebooks

The [Gaussian Process for Machine Learning](https://scikit-learn.org/stable/auto_examples/gaussian_process/index.html) page on the [scikit-learn website](https://scikit-learn.org/stable/index.html) is a great source of code and documentation and examples for GPs.

Here we have adapted their demonstration notebooks for:
* {ref}`demo:one-dimension-regression-example`. Compares noise-free (interpolation) and noisy (regression) for a one-dimensional function (which can be easily changed). An RBF kernel is the default, but this is exchangeable for any of the standard sklearn kernels. A maximum likelihood fit determines the hyperparameters (so it might fail to find a good solution, but the hyperparameter values are given so this can be diagnosed). 
* {ref}`demo:prior-and-posterior-with-different-kernels`. This example illustrates the prior and posterior of the Scikit-learn class `GaussianProcessRegressor` with different kernels. Mean, standard deviation, and 5 samples are shown for both prior and posterior distributions.  

We also have additional demo notebooks 
* {ref}`demo:gaussian-processes`, which builds an RBF-based kernel (with signal scale and noise term), fits the GP on a subset (e.g., every 3rd point), predicts mean and uncertainty on a target grid or the full input, plots mean ±2σ and data, and computes simple validation metrics.

* {ref}`exercise:gaussian-processes`, which build RBF kernels with signal variance and length-scale, fit GaussianProcessRegressor with a white-noise term, predict posterior mean and uncertainty, plot mean ±2σ and data, examine setting hyperparameters explicitly vs. optimizing by LML.

* {ref}`sec:gaussian-processes-exercises`, which build RBF kernels and visualize samples, fit a GP to 1D data (train/test split), plot the posterior mean and ±2σ band, apply the workflow to a small dataset.

