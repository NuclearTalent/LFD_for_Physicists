---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(sec:ErrorPropagationI)=
# Error propagation (I): Nuisance parameters and marginalization

The Bayesian approach offers a straightforward approach for dealing with (known) systematic uncertainties; namely by marginalization. 

Assume that we have a model with two parameters, $\theta,\phi$, although only one of them (say $\theta$) is of physical relevance. The other one is then labeled a nuisance parameter. Through a Bayesian data analysis we can get the the joint posterior PDF

\begin{equation}
\pdf{\theta, \phi}{\data, I}.
\end{equation}

The marginal posterior PDF $\pdf{\theta}{\data, I}$ is obtained via marginalization

\begin{equation}
\pdf{\theta}{\data, I} = \int \pdf{\theta, \phi}{\data, I} d\phi.
\end{equation}

This simple procedure allows to propagate the uncertainty in $\phi$ to the probability distribution for $\theta$.

{prf:ref}`example:BayesianAdvantage:inferring-galactic-distances` provides an illustration of this scenario.

```{admonition} Marginalization using samples
:class: tip
Assume that we have $N$ samples from the joint pdf $\pdf{\theta, \phi}{\data, I}$. This might a sample chain from an MCMC sampler: $\left\{ (\theta, \phi)_i \right\}_{i=0}^{N-1}$. Then the marginal distribution of $\theta$ will be given by the same chain by simply ignoring the $\phi$ column, i.e., $\left\{ \theta_{i} \right\}_{i=0}^{N-1}$. 

See the interactive demos created by Chi Feng for an illustration of this: [The Markov-chain Monte Carlo Interactive Gallery](https://chi-feng.github.io/mcmc-demo/).
```

A slightly more general scenario for which the marginalization procedure is useful is the following: Assume that we have measured or inferred the parameters $X$ and $Y$; what can we say about the difference $X-Y$ or the raio $X/Y$, or the sum of their squares $X^2+Y^2$, etc? 

Such questions can be rephrased as: Given the joint PDF $\pdf{x,y}{I}$, what is $\pdf{z}{I}$, where $z=f(x,y)$? Here, and in the following, we use shorthands $\pdf{z}{I}$, $\pdf{x,y}{I}$ instead of the more correct $p_Z(z|I)$, $p_{X,Y}(x,y|I)$. The context should make it clear which random variable(s) that are referred to.

In this situation we can use marginalization and the product rule. 

\begin{equation}
\pdf{z}{I} = \int \pdf{z,x,y}{I}dxdy = \int \pdf{z}{x,y,I} \pdf{x,y}{I}dxdy.
\end{equation}

We realize that $\pdf{z}{x,y,I} = \delta(z-f(x,y))$ due to the functional relationship between the parameters.

```{admonition} Dirac delta functions
A delta function $\delta(x-x_0)$ can be constructed as the limiting case of a distribution

$$
\delta(x-x_0) = \lim_{\varepsilon \to 0^+} h_{\varepsilon}(x-x_0).
$$

For example, it can be constructed as an infinitely narrow (and tall) normal distribution

$$
\delta(x-x_0) = \lim_{\varepsilon \to 0^+} \frac{1}{\sqrt{2\pi}\varepsilon} \exp\left( -\frac{(x-x_0)^2}{2\varepsilon^2}\right).
$$

This function will be zero for $x \neq x_0$, and goes to infinity at $x_0$ in a way such that the integral $\int_{-\infty}^{+\infty} \delta(x-x_0) dx = 1$, which is a defining property.

More general, for well-behaved functions $f(x)$, we have $\int_{-\infty}^{+\infty} f(x) \delta(x-x_0) dx = f(x_0)$.
```

The joint PDF for $X$ and $Y$ becomes a product if the errors are independent $\pdf{x,y}{I} = \pdf{x}{I} \pdf{y}{I}$ . The delta function can be used to evaluate one of the integrals, giving some inverse transformation $y=g(x,z)$, and the PDF for $Z$ becomes a convolution

$$
\pdf{z}{I} = \int \pdf{x}{I} \pdf{y=g(x,z)}{I}dx.
$$ (eq:BayesianAdvantage:marginalization)


````{prf:example} $Z = X + Y$
:label: example:BayesianAdvantage:Z=X+Y

Let us consider the situation where you are interested in the quantity $Z = X + Y$, and you have information $I$ about $X$ and $Y$ which tells you that $\expect{X} = x_0$, $\var{X} = \sigma_x^2$ and $\expect{Y} = y_0$, $\var{Y} = \sigma_y^2$. If this is all the information that we have, it is reasonable to assume that $X$ and $Y$ are independent and that we should assign Gaussian  PDFs (the argument for this is known as the Maximum Entropy principle)

