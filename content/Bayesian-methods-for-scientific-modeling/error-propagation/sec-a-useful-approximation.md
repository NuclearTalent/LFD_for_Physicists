---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:ErrorPropagationIII)=
# A useful approximation


We have seen in {numref}`sec:ErrorPropagationI` and {numref}`sec:BayesianAdvantages:ChangingVariables` how to exactly calculate the probability distribution for a random variable that is a function of other random variables.
That is, given distributions for random variables $X$ and $Y$, we can find the distribution for $Z = f(X,Y)$. 
But it will often be sufficient to approximate PDFs with (uncorrelated) Gaussian distributions, in which case we can anticipate being able to approximate how such distributions combine. 
Intuitively, if the distributions for $X$ and $Y$ are sharply peaked about their means, we expect we can linearize $f(X,Y)$ and then $Z$ will also be a Gaussian.
Let's see how this plays out successfully and where it can fail.

If we assume $X$ and $Y$ are independent, then in the Gaussian approximation, the distributions for $X$ and $Y$ are fully characterized by their means $\mu_X, \mu_Y$ and variances $\sigma_X^2, \sigma_Y^2$, respectively. These are given by expectation values (recall {ref}`sec:Inference:moments`)

$$
  \mu_X = \expect{X}, \quad \mu_Y = \expect{Y} 
$$ (eq:mean-abbreviations)

$$
  \sigma_X^2 = \expect{(\delta X)^2}, \quad \sigma_Y^2 = \expect{(\delta Y)^2}, \quad \sigma_{XY} = \expect{\delta X \delta Y} = \expect{\delta X}\times\expect{\delta Y} = 0,
$$ (eq:variance-abbreviations)

where we have defined the deviations from the mean

$$
  \delta X \equiv X - \mu_X, \quad  \delta Y \equiv Y - \mu_Y,
$$

and used that $\delta X$ and $\delta Y$ are independent zero-mean distributions.

By assumption, we should be able to expand about the means, so for small $\delta X$ and $\delta Y$ we Taylor expand (here to second order):

$$
  \begin{aligned}
  Z &= f(X, Y) \\
    &\approx f(\mu_X, \mu_Y) + f_X \delta X + f_Y \delta Y
    + \frac12 f_{XX}(\delta X)^2   + \frac12 f_{YY}(\delta Y)^2  + f_{XY}\delta X\delta Y + \ldots
  \end{aligned}
$$ (eq:Z-expansion-second-order)

where we use the abbreviations

$$
  f_X \equiv \left.\frac{\partial f}{\partial X}\right|_{\mu_X,\mu_Y}, \quad
  f_Y \equiv \left.\frac{\partial f}{\partial Y}\right|_{\mu_X,\mu_Y}, 
$$

$$
  f_{XX} \equiv \left.\frac{\partial^2 f}{\partial X^2}\right|_{\mu_X,\mu_Y}, \quad
  f_{YY} \equiv \left.\frac{\partial^2 f}{\partial Y^2}\right|_{\mu_X,\mu_Y}, \quad
  f_{XY} \equiv \left.\frac{\partial^2 f}{\partial X\partial Y}\right|_{\mu_X,\mu_Y}.
$$

Let's first work to linear order (i.e., keep through $\delta X$ and $\delta Y$). 
Then $Z$ is a linear combination of Gaussian distributions, hence is itself Gaussian.
We can find its mean and variance by using the linearity of expectation values and that the $\delta X$ and $\delta Y$ are independent, zero-mean distributions:

$$
  \mu_Z = \expect{Z} = \expect{f(X,Y)} \approx f(\mu_X, \mu_Y)\, 
$$ (eq:mu-Z-equation)

$$
  \begin{aligned}
  \sigma_Z^2 &= \expect{(Z - \mu_Z)^2}
  \approx\expect{f_X^2 (\delta X)^2 + f_Y^2 (\delta Y)^2 + 2 f_X f_Y \delta X \delta Y} \\
  &\approx f_X^2 \sigma_X^2 + f_Y^2 \sigma_Y^2 .
  \end{aligned}
$$ (eq:sigma-Z-equation)

