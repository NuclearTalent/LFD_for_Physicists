# Important definitions

The set of all possible outcomes of an experiment is known as the sample space and is here denoted by $S$. We can think of events $A$ as subsets of the sample space.

Whenever $A$ and $B$ are events that we are interested in, then we can also reasonably concern ourselves with the events ($A \cap B$), ($A \cup B$), and ($\bar{A}$) which correspond to ($A$ and $B$), ($A$ or $B$), and (not $A$), respectively.

(introduction:definitions)=
## The probability measure

```{prf:definition} Probability measure
:label: definition:probability-measure

A probability measure is a function $\prob : A \to [0,1]$ satisfying
  
* $\prob (S)=1$
* $\prob (\emptyset)=0$
* If $A_1, A_2, \ldots A_n$ is a collection of disjoint events, such that $A_i \cap A_j = \emptyset$ for all $i \neq j$, then
  $\prob \left( \cup_{i=1}^n A_i \right) = \sum_{i=1}^n \prob (A_i)$.
```  
    
  
In particular, we will often consider the probability for two events to be true $\prob (A \cap B)$. For brevity, we will often use the simpler notation $\prob (A, B)$.
  
    
    
```{prf:definition} Independent events
:label: definition:independent-events

Two events $A$ and $B$ are independent if

\begin{equation}
  \prob (A, B) = \prob (A)\prob (B)
\end{equation}
```
  
  
  
```{prf:definition} Conditional probability
:label: definition:conditional-probability

Given $\prob (A) > 0$ we define the conditional probability of $B$ given $A$ as

$$
  \cprob{B}{A} = \frac{\prob (A, B)}{\prob (A)}.
$$ (eq:Statistics:conditional-probability)

Alternatively this can be expressed via the **product rule** of probability theory

$$
\prob (A, B) = \cprob{B}{A} \prob (A).
$$ (eq:Statistics:product-rule)
  
```

Given $\prob (A) > 0$ we have that $A$ and $B$ are independent if and only if $\cprob{B}{A} = \prob (B)$.

The **total law of probability** can be obtained from the disjoint-union property of {prf:ref}`definition:probability-measure` and the product rule {eq}`eq:Statistics:product-rule`. Consider a partition $B_1, B_2, \ldots, B_n$ of the complete state space (meaning that $B_i \cap B_j = \emptyset$ for all $i \neq j$ and $\sum_{i=1}^n \prob (B_i) = 1$) such that $\prob (B_i) > 0$ for all $i$. Then

$$
\prob (A) = \sum_{i=1}^n \cprob{A}{B_i} \prob (B_i) = \sum_{i=1}^n \prob (A, B_i). 
$$ (eq:Statistics:discrete-total-probability)
  
This process of summing over all possible states of an event in a joint probability to obtain the **marginal** probability of the other event is known as marginalization. 

A simple example of this law would be the statement

> The total probability that it rains tomorrow is the sum of the probability that it rains tomorrow and that it rains today plus the probability that it rains tomorrow and not today.

Each of those joint probabilities can be factorized according to the product rule. For example, the probability that it rains tomorrow and that it rains today is the conditional probability of raining tomorrow given that it rains today times the probability that it rains today.

The point here is that the total probability of rain tomorrow is the sum of those two terms since the two events "it rains today" and "it does not rain today" form a complete and exhaustive partition of outcomes of the experiment "will it rain today?".

## Random variables: probability distribution and density

Let us introduce the concept of random variables and use those to introduce probability distribution and density functions. 
  
```{prf:definition} Random variable and distribution function
:label: definition:random-variable

A random (or stochastic) variable is a function $X: S \to \mathbb{R}$.

The **distribution function** $P$ for a random variable $X$ is the function $P : \mathbb{R} \to [0,1]$, given by
  
\begin{equation}
    P(x) = \prob (X \leq x).
\end{equation}
  
We can write $P_X(x)$ where it is necessary to emphasize the role of $X$.
```


```{prf:definition} Joint probability distribution
:label: definition:joint-probability-distribution

The joint distribution function of a vector $\boldsymbol{X}$ of random variables $\boldsymbol{X} = (X_1, X_2, \ldots, X_n)$ is the function $P : \mathbb{R}^n \to [0,1]$ given by

\begin{equation}
P(\boldsymbol{x}) = \prob (\boldsymbol{X} \leq \boldsymbol{x}), \qquad x \in \mathbb{R}^n. 
\end{equation}

We can write $P_{\boldsymbol{X}}$ where it is necessary to emphasize the role of $\boldsymbol{X}$.
```

For random variables that are continuous it will be very useful to work with probability densities. Let us define those, starting however with the corresponding quantity (probability mass) for discrete random variables.

```{prf:definition} Probability mass function
:label: definition:probability-mass-function

The random variable $X$ is called **discrete** if it takes values only in some countable subset $\{ x_1, x_2, \ldots\}$ of $\mathbb{R}$. The function $p : \mathbb{R} \to [0,1]$, given by

\begin{equation}
    p(x) = \prob (X = x),
\end{equation}

is known as its **probability mass function**. Again, we can write $p_X(x)$ where it is necessary to emphasize the role of $X$.

The **joint probability mass function** of a random vector $\boldsymbol{X} = (X_1, X_2, \ldots, X_n)$ is the function $p : \mathbb{R}^n \to [0,1]$ given by

\begin{equation}
p(x_1, x_2, \ldots, x_n) = \prob (X_1=x_1, X_2=x_2, \ldots, X_n=x_n). 
\end{equation}
```



```{prf:definition} Probability density function
:label: definition:probability-density-function

The random variable $X$ is called **continuous** if its distribution function can be expressed as

\begin{equation}
P(x) = \int_{-\infty}^x p(z) dz, \qquad x \in \mathbb{R}, 
\end{equation}

for some integrable function $p : \mathbb{R} \to [0,\infty)$ called the **probability density function** (PDF). Again, we can write $p_X(x)$ where it is necessary to emphasize the role of $X$.

The **joint probability density function** of a random vector $\boldsymbol{X} = (X_1, \ldots, X_n)$ of continuous variables is the function $p : \mathbb{R}^n \to [0,\infty)$ given by

\begin{equation}
P(x_1, \ldots, x_n) = \int_{u_1=-\infty}^{x_1} \ldots \int_{u_n=-\infty}^{x_n} p(u_1, \ldots, u_n) du_1, \ldots, du_n. 
\end{equation}

```

Note that we will not differentiate in notation between probability mass and density functions as the context should make it clear whether it describes the probability density of a discrete or continuous variable. We will also refer to both as a PDF.

While discrete examples tend to be simpler, situations with continuous variables are more common in physics. 

Following the above definition, there are some properties that all PDFs must have. Here we list some important ones using the simplest example of a single (continuous) random variable $X$ 

1. The first one is positivity
   \begin{equation}
	0 \leq p(x).
	\end{equation}

	Naturally, it would be nonsensical for any of the values of the domain to occur with a probability density less than $0$. 
2. Also, the PDF must be normalized. That is, all the probabilities must add up
to one.  The probability of *anything* to happen is always unity. For a continuous PDF this condition is

   \begin{equation}
	\int_{-\infty}^\infty p(x)\,dx =  1.
   \end{equation}
   
   The corresponding condition for a discrete PDF is $\sum_{i} p(x_i) =  1$.
3. The probability for *any* specific outcome $x$ of a continuous variable $X$ is zero

   \begin{equation}
	\prob (X=x) =  0, \qquad \text{for all } x \in \mathbb{R},
   \end{equation}
   
   since probabilities will be computable from the integral measure $p(x) dx$ and $\prob (X=x)$ would correspond to $dx \to 0$. 
 
4. Instead it makes more sense to discuss the probability for the outcome being within a domain. E.g., for the univariate case we can quantify

   \begin{equation}
	\prob (a \leq X \leq b) =  \int_a^b p(x) dx. 
   \end{equation}
   
   From which we can also note that PDFs are not dimensionless objects. We must have $[p(x)] = [x]^{-1}$ for the integral to produce a dimensionless probability.

These properties can be generalized to the multivariate case $p(x_1, x_2, \ldots)$.

For the multivariate case we also introduce the important concepts of **marginalization** and **independence** .



```{prf:property} Marginal density functions
:label: property:marginal-density-functions

Given a joint density function $p(x,y)$ of two random variables $X$ and $Y$, the (marginal) probability density function of $X$ is obtained via marginalization

\begin{equation}
p(x) = \int_{-\infty}^\infty p(x,y) dy,
\end{equation}

and vice versa for $p(y)$. 
```



Marginalization is a very powerful technique as it allows to extract probabilites for a variable of interest when dealing with multivariate problems. 



```{prf:property} Independence
:label: property:independence

Two random variables $X$ and $Y$ are independent if (and only if) the joint density function factorizes

$$
p(x,y) = p(x) p(y).
$$ (eq:Statistics:independence)

```

Suppose that $X$ and $Y$ have the joint distribution function $p(x,y)$. We wish to discuss the conditional probability distribution of $Y$ given that $X$ takes the value $x$. However, we need to be careful since the event $X=x$ has zero probability. Instead, we can consider the event $x \leq X \leq x+dx$ which leads to the following definition

```{prf:definition} Conditional probability-distribution
:label: definition:conditional-probability-distribution

The conditional distribution function of $Y$ given $X=x$ is

\begin{equation}
  P_{Y \vert X}(y \vert x) = \int_{-\infty}^y \frac{p(x,y')}{p_X(x)} dy'
\end{equation}

for any $x$ such that $p_X(x) > 0$.
```

The integrand is then defined as the conditional PDF

\begin{equation}
p_{Y \vert X}(y \vert x) = \frac{p(x,y)}{p_X(x)} = \frac{p(x,y)}{\int_{-\infty}^{\infty} p(x,y) dy},
\end{equation}

for any $x$ such that $p_X(x)>0$.