\begin{align}
\pdf{x,y}{I} &= \pdf{x}{I}\pdf{y}{I} \\
&= \frac{1}{2\pi\sigma_x\sigma_y} \exp\left[ - \frac{(x-x_0)^2}{2\sigma_x^2} \right] \exp\left[ - \frac{(y-y_0)^2}{2\sigma_y^2} \right].
\end{align}

Let us now use marginalization and the product rule to find

\begin{equation}
\pdf{z}{I} = \int \pdf{z,x,y}{I}dxdy = \int \pdf{z}{x,y,I} \pdf{x,y}{I}dxdy.
\end{equation}

We realize that $\pdf{z}{x,y,I} = \delta(z-(x+y))$ due to the functional relationship between the parameters, and we have $\pdf{x,y}{I}$ as a product of Gaussian  PDFs from above. The delta function can be used to evaluate one of the integrals, and the PDF for $Z$ becomes a convolution

\begin{align}
\pdf{z}{I} &= \int \pdf{x}{I} \pdf{y=z-x}{I} dx \\
&= \frac{1}{2\pi\sigma_x\sigma_y} \int \exp\left[ - \frac{(x-x_0)^2}{2\sigma_x^2} \right] \exp\left[ - \frac{(z - x - y_0)^2}{2\sigma_y^2} \right] dx.
\end{align}

After some tedious algebra that involves completing the square for $X$ in the exponent we obtain

$$
\pdf{z}{I} = \frac{1}{\sqrt{2\pi}\sigma_z} \exp\left[ - \frac{(z-z_0)^2}{2\sigma_z^2} \right], 
$$ (eq:BayesianAdvantage:sum-of-gaussians)

with $z_0 = x_0 + y_0$ and $\sigma_z^2 = \sigma_x^2 + \sigma_y^2$. Thus, the PDF for the sum $Z=X+Y$, with $X$ and $Y$ being described by Gaussian  PDFs, is another Gaussian.
````

```{exercise} Correlated errors
:label: exercise:BayesianAdvantage:correlated-errors

For correlated errors the joint PDF $\pdf{x,y}{I}$ does not factorize into a product. Consider, for example, a situation with a bivariate normal distribution

$$
\pdf{x,y}{I} = \frac{1}{(2\pi) |\boldsymbol{\Sigma}|^{1/2}} \exp{ \left( -\frac{1}{2}(x, y)\boldsymbol{\Sigma}^{-1}(x, y)^T\right)}.
$$

Furthermore, let us assume that the variances in $X$ and $Y$ are the same ($\sigma_x^2=\sigma_y^2\equiv\sigma^2$) and the covariance is positive and almost as large as the variance (i.e., errors are strongly correlated). Then, the linear transformation $S=(X-Y)/\sqrt{2}$ and $T=(X+Y)/\sqrt{2}$ gives two new random variables $S$ and $T$ that turn out to be independent. This implies 

$$
\pdf{x,y}{I} = 
\left\{ 
\begin{array}{l}
s = \frac{x-y}{\sqrt{2}} \\
t = \frac{x+y}{\sqrt{2}} \\
\end{array}
\right\}
= \frac{1}{\sqrt{2\pi}\sigma_s}\exp \left( - \frac{s^2}{2\sigma_s^2} \right) \frac{1}{\sqrt{2\pi}\sigma_t}\exp \left( - \frac{t^2}{2\sigma_t^2} \right).
$$

Furthermore, given the strong positive correlation one finds that $\sigma_s \ll \sigma$. What is the PDF for the difference $Z=X-Y$ in this situation?
```

```{exercise} Sum of two Gaussian  PDFs
:label: exercise:BayesianAdvantage:complete-the square

Complete the derivation of Eq. {eq}`eq:BayesianAdvantage:sum-of-gaussians`.
```


````{prf:example} Inferring galactic distances
:label: example:BayesianAdvantage:inferring-galactic-distances

The Hubble constant $H$ acts as a galactic ruler as it is used to measure astronomical distances ($d$) according to $v = H d$ where $v$ is the velocity that can be measured with observations of redshifts. An error in $H$ will therefore correspond to a systematic uncertainty in such measurements.

