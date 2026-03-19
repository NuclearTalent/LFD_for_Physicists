# Computing the Bayesian evidence

There are many possible challenges in calculating the evidence, including
* The likelihood may be sharply peaked in the prior range, but could have long tails and significant contributions to the required integrals;
* The likelihood could be multimodal;
* The posterior may only be significant on thin "sheets" in parameter space (cf. visualization of sampling).

Trotta {cite}`Trotta:2008qt` gives a summary of methods (which is somewhat out-of-date in places):
1. Thermodynamic integration $\longrightarrow$ simulated annealing. The computational cost depends heavily on dimensionality of parameter space and on details of likelihood function.
For example, cosmological applications require up to $10^7$ likelihood evaluations (100 times MCMC-based parameter estimation). A solution is to use parallel tempering (more to follow!).
1. Nested sampling recasts multidimensional evidence integral into a one-dimensional integral, which is easy to evaluate numerically.
Generall this takes $\sim 10^5$ likelihood evaluations.
`multinest` and newer versions are more efficient still.
1. Approximations to the Bayes factor:
    * If models are nested: ask whether a new parameter is supported by data.
    * Laplace approximation may be good but be careful of priors.
    * Define the effective number of parameters (see BDA3 {cite}`gelman2013bayesian`)
    * AIC, BIC, DIC, WAIC (summary to follow; see BDA3 for details)
    * The paper ["Practical Bayesian model evaluation using leave-one-out cross-validation and
WAIC"](https://arxiv.org/abs/1507.04544) by Vehtari, Gelman, and Gabry is a good (and reliable) source for theoretical and practical details on assessing and comparing the predictive accuracy of different models. Quote: "Cross-validation and information criteria are two approaches to estimating out-of-sample predictive accuracy using within-sample fits." The computations use the log-likelihood evaluated at posterior simulations of the parameters. 

