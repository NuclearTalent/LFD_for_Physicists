---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:blr-workflow)=
# BLR-II: Workflow

In following the four-step workflow for Bayesian inference (see {numref}`sec:Intro:Workflow`), we need to
1. Identify the observable and unobservable quantities and formulate appropriately informative priors before new data is used.
2. Set up a full statistical model relating the physics model and data, including all errors. We need to consistently build in our knowledge of the underlying physics and of the data measurement process. 
3. Calculate and interpret the relevant posterior distributions.  This is the conditional probability distribution of the unobserved quantities of interest, given the observed data.
4. Do model checking: assess the fit of the model and the reasonableness of the conclusions, testing the sensitivity to model assumptions in steps 1 and 2. From this assessment we modify the model appropriately and repeat all four steps. 


To carry out this workflow for BLR, 
we note that our goal is to relate data $\data$ to the output of a linear model expressed in terms of its design matrix $\dmat$ and its model parameters $\parsLR$ by $M = \dmat \parsLR$.
We consider the special case of one dependent response variable ($\output$) and a single independent variable ($\inputt$), for which the data set ($\data$) and the residual vector ($\residuals$) are both $N_d \times 1$ column vectors with $N_d$ the length of the data set. The design matrix ($\dmat$) has dimension $N_d \times N_p$ and the parameter vector ($\parsLR$) is $N_p \times 1$.

For the residuals, consider a statistical model that describes the mismatch between our model and observations as in Eq. {eq}`eq:BayesianLinearRegression:eq_StatModel` (recall that we assume here that $\delta M = 0$). Knowledge (and/or assumptions) concerning measurement uncertainties, or modeling errors, then allows to describe the residuals as a vector of random variables that are distributed according to a PDF


\begin{equation}
  \residuals \sim \pdf{\residuals}{I},
\end{equation}

where we introduce the relation $\sim$ to indicate how a (random) variable is *distributed*. 
A very common assumption is that errors are normally distributed with zero mean. As before we let $N_d$ denote the number of data points in the (column) vector $\data$. Introducing the $N_d \times N_d$ covariance matrix $\covres$ for the errors we then have the explicit distribution

$$
\pdf{\residuals}{\covres, I} = \mathcal{N}(\zeros,\covres).
$$ (eq:BayesianLinearRegression:ResidualErrors)

Recall that the notation for the multivariate normal distribution $\mathcal{N}$ here is that the mean is $\zeros$ and the covariance matrix is $\covres$.

To carry out step 2. we adapt Bayes' theorem to the current problem

$$
\pdf{\pars}{\data,I} = \frac{\pdf{\data}{\pars,I}\pdf{\pars}{I}}{\pdf{\data}{I}}
  \quad\longrightarrow\quad
  \pdf{\parsLR}{\data, \covres, I} = \frac{\pdf{\data}{\parsLR,\covres,I}\pdf{\parsLR}{I}}{\pdf{\data}{I}} ,
$$ (eq:BayesianLinearRegression:eq_bayes)

which is the conditioned probability of the quantities of interest, namely the model parameters, on the observed measurements with known covariance for the measurement errors. 
In most realistic data analyses we will then have to resort to numerical evaluation or sampling of the posterior. However, certain combinations of likelihoods and priors facilitate analytical derivation of the posterior. In this chapter we will explore one such situation and also demonstrate how we can recover the results from an ordinary least squares approach with certain assumptions. A slightly more general approach involves so called **conjugate priors**. This class of probability distributions have clever functional relationships with corresponding likelihood distributions that facilitate analytical derivation. 

To evaluate this posterior we must have expressions for both factors in the numerator on the right-hand side (following the Bayesian research workflow in {numref}`sec:BayesianWorkflow`): the prior $\pdf{\parsLR}{I}$ and the likelihood $\pdf{\data}{\parsLR,\covres,I}$. Note that the prior does not depend on the data or the error model. The denominator $\pdf{\data}{I}$, sometimes known as the evidence, becomes irrelevant for the task of parameter estimation since it does not depend on $\parsLR$. It is typically quite challenging, if not impossible, to evaluate the evidence for a multivariate inference problem except for some very special cases. In this chapter we will only be dealing with analytically tractable problems and will therefore (in principle) be able to evaluate also the evidence.

