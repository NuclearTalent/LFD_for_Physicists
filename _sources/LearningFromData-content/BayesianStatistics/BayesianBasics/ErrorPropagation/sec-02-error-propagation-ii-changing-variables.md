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

(sec:BayesianAdvantages:ChangingVariables)=
# Error propagation (II): Changing variables

Let us consider a single variable $X$ and a function $Y=f(X)$ that offers a unique mapping between $X$ and $Y$. Assume that we know $X$ via a PDF $\pdf{x}{I}$. What is the relation between $\pdf{x}{I}$ and $\pdf{y}{I}$? In this scenario the extraction of $\pdf{y}{I}$ turns out to be an exercise in transformation of variables.

Consider a point $x^*$ and a small interval $\delta x$ around it. The probability that $X$ lies within that interval can be written

\begin{equation}
\pdf{x^* - \frac{\delta x}{2} \le x < x^* + \frac{\delta x}{2}}{I}
\approx \pdf{x=x^*}{I} \delta x.
\end{equation}

Assume now, as stated above, that the function $f$ maps the point $x=x^*$ uniquely onto $y=y^*=f(x^*)$. Then there must be an interval $\delta y$ around $y^*$ so that the probability is conserved

\begin{equation}
\pdf{x=x^*}{I} \delta x = \pdf{y=y^*}{I} \delta y.
\end{equation}

In the limit of infinitesimally small intervals, and with the realization that this should be true for any point $x$, we obtain the relationship

$$
\pdf{x}{I} = p(y=y(x)|I) \left| \frac{dy}{dx} \right|,
$$ (eq:BayesianAdvantage:transformation)

where the term on the far right is called the *Jacobian*. We also note that we can inverse the transformation

$$
\pdf{y}{I} = \pdf{x(y)}{I} \left| \frac{dx}{dy} \right|,
$$ (eq:BayesianAdvantage:inverse-transformation)

The generalization to several variables, relating the PDF for $M$ variables $\{ Xx_j \}$ in terms of the same number of quantities $\{ y_j \}$ related to them, is

$$
p(\{x_j\}|I) = p(\{y_j\}|I) \left| \frac{\partial (y_1, y_2, \ldots, y_M)}{\partial (x_1, x_2, \ldots, x_M)} \right|,
$$ (eq:BayesianAdvantage:multivariate-transformation)

where the multivariate Jacobian is given by the determinant of the $M \times M$ matrix of partial derivatives $\partial y_i / \partial x_j$.

```{exercise} The standard random variable
:label: exercise:BayesianAdvantages:standard-random-variable

Find $\pdf{z}{I}$ when $Z = (X-\mu)/\sigma$ and $\pdf{x}{I} = \frac{1}{\sqrt{2\pi}\sigma} \exp \left( -\frac{(x-\mu)^2}{2\sigma^2} \right)$. 
```
```{exercise} The square root of a number
:label: exercise:BayesianAdvantages:square-root-of-a-number

Find an expression for $\pdf{z}{I}$ when $Z = \sqrt{X}$ and $\pdf{x}{I} = \frac{1}{x_{\max} - x_{\min}}$ for $x_{\min} \leq x \leq x_{\max}$ and 0 elsewhere. Verify that $\pdf{z}{I}$ is properly normalized.
```


```{admonition} Summary
:class: tip 
We have now seen the basic ingredients required for the propagation of errors: it either involves a transformation in the sense of Eq. {eq}`eq:BayesianAdvantage:multivariate-transformation` or an integration as in Eq. {eq}`eq:BayesianAdvantage:marginalization`.
```


