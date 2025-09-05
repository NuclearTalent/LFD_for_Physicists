(sec:Inference:looking_ahead)=
# Looking ahead

We have put on the table the axioms of probability theory and some of their consequences, in particular Bayes' theorem. 
Before looking further at concrete applications of Bayesian inference, we provide further insight into Bayes' theorem in {ref}`sec:MoreBayesTheorem` and introduce some additional ingredients for Bayesian inference in {ref}`sec:DataModelsPredictions`. The latter include the idea of a statistical model, how to predict future data conditioned on (i.e., given) past data and background information (the posterior predictive distribution), and Bayesian parameter estimation.

In Appendix A there is a summary and further details on {ref}`sec:Statistics`. Particularly important are {ref}`sec:ExpectationValuesAndMoments` and {ref}`sec:CentralMoments`; we summarize the key discrete and continuous definitions here.
Note: there are multiple notations out there for these quantities!

:::{admonition} Brief summary of expectation values and moments
The *expectation value* of a function $h$ of the random variable $X$ with respect to its distribution $p(x_i)$ (a PMF) or $p(x)$ (a PDF) is

$$
\mathbb{E}_{p}[h] =  \sum_{i}\! h(x_i)p(x_i) \quad\Longrightarrow\quad
  \mathbb{E}_p[h] = \int_{-\infty}^\infty \! h(x)p(x)\,dx .
$$

The $p$ subscript is usually omitted. *Moments* correspond to $h(x) = x^n$, with $n=0$ giving 1 (this is the normalization condition) and the mean $\mu$ by $n=1$:

$$
\mathbb{E}[X] \equiv \mu =  \sum_{i}\! x_ip(x_i) \quad\Longrightarrow\quad
  \mathbb{E}[X] \equiv \mu = \int_{-\infty}^\infty \! xp(x)\,dx \equiv \langle x \rangle \equiv \bar x ,
$$

where we have also indicated two other common notations for the mean.

The variance and covariance are moments with respect to the mean for one and two random variables:

$$\begin{align}
\text{Var}(X) &\equiv \sigma_{X}^2  \equiv \mathbb{E}\left[ \left( X - \mathbb{E}[X] \right)^2 \right] \\
\text{Cov}(X,Y) &\equiv \sigma_{XY}^2 \equiv \mathbb{E}\left[ \left( X - \mathbb{E}[X] \right) \left( Y - \mathbb{E}[Y] \right)  \right].
\end{align}$$

The standard deviation $\sigma$ is simply the square root of the variance $\sigma^2$. 
The **correlation coefficient** of $X$ and $Y$ (for non-zero variances) is 

$$
\rho_{XY} \equiv \frac{\text{Cov}(X,Y)}{\sqrt{\text{Var}(X)\text{Var}(Y)}},
$$

The **covariance matrix** $\Sigma_{XY}$ is

$$
 \Sigma_{XY} 
  = \pmatrix{\sigma_X^2 &  \sigma_{XY}^2 \\
                    \sigma_{XY}^2 & \sigma_Y^2}
  = \pmatrix{\sigma_X^2 & \rho_{XY} \sigma_X\sigma_Y \\
                    \rho_{XY}\sigma_X\sigma_Y & \sigma_Y^2}
        \quad\mbox{with}\ 0 < \rho_{XY}^2 < 1  .          
$$

:::


::::{admonition} Checkpoint question
:class: my-checkpoint
Show that we can also write

$$
\sigma^2 = \mathbb{E}[X^2]  - \mathbb{E}[X]^2
$$
:::{admonition} Answer 
:class: dropdown, my-answer 
$$\begin{align}
\sigma^2 &= \int_{-\infty}^\infty (x-\mathbb{E}[X] )^2 p(x)dx\\
&=  \int_{-\infty}^\infty \left(x^2 - 2 x \mathbb{E}[X] +\mathbb{E}[X]^2\right)p(x)dx \\
& =  \mathbb{E}[X^2]  - 2 \mathbb{E}[X] \mathbb{E}[X]  + \mathbb{E}[X]^2 \\
&=  \mathbb{E}[X^2]  - \mathbb{E}[X]^2
\end{align}$$

Make sure you can justify each step.
:::
::::

::::{admonition} Checkpoint question
:class: my-checkpoint
Show that the mean and variance of the normalized Gaussian distribution

$$
p \longrightarrow \mathcal{N}(x | \mu,\sigma^2) = \frac{1}{\sigma\sqrt{2\pi}} \exp{\Bigl(-\frac{(x-\mu)^2}{2\sigma^2}\Bigr)},
$$

are $\mu$ and $\sigma^2$, respectively.
:::{admonition} Answer 
:class: dropdown, my-answer 
Just do the integrals!

$$\begin{align}
  \mu &= \int_{-\infty}^\infty \! x \frac{1}{\sigma\sqrt{2\pi}} \exp{\Bigl(-\frac{(x-\mu)^2}{2\sigma^2}\Bigr)}\,dx = \mu \quad\checkmark \\
  \sigma^2 &= \int_{-\infty}^\infty (x-\mu )^2 
  \frac{1}{\sigma\sqrt{2\pi}} \exp{\Bigl(-\frac{(x-\mu)^2}{2\sigma^2}\Bigr)} \,dx
  = \sigma^2 \quad\checkmark
\end{align}$$

In doing these integrals, simplify by changing the integration variable to $x' = x-\mu$ and use that the distribution is normalized (integrates to one) and that integrals of odd integrands are zero.
:::
::::


:::{admonition} Covariance matrix for a bivariate (two-dimensional) normal distribution 

With vector $\boldsymbol{x} = \pmatrix{x_1\\ x_2}$, the distribution is

$$
  p(\boldsymbol{x}|\boldsymbol{\mu},\Sigma) = \frac{1}{\sqrt{\det(2\pi\Sigma)}}
    e^{-\frac{1}{2}(\boldsymbol{x}-\boldsymbol{\mu})^\intercal\Sigma^{-1}(\boldsymbol{x}-\boldsymbol{\mu})}
$$

with mean and covariance matrix:

$$
  \boldsymbol{\mu} = \pmatrix{\mu_1\\ \mu_2} \quad\mbox{and}\quad
  \Sigma = \pmatrix{\sigma_1^2 & \rho_{12} \sigma_1\sigma_2 \\
                    \rho_{12}\sigma_1\sigma_2 & \sigma_2^2}
        \quad\mbox{with}\ 0 < \rho_{12}^2 < 1  .          
$$

Note that $\Sigma$ is symmetric and positive definite.
See the {doc}`../Visualizing_correlated_gaussians` notebook for plotting what this looks like.

:::






