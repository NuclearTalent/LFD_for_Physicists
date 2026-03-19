

* Strategies to monitor convergence:
    1. Run multiple chains with distributed starting points.
    1. Compute variation between and within chains $\Lra$ look for mixing and stationarity.
    1. Make sure the acceptance rate for MC steps is not too low or too high.

* 
* Some notes:
    * In BDA-3 Figure 11.1, a) is not converged; b) has 1000 iterations and is possibly converged; c) shows (correlated) draws from the target distribution.
    * We're doing straight-line fitting again using the `emcee` sampling, but now with the Metropolis-Hasting algorithm (more below on the default algorithm). 
    * In `emcee`, we use `moves.GaussianMove(cov)`, which implements a Metropolis step using a Gaussian proposal with mean zero and covariance `cov`. 

            # MH-Sampler setup
            stepsize = .005
            cov = stepsize * np.eye(ndim)
            p0 = np.random.rand(nwalkers,ndim)
            
            # initialize the sampler
            sampler = emcee.EnsembleSampler(nwalkers, ndim, log_posterior, args=[x, y, dy],
            moves=emcee.moves.GaussianMove(cov))

    * The covariance `cov` could be a scalar, as it is here, or a vector or a matrix. See the relevant [emcee manual page](https://emcee.readthedocs.io/en/stable/user/moves/) for further details and more general moves.

    * The `stepsize` parameter is at our disposal to explore the consequences on convergence of it being too large or too small.

    * To get the chains from the above code snippet we use `sampler.chain`, which will give a list with the shape (# walkers, # steps, # dimensions). So 10 walkers taking 2000 steps each for a two-dimensional posterior (that is, $\thetavec$ has two components) has the shape (10, 2000, 2). We can combine the results from all the walkers with `sampler.chain.reshape((-1,ndim))`, which flattens the first two axes of the list. (One reshape dimension can always be $-1$, which infers the value from the length of the array. So here the reshaped array will have two axes with the second one having dimension `ndim`.)

    * How do we know a chain has converged to a representation of the posterior? **Standard error of the mean $SE(\overline\thetavec)$.**
        * This asks how the *mean* of $\thetavec$ deviates in the chain     from the true distribution mean. Thus it is the simulation (or     sampling) error of the mean, not the underlying uncertainty (or spread) of $\thetavec$.


    * Acceptance rate. Usually autotuned in packaged MCMC software.

 

