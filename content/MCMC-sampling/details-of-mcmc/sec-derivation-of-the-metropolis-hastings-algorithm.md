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

(sec:MetropolisHastings)=
# Derivation of the Metropolis-Hastings algorithm

How can we collect random samples from an arbitrary probability distribution $p(\pars)$? In particular, how can we perform this task when we might not even have a closed form expression for the PDF? It is common in Bayesian inference that we find ourselves in the situation that we can evaluate $p(\pars)$ at any position $\pars$, but we don't know beforehand if it will be large or small.

We will now show that it is possible to construct a Markov chain that has $p(\pars)$ as its stationary distribution. Once this chain has converged it will provide us with samples from $p(\pars)$. 

As we have learned, the evolution of positions is described by the transition density $T$. The generalization to continuous variables of the stationary-chain equilibrium described in Eq. {eq}`eq:MarkovChains:discrete-equlibrium` is

\begin{equation}
p(\pars) = \int_{\Omega'} p(\pars')T(\pars',\pars) d\pars'.
\end{equation}

This equilibrium condition can be replaced with the more stringent **detailed-balance** condition

$$
p(\pars)T(\pars,\pars') = p(\pars') T(\pars',\pars),
$$ (eq:MCMC:detailed-balance)

which can be understood from the integral relation

\begin{equation}
\int d\pars' p(\pars)T(\pars,\pars') = \int d\pars' p(\pars') T(\pars',\pars),
\end{equation}

that describes the balance between the transitions of probability density out of $\pars$ and into $\pars$. At equilibrium, these integrals must be equal.


The trick to achieve this for a certain $p(\pars)$ is to write $T$ as a product of a simple step proposal function $S(\pars,\pars')$, that provides probability densities for steps in $\pars$-space, and a function $A(\pars,\pars')$ that we will call the **acceptance probability**

\begin{equation}
T(\pars,\pars') = A(\pars,\pars') S(\pars,\pars').
\end{equation}

The step proposal function can be almost anything, but a key property is that it should be easy to draw a sample from it. The probability for proposing a new position $\pars'$ will depend on the current position $\pars$

\begin{equation}
\pdf{\text{proposing $\pars'$}}{\text{current position}=\pars} = S(\pars,\pars')
\end{equation}

For example, assuming that $\pars$ is a vector in a $D$-dimensional parameter space we can take $S(\pars,\pars')$ to be a uniform distribution within a $D$-dimensional hypercube with side length $\Delta$

\begin{equation}
S(\pars,\pars') = \left\{ 
\begin{array}{ll}
\frac{1}{\Delta^D} & \text{if $\left| \pars'_i - \pars_i \right| \leq \frac{\Delta}{2}$ for all $i \in \{1, \ldots, D\}$} \\
0 & \text{otherwise}
\end{array}
\right.
\end{equation}

Alternatively we can use a multivariate Gaussian distribution with a mean that corresponds to the current position $\pars$ and a covariance matrix that we can specify. 

The probability of actually accepting the proposed step from $\pars$ to $\pars'$ will then be given by $0 \leq A(\pars,\pars') \leq 1$.

The detailed balance condition {eq}`eq:MCMC:detailed-balance` can be fulfilled by placing the following condition on the acceptance probability

\begin{equation}
\frac{A(\pars,\pars')}{A(\pars',\pars)} = \frac{p(\pars')S(\pars',\pars)}{p(\pars)S(\pars,\pars')}.
\end{equation}

The expression for $A$ that fulfils this condition is

\begin{equation}
A(\pars,\pars') = \text{min} \left( \frac{p(\pars')S(\pars',\pars)}{p(\pars)S(\pars,\pars')},1\right),
\end{equation}

and holds the probability by which we decide whether to accept the proposed position $\pars'$, or remain in the old one $\pars$. The ratio that appears in the acceptance probability is called the Metropolis-Hastings ratio and will here be denoted $r$. We note that it gets further simplified for symmetric proposal functions (for which it is sometimes referred to as the Metropolis ratio)

$$
r = \left\{
\begin{array}{ll}
\frac{p(\pars')S(\pars',\pars)}{p(\pars)S(\pars,\pars')} 
& \text{for general proposal functions}, \\
\frac{p(\pars')}{p(\pars)}
& \text{for symmetric proposal functions}.
\end{array}
\right.
$$ (eq:MCMC:metropolis-ratio)

Note how the proposal function $S(\pars,\pars')$ in combination with the acceptance probability $A(\pars,\pars') = \text{min} (r,1)$ provides a simple process for generating samples in a Markov chain that has the required equilibrium distribution. It only requires simple draws of proposal steps, and the evaluation of $p$ at these positions. It is stochastic due to the random proposal of steps and since the decision to accept a proposed step contains randomness via the acceptance probability.

```{note}
The proposal function must allow the chain to be irreducible, positively recurrent and aperiodic.
```


The basic structure of the Metropolis (and Metropolis-Hastings) algorithm is the following:

```{prf:algorithm} The Metropolis-Hastings algorithm
1. Initialize the sampling by choosing a starting point $\boldsymbol{\pars}_0$.
2. Collect samples by repeating the following:
   1. Given $\boldsymbol{\pars}_i$, *propose* a new point $\boldsymbol{\phi}$, sampled from the proposal distribution $S( \boldsymbol{\pars}_i, \boldsymbol{\phi} )$. This proposal distribution could take many forms. However, for concreteness you can imagine it as a multivariate normal with mean vector given by $\boldsymbol{\pars}_i$ and (position-independent) variances $\boldsymbol{\sigma}^2$ specified by the user.
      * The propsal function will (usually) give a smaller probability for visiting positions that are far from the current position.
      * The width $\boldsymbol{\sigma}$ determines the average step size and is known as the proposal width.
   2. Compute the Metropolis(-Hastings) ratio $r$ given by Eq. {eq}`eq:MCMC:metropolis-ratio`. For symmetric proposal distributions, with the simpler expression for the acceptance probability, this algorithm is known as the Metropolis algorithm.
   3. Decide whether or not to accept candidate $\boldsymbol{\phi}$ for $\boldsymbol{\pars}_{i+1}$. 
      * If $r \geq 1$: accept the proposal position and set $\boldsymbol{\pars}_{i+1} = \boldsymbol{\phi}$.
      * If $r < 1$: accept the position with probability $r$ by sampling a uniform $\mathcal{U}([0,1])$ distribution (note that now we have $0 \leq r < 1$). 
        - If $u \sim \mathcal{U}([0,1]) \leq r$, then $\boldsymbol{\pars}_{i+1} = \boldsymbol{\phi}$ (accept); 
        - else $\boldsymbol{\pars}_{i+1} = \boldsymbol{\pars}_i$ (reject). 
        
      Note that the chain always grows since you add the current position again if the proposed step is rejected.
   4. Iterate until the chain has reached a predetermined length or passes some convergence tests.
   ```

* The Metropolis algorithm dates back to the 1950s in physics, but didn't become widespread in statistics until almost 1980.
* It enabled Bayesian methods to become feasible.
* Note, however, that nowadays there are much more sophisticated samplers than the original Metropolis one.



## Exercises

```{exercise} Metropolis sampling of a uniform distribution
:label: exercise:metropolis-sampling-uniform

Show that the update rule implemented in {prf:ref}`example:reversible-markov-process` has the uniform distribution $\mathcal{U}(0,1)$ as its limiting distribution.

```

```{exercise} Power-law distributions
:label: exercise:power-law-distribution-sampling

Discrete power-law distributions have the general form $p(i) \propto i^\alpha$. for some constant $\alpha$. Unlike exponentially decaying distributions (such as the normal distribution and many others), power-law distributions have *fat tails*. They are therefore often used to model skewed data sets. Let

$$
\pi_i = \frac{i^{-3/2}}{\sum_{k=1}^\infty k^{-3/2}}, \quad \text{for } i = 1, 2, \ldots
$$

Implement a Metropolis algorithm to sample for $\boldsymbol{\pi}$.

```

```{exercise} The Metropolis algorithm for a discrete distribution
:label: exercise:MCMC:discrete-metropolis

Use the Metropolis algorithm as outlined in {prf:ref}`remark:MCMC:Metropolis-discrete` to construct a transition matrix $T$ for a Markov chain that gives the discrete limiting distribution

$$
\pi = \left(\frac{1}{9},\frac{3}{4},\frac{5}{36}\right).
$$


Assume that the step proposal matrix has $S(i,j)=1/3$ for all $i,j$.

- Compute $T$ by hand, or numerically using Python. Verify that it is a valid transition matrix and that the above distribution is stationary.

- Verify that $\pi$ and $T$ fulfills detailed balance. 

- Note that this distribution is the limiting distribution found in {numref}`exercise:stationary-gothenburg-winter-weather`. However, the transition matrices are not the same. Try to explain why. Can you construct other transition matrices with the same limiting distribution?

- Construct the Markov chain outcomes of random variable $\{X_n\}$ numerically. Plot the convergence of the discrete distribution for different 
starting distributions and see if the correct limiting distribution is obtained.

```


## Solutions

```{solution} exercise:metropolis-sampling-uniform
:label: solution:metropolis-sampling-uniform
:class: dropdown

Check the acceptance criterion.

```

````{solution} exercise:power-law-distribution-sampling
:label: solution:power-law-distribution-sampling
:class: dropdown

It is suggested to use $\{-1,1\}$ as the proposal step (with $p=0.5$ a step to the left). The acceptence fraction involves a ratio of probabilities, which removes the infinite sum in the denominator. Note also that the acceptance criterion must include the reflective boundary at $i=1$.

````

````{solution} exercise:MCMC:discrete-metropolis
:label: solution:MCMC:discrete-metropolis
:class: dropdown

- Construct the $T$-matrix

$$
T =
\begin{pmatrix}
0.33333333 & 0.33333333 & 0.33333333 \\
0.04938272 & 0.88888889 & 0.0617284 \\
0.26666667 & 0.33333333 & 0.4       
\end{pmatrix}
$$

and note that all elements are positive and that the row sums equal one. You can verify by hand that $\pi = \pi T$ with the given distribution.

- Eq. {eq}`eq:MarkovChains:detailed-balance` gives nine equalities that should be checked.

- The stationary distribution $\pi$ is a left eigenvector of $T$ with eigenvalue $+1$. But there is no uniqueness theorem that dictates that there can only be one matrix with this eigenvalue/vector. It is easy to create other transition matrices with the same limiting distribution by just changing the step proposal matrix.

- Generate the Markov chain and see that it converges

```{code-block} python
import numpy as np

t=np.array([[0.33333333, 0.33333333, 0.33333333],
 [0.04938272, 0.88888889, 0.0617284 ],
 [0.26666667, 0.33333333, 0.4       ]])

N = 40 # Number of steps
x0 = np.array([1,0,0]) # Start distribution

X = []
X.append(x0)
for i in range(1,N):
    X.append(np.matmul(X[i-1],t))

X = np.array(X)
print(X)
```

 
````