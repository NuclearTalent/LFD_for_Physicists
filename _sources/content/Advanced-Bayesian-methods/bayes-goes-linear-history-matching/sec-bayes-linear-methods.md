# Bayes linear methods

```{Admonition} Bayes linear statistics
:class: tip
Bayes linear methods are subjective statistical analyses based on expectation and covariance structures, rather than on distributional assumptions.

The use of the word linear refers to Bruno de Finetti's arguments that probability theory is a linear theory (he argued against the more common measure theory approach).
```

The full Bayesian approach requires a complete, probabilistic enumeration of all possible outcomes. In practice. for scientific applications, this usually translates to the use of probability distributions to capture all prior knowledge as well as the statistical model that goes into the data likelihood. Such a specification can often be largely arbitrary.

Bayes linear methodology is similar in spirit to the standard Bayes analysis, but is constructed so as to avoid much of the burden of specification and computation of a fully Bayesian analysis. The aim is to develop a methodology which allows to state and analyse relatively small, carefully chosen collections of quantitative judgements that are within our ability to specify in a meaningful way.

We will in particular restrict ourselves to specifying mean values and covariances for a set $\mathcal{Z} = \{ Z_1, Z_2, \ldots, Z_M \}$ of (random) quantities, for which we shall make statements of uncertainty. For each $Z_i, Z_j \in \mathcal{Z}$ we specify

1. The expectation $\expect{Z_i}$, giving a simple quantification of our belief as to the magnitude of $Z_i$;
1. The variance $\var{Z_i}$, quantifying our uncertainty or degree of confidence in our judgements of the magnitude of $Z_i$;
1. The covariance $\cov{Z_i}{Z_j}$, expressing a judgement on the relationship between the quantities, quantifying the extent to which observation on $Z_j$ may (linearly) influence our belief as to the size of $Z_i$.

This restricted collection of belief statements then replaces the full specification of $\p{\mathcal{Z}}$.

For a thorough reference on Bayes linear methods, see the textbook *"Bayes Linear Statistics: Theory and Methods"** by Michael Goldstein and David Wooff {cite}`Goldstein2007`.

## Pukelsheim's three-sigma rule

While avoiding the full probabilistic treatment, it is still possible to make some quantitative statements using expectation values and (co)variances as ingredients in general probability inequalities. The most famous one is Pukelsheim's three-sigma rule which we will now discuss. For a full derivation, the reader is encouraged to study Pukelheim's paper from 1994 {cite}`Pukelsheim:1994` that also contains the original references. The original bound is due to Vysochanskii and Petunin (1980, 1983).

Consider a random varable $X$ with mean value $\mu = \expect{X}$ and variance $\sigma^2 = \var{X}$. A very general inequality was provided by Bienaymé (1853) and Chebyshev (1867) about the probability that $X$ falls outside of a radius $r > 0$,

\begin{equation}
\prob(|X-\mu| \geq r) \leq \frac{\sigma^2}{r^2}.
\end{equation}

This is a rough bound. For example, we find that the probability of finding $X$ outside of $r = 3\sigma$ is smaller than or equal to $1/9 \approx 11\%$.

It is possible to find a tighter constraint with an additional assumption. For a unimodal distribution, the probability density is non-decreasing up to the mode, and non-increasing after. For this class, the bound becomes more than halved 

$$
\prob(|X-\mu| \geq r) \leq \frac{4}{9} \frac{\sigma^2}{r^2} \quad \text{for } r > \sqrt{\frac{8}{3}} \sigma \approx 1.63 \sigma.
$$ (eq:BayesLinear:unimodal-bound)

In particular, for $r = 3\sigma$ we get the celebrated Pukelsheim's three-sigma rule.

```{Admonition} Pukelsheim's three-sigma rule
:class: tip
The probability for a random quantity $X$ to fall away from its mean $\mu$ by more than three standard deviations $3\sigma$ is at most 5%,

$$
\prob(|X-\mu| \geq 3\sigma) \leq \frac{4}{81} < 0.05,
$$

given that $X$ is described by a unimodal probability density function.
```
