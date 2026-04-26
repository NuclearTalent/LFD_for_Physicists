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

```{math}

\newcommand\pos{\boldsymbol{x}}
\newcommand\mom{\boldsymbol{p}}
\newcommand\mass{\mathcal{M}}
```

(sec:parallel-tempering)=
# Parallel tempering

Parallel tempering was particularly introduced to deal with multimodal distributions.
This is analogous to the problem of *global* (as opposed to local) optimization, which can mean either minimizing or maximizing a function.
It is a challenging problem: how do you jump from one region of high posterior density to another when there is a large region of low probability in between?
This problem shows up for evidence calculations, because we need to integrate over the entire parameter space.
In contrast, for parameter estimation, it may be sufficient to start walkers in the vicinity of the "best" (highest posterior) part of the posterior.

Parallel tempering is built on top of an MCMC sampler.
The general idea is to simulate $N$ *replicas* of a system, each at a different temperature.
The temperature of a Metropolis-Hastings Markov chain specifies how likely it is to sample from a low-density part of the target distribution.
At high temperature, large volumes of phase space are sampled roughly, while low temperature systems have precise sampling in a local region of the parameter space, where they can get stuck in a local energy minimum (meaning a local posterior maximum).
Parallel tempering works by letting the systems at different temperatures exchange configurations, which enables the low $T$ system access to a complete set of low-temperature regions.

The temperature enters in analogy to a Boltzmann factor $e^{-E/k_B T}= e^{-\beta E}$ where $\beta \equiv 1/k_B T$.
Instead of $E$ we have $-\log p_\beta(x)$ so

$$
  p_\beta(x) = e^{-\beta(-\log p(x))} = \bigl(p(x)\bigr)^\beta
$$   

We seek the posterior written with Bayes' theorem and normalization constant $C$:
    
$$
 p(\thetavec|D,I) = C p(D|\thetavec,I) p(\thetavec|I)
$$

and generalize to the temperature-dependent posterior $p_\beta$:

$$
 p_{\beta(\thetavec|D,I)} \propto p(D|\thetavec,I)^\beta
    p(\thetavec|I) \qquad 0 \leq \beta \leq 1
$$

or

$$
  \log p_{\beta(\thetavec|D,I)} = C + \beta\log p(D|\thetavec,I) + \log p(\thetavec|I) .
$$  

So the desired distribution is $\beta = 1$, and $\beta = 0$ is the prior alone.
At large temperature, $\beta = 0$, and we sample the prior, which should encompass the full (accessible) space.
As we approach $\beta = 1$ we fous increasingly on where the likelihood is large.

We will use $\beta \in \{1,\beta_2, \ldots, \beta_N\}$ running *in parallel*, but swapping members of the chains in such a way that detailed balance is preserved. 
The general sampling strategy is:
* at intervals, pick a pair of *adjacent* chains at random: $\beta_i$ and $\beta_{i+1}$;
* propose a swap of their current positions at this time $t$, namely exchange $\thetavec_{t,i}$ and $\thetavec_{t,i+1}$;
* accept this proposal with probability (note the $i$s and $(i+1)$s):

$$
  r = \min\left\{1, 
    \frac{p_\beta(\thetavec_{t,i+1}|D,\beta_i,I)
          p_\beta(\thetavec_{t,i}|D,\beta_{i+1},I)}
         {p_\beta(\thetavec_{t,i}|D,\beta_i,I)
          p_\beta(\thetavec_{t,i+1}|D,\beta_{i+1},I)}
    \right\}
$$

This algorithm will preserve detailed balance.


We can make this expression more intuitive if we connect back to the physics analogy.

$$
  p_\beta(\thetavec|D,I) \propto p(D|\thetavec,I)^\beta p(\thetavec|I)
  \propto e^{-\beta(-\log p(D|\thetavec,I)) p(\thetavec|I)}
$$

and $-\log p(D|\thetavec,I)$ is the potential energy $U(\rvec)$ (by analogy). Then the priors drop out of the ratio in $r$ (the prior is independent of $\beta$), leaving:

$$
r = \min\left\{1,e^{-(\beta_i - \beta_{i+1})(U(\rvec_{i+1}-U(\rvec_i)))}\right\}
$$

so the four terms in $r$ arise from the Boltzman factors of the energy difference at the two temperatures.

Things to specify for the sampler:
    * $n_s$: propose a swap every $n_s$ iterations, which is implemented by drawing a random number $U_1 \sim \text{Uniform}[0,1]$ every iteration and proposing a swap if $U_1 \leq 1/n_s$.
    * The length and spacing of the temperature ladder.

## Calculating the evidence

To calculate the *evidence* from parallel tempering, we can use *thermodynamic integration* see Ref. {cite}`Goggans2004`.

Define the temperature dependent evidence:

$$
  Z(\beta) \equiv \int d\thetavec\, p(D|\thetavec,I)^\beta p(\thetavec|I) = \int d\thetavec\, e^{\beta\log p(D|\thetavec,I)} p(\thetavec|I)
$$  

so we want $Z(1)$.

Now $Z(\beta)$ satisfies a differential equation:

$$\begin{align}
  \frac{d\log Z(\beta)}{d\beta} &= 
     \frac{1}{Z(\beta)}
     \int d\thetavec \bigl(\log p(D|\thetavec,I)\bigr)
          p(D|\thetavec,I)^\beta p(\thetavec|I) \\
     &\equiv \langle \log p(D|\thetavec,I\rangle_\beta ,
\end{align}$$

which is the average of the log likelihood at temperature $\beta$.
So we can integrate over $\beta$ (the first term is doesn't contribute if the prior is normalized):

$$
  \log Z(1) = \log Z(0) + \int_0^1 d\beta\, \langle \log p(D|\thetavec,I)\rangle_\beta ,
$$

$\Lra$ estimate from emcee samples by computing the average of $p(D|\thetavec,I)$ within each chain and then evaluating the integral from a quadrature formula (e.g., Simpson's rule).



## Example of parallel tempering       

An example of parallel tempering is given in {ref}`demo:multimodal-distributions-with-two-samplers`.

Comments:
* First we set up a bi-modal distribution (it was originally intended to be a surprise, so the code was hidden). Just two Gaussians with different amplitudes.

* A first sampling try with an ordinary Metropolis-Hastings (MH) sampler fails by only finding one mode.

* But then if one checks two chains, separate modes are found but the chains do not mix. With many walkers one might find multiple modes, but the relative normalizations would not work because each walker would not explore the space.

* The setup for `ptemcee` includes a temperature grid chosen so that numerically integrating over temperature for the evidence has a finer grid at low temperatures for greater accuracy.

* Note the corner plots for different temperatures and how the multimodal structure emerges. 