```{admonition} Summary
:class: tip 
The application of these approximations: 

$$
\mu_Z \approx f(\mu_X, \mu_Y), \quad 
\sigma_Z^2 \approx f_X^2 \sigma_X^2 + f_Y^2 \sigma_Y^2 
$$ (eq:gaussian_error_propagation)

is sometimes called *Gaussian error propagation*. 
In fact, these relations apply at this linear order regardless of how the random variables $X$ and $Y$ are distributed. Although the above discussion was motivated by assuming they were normally distributed nothing we have done so far actually used that. The derivation does, though, assume that $X$ and $Y$ are independent random variables.
```

::::{admonition} Checkpoint question
:class: my-checkpoint
Why are expectation values linear operations?
:::{admonition} Answer 
:class: dropdown, my-answer 
Recall from {ref}`sec:Inference:moments` that expectation values are integrals over probability definitions. As such, they inherit linearity from the linearity of integrals.
:::
::::

Let's apply the formulas in {eq}`eq:gaussian_error_propagation` to $Z=X-Y$. 
For the mean we get $\mu_Z = \mu_X - \mu_Y$, which is intuitive.
For the variance the relevant derivatives are $f_X = +1$ and $f_Y = -1$, so
we find that

$$
\sigma_z^2 = \sigma_x^2 + \sigma_y^2 ,
$$

i.e., the familiar result that variances add in quadrature.
Since the expansion of $f$ in this case truncates at linear order, these results are exact.

````{prf:example} Inferring galactic distances---revisited
:label: example:BayesianAdvantage:inferring-galactic-distances-revisited

Consider, as a second example, the ratio of two parameters $Z = X/Y$ that appeared in {prf:ref}`example:BayesianAdvantage:inferring-galactic-distances` (in which we wanted to infer $d = v/H$). 

Applying {eq}`eq:gaussian_error_propagation`, the mean is

$$ 
 \mu_Z = \frac{\mu_X}{\mu_Y}
$$

and, with $f_X = 1/\mu_Y$ and $f_Y = -\mu_X/\mu_Y^2$, we find for the propagated variance

$$
  \sigma_Z^2 = \frac{\sigma_X^2}{\mu_Y^2} + \frac{\mu_X^2}{\mu_Y^4} \sigma_Y^2
$$

or

$$
  \frac{\sigma_Z^2}{\mu_Z^2} = \frac{\sigma_X^2}{\mu_X^2} + \frac{\sigma_Y^2}{\mu_Y^2},
$$

(we can take the square root to get the ratio of standard deviation to mean).
````

```{exercise} Linear combination of Gaussians
:label: exercise:BayesianAdvantages:gaussian-sum-of-errors

Consider $Z=aX+bY$, with $a$ and $b$ constants. Derive a PDF for $Z$ assuming Gaussian errors in $X$ and $Y$ and applying {eq}`eq:gaussian_error_propagation`. Compare with the result for $X+Y$ from the full convolution of  PDFs in {prf:ref}`example:BayesianAdvantage:Z=X+Y`.
```

```{exercise} Gaussian product of errors
:label: exercise:BayesianAdvantages:gaussian-product-of-errors

Consider $Z=XY$ and derive a PDF for $Z$ assuming Gaussian errors in $X$ and $Y$ and applying {eq}`eq:gaussian_error_propagation`. 
```

What if the first-order approximation is not enough? We can return to {eq}`eq:mu-Z-equation` and {eq}`eq:sigma-Z-equation` and keep the second-order terms in {eq}`eq:Z-expansion-second-order`.  We find improved formulas:

$$
\begin{aligned}
  \mu_Z &\approx f(\mu_X,\mu_Y) + \frac12 f_{XX}\sigma_X^2 + \frac12 f_{YY}\sigma_Y^2 \\
  \sigma_Z^2 &\approx f_X^2 \sigma_X^2 + f_Y^2 \sigma_Y^2 
  + \frac12 f_{XX}^2 (\sigma_X^2)^2 +  \frac12 f_{YY}^2 (\sigma_Y^2)^2 + f_{XY}^2 \sigma_X^2 \sigma_Y^2 .
\end{aligned}
$$ (eq:second-order-errors)

In this case it is relevant that we assumed independent Gaussian distributions for $X$ and $Y$.

