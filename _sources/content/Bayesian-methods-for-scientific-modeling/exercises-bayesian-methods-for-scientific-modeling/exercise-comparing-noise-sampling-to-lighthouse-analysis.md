(exercise:GaussianLighthouseCompare)=
# Compare Gaussian noise sampling to lighthouse analysis

Here we observe that Gaussian noise sampling is carried out just like the radioactive lighthouse analysis from exercise notebook {ref}`problem:radioactive-lighthouse-problem` (which we assume you have worked through). 
Jump to the Bayesian approach in the exercise notebook {ref}`problem:gaussian-noise-and-averages-ii`.
The goal is to sample a posterior $p(\pars|D,I)$

$$
         p(\mu,\sigma | D, I) \leftrightarrow p(x_0,y_0|X,I)
$$

where $D$ on the left are the $x$ points and $D=X$ on the right are the $\{x_k\}$ where scintillation flashes are detected.

What do we need? From Bayes' theorem, we need 

$$\begin{align}
      \text{likelihood:}& \quad p(D|\mu,\sigma,I) \leftrightarrow p(D|x_0,y_0,I) \\
      \text{prior:}& \quad p(\mu,\sigma|I) \leftrightarrow p(x_0,y_0|I)
\end{align}$$

You are generalizing the functions for log PDFs and the plotting of posteriors that are in {ref}`problem:radioactive-lighthouse-problem`.
Note the functions for log-prior and log-likelihood in {ref}`problem:gaussian-noise-and-averages-ii`. Here $\pars = [\mu,\sigma]$ is a vector of parameters; cf.  $\pars = [x_0,y_0]$.

Let's step through the essential set up for `emcee`.
 * It is best to create an environment that will include `emcee` and `corner`. 
   :::{hint} Nothing in the `emcee` sampling part needs to change!
   ::: 
 * Basically we are doing 50 random walks in parallel to explore the posterior. Where the walkers end up will define our samples of $\mu,\sigma$
   $\Longrightarrow$ the histogram *is* an approximation to the (unnormalized) joint posterior.
 * Plotting is also the same, once you change labels and `mu_true`, `sigma_true` to `x0_true`, `y0_true`. (And skip the `maxlike` part.)

Maximum likelihood here is the frequentist estimate $\longrightarrow$ this is an optimization problem. And you can read off marginalized estimates for $\mu$ and $\sigma$.
::::{admonition} Question
Are $\mu$ and $\sigma$ correlated or uncorrelated?
:::{admonition} Answer
:class: dropdown 
They are *uncorrelated* because the contour ellipses in the joint posterior have their major and minor axes parallel to the $\mu$ and $\sigma$ axes. Note that the fact that they look like circles is just an accident of the ranges chosen for the axes; if you changed the $\sigma$ axis range by a factor of two, the circle would become flattened.
:::
::::

Bottom line: the two analyses are completely analogous.