A modern value for the Hubble constant is $H = 70 \pm 10$ km s$^{-1}$ MPc$^{-1}$. We introduce the expectation value $\expect{H} = H_0 = 70$ km s$^{-1}$ MPc$^{-1}$ and the standard deviation $\std{H} = \sigma_H = 10$ km s$^{-1}$ MPc$^{-1}$. Note that astronomical distances are usually measured in million parsecs (MPc). Suppose that a specific galaxy has a measured recessional velocity $v_0 = 100 \times 10^3$ km/s with an observational error quantified by a standard deviation $\sigma_v = 5 \times 10^3$ km/s. Determine the posterior PDF for the distance to a galaxy under the following analysis assumptions:

1. We use the expectation value of $H$ in the analysis: $H = H_0 = 70$ km s$^{-1}$ MPc$^{-1}$. 
2. We include the uncertainty in the value of the Hubble constant via a Gaussian PDF:

   $$
   \pdf{H}{I} = \frac{1}{\sqrt{2\pi}\sigma_H} \exp\left( - \frac{(H-H_0)^2}{2 \sigma_H^2} \right).
   $$
   
3. We include the uncertainty in the value of the Hubble constant via a uniform PDF:

   $$
   \pdf{H}{I} = \left\{ 
   \begin{array}{ll}
   \frac{1}{4 \sigma_H} & \text{for } H_0 - 2\sigma_H \leq H \leq H_0 + 2\sigma_H, \\
   0 & \text{otherwise.}
   \end{array}
   \right.
   $$
   
4. In addition, an approximate propagation of errors is demonstrated in {prf:ref}`example:BayesianAdvantage:inferring-galactic-distances-revisited`.

Here we use marginalization to obtain the desired posterior PDF $\pdf{d}{\data,I}$ from the joint distribution of $\pdf{d,H}{\data,I}$

$$
\pdf{d}{\data,I} = \int_{-\infty}^\infty \pdf{d,H}{\data,I} dH .
$$ (eq:marginalization-hubble)

Using 
* Bayes' rule: $\pdf{d,H}{\data,I} \propto \pdf{\data}{d,H,I} \pdf{d,H}{I}$, 
* the product rule: $\pdf{d,H}{I} = p(H|d,I)\pdf{d}{I}$, 
* and the fact that $H$ is independent of $d$: $p(H|d,I) = \pdf{H}{I}$, 

we find that

\begin{equation}
\pdf{d}{\data,I} \propto \pdf{d}{I} \int \pdf{H}{I} \pdf{\data}{d,H,I} dH ,
\end{equation}

which means that we have expressed the quantity that we want (the posterior of $d$) in terms of quantities that we can specify. 

First, we need to state our prior knowledge concerning the distance $\pdf{d}{I}$. You might ask yourself what information is contained in this quantity. It should summarize our state of knowledge *before* accumulating the new data. For starters, we do know that it is a distance (meaning that it is a positive quantity) and we would also expect it to be smaller than the (visible) size of the universe. We might argue that it should be at least as far away as the previously known closest galaxy. Further arguments can be made on the basis of indifference, but we will defer such discussions for now. For simplicity, we just assign a uniform PDF 

$$
\pdf{d}{I} \propto 1,
$$ 

within some huge range $0 < d  < 10^9$ MPc.

The likelihood for the observed can be written down from a statistical model

$$
v_\mathrm{measured} = H d + e,
$$

where $H d$ represents our model for the velocity and $e$ is the observational error, which is a random variable. We know that $\expect{v_\mathrm{measured}} = v_0$ and $\text{Var}(v_\mathrm{measured}) = \sigma_v^2$. Given this information it is motivated to use a Gaussian PDF (with this mean and variance) for the likelihood

$$
\pdf{\data}{d,H,I} = \frac{1}{\sqrt{2\pi}\sigma_v} \exp\left( - \frac{(v_0 - Hd)^2}{2\sigma_v^2} \right).
$$

The results for the different analysis strategies (1-3 in the list above) should be obtained in {numref}`exercise:BayesianAdvantages:inferring-galactic-distances-ex`. A comparison figure that also includes the approximative error propagation (4) is shown in the solution to this exercise.
````

```{exercise} Inferring galactic distances
:label: exercise:BayesianAdvantages:inferring-galactic-distances-ex

Apply the first three analysis strategies and derive the posterior distribution $\pdf{d}{\data,I}$. The first case allows an analytical solution while the second and third are probably best approached numerically (although it is, in fact, possible to find an analytical result also for case 2). Plot the results.

Hint 1: Since the goal is to extract a probability distribution, and we are already ignoring the denominator in Bayes' theorem, it is allowed to ignore all normalization constants. The final  PDFs can be normalized by integration.

Hint 2: A fixed value for $H$ can be assigned with the PDF $\pdf{H}{I} = \delta(H-H_0)$, where $\delta(x)$ is the Kronecker delta. 
```