::::{admonition} Checkpoint question
:class: my-checkpoint
Why is it possible to perform parameter estimation without computing the evidence? 
:::{admonition} Hint
:class: dropdown, my-hint
In Bayes theorem, the posterior is normalized. Verify this by integrating both sides over the parameters. 
For parameter estimation, do you need the posterior to be normalized (e.g., do you need more than the shape and location of the posterior density)?
:::
::::

::::{admonition} Checkpoint question
:class: my-checkpoint
Can you think of why it is so challenging to compute the evidence? 
:::{admonition} Hint
:class: dropdown, my-hint 
To evaluate the evidence, you need to introduce an integral over all possible values of
$\pars$. Why might this integral harder to do than the likelihood or prior evaluation?
:::
::::


<!--
The Bayesian research workflow in {numref}`sec:BayesianWorkflow` breaks the steps leading to {eq}`eq:BayesianLinearRegression:eq_bayes` 

Having such a statistical model for the errors makes it possible to derive an expression for the data likelihood $\pdf{\data}{\parsLR,\covres,I}$ (see below). Using Bayes' theorem {eq}`eq:BayesTheorem:bayes-theorem-for-data` we can then "invert" this conditional probability distribution and write the parameter posterior
-->


<!--
## Bayes' theorem for the normal linear model
-->


## The prior

First we assign a prior probability $\pdf{\parsLR}{I}$ for the model parameters. In order to facilitate analytical expressions we will explore two options: (i) a very broad, uniform prior, and (ii) a Gaussian prior. For simplicity, we consider both these priors to have zero mean and with all model parameters being i.i.d. 

As discussed earlier, we rarely want to use a truly uniform prior, preferring a wide beta  or Gaussian distribution instead. 
We will assume that the width is large enough that it will be effectively flat where our Bayesian linear regression likelihood is not negligible.
Then for the analytic calculations here we can take the uniform prior for the $N_p$ parameters to be

