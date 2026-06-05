---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---
(sec:Inference:moments)=
# Expectation values and moments


In this section we provide a brief introduction to expectation values and moments, summarizing the key discrete and continuous definitions.
Warning: there are multiple notations in the literature for expectation values and moments!
In Appendix A there are further details on {ref}`sec:Statistics`, which includes {ref}`sec:ExpectationValuesAndMoments` and {ref}`sec:CentralMoments`.

We also address the question: *Is a continuous PDF determined by its moments?*
and consider the effective number of samples when the sampling process implies correlation. For independent (and hence uncorrelated) samples, we expect new information with each sample. But this is not the case if there are strong correlations between samples! 

## Summary of expectation values and moments

The *expectation value* of a function $h$ of the random variable $X$ with respect to its distribution $p(x_i)$ (a PMF) or $p(x)$ (a PDF) is

$$
\mathbb{E}_{p}[h] =  \sum_{i}\! h(x_i)p(x_i) \quad\Longrightarrow\quad
  \mathbb{E}_p[h] = \int_{-\infty}^\infty \! h(x)p(x)\,dx .
$$

The $p$ subscript is often omitted if it is clear which distribution is being considered. *Moments* correspond to $h(x) = x^n$. The zeroth moment (with $n=0$) is always equal to one since it is the normalization condition of the PDF. The first moment ($n=1$) gives the mean, which is often denoted $\mu$:

$$
\mathbb{E}[X] \equiv \mu =  \sum_{i}\! x_ip(x_i) \quad\Longrightarrow\quad
  \mathbb{E}[X] \equiv \mu = \int_{-\infty}^\infty \! xp(x)\,dx \equiv \langle x \rangle \equiv \bar x ,
$$

where we have also indicated two other common notations for the mean.

The variance and covariance are (central) moments with respect to the mean for one and two random variables:

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
  = 
   \begin{pmatrix}
    \sigma_X^2 &  \sigma_{XY}^2 \\
    \sigma_{XY}^2 & \sigma_Y^2
   \end{pmatrix}
  = 
   \begin{pmatrix}
      \sigma_X^2 & \rho_{XY} \sigma_X\sigma_Y \\
      \rho_{XY}\sigma_X\sigma_Y & \sigma_Y^2
    \end{pmatrix}
        \quad\mbox{with}\ 0 < \rho_{XY}^2 < 1  .          
$$ (eq:covariance_Sigma_XY)


::::{admonition} Checkpoint question
:class: my-checkpoint
Show that we can also write
$\sigma^2 = \mathbb{E}[X^2]  - \mathbb{E}[X]^2$.
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

$$\begin{aligned}
  \mu &= \int_{-\infty}^\infty \! x \frac{1}{\sigma\sqrt{2\pi}} \exp{\Bigl(-\frac{(x-\mu)^2}{2\sigma^2}\Bigr)}\,dx = \mu \quad\checkmark \\
  \sigma^2 &= \int_{-\infty}^\infty (x-\mu )^2 
  \frac{1}{\sigma\sqrt{2\pi}} \exp{\Bigl(-\frac{(x-\mu)^2}{2\sigma^2}\Bigr)} \,dx
  = \sigma^2 \quad\checkmark
\end{aligned}$$

In doing these integrals, simplify by changing the integration variable to $x' = x-\mu$ and use that the distribution is normalized (integrates to one) and that integrals of odd integrands are zero.
:::
::::


:::{admonition} Covariance matrix for a bivariate (two-dimensional) normal distribution 

With vector $\boldsymbol{x} = \begin{pmatrix} x_1\\ x_2 \end{pmatrix}$, the distribution is

$$
  p(\boldsymbol{x}|\boldsymbol{\mu},\Sigma) = \frac{1}{\sqrt{\det(2\pi\Sigma)}}
    e^{-\frac{1}{2}(\boldsymbol{x}-\boldsymbol{\mu})^\intercal\Sigma^{-1}(\boldsymbol{x}-\boldsymbol{\mu})}
$$

with mean and covariance matrix:

$$
  \boldsymbol{\mu} = \begin{pmatrix} \mu_1\\ \mu_2 \end{pmatrix} \quad\mbox{and}\quad
  \Sigma = \begin{pmatrix}
            \sigma_1^2 & \rho_{12} \sigma_1\sigma_2 \\
            \rho_{12}\sigma_1\sigma_2 & \sigma_2^2
           \end{pmatrix}
        \quad\mbox{with}\ 0 < \rho_{12}^2 < 1  .          
$$

