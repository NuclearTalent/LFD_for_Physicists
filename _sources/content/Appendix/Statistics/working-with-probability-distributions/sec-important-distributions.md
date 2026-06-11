# Important distributions

Let us consider some important, univariate distributions.

## The uniform distribution

The first one is the most basic PDF; namely the uniform distribution. This distribution is constant in a range $[a,b]$ and zero elsewhere. Thus, when a random variable $X$ is uniformly distributed on $[a,b]$ we can write $X  \sim \mathcal{U}([a,b])$ with

\begin{equation}
\mathcal{U}\left( [a,b]\right) = \frac{1}{b-a}\theta(x-a)\theta(b-x).
\label{eq:Statistics:unifromPDF}
\end{equation}

For $a=0$ and $b=1$ we have the standard uniform distribution

\begin{equation}
\mathcal{U}\left( [0,1]\right) = \left\{
\begin{array}{ll}
1 & x \in [0,1],\\
0 & \mathrm{otherwise}
\end{array}
\right.
\end{equation}

Note that these functions correspond to properly normalized PDFs such that they give a total probability of one when integrated over $x \in (-\infty,\infty)$.

(sec:univariate_gaussian)=
## Gaussian distribution
The second one is the univariate Gaussian distribution (or normal distribution). A random variable $X \sim \mathcal{N}(\mu,\sigma^2)$ is normally distributed with mean value $\mu$ and standard deviation $\sigma$ with

\begin{equation}
\mathcal{N}(\mu,\sigma^2) = \frac{1}{\sigma\sqrt{2\pi}} \exp{(-\frac{(x-\mu)^2}{2\sigma^2})},
\end{equation}

the corresponding PDF. If $\mu=0$ and $\sigma=1$, it is called the **standard normal distribution**

\begin{equation}
\mathcal{N}(0,1) = \frac{1}{\sqrt{2\pi}} \exp{(-\frac{x^2}{2})}.
\end{equation}

We sometimes denote distributions using a notation like $\mathcal{N}(x|\mu,\sigma^2)$. This should be understood as a variable $x$ being normally distributed with mean $\mu$ and variance $\sigma^2$. 

(sec:distribution_mvn)=
## Multivariate Gaussian distribution

The univariate [](sec:univariate_gaussian) can be generalized to a multivariate distribution. A multivariate random variable $\boldsymbol{X} \sim \mathcal{N}(\boldsymbol{\mu},\boldsymbol{\Sigma})$ is normally distributed with mean _vector_ $\boldsymbol{\mu} \in \mathbb{R}^k$ and covariance _matrix_ $\boldsymbol{\Sigma} \in \mathbb{R}^{k \times k}$ with

$$
\mathcal{N}(\boldsymbol{\mu},\boldsymbol{\Sigma}) = \frac{1}{(2\pi)^{k/2} |\boldsymbol{\Sigma}|^{1/2}} \exp{ \left( -\frac{1}{2}(\boldsymbol{x} - \boldsymbol{\mu})^T\boldsymbol{\Sigma}^{-1}(\boldsymbol{x} - \boldsymbol{\mu})\right)}.
$$ (eq:Statistics:multivariate-normal-PDF)

This distribution only exists for a positive definite covariance matrix $\boldsymbol{\Sigma}$.
