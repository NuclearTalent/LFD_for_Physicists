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
# Solutions

Here are answers and solutions to selected exercises.

```{solution} exercise:StochasticProcess:first-example
:label: solution:StochasticProcess:first-example
:class: dropdown

- The initial variable is from a uniform distribution: $p_{X_0}(x_0) = \mathcal{U}\left( [0,1] \right)$.
- Variable $X_n$ is obtained from
$p_{X_n \vert X_0, X_1, \ldots, X_{n-1}} \left( x_n | x_0, x_1, \ldots, x_{n-1} \right) = \mathcal{U}\left( [0,1] \right) + \sum_{i=0}^{n-1} x_i$
```

````{solution} exercise:conditional-probabilities-stochastic-process
:label: solution:conditional-probabilities-stochastic-process
:class: dropdown

The histograms on the diagonal show the distributions $\p{X_n}$ which are marginalized over $X_{n−1}, \ldots, X_0$. The off-diagonal plots show the joint distributions $\p{X_i,X_j}$ which are marginalized over $X_{n−1}, \ldots, X_0$ with $n=\max(i,j)$ and excluding $X_{\min(i,j)}$. Note that these are distributions of random variables $X_n$, not random values $x_n$.

More explicitly:

* $\p{X_0}$ has no correlated random variables marginalized out since it starts the sequence.
* $\p{X_1}$ is marginalized over $X_0$.
* $\p{X_2}$ is marginalized over $X_1,X_0$.
* $\p{X_3}$ is marginalized over $X_2,X_1,X_0$.
* $\p{X_0,X_1}$ has no correlated random variables marginalized out.
* $\p{X_1,X_2}$ is marginalized over $X_0$.
* $\p{X_2,X_3}$ is marginalized over $X_0, X_1$.
* $\p{X_1,X_3}$ is marginalized over $X_0, X_2$.
* $\p{X_0,X_3}$ is marginalized over $X_1, X_2$.
* $\p{X_0,X_2}$ is marginalized over $X_1, X_3$.

The dependence of $X_3$ on $X_0$ is not directly observed since $\pdf{X_3}{X_0}$ is not shown. However, from Eq. {eq}`eq:Statistics:conditional-probability` we have that $\pdf{X_3}{X_0} = \p{X_0,X_3} / \p{X_0}$. And since $\p{X_0}$ is uniform, we find that $\pdf{X_3}{X_0} \neq \p{X_3}$.
In other words, $X_3$ "remembers" $X_0$.
````

````{solution} exercise:construct-stochastic-process
:label: solution:construct-stochastic-process
:class: dropdown

Here's one possible solution. It is a slightly more general random walk.

```{code-block} python
class exerciseSP(SP):
    def start(self,random_state):
        return random_state.uniform()

    def update(self, random_state, history):
    	return history[-1] + random_state.uniform())
```
````














%========================
% Extra exercises not yet coordinated with the text.
%========================
%--```{exercise}
%--:label: exercise:the-poisson-process-1
%--
%--This exercise will explore the important Poisson distribution in
%--more detail and illustrate how the Poisson distribution can arise from a 
%--stochastic proccess.
%--
%--Define a stochastic process $\{X_i : i \in \{1,2,\dots\}\}$ where $X_i \sim 
%--\mathrm{exp}(\lambda)$ and independent. This means that the pdf is 
%--
%--$$f_{X_i}(x) = \begin{cases} \lambda e^{-\lambda x},
%--\quad x \geq 0, \\ 0, \quad x < 0. \end{cases}
%--$$
%--
%--This stochatic process is quite trivial, sice it is just an i.i.d sequence of random variables being exponentially 
%--distributed.
%--
%--From this process define a new process $\{T_n : n \in \{1,2,\dots\}\}$ where
%--$T_n = \sum_{i=1}^n X_i$.
%--
%--(i) Show that $\{T_n : n\in\{1,2,\dots\}\}$ is a Markov Process.
%--
%--(ii) Calculate the distribution function (cdf) of $T_n$, i.e. 
%--$F_{T_n} (t) = P(T_n \leq t)$ to show that $T_n \sim \Gamma(\lambda,n)$ 
%--
%--*Hint*: This is most easily shown by indction. (1.) Show that a exponential 
%--distribution is a special case of the $\Gamma$ distribution (2.) Consider 
%--the distribution of $Z = T_{n-1} + X_n$ where you assume that $T_{n-1}$ has a 
%--$\Gamma$--distribution.
%--
%--(iii) (optional) Try implementing this stochastic process in the Python class.
%--
%--
%--(iv) Define a random variable $N(t) =$ max$\{n : T_n \leq t \}$.
%--Show that $N(t) \sim \mathrm{Poisson}(\lambda t)$.
%--
%--*Hint*: First show that $N(t)\geq j$ if and only if  $T_j \leq t$. Use this to express 
%--$P(N(t) = j)$ in terms of the distribution function you calculated earlier.
%--
%--
%--```
%--```{exercise}
%--:label: exercise:the-poisson-process-2
%--This exercise will illustrate another situation where the Poisson distribution 
%--shows up.
%--
%--Consiser a physics experiment where you want to measure some process that emitts 
%--some kind of particle in different directions. The goal is to infer the probability
%--distribution that the particles follow. Consider that the detector is a screen
%--with some length, $L$, which is divided up in $K$ bins. The number of particels 
%--detected in each bin will approach the underlying probability distribution after 
%--long enough time, but for a finite number of samples it may look somethig like the
%--figure below. The red curv is the underlying pdf that we want to know, and the blue
%--histogram shown the outcome of the experiment.
%--
%--![file](./figs/prob_fig.png)
%--
%--We will study the distribution of the number of particles in each bin, and how
%--that is affected by the number of particales that are detected, $N$, and the setup 
%--of the experiment. This distribution is important to be able to cunstruct the 
%--likelihood of the observed data given some model to describe the process.
%--
%--Suppuse that $N_i, \ i=1,\dots,K$ is the number of particles detected in the 
%--experiment in the corresponding bins. Let's focus on bin $i=1$.
%--
%--(*i*) Show that if all the particles can be considered independent the probability
%--of observing $N_i$ particles in bin $i=1$ is following a Binomial distribution. 
%--Assume that the variation of the underlying pdf can be considered constant 
%--in each bin, meaning that the widths of the bins are very small.
%--
%--*Hint*: Use that the random variable $N_i$ is a sum of Bernoulli distributed 
%--random variables.
%--
%--(*ii*) Compute the *generating function* for the Binomial distribution and 
%--the Poisson distribution.
%--
%--*Hint*: Remember that the generating function for a discrete random varaiable, $X$,
%--is defined as
%--
%--$$
%--G(s) =  \mathbb{E}\left(s^{X}\right) = \sum_n s^n \cdot f_X(n).
%--$$
%--
%--For the calculation of the generating function for the binomial distribution
%--you can use the fact that the binomial distribution is a sum of independent 
%--random variables with a generating function that is easier to compute.
%--
%--(*iii*) Prove the so-called Poisson Limit Theorem, that the binomial
%--distribution approaches the Poisson distribution in the limit 
%--
%--$$
%--N \to \infty, \quad N p_i \to \lambda. 
%--$$
%--
%--where $\lambda$ is a finite constant, i.e. 
%--
%--$$
%--P(N_i = n_i) \to_{N\to\infty} \frac{\lambda^{n_i}}{n_i!}e^{-\lambda}
%--$$
%--
%--*Hint*: Use the definition of $e$ and explicitly construct a sequence of decreasing 
%--probabilities $p_i \to_{N\to\infty} 0$ that fulfills the constraint above.
%--
%--(*iv*) Use scipy-stats to compare the binomial distribution and the Poisson distribution
%--and verify that the statement you just prove makes sense. Vary the size of 
%--$\lambda = p_i N \in \{0.5,2,10\}$ for large $N \sim 1000$. What do you observe? 
%--How can you explain it?
%--
%--```
%========================
% Solutions to extra exercises.
%========================
%--```{solution} exercise:the-poisson-process-1
%--:label: solution:the-poisson-process-1
%--:class: dropdown
%--
%--(*i*)
%--- Want to show that
%--
%--$$
%--P(T_n = t_n | T_{n-1} = t_{n-1}, 
%--\dots, T_1 = t_1) = P(T_n=t_n| T_{n-1} = t_{n-1}).
%--$$
%--
%--\begin{align}
%--P(T_n = t_n | T_{n-1} = t_{n-1}, 
%--\dots, T_1 = t_1) =\\= P(X_n + T_{n-1} = t_n | T_{n-1} = t_{n-1}, 
%--\dots, T_1 = t_1) =\\= P(X_n = t_n - t_{n-1}| T_{n-1} = t_{n-1}, 
%--\dots, T_1 = t_1)
%--\end{align}
%--
%--- Multiply and divide by $P(X_{n} | T_n)$ and show by independence that
%--all the remaining factors cancel and you are left with
%--
%--\begin{align}
%--P(T_n = t_n | T_{n-1} = t_{n-1}, 
%--\dots, T_1 = t_1) =\\ = P(X_n=t_n - t_{n-1} | T_{n-1} = t_{n-1}) = 
%--P(T_n=t_n| T_{n-1} = t_{n-1})
%--\end{align}
%--
%--which shows that it is a Markov process.
%--
%--(*ii*)
%--
%--- Use the hint.
%--
%--(*iii*)
%--
%--- We follow the hints.
%--- Assume that $N(t) \geq j$. Since $N(t)$ is the maximum $n$ for whith $T_n \leq t$
%--we get that $T_j \leq t$. Assume that $T_j \leq t$. This means that the maximum 
%--$n$ for which $T_n \leq t$ hold must be larger of equal to $j$, hence $N(t) \leq j$.
%--- The probability $P(N(t) = j)$ can be expressed as
%--
%--$$
%--P(N(t) = j) = P(N(t)\geq j) - P(N(t)\geq j+1).
%--$$
%--
%--By the above equality we can express these probabilities as
%--
%--$$
%--P(N(t) = j) = P(T_j \leq t) - P(T_{j+1} \leq t) = F_{T_j}(t) - F_{T_{j+1}}(t) = 
%--\frac{(\lambda t )^j}{j!} e^{-\lambda t}.
%--$$
%--
%--```
%--
%--
%--```{solution} exercise:the-poisson-process-2
%--:label: solution:the-poisson-process-2
%--:class: dropdown
%--
%--(*i*)
%--- We use the hint and assume that the probability of hitting bin $i$ is $p_i$.
%--This means that each particle is hitting this bin with probability $p_i$ and
%--missing with probability $1-p_i$. This experiment is repeated $N$ times. This means 
%--that
%--
%--$$
%--N_i = \sum_{k=1}^N B_k,  
%--$$
%--where $B_k \sim$ Bernoulli$(p_i)$ and independent. This means that the probability
%--of $n_i$ hits among $N$ can be obtained from the Binomial theorem 
%--
%--$$
%--P(N_i = n_i) = \left(\frac{N}{n_i}\right) p_i^{n_i}(1-p_i)^{N-n_i}.
%--$$
%--
%--(*ii*)
%--
%--- Use the definition of the generating function to obtain for the Poisson
%--distribution
%--
%--$$
%--G_P(s) = \sum_k s^k \frac{\lambda^k}{k!} e^{-\lambda} = e^{\lambda(s-1)}
%--$$
%--
%--- For the Binomial distribution we use the property of the generating functions
%--that $G_{Bin}(s) = \left(G_{Bern}(s)\right)^N$, which holds by independence.
%--
%--$$
%--G_{Bin}(s) = \left( (ps) + (1-p)\right)^N
%--$$
%--
%--(*iii*)
%--- We will prove this by proving that the generating function for the binomial 
%--distribution approaches the generating function for the Poisson distribution in
%--the $N\to \infty$ limit. We drope the $i$ index from now on.
%--
%--- Using the hint an explicit secuence is for example $p_N = \frac{\lambda}{N} + 
%--o\left(\frac{1}{N}\right)$ (The small $o$ notation means that $N^m o(1/N^m)
%--\to_{N\to\infty} 0$) 
%--
%--- Looking at the generating function for the Binomial distribution we have
%--
%--$$
%--(ps + (1-p))^N = (1+p_N(s-1))^N = \exp{\left[N \ln\left( 1 +\frac{\lambda}{N} + 
%--o\left(\frac{1}{N}\right)\right)\left(s-1\right)\right]}
%--$$
%--
%--Taylor expanding the logarithm and takning the limit gives
%--
%--$$
%--\exp\left[N\left(p_N(s-1) + o\left(\frac{1}{N}\right)\right)\right] 
%--\to_{N\to\infty} \exp\left[\lambda(s-1)\right]
%--$$
%--
%--```