```{exercise} Deriving second-order results
:label: exercise:BayesianAdvantages:second-order-error-propagation

Derive the results in {eq}`eq:second-order-errors`. You will need to use that the skewness for a Gaussian distribution is zero and that the kurtosis can be expressed in terms of the variance.
```

So where can these approximations fail?
The first-order approximation
can perform poorly for strongly nonlinear transformations (so that higher-order corrections are important), ratios with denominators near zero, or transformations that impose boundaries or produce substantial skewness.
The second-order corrections may help, but can also fail completely in some cases.
Consider the following example.


```{prf:example} Taking the square root of a number
:label: example:BayesianAdvantage:taking-square-root

This example was adapted from {cite}`Sivia2006`.
* Assume that the amplitude of a Bragg peak is measured with an uncertainty $A = A_0 \pm \sigma_A$ from a least-squares fit to experimental data.
* The Bragg peak amplitude is proportional to the square of a complex structure function: $A = |F|^2 \equiv f^2$.
* What is $f = f_0 \pm \sigma_f$?

If we blindly apply {eq}`eq:gaussian_error_propagation`, we find

$$
  f_0 = \sqrt{A_0}\, \quad \sigma_f^2 = \frac{\sigma_A^2}{4 A_0} .
$$

But what happens if the best fit gives $A_0 < 0$, which would not be impossible if we have weak and strongly overlapping peaks. The above equation obviously does not work since $f_0$ would be a complex number and the variance would be negative.

We have made two mistakes:
1. The likelihood is not the posterior!
2. The Gaussian error approximation around the peak does not always work.

Consider first the best fit of the signal peak. It implies that the likelihood can be approximated by

\begin{equation}
\pdf{\data}{A,I} \propto \exp \left[ -\frac{(A-A_0)^2}{2\sigma_A^2} \right].
\end{equation}

However, the posterior for $A$ is $\pdf{A}{{\data},I} \propto \pdf{\data}{A,I} \pdf{A}{I}$ and we should use the fact that we know that $A \ge 0$.

We will incorporate this information through a simple step-function prior

\begin{equation}
\pdf{A}{I} = \left\{
\begin{array}{ll}
\frac{1}{A_\mathrm{max}}, & 0 \le A \le A_\mathrm{max}, \\
0, & \mathrm{otherwise}.
\end{array}
\right.
\end{equation}

This implies that the posterior will be a truncated Gaussian, and its maximum will always be above zero.

This also implies that we cannot use the Gaussian error propagation approximation. Instead we will do the proper calculation using the transformation {eq}`eq:BayesianAdvantage:transformation`

\begin{equation}
p(f|{\data},I) = \pdf{A}{{\data},I} \left| \frac{dA}{df} \right| = 2 f \pdf{A}{{\data},I}
\end{equation}

In the end we find the proper Bayesian error propagation given by the PDF

\begin{equation}
p(f|{\data},I) \propto \left\{
\begin{array}{ll}
f \exp \left[ -\frac{(A-A_0)^2}{2\sigma_A^2} \right], & 0 \le f \le \sqrt{A_\mathrm{max}}, \\
0, & \mathrm{otherwise}.
\end{array}
\right.
\end{equation}

{numref}`fig-example-BayesianAdvantage-taking-square-root` visualizes the difference between the Bayesian and the naive error propagation for a few scenarios. The code to generate these plots is in the hidden cell below.

```

```{glue:figure} Af_fig
:name: fig-example-BayesianAdvantage-taking-square-root

The left-hand panels show the posterior PDF for the amplitude of a Bragg peak in three different scenarios. The right-hand plots are the corresponding PDFs for the modulus of the structure factor $f=\sqrt{A}$. The solid lines correspond to a full Bayesian error propagation, while the dashed lines are obtained with the short-cut error propagation.
The short-cut approximation works well for the first case, poorly for the second case, and fails completely for the third case where $A_0 < 0$.
```