Note that $\Sigma$ is symmetric and positive definite.
See {numref}`sec:2dPDFs` for plotting what this looks like.

:::


::::{admonition} Checkpoint question
:class: my-checkpoint
What can't we have $\rho > 1$ or $\rho < -1$?

:::{admonition} Answer 
:class: dropdown, my-answer 
The bounds on the correlation coefficient $\rho$ arise from the [Cauchy-Schwarz inequality](https://en.wikipedia.org/wiki/Cauchy%E2%80%93Schwarz_inequality), which says that if $\langle\cdot,\cdot\rangle$ defines an inner product, then for all vectors $\uvec,\vvec$ in the space, this inequality holds:

$$
  |\langle\uvec,\vvec\rangle|^2 \leq |\langle \uvec,\uvec\rangle| |\langle\vvec,\vvec\rangle| .
$$

The expectation value of a random variable satisfies the conditions to be an inner product,
so that the Cauchy-Schwarz inequality implies that

$$
  |\mathbb{E}[UV]| \leq \sqrt{\mathbb{E}[U^2]}\sqrt{\mathbb{E}[V^2]}.
$$

With $U = X - \mu_{X}$ and $V = Y - \mu_{Y}$, the inequality implies that

$$
   |\text{Cov}(X,Y)| \leq \sigma_X \sigma_Y . 
$$

Dividing through by $\sigma_X \sigma_Y$ yields $-1 \leq \rho \leq 1$.

A consequence is that the matrix $\Sigma$ would not be a valid covariance matrix because the determinant would be negative.
:::
::::

## Is a continuous PDF determined by its moments?

If we know some (or all) of the moments of a one-dimensional distribution $p(x)$, how can we find the PDF?
Let us define the moments $m_k$ for integer $k$ as

$$
    m_k = \int_S x^k\, p(x)\, dx,  \qquad k= 0,1,2,\ldots,
$$

where $S$ denotes the support of the PDF (e.g., $(-\infty,\infty)$ for a Gaussian or $[0,1]$ for a Beta distribution). So $m_0 = 1$, the mean $\mu$ is $m_1$, the variance $\sigma^2$ is $m_2 - m_1^2$, and so on. 

```{note}
We can generalize this discussion to multi-dimensional PDFs with vector $\mathbf{x}$, for which the moments will have multiple indices and the defining expression will be integrated over the space of $\mathbf{x}$.
```

Here are some ways to find $p(x)$ given a set of moments $\{m_k\}$:
1. If we know the PDF belongs to a particular parametric family, such as Gaussian or Beta (see {ref}`sec:1dPDFs`), then we can solve for the defining parameters if we know the appropriate moments. For the case of a Gaussian, we know it is defined by its mean $\mu$ and variance $\sigma^2$, so those are the only two moments we need. (In fact, we can determine the mean and variance even if we only know higher moments!) This is also true for the less familiar case of a Beta distribution that is specified by the shape parameters $\alpha, \beta > 0$ (see [Beta distribution](https://en.widipedia.org/wiki/Beta_distribution) on Wikipedia). If the variance satisfies $\sigma^2 < \mu(1-\mu)$, then

   $$
     \alpha = \mu \left(\frac{\mu(1-\mu)}{\sigma^2} - 1\right), \qquad
     \beta = (1-\mu) \left(\frac{\mu(1-\mu)}{\sigma^2} - 1\right).
   $$  

1. We can use a maximum entropy reconstruction. With a finite number of known moments, we choose among distributions that reproduce these moments the one with the largest entropy. See {numref}`sec:MaxEnt` to learn about the principle of maximum entropy and there is a demo notebook in {numref}`demo:maximum-entropy-for-reconstructing-a-function-from-its-moments` illustrating how to do a maximum entropy reconstruction from moments.

1. We can try to invert from a *moment-generating function* or a *characteristic function*. 
   If $X$ is a random number with distribution $p_X(x)$, then the moment-generating function $M_X(t)$ and characteristic function $\phi_X(t)$ are for $t\in\mathbb{R}$:

   $$\begin{align*}
     M_X(t) &= \mathbb{E}[e^{tX}] = \sum_{k=0}^\infty \frac{t^k}{k!}\mathbb{E}[X^k] = \sum_{k=0}^\infty \frac{m_k}{k!} t^k 
     \quad\Longrightarrow\quad 
     M^{(k)}_X(0) = m_k ,
    \\
     \phi_X(t) &= \mathbb{E}[e^{itX}] = \sum_{k=0}^\infty \frac{(it)^k}{k!}\mathbb{E}[X^k] = \sum_{k=0}^\infty \frac{m_k}{k!} (it)^k 
     \quad\Longrightarrow\quad 
     \phi^{(k)}_X(0) = m_k ,
   \end{align*}$$

   where we have formally performed Taylor expansions and inverted the order of summation and expectation value (we're assuming here that these are valid operations). The superscript $(k)$ means the $k^{\text{th}}$ derivative. In integral form,

   $$
     M_X(t) = \int_{-\infty}^{\infty} e^{tx}\, p_X(x)\, dx, \qquad
     \phi_X(t) = \int_{-\infty}^{\infty} e^{itx}\, p_X(x)\, dx.
   $$

   So the moment-generating function is essentially a Laplace transform of the distribution, while the characteristic function is essentially a Fourier transform.
   As such, we can try to invert them to find $p_X(x)$. 

   ```{note}
   We can derive immediately that for a Gaussian distribution with mean $\mu$ and variance $\sigma^2$,

   $$
       M_X(t) = \exp(\mu t + \frac{1}{2}\sigma^2 t^2) , \qquad
       \phi_X(t) = \exp(i\mu t - \frac{1}{2}\sigma^2 t^2) .
   $$  (eq:expectation:moments_gaussian)
   ```

1. We can use *discrete quadrature reconstruction*. In this case we approximate the PDF by a finite sum of $n$ point masses (i.e., delta functions) with weights and locations chosen to reproduce the first $n$ moments. That is, replace the continuous $p(x)$ by the discrete $p_N(x)$:

   $$
     p_N(x) = \sum_{i=1}^N w_i \delta(x-x_i), \qquad w_i \geq 0, \qquad \sum_{i=1}^N w_i = 1,
   $$

   where the $x_i$ are nodes and the $w_i$ are the weights, such that

   $$
      m_k \approx \sum_{i=1}^N w_i x_i^k .
   $$

   If $K$ moments $m_k$ for $k = 0, 1, \ldots , K$ are known and the $x_i$ are fixed, this is a linear problem in the weights $w_i$. If both $x_i$ and $w_i$ are unknown, one has more flexibility.
   Under suitable conditions, $2N−1$ moments can be exactly matched by an $N$-point discrete representation (so this is closely related to Gaussian quadrature). 

In most, but not all, cases a PDF will uniquely be determined by a complete set of moments.



## Correlations and the effective number of samples

Consider $n$ quantities $y_1$, $y_2$, $\ldots$, $y_n$, which individually are identically distributed with  mean $\mu_0$ and variance $\sigma_0^2$, but with unspecified covariances between the $y_i$. For concreteness we'll say that the distribution of $\yvec = (y_1, y_2, \ldots, y_n)$ is a multivariate Gaussian:

$$
  \yvec \sim \mathcal{N}(\mu_0 \boldsymbol{1_n}, \Sigma) ,
$$

where $\boldsymbol{1_n}$ is a $n$-dimensional vector of ones and $\Sigma$ is an $n\times n$ covariance matrix with all diagonal elements equal to $\sigma_0^2$.

Let us consider two limits of this distribution: (i) the uncorrelated one with all off-diagonal elements of $\Sigma$ equal to zero and (ii) the fully correlated one with all covariances equal to $\sigma_0^2$. The covariance matrix of case (ii) is singular but this will not be a concern for our argument.

If we repeatedly draw $y_1$ and $y_2$ from the uncorrelated distribution, the joint distribution on a corner plot is 2-dimensional (in particular, the contours are circular). With $n$ draws, the joint distribution is $n$-dimensional (and the contours for the marginalized 2-dimensional plots are all circular). 
But the same analysis with the fully correlated distribution would yield a straight line for the $n=2$ case; that is to say all samples can be found in a single dimension. Further, it remains 1-dimensional for any $n$.
We can interpret this as meaning the effective number of draws or samples is $n$ in the uncorrelated case and 1 in the correlated case.

Consider the average value of $y_1, y_2, \ldots, y_n$ and the variance of that average. For convenience, define $z$ as

$$
  z = \frac{1}{n}(y_1 + y_2 + \ldots + y_n) .
$$

Then if we make many draws of $y_1$ through $y_n$, the expectation values of each $y_i$ is the same, namely $\mu_0$, so the expectation value of $z$ is

$$ 
  \langle z \rangle = \frac{1}{n}(\langle y_1 \rangle + \ldots + \langle y_n \rangle)
   = \frac{1}{n} n \langle y_1 \rangle = \mu_0 .
$$

Now define $\widetilde y_i = y_i - \mu_0$ and $\widetilde z = z - \mu_0$, so that these new random variables are all mean zero (this is for clarity, not necessity). 
The variance of $\widetilde y_i$ is equal to $\langle y_i^2 \rangle = \sigma_0^2$. 
Consider now the variance of $\widetilde z$ which is equal to the expectation value of $\widetilde z^2$,

$$
 \langle \widetilde z^2 \rangle = \frac{1}{n^2} (
  \widetilde y_1^2 + \widetilde y_2^2 + \ldots + \widetilde y_1 \widetilde y_2 + \widetilde y_1 \widetilde y_3 + \widetilde y_2 \widetilde y_3 + \ldots
 ) 
$$ (eq:variance_n_effective)

Since $\langle\widetilde y_i \widetilde y_j\rangle$ either is zero or equals $\sigma_0^2$ for the two extremes of correlation, we find

$$\begin{align}
   &\text{uncorrelated}\  & \langle \widetilde z^2 \rangle &= \frac{1}{n^2}\cdot n\langle y_i^2 \rangle = \frac{\sigma_0^2}{n} , \\
   &\text{fully correlated}\ & \langle \widetilde z^2 \rangle &= \frac{1}{n^2} \cdot n^2 \langle \widetilde y_i \widetilde y_j \rangle = \frac{\sigma_0^2}{1} ,
\end{align}$$

where we have $n$ nonzero terms in the uncorrelated case but $n^2$ nonzero terms in the fully correlated case.
Thus the standard deviation in the uncorrelated case decreases with the familiar $1/\sqrt{n}$ factor, so the effective number of samples is $n$. But in the fully correlated case the width is independent of $n$: increasing $n$ adds no new information, so the effective number of samples is one.

We can do the more general case by considering
$\yvec$ distributed as above with $\Sigma = \sigma_0^2 M$, where $M$ is the $n\times n$ matrix:

$$
  M = \begin{pmatrix}
1      & \rho  & \rho  & \cdots & \rho \\
\rho   & 1     & \rho  & \cdots & \rho \\
\rho   & \rho  & 1     & \cdots & \rho \\
\vdots & \vdots& \vdots& \ddots & \vdots \\
\rho   & \rho  & \rho  & \cdots & 1
\end{pmatrix} ,
$$

with $0 \leq \rho < 1$ (we assume only positive correlation here). So the two extremes just considered correspond to $\rho =0$ and $\rho = 1 - \epsilon$ (we introduce $\epsilon$ as a small positive number to be taken to zero at the end, needed because otherwise the covariance matrix $\Sigma$ cannot be inverted).
Then the variance of $\widetilde z$ given $\yvec$ is

$$
  \text{Var}(\widetilde z | \yvec, \sigma_0^2, M) = \bigl[\boldsymbol{1_n}^{\top} (\sigma_0^2 M) \boldsymbol{1_n} \bigr]^{-1}
  = \frac{\sigma_0^2 [1 + (n-1)\rho]}{n} .
$$

We can get this result directly from {eq}`eq:variance_n_effective` by noting there are $n$ terms with $i = j$ and $n(n-1)$ terms with $i \neq j$. So the variance is 

$$
  \langle \widetilde z^2 \rangle = \frac{\sigma_0^2}{n^2} \bigl(n\cdot 1 + n(n-1)\cdot\rho \bigr)
    = \frac{\sigma_0^2 [1 + (n-1)\rho]}{n} = \frac{\sigma_0^2}{n_{\text{eff}}}
$$

Thus the effective number of degrees of freedom is 

$$
   n_{\text{eff}}
   = \frac{n}{[1 + (n-1)\rho]} .
$$

This also follows from the Fisher information matrix.


For $n=20$, $n_{\text{eff}}$ looks like:

 ```{code-cell} python3
:tags: [hide-input]


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FixedLocator

n = 20
rho_values = np.linspace(0, 0.99, 100)

n_eff = n / (1 + (n-1)*rho_values)

fig, ax = plt.subplots(figsize=(5,4))
ax.plot(rho_values, n_eff)
ax.set_xlabel(r"$\rho$")
ax.set_ylabel(r"$n_\mathrm{eff}$")
ax.set_title(f"Effective sample size vs correlation for n={n}")
ax.set_ylim(0, 20)
ax.yaxis.set_major_locator(FixedLocator([0, 5, 10, 15, 20]))   # tick + label
ax.yaxis.set_minor_locator(MultipleLocator(1))              # tick only, no label

plt.grid(True)
plt.show()
```