$$
\pdf{\parsLR}{I} = \frac{1}{(\Delta\paraLR)^{N_p}} \left\{ 
\begin{array}{ll}
1 & \text{if all } \paraLR_i \in [-\Delta\paraLR/2, +\Delta\paraLR/2] \\
0 & \text{else},
\end{array}
\right.
$$ (eq:BayesianLinearRegression:uniform_iid_prior)

with $\Delta\paraLR$ the width of the prior range in all parameter directions (this assumes we have standardized the data so that it has roughly the same extent in all directions). 

The Gaussian prior that we will also be exploring is

$$
\pdf{\parsLR}{I} = \left(\frac{1}{2\pi\sigma_\paraLR^2}\right)^{N_p/2} \exp\left[ -\frac{1}{2}\frac{\parsLR^T\parsLR}{\sigma_\paraLR^2} \right],
$$ (eq:BayesianLinearRegression:gaussian_iid_prior)

with $\sigma_\paraLR$ the standard deviation of the prior for all parameters.

::::{admonition} Checkpoint question
:class: my-checkpoint
Are these priors normalized?
:::{admonition} Hint-1
:class: dropdown, my-hint 
Integrate both sides over $\parsLR$ to check normalization, remembering that $\parsLR$ is a vector, so this is a multidimensional integral.
:::
:::{admonition} Hint-2
:class: dropdown, my-hint 
Both normalization integrals in this case can be *factorized* into the product of one-dimensional integrals. This is true here for the Gaussian prior because the covariance matrix is taken to be diagonal.
:::
:::{admonition} Answer
:class: dropdown, my-answer
Yes, they are normalized.
:::
::::


::::{admonition} Checkpoint question
:class: my-checkpoint
In what limit are the uniform and Gaussian priors (as defined here) effectively equivalent?
:::{admonition} Answer
:class: dropdown, my-answer
The limit where $\Delta\paraLR/2$ and $\sigma_\paraLR$ are both so large that the priors are effectively flat where the likelihood is not negligible.
:::
::::



::::{admonition} Checkpoint question
:class: my-checkpoint
What is implied (i.e., what are you assuming) if you use a truly uniform prior for model parameters?
:::{admonition} Hint
:class: dropdown, my-hint 
Is it possible that the parameters could be arbitrarily large?
:::
:::{admonition} Answer
:class: dropdown, my-answer
It is implied that not only is any magnitude possible for the model parameters, but all values for a given parameter are equally likely. This is very unlikely to be true.
:::
::::




## The likelihood

Assuming normally distributed residuals, as we have done, it turns out to be straightforward to express the data likelihood. In the following we will make the further assumption that errors are *independent*. This implies that the covariance matrix $\covres$ is diagonal and given by a vector $\sigmas$,

$$
\covres &= \mathrm{diag}(\sigmas^2), \, \text{where} \\ 
\sigmas^2 &= \left( \sigma_0^2, \sigma_1^2, \ldots, \sigma_{N_d-1}^2\right),
$$ (eq:BayesianLinearRegression:independent_errors)

and $\sigmai^2$ is the variance for residual $\residual_i$. 

Let's first consider a single datum $\data_i$ and the corresponding model prediction $M_i = \left( \dmat \parsLR \right)_i$. We are interested in the likelihood for this single data point

\begin{equation}
\pdf{\data_i}{\parsLR,\sigmai^2,I}.
\end{equation}

Since the relation between data and residual is a simple additive transformation $\data_i = \modeloutput_i + \residual_i$,
we can use the standard probability rules to obtain (alternatively we can apply the recipe for changing variables *(add reference)*) 

$$
\begin{align}
\pdf{\data_i}{\parsLR,\sigmai^2,I} &= \int d\residual_i\, \pdf{\data_i, \residual_i}{\parsLR,\sigmai^2,I} \\
  &= \int d\residual_i\, \pdf{\data_i}{\residual_i, \parsLR, I}\, \pdf{\residual_i}{\sigmai^2} \\
  &= \int d\residual_i\, \delta\bigl(\data_i - (\modeloutput_i + \residual_i)\bigr)
     \frac{1}{\sqrt{2\pi}\sigmai} e^{-\residual_i^2/2\sigmai^2} \\
&= \frac{1}{\sqrt{2\pi}\sigmai} \exp \left[ -\frac{(\data_i - \modeloutput_i)^2}{2\sigmai^2} \right]
\end{align}
$$ (eq:BayesianLinearRegression:likelihood_eq_1)

where we used that $\residual_i \sim \mathcal{N}(0,\sigmai^2)$. Note that the parameter dependence sits in $\modeloutput_i \equiv \modeloutput(\parsLR, \inputs_i)$.

::::{admonition} Checkpoint question
:class: my-checkpoint
Fill in the details for the steps in {eq}`eq:BayesianLinearRegression:likelihood_eq_1`.
:::{admonition} Hint
:class: dropdown, my-hint 
Review the probability rules in {numref}`Chapter %s <ch:Inferenceandpdfs>`. The first step integrates in $\residual_i$.
:::
:::{admonition} Answer
:class: dropdown, my-answer
1. Apply the sum rule to integrate in $\residual_i$.
1. Apply the product rule, taking into account that $\residual_i$ depends only on $\sigmai$.
1. Use $\data_i = \modeloutput_i + \residual_i$ to evaluate the first pdf; it is a $\delta$ function because $\data_i$ is exactly specified given $\modeloutput_i \equiv \modeloutput(\parsLR, \inputs_i)$ and $\epsilon_i$.
1. Evaluate the integral using the $\delta$ function and $\delta\bigl(\data_i - (\modeloutput_i + \residual_i)\bigr) = \delta\bigl(\epsilon_i - (\data_i - \modeloutput_i)\bigr)$.
:::
::::







Furthermore, since we assume that the residuals are independent we find that the total likelihood becomes a product of the individual ones for each element of $\data$:

$$
\pdf{\data}{\parsLR,\sigmas^2,I} &= \prod_{i=0}^{N_d-1} \pdf{\data_i}{\parsLR,\sigmai^2,I} \\
&= \left(\frac{1}{2\pi}\right)^{N_d/2} \frac{1}{\left| \covres \right|^{1/2}} \exp\left[ -\frac{1}{2} (\data - \dmat \parsLR)^T \covres^{-1} (\data - \dmat \parsLR) \right],
$$ (eq:BayesianLinearRegression:normal_likelihood)

where we note that the diagonal form of $\covres$ implies that $\left| \covres \right|^{1/2} = \prod_{i=0}^{N_d-1} \sigmai$ and that the exponent becomes a sum of squared and weighted residual terms

$$
-\frac{1}{2} (\data - \dmat \parsLR)^T \covres^{-1} (\data - \dmat \parsLR) = -\frac{1}{2} \sum_{i=0}^{N_d - 1} \frac{(\data_i - (\dmat \parsLR)_i)^2}{\sigma_i^2}.
$$ (eq:BayesianLinearRegression:LR_likelihood_exponent)

In the special case that all residuals are both *independent and identically distributed* (i.i.d.) we have that all variances are the same, $\sigmai^2 = \sigmares^2$, and the full covariance matrix is completely specified by a single parameter $\sigmares^2$. For this special case, the likelihood becomes

$$
\pdf{\data}{\parsLR,\sigmares^2,I} = \left(\frac{1}{2\pi\sigmares^2}\right)^{N_d/2} \exp\left[ -\frac{1}{2\sigmares^2} \sum_{i=0}^{N_d - 1} (\data_i - (\dmat \parsLR)_i)^2 \right].
$$ (eq:BayesianLinearRegression:normal_iid_likelihood)

```{caution} 
For computational performance it is always better (if possible) to write sums, such as the one in the exponent of {eq}`eq:BayesianLinearRegression:normal_iid_likelihood`, in the form of vector-matrix operations rather than as for-loops. This particular sum should therefore be implemented as $(\data - \dmat \parsLR)^T (\data - \dmat \parsLR)$ to employ powerful optimization for vectorized operations in existing numerical libraries (such as [`numpy`](https://numpy.org/) in `python` and [`gsl`](https://www.gnu.org/software/gsl/), [`mkl`](https://www.intel.com/content/www/us/en/developer/tools/oneapi/onemkl.html) for C and other compiled programming languages).
```

```{admonition} Two views on the likelihood
Since observed data is generated stochastically, through an underlying $\text{``data-generating process''}$, it is appropriately described by a probabibility distribution. This is the $\text{``data likelihood''}$ that describes the probability distribution for observed data given a specific data-generating process (as indicated by the information on the right-hand side of the conditional). 

- View 1: Assuming fixed values of $\parsLR$; what are long-term frequencies of future data observations as described by the likelihood? 
- View 2: Focusing on the data $\data_\mathrm{obs}$ that we have; how does the likelihood for this data set depend on the values of the model parameters?

This second view is the one that we will be adopting when allowing model parameters to be associated with probability distributions. The likelihood still describes the probability for observing a set of data, but we emphasize its parameter dependence by writing

\begin{equation}
\pdf{\data}{\parsLR,\sigma^2,I} = \mathcal{L}(\parsLR).
\end{equation}

This function is **not** a probability distribution for model parameters. The parameter posterior, left-hand side of Eq. {eq}`eq:BayesianLinearRegression:eq_bayes`, regains status as a probability density for $\parsLR$ since the likelihood is multiplied with the prior $\pdf{\parsLR}{I}$ and normalized by the evidence $\pdf{\data}{I}$.
```



## The posterior

Given the likelihood with i.i.d. errors {eq}`eq:BayesianLinearRegression:normal_iid_likelihood` and the two alternative priors, {eq}`eq:BayesianLinearRegression:uniform_iid_prior` and {eq}`eq:BayesianLinearRegression:gaussian_iid_prior`, we will derive the corresponding two different expressions for the posterior (up to multiplicative normalization constants). 

### Rewriting the likelihood

First, let us rewrite the likelihood in a way that is made possible by the fact that we are considering a linear model. In particular, this implies quadratic dependence on model parameters in the exponent, which means one can show (by performing a Taylor expansion of the log likelihood around the mode) that the likelihood becomes proportional to the functional form of a multivariate normal distribution for the model parameters:

$$
\pdf{\data}{\parsLR,\sigmares^2,I} = \pdf{\data}{\optparsLR,\sigmares^2,I} \exp\left[ -\frac{1}{2} (\parsLR-\optparsLR)^T \covparsLR^{-1} (\parsLR-\optparsLR) \right].
$$ (eq:BayesianLinearRegression:likelihood_pars_b)

Note that this expression still describes a probability distribution for the data. The data dependence sits in the amplitude of the mode, $\pdf{\data}{\optparsLR,\sigmares^2,I}$, and its position, $\optparsLR = \optparsLR(\data) = \left(\dmat^T\dmat\right)^{-1}\dmat^T\data$. The latter is the solution {eq}`eq:BayesianLinearRegression:OLS_optimum_b` of the normal equation when the covariance matrix is proportional to the identity: $\covres = \mathrm{diag}(\sigmares^2)$. Furthermore, the statistical model for the errors in this case enter in the covariance matrix,

$$
\covparsLR^{-1} = \frac{\dmat^T\dmat}{\sigmares^2},
$$ (eq:BayesianLinearRegression:likelihood_hessian_b)

which can be understood as the curvature (Hessian) of the negative log-likelihood.

````{exercise} Prove the Gaussian likelihood
:label: exercise:BayesianLinearRegression:likelihood_pars_b

Prove Eq. {eq}`eq:BayesianLinearRegression:likelihood_pars_b`. 

```{admonition} Hints
:class: toggle, my-exercise-hint

1. Identify $\optparsLR$ as the position of the mode of the likelihood by inspecting the negative log-likelihood $L(\parsLR)$ and comparing with the derivation of the normal equation.
2. Taylor expand $L(\parsLR)$ around $\optparsLR$. For this you need to argue (or show) that the gradient vector $\nabla_{\parsLR} L(\parsLR) = 0$ at $\pars=\optparsLR$, and show that the Hessian $\boldsymbol{H}$ (with elements $H_{ij} = \frac{\partial^2 L}{\partial\paraLR_i\partial\paraLR_j}$) is a constant matrix $\boldsymbol{H} = \frac{\dmat^T\dmat}{\sigmares^2}$.
3. Compare with the Taylor expansion of a normal distribution $\mathcal{N}\left( \parsLR \vert \optparsLR, \covparsLR \right)$.
```
````

::::{exercise} Generalized normal equation
:label: exercise:BayesianLinearRegression:GeneralizedNormalEquation
Prove for the case of the general exponent in Eq. {eq}`eq:BayesianLinearRegression:normal_likelihood` that the position of the mode $\optparsLR$ is given by

$$
   \optparsLR(\data) = \bigl[\dmat^T \covres^{-1} \dmat\bigr]^{-1} \bigl[\dmat^T \covres^{-1} \data\bigr] 
$$

::::

::::{admonition} Checkpoint question
:class: my-checkpoint
  Why can't I say 
 $ \bigl[\dmat^T \covres^{-1} \dmat\bigr]^{-1} \bigl[\dmat^T \covres^{-1} \data\bigr]
   = \dmat^{-1} \covres (\dmat^T)^{-1} \dmat^T \covres^{-1} \data = \dmat^{-1}\data$?
:::{admonition} Answer
:class: dropdown, my-answer
Because these are not square, invertible matrices, so those operations don't hold.
:::
::::



### Posterior with a uniform prior

Let us first consider a uniform prior as expressed in Eq. {eq}`eq:BayesianLinearRegression:uniform_iid_prior`. The prior can be considered very broad if its boundaries $\pm \Delta\para/2$ are very far from the mode of the likelihood {eq}`eq:BayesianLinearRegression:likelihood_pars_b`. "Distance" in this context is measured in terms of standard deviations. A "far distance", therefore, implies that $\pdf{\data}{\parsLR,\sigmares^2,I}$ is very close to zero. This implies that the posterior

\begin{equation}
\pdf{\parsLR}{\data,\sigmares^2,I} \propto \pdf{\data}{\parsLR,\sigmares^2,I} \pdf{\parsLR}{I},
\end{equation}

simply becomes proportional to the data likelihood (with the prior just truncating the distribution at very large distances). Thus we find from Eq. {eq}`eq:BayesianLinearRegression:likelihood_pars_b`

$$
\pdf{\parsLR}{\data,\sigmares^2,I} \propto \exp\left[ -\frac{1}{2} (\parsLR-\optparsLR)^T \covparsLR^{-1} (\parsLR-\optparsLR) \right],
$$ (eq:BayesianLinearRegression:posterior_with_iid_uniform_prior)

if all $\paraLR_i \in [-\Delta\paraLR/2, +\Delta\paraLR/2]$ while it is zero elsewhere. The mode of this distribution is obviously the mean vector $\optparsLR = \optparsLR(\data)$. We can therefore say that we have recovered the ordinary least-squares result. At this stage, however, the interpretation is that this parameter optimum corresponds to the maximum of the posterior PDF {eq}`eq:BayesianLinearRegression:posterior_with_iid_uniform_prior`. Such an optimum is sometimes known as the maximum a posteriori, or MAP.

::::{admonition} Checkpoint question
:class: my-checkpoint
Why is it obvious that the mode of $\pdf{\parsLR}{\data,\sigmares^2,I}$ is the mean vector $\optparsLR$?
:::{admonition} Answer
:class: dropdown, my-answer
The argument of the exponent is negative semi-definite, so the mode (maximum value) of the distribution is when the exponent is equal to zero, which is when $\parsLR = \optparsLR$.
:::
::::


```{admonition} Discuss
In light of the results of this section, what assumption(s) are implicit in linear regression while they are made explicit in Bayesian linear regression?
```


### Posterior with a Gaussian prior

Assigning instead a Gaussian prior for the model parameters, as expressed in Eq. {eq}`eq:BayesianLinearRegression:gaussian_iid_prior`, we find that the posterior is proportional to the product of two exponential functions

$$
\pdf{\parsLR}{\data,\sigmares^2,I} &\propto \exp\left[ -\frac{1}{2} (\parsLR-\optparsLR)^T \covparsLR^{-1} (\parsLR-\optparsLR) \right] \exp\left[ -\frac{1}{2}\frac{\parsLR^T\parsLR}{\sigma_{\paraLR}^2} \right] \\
&\propto \exp\left[ -\frac{1}{2} (\parsLR-\tilde{\parsLR})^T \tildecovparsLR^{-1} (\parsLR-\tilde{\parsLR}) \right].
$$ (eq:BayesianLinearRegression:posterior_with_iid_gaussian_prior)

The second proportionality is a consequence of both exponents being quadratic in the model parameters, and therefore that the full expression looks like the product of two Gaussians. This product is proportional to another Gaussian distribution which has mean vector and (inverse) covariance matrix given by

$$
\tilde{\parsLR} &= \tildecovparsLR \covparsLR^{-1} \optparsLR \\
\tildecovparsLR^{-1} &= \covparsLR^{-1} + \sigma_{\paraLR}^{-2} \boldsymbol{1} 
$$ (eq:BayesianLinearRegression:posterior_pars_with_iid_gaussian_prior)

where $\boldsymbol{1}$ is the $N_p \times N_p$ unit matrix. In effect, what has happend is that the prior normal distribution becomes updated to a posterior normal distribution via an inference process that involves a data likelihood. In this particular case, learning from data implies that the mode changes from $\parsLR$ to $\tilde{\parsLR}$ and the covariance from a diagonal structure with $\sigma_{\paraLR}^2$ in all directions to the covariance matrix $\tildecovparsLR$.

```{admonition} Checkpoint question
:class: my-checkpoint
What happens if the data is of high quality (i.e., the likelihood $\mathcal{L}(\parsLR)$ is sharply peaked around $\optparsLR$), and what happens if it is of poor quality (providing a very broad likelihood distribution)?
```

### Marginal posterior distributions

Given a multivariate probability distribution we are often interested in lower dimensional marginal distributions. Consider for example $\parsLR^T = [\parsLR_1^T, \parsLR_2^T$], that is partitioned into dimensions $D_1$ and $D_2$. The marginal distribution for $\parsLR_2$ corresponds to the integral

$$
\p{\parsLR_2} = \int d\parsLR_1 \p{\parsLR}.
$$


```{admonition} Transformation property of multivariate normal distributions
Let $\mathbf{Y}$ be a multivariate normal-distributed random variable of length $N_p$ with mean vector $\boldsymbol{\mu}$ and covariance matrix $\boldsymbol{\Sigma}$. We use the notation $\psub{\mathbf{Y}}{\mathbf{y}} = \mathcal{N} (\mathbf{y} | \mathbf{\mu}, \mathbf{\Sigma})$ to emphasize which variable is normally distributed.

Consider now a general $N_p \times N_p$ matrix $\boldsymbol{A}$ and $N_p \times 1$ vector $\boldsymbol{b}$. Then, the random variable $\mathbf{Z} = \boldsymbol{A} \mathbf{Y} + \boldsymbol{b}$ is also multivariate normal-distributed with the PDF

$$
\psub{\mathbf{Z}}{\mathbf{z}} = \mathcal{N} (\mathbf{z} \vert \mathbf{A}\boldsymbol{\mu} + \boldsymbol{b},\boldsymbol{A}\boldsymbol{\Sigma}\boldsymbol{A}^T).
$$ (eq:BayesianLinearRegression:transformed-normal)
```

For multivariate normal distributions we can employ a useful transformation property, shown in Eq. {eq}`eq:BayesianLinearRegression:transformed-normal`. Considering the posterior {eq}`eq:BayesianLinearRegression:posterior_with_iid_gaussian_prior` we partition the parameters $\parsLR^T = [\parsLR_1^T, \parsLR_2^T$] and the mean vector and covariance matrix into $\boldsymbol{\mu}^T = [\boldsymbol{\mu}_1^T,\boldsymbol{\mu}_2^T]$ and

$$
\boldsymbol{\Sigma} = \left[
    \begin{array}{cc}
        \boldsymbol{\Sigma}_{11} & \boldsymbol{\Sigma}_{12} \\	
        \boldsymbol{\Sigma}_{12}^T & \boldsymbol{\Sigma}_{22}
    \end{array}
\right].
$$

We can obtain the marginal distribution for $\parsLR_2$ by setting

$$
\mathbf{A} = \left[
    \begin{array}{cc}
        0 & 0 \\
        0 & \mathbf{1}_{D_2\times D_2}
    \end{array}
\right], \,\, \mathbf{b} = 0,
$$

which yields 

$$
\pdf{\parsLR_2}{\data, I} = 
\mathcal{N}(\parsLR_2|\boldsymbol{\mu}_2,\boldsymbol{\Sigma}_{22}).
$$ (eq_marginal_N)


(sec:ppd)=
## The posterior predictive

One can also derive the posterior predictive distribution (PPD), i.e., the probability distribution for predictions $\widetilde{\boldsymbol{\mathcal{F}}}$ given the model $M$ and a set of new inputs for the independent variable $\boldsymbol{x}$. The new inputs give rise to a new design matrix $\widetilde{\dmat}$.

We obtain the posterior predictive distribution by marginalizing over the uncertain model parameters that we just inferred from the given data $\data$.

$$
\pdf{\widetilde{\boldsymbol{\mathcal{F}}}}{\data}
\propto \int \pdf{\widetilde{\boldsymbol{\mathcal{F}}}}{\parsLR,\sigmares^2,I}  \pdf{\parsLR}{\data,\sigmares^2,I}\, d\parsLR,
$$ (eq:BayesianLinearRegression:ppd_pdf)

where both distributions in the integrand can be expressed as Gaussians. Alternatively, one can express the PPD as the set of model predictions with the model parameters distributed according to the posterior parameter PDF

$$
\left\{ \widetilde{\dmat} \parsLR \, : \, \parsLR \sim \pdf{\parsLR}{\data,\sigmares^2,I} \right\}.
$$ (eq:BayesianLinearRegression:ppd_pdf_set)

This set of predictions can be obtained if we have access to a set of samples from the parameter posterior.

::::{admonition} Checkpoint question
:class: my-checkpoint
Fill in the details to obtain the right side of {eq}`eq:BayesianLinearRegression:ppd_pdf`.
:::{admonition} Answer
:class: dropdown, my-answer
Introduce the integration over $\parsLR$ using the sum rule and then obtain the right side from the product rule. 
:::
::::


## Solutions to selected exercises


```{solution} exercise:BayesianLinearRegression:likelihood_pars_b
:label: solution:BayesianLinearRegression:likelihood_pars
:class: dropdown

- The likelihood can be written $\pdf{\data}{\parsLR,I} = \exp\left[ -L(\parsLR) \right]$, where we include information on the error distribution ($\sigmares$) in the conditional $I$. The negative log-likelihood, including the normalization factor, is

$$
L(\parsLR) = \frac{N_d}{2}\log(2\pi\sigmares^2) + \frac{1}{2\sigmares^2} \sum_{i=0}^{N_d - 1} (\data_i - (\dmat \parsLR)_i)^2.
$$

- Comparing with Eq. {eq}`eq:BayesianLinearRegression:cost-function` and the corresponding gradient vector {eq}`eq:BayesianLinearRegression:gradient` we find that

  $$
  \nabla_{\pars} L(\parsLR) = -\frac{\dmat^T\left( \data-\dmat\pars\right)}{\sigmares^2},
  $$

  which is zero at $\pars = \optparsLR = \left(\dmat^T\dmat\right)^{-1}\dmat^T\data$ corresponding to the solution of the normal equation.

- We can Taylor expand $L(\parsLR)$ around $\parsLR=\optparsLR$ realizing that the linear (gradient) term is zero. Furthermore, the quadrating term depends on the second derivative (hessian) which is a constant matrix since $L$ only depends quadratically on the parameters

$$
H = \Delta L = \nabla_{\parsLR} \cdot (\nabla_{\pars} L(\parsLR)) = \frac{\dmat^T\dmat}{\sigmares^2}
$$

- Since higher derivatives therefore must be zero, the Taylor expansion actually terminates at second order

$$
L(\parsLR) = L(\optparsLR) + \frac{1}{2} (\parsLR-\optparsLR)^T \frac{\dmat^T\dmat}{\sigmares^2} (\pars-\optparsLR)
$$

- We introduce $\covparsLR^{-1} \equiv {\dmat^T\dmat} / {\sigmares^2}$ and use that $\exp\left[ - L(\optparsLR) \right] = \pdf{\data}{\optparsLR,I}$. Therefore, evaluating $\exp\left[ -L(\parsLR) \right]$ gives

  $$
  \pdf{\data}{\parsLR,I} = \pdf{\data}{\optparsLR,I} \exp\left[ -\frac{1}{2} (\pars-\optparsLR)^T \covparsLR^{-1} (\pars-\optparsLR) \right],
  $$

  as we wanted to show.
```