```{code-cell} python3
:tags: [hide-cell]
import numpy as np
import matplotlib.pyplot as plt
from myst_nb import glue

def A_posterior(A,A0,sigA):
    pA = np.exp(-(A-A0)**2/(2*sigA**2))
    return pA/np.max(pA)

# Wrong analysis
def f_likelihood(f,A0,sigA):
    sigf = sigA / (2*np.sqrt(A0))
    pf = np.exp(-(f-np.sqrt(A0))**2/(2*sigf**2))
    return pf/np.max(pf)

# Correct error propagation
def f_posterior(f,A0,sigA):
    pf = f*np.exp(-(f**2-A0)**2/(2*sigA**2))
    return pf/np.max(pf)
    
fig_Af,axs=plt.subplots(3,2,figsize=(5,7))
for iA, (A0,sigA) in enumerate([(9,1),(1,9),(-20,9)]):
    maxA = max(2*A0,3*sigA)
    A_arr = np.linspace(0.01,maxA,100)
    f_arr = np.sqrt(A_arr)
    axs[iA,0].plot(A_arr,A_posterior(A_arr,A0,sigA))
    axs[iA,1].plot(f_arr,f_posterior(f_arr,A0,sigA),label='Bayesian')
    if A0>0:
        axs[iA,1].plot(f_arr,f_likelihood(f_arr,A0,sigA),'--',label='Naive')
    axs[iA,0].set(xlabel='A',ylabel=r'$p(A | \mathcal{D},I)$')
    axs[iA,0].text(0.95,0.8,f'$A_0={A0}$, $\sigma_A={sigA}$', \
    	horizontalalignment='right',\
    	transform=axs[iA,0].transAxes,fontsize=10)
    axs[iA,1].set(xlabel='f',ylabel=r'$p(f | \mathcal{D},I)$')
axs[0,1].legend(loc='best')
fig_Af.tight_layout()
glue(f"Af_fig", fig_Af, display=False)
```

## Solutions to exercises



```{solution} exercise:BayesianAdvantages:gaussian-sum-of-errors
:label: solution:BayesianAdvantages:gaussian-sum-of-errors
:class: dropdown

The PDF $\pdf{Z}{I}$ is Gaussian with mean $\expect{Z} = \mu_Z = a \mu_X + b \mu_Y$ and variance $\var{Z} = \sigma_Z^2 = a^2\sigma_Z^2 + b^2\sigma_Z^2$, where $\mu_X,\mu_Y$ and $\sigma_X^2, \sigma_Y^2$ are the means and variances of $X$ and $Y$, respectively.

For $a=b=1$ this is the same result as in {prf:ref}`example:BayesianAdvantage:Z=X+Y`, which should not be surprising since the errors were in fact Gaussian.
```

```{solution} exercise:BayesianAdvantages:gaussian-product-of-errors
:label: solution:BayesianAdvantages:gaussian-product-of-errors
:class: dropdown

The PDF $\pdf{Z}{I}$ is Gaussian with mean $\expect{Z} = \mu_Z = \mu_X \mu_Y$ and variance $\var{Z} = \sigma_Z^2 = \mu_Y^2 \sigma_X^2 + \mu_X^2 \sigma_Y^2$, where $\mu_X,\mu_Y$ and $\sigma_X^2, \sigma_Y^2$ are the means and variances of $X$ and $Y$, respectively.
```


```{solution} exercise:BayesianAdvantages:second-order-error-propagation
:label: solution:BayesianAdvantages:second-order-error-propagation
:class: dropdown

We get the second-order expression for $\mu_Z$ immediately by applying {eq}`eq:mu-Z-equation` and {eq}`eq:variance-abbreviations`.

For the variance, when applying {eq}`eq:sigma-Z-equation` we need to remember to apply both the expansion of $Z$ *and* the expansion of $\mu_Z$ to second order. Once squared, there will be expectation values of third-order terms and fourth-order terms; after using independence to factorize terms, any expectation value of an odd power of $\delta X$ or $\delta Y$ vanishes for zero-mean Gaussian distributions (mean and skewness are both zero).
As before, any expectation value of quadratic terms yields variances, but now we have $\expect{(\delta X)^4} = 3(\sigma_X^2)^2$ and $\expect{(\delta Y)^4} = 3(\sigma_Y^2)^2$ for Gaussian distributions. When the dust settles, terms like $f_{XX} f_{YY}\sigma_X^2 \sigma_Y^2$ will have canceled and the factors work out to reproduce {eq}`eq:second-order-errors`.
```




