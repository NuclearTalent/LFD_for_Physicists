---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:BayesianAdvantages:ChangingVariables)=
# Changing variables

Let us consider a single variable $X$ and a function $Y=f(X)$ that offers a unique mapping between $X$ and $Y$. Assume that we know $X$ via a PDF $\pdf{x}{I}$. What is the relation between $\pdf{x}{I}$ and $\pdf{y}{I}$? In this scenario the extraction of $\pdf{y}{I}$ turns out to be an exercise in transformation of variables.

Consider a small interval between a point $x^*$ and $x^* + \delta x$. The probability that $X$ lies within that interval can be written

$$
\pdf{x^* \le x < x^* + \delta x}{I}
\approx \pdf{x=x^*}{I} \delta x.
$$

This probability can't depend on how the interval is parametrized, so it must be the same as the probability between $y^*$ and $y^* + \delta y$, where $y^* = f(x^*)$ and $y^* + \delta y = f(x^*+\delta x)$. Thus, we have

$$
\pdf{x=x^*}{I} \delta x = \pdf{y=y^*}{I} \delta y.
$$

In the limit of infinitesimally small intervals, and with the realization that this should be true for any point $x$, we obtain the relationship

$$
\pdf{x}{I} = p(y=y(x)|I) \left| \frac{dy}{dx} \right|,
$$ (eq:BayesianAdvantage:transformation)

where the term on the far right is called the *Jacobian*. We also note that we can invert the transformation

$$
\pdf{y}{I} = \pdf{x(y)}{I} \left| \frac{dx}{dy} \right|.
$$ (eq:BayesianAdvantage:inverse-transformation)

The generalization to several variables, relating the PDF for $M$ variables $\{ x_j \}$ in terms of the same number of quantities $\{ y_j \}$ related to them, is

$$
p(\{x_j\}|I) = p(\{y_j\}|I) \left| \frac{\partial (y_1, y_2, \ldots, y_M)}{\partial (x_1, x_2, \ldots, x_M)} \right|,
$$ (eq:BayesianAdvantage:multivariate-transformation)

where the term on the far right is called the Jacobian of the transformation from $x$ to $y$.
In general it is given by the determinant of the $M \times M$ matrix of partial derivatives $\partial y_i / \partial x_j$. 

Note that {eq}`eq:BayesianAdvantage:transformation` is also how physical densities transform: if I know the mass density per unit length in variable $x$, but I want it in variable $y$, the relationship between the two is exactly {eq}`eq:BayesianAdvantage:transformation`. $p(x|I)$ and $p(y=y(x)|I)$ are not the same distribution because they're probability densities, not probabilities.


```{admonition} Summary
:class: tip 
We have now seen the basic ingredients required for the propagation of errors: it either involves a transformation in the sense of Eq. {eq}`eq:BayesianAdvantage:multivariate-transformation` or an integration as in Eq. {eq}`eq:BayesianAdvantage:marginalization`.
```



```{exercise} The standard random variable
:label: exercise:BayesianAdvantages:standard-random-variable

Find $\pdf{z}{I}$ when $Z = (X-\mu)/\sigma$ and $\pdf{x}{I} = \frac{1}{\sqrt{2\pi}\sigma} \exp \left( -\frac{(x-\mu)^2}{2\sigma^2} \right)$. 
```
```{exercise} The square root of a number
:label: exercise:BayesianAdvantages:square-root-of-a-number

Find an expression for $\pdf{z}{I}$ when $Z = \sqrt{X}$ and $\pdf{x}{I} = \frac{1}{x_{\max} - x_{\min}}$ for $x_{\min} \leq x \leq x_{\max}$ and 0 elsewhere. Verify that $\pdf{z}{I}$ is properly normalized.
```


## Solutions to exercises


```{solution} exercise:BayesianAdvantages:standard-random-variable
:label: solution:BayesianAdvantages:standard-random-variable
:class: dropdown

The transformation $z = f(x) = (x-\mu)/\sigma$ gives the inverse $x = f^{-1}(z) = \sigma z + \mu$ and the Jacobian $|dx/dz = \sigma|$.

Therefore $\pdf{z}{I} = \pdf{x}{I} \sigma$. With the given form of $\pdf{x}{I}$ we get

$$
\pdf{z}{I} = \frac{1}{\sqrt{2\pi}} \exp \left( -\frac{z^2}{2}\right),
$$

which corresponds to a Gaussian distribution with mean zero and variance one, sometimes known as a standard random variable.
```

```{solution} exercise:BayesianAdvantages:square-root-of-a-number
:label: solution:BayesianAdvantages:square-root-of-a-number
:class: dropdown

With $z = f(x) = \sqrt{x}$ we have $x = f^{-1}(z) = z^2$ such that $|dx/dz| = 2|z|$. We note that $z$ is positive such that $|z| = z$ and we therefore have

$$
\pdf{z}{I} = 2 z \pdf{x}{I} = 2 z \frac{1}{x_{\max} - x_{\min}} \quad \text{for } \sqrt{x_{\min}} \leq z \leq \sqrt{x_{\max}},
$$

and 0 elsewhere. 

We check the normalization by performing the integral

$$
\int_0^\infty \pdf{z}{I}\, dz = \int_{\sqrt{x_{\min}}}^{\sqrt{x_{\max}}} \frac{2z}{x_{\max} - x_{\min}}\, dz = \frac{1}{x_{\max} - x_{\min}} \left[ z^2 \right]_{\sqrt{x_{\min}}}^{\sqrt{x_{\max}}} = 1.
$$
```


