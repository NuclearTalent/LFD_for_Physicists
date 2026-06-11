---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

# Exercises

```{exercise} Random and colorblind
:label: exercise:Statistics:colorblind

The gene responsible for color blindness is located on the X chromosome. In other words, red-green color blindness is an X-linked recessive condition and is much more common in males (with only one X chromosome).
According to the Howard Hughes medical institute about 7% of men and 0.4% of women are red-green colorblind. Furthermore, sccording to SCB, the Swedish population is 50,3% male and 49,7% female. What is the probability that a person selcted at random is colorblind?
```

```{exercise} Conditional discrete probability mass function
:label: exercise:Statistics:conditional-discrete-pmf

The joint probability mass function of the discrete variables $X,Y$ is

$$
p(x,y) = \frac{x+y}{18}, \quad \text{for } x,y \in \{0,1,2\}.
$$

- Find the conditional probability mass function $\pdf{y}{x}$. 
- Verify that it is properly normalized.
```

```{exercise} Conditional probability for continuous variables
:label: exercise:Statistics:conditional-probability-continuous

The continuous random variables $X,Y$ have the joint density

$$
p(x,y) = e^{-x}, \quad \text{for } 0 < y < x < \infty.
$$

Find the probability $\cprob{Y<2}{X=5}$.
```

```{exercise} Conditional expectation
:label: exercise:Statistics:conditional-expectation

Assume that the continuous random variables $X,Y$ have the joint density

$$
\p{x,y} = \frac{2}{xy}, \quad \text{for } 1 < y < x < e.
$$

Find the conditional expectation $\expect{Y \vert X=x}$.
```

## Solutions

```{solution} exercise:Statistics:colorblind
:label: solution:Statistics:colorblind
:class: dropdown

Let $C$, $M$, $F$ denote the events that a random person is colorblind, male, and female, respectively. By the law of total probability

\begin{align*}
\prob{(C)} &= \cprob{C}{M}\prob{(M)} + \cprob{C}{F}\prob{(F)} \\
&(0.07)(0.503) + (0.004)(0.497) = 0.037.
\end{align*}
```

```{solution} exercise:Statistics:conditional-discrete-pmf
:label: solution:Statistics:conditional-discrete-pmf
:class: dropdown

The conditional probability mass function can be obtained from the ratio

$$
\pdf{y}{x} = \frac{p(x,y)}{p(x)}.
$$

Let us therefore find the marginal probability mass function

$$
p(x) = \sum_{y=0}^2 p(x,y) = \frac{x}{18} + \frac{x+1}{18} + \frac{x+2}{18} = \frac{x+1}{6}.
$$

Thus we get $\pdf{y}{x} = \frac{(x+y)/18}{(x+1)/6} = \frac{x+y}{3(x+1)}$ for $y \in \{0,1,2\}$.

We find that this pdf (over $y$) is properly normalized since

$$
\sum_{y=0}^2 \pdf{y}{x} = \frac{x+0+x+1+x+2}{3(x+1)} = 1.
$$ 
```

```{solution} exercise:Statistics:conditional-probability-continuous
:label: solution:Statistics:conditional-probability-continuous
:class: dropdown

The desired probability is

$$
\cprob{Y<2}{X=5} = \int_0^2 p_{Y|X}(y \vert 5) dy.
$$

To find the conditional density $p_{Y|X}(y \vert x)$ we need the marginal one

$$
\p{x} = \int_0^\infty \p{x,y} dy = \int_0^x e^{-x} dy = x e^{-x},
$$

for $x > 0$. This gives

$$
p_{Y|X}(y \vert x) = \frac{\p{x,y}}{\p{x}} = \frac{e^{-x}}{x e^{-x}} \frac{1}{x},
$$

for $0 < y < x$. Note that this is a uniform distribution for $y$ given $x$. Therefore

$$
\cprob{Y<2}{X=5} = \int_0^2 \frac{1}{5} dy = \frac{2}{5}.
$$
```

```{solution} exercise:Statistics:conditional-expectation
:label: solution:Statistics:conditional-expectation
:class: dropdown

We need the marginal density

$$
\p{x} = \int_1^x \frac{2}{xy} dy = \frac{2 \ln x}{x}, \quad \text{for } 1 < x < e,
$$

to get the conditional one

$$
p_{Y|X}(y|x) = \frac{2/xy}{2 \ln x / x} = \frac{1}{y\ln x}, \quad \text{for } 1 < y < x.
$$

The conditioned expectation is therefore

$$
\expect{Y \vert X=x} = \int_1^x y p_{Y|X}(y|x)  dy = \int_1^x \frac{y}{y\ln x} dy = \frac{x-1}{\ln x}.
$$
```