```{note}
Probability densities are usually introduced in the context of random variables (as we did here). However, from the Bayesian viewpoint, probabilities are used more generally to describe our state of knowledge. This means, for example, that we will use probability densities to quantify our knowledge of physics model parameters. Such a PDF would not make sense in an approach that requires randomness in considered variables.
```


(sec:ExpectationValuesAndMoments)=
## Expectation values and moments

```{prf:definition} Expectation value
:label: definition:expectation-value

Let $h(x)$ be an arbitrary continuous function on the domain $\mathbb{R}$ of the continuous, random
variable $X$ whose PDF is $p(x)$. We define the *expectation value*
of $h$ with respect to $p$ as follows

\begin{equation}
\mathbb{E}_p[h] = \int_{-\infty}^\infty \! h(x)p(x)\,dx .
\end{equation}

The corresponding definition for a discrete variable $X$ is

\begin{equation}
\mathbb{E}_p[h] =  \sum_{i}\! h(x_i)p(x_i) .
\end{equation}

```

Note that we usually drop the index $p$ and just write $\mathbb{E}[h]$.  

A particularly useful class of expectation values are the **moments**. The $n$-th moment of the PDF $p(x)$ is defined as follows

\begin{equation}
\mathbb{E}[X^n] = \int_{-\infty}^\infty \! x^n p(x)\,dx
\end{equation}

The zero-th moment $\mathbb{E}[1]$ is just the normalization condition of
$p$. The first moment, $\mathbb{E}[X]$, is called the **mean** of $p$
and is often denoted by the greek letter $\mu$

$$
\mathbb{E}[X] \equiv \mu \equiv \int_{-\infty}^\infty x p(x)dx,
$$ (eq:Statistics:mean)

for a continuous distribution and 

\begin{equation}
\mathbb{E}[X] \equiv \mu \equiv \sum_{i} x_i p(x_i),
\end{equation}

for a discrete distribution. 

Qualitatively it represents the average value of the
PDF and is therefore sometimes called the expectation value of $p(x)$.

(sec:CentralMoments)=
## Central moments: Variance and Covariance

Another special case of expectation values is the set of **central moments**, with the $n$-th central moment defined as

\begin{equation}
\mathbb{E}\left[ \left( X - \mathbb{E}[X] \right)^n \right] = \int_{-\infty}^\infty \! \left( x-\mathbb{E}[X] \right)^n p(x)\,dx .
\end{equation}

The zero-th and first central moments are both trivial; equal to $1$ and
$0$, respectively. Instead, the second central moment is of particular interest. 



```{prf:definition} Variance
:label: definition:variance

The **variance**  of a random variable $X$ is usually denoted $\sigma^2$ or Var$(X)$ and is defined as 

\begin{equation}
\text{Var}(X) \equiv \sigma^2  \equiv \mathbb{E}\left[ \left( X - \mathbb{E}[X] \right)^2 \right]
\end{equation}

```

We note that

\begin{align}
\sigma^2 &= \int_{-\infty}^\infty (x-\mathbb{E}[X] )^2 p(x)dx\\
&=  \int_{-\infty}^\infty \left(x^2 - 2 x \mathbb{E}[X] +\mathbb{E}[X]^2\right)p(x)dx \\
& =  \mathbb{E}[X^2]  - 2 \mathbb{E}[X] \mathbb{E}[X]  + \mathbb{E}[X]^2 \\
&=  \mathbb{E}[X^2]  - \mathbb{E}[X]^2
\end{align}

The positive square root of the variance, $\sigma = +\sqrt{\sigma^2}$ is called the 
**standard deviation** of $p$. It is the root-mean-square (RMS)
value of the deviation of the PDF from its mean value, interpreted
qualitatively as the "spread" of $X$ around its mean.

When dealing with two random variables it is useful to introduce the **covariance**



```{prf:definition} Covariance and correlation
:label: definition:covariance-correlation

The **covariance**  of two random variables $X$ and $Y$ is usually denoted $\sigma_{XY}^2$ or $\text{Cov}(X,Y)$ and is defined as 

\begin{equation}
\text{Cov}(X,Y) \equiv \sigma_{XY}^2 \equiv \mathbb{E}\left[ \left( X - \mathbb{E}[X] \right) \left( Y - \mathbb{E}[Y] \right)  \right].
\end{equation}

The **correlation coefficient** of $X$ and $Y$ is defined as

\begin{equation}
\rho_{XY} \equiv \frac{\text{Cov}(X,Y)}{\sqrt{\text{Var}(X)\text{Var}(Y)}},
\end{equation}

as long as the variances are non-zero.

```


You can show that the correlation coefficient is $-1 \leq \rho \leq 1$. In particular, the diagonal covariance is the variance and therefore $\rho_{XX} = 1$.

Two variables $X$ and $Y$ are called *uncorrelated* if Cov$(X,Y)=0$. Note that the independence property of Eq. {eq}`eq:Statistics:independence` implies that two independent variables are always uncorrelated. However, the converse is not necessarily true.

