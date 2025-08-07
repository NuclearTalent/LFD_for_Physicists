# Hamiltonian Monte Carlo (HMC) overview and visualization

* We've seen some different strategies for sampling difficult posteriors, such as an affine-invariant sampling approach (emcee) and a thermodynamic approach (parallel tempering).

* One of the most widespread techniques in contemporary samplers is Hamiltonian Monte Carlo, or HMC.
    * We'll look at some visualizations as motivation, then consider some examples using PyMC.

* We return to the excellent set of interactive demos by Chi Feng at [https://chi-feng.github.io/mcmc-demo/](https://chi-feng.github.io/mcmc-demo/) and their adaptation by Richard McElreath at [http://elevanth.org/blog/2017/11/28/build-a-better-markov-chain/](http://elevanth.org/blog/2017/11/28/build-a-better-markov-chain/). These are also linked on the 8820 Carmen visualization page.

* The McElreath blog piece forcefully advocates abandoning Metropolis-Hasting (MH) sampling in favor of HMC. Let's take a look.
    * First recall the random walk MH:
        1. Make a random proposal for new parameter values (a step in parameter space, indicated in the visualization by an arrow).
        2. Aceept (green arrow) or reject (red arrow) based on a Metropolis criterion (which is not deterministic but has a random element).
    * This is *diffusion* (i.e., a random walk), so it is not efficient in exploring the parameter space and needs special tuning to avoid too high a rejection rate.
    * The donut shape in the simulation is common in higher dimensions and it is difficult to explore. (I.e., consider a multidimensional uncorrelated Gaussian distribution. In spherical coordinates the distribution is $\propto r^n e^{-r^2/2\sigma^2}$, so the marginalized distribution will be peaked away from $r=0$.)

* Now consider the "Better living through Physics" part $\Lra$ an HMC simulation.
    * The idea is that we map our parameter vector $\thetavec$ of length $n$ to a particle in an $n$-dimensional space. The surface is an $n$-dimensional (inverted) bowl with the shape given by minus-log(target distribution), where the target distribution is the posterior.
    * Treat the system as frictionless. "Flick" the particle in a random direction, so it travels across the bowl.
    * See the simulation: the little gray arrow is the flick. After the particle travels some distance, decide whether to accept.
    Most endpoints are within a high probability region, so a high percentage is accepted.
    * Chains can get far from the starting point easily $\Lra$ efficient exploration of the full shape.
    * More calculation along the path is needed, but fewer samples $\Lra$ this is typically a winning trade-off.
    * Check the donut example $\Lra$ works very well!


```{image} ./figs/HMC_demo_screenshot_1.png
:alt: Screenshot from HMC demo
:class: bg-primary
:width: 450px
:align: center
```

```{image} ./figs/HMC_demo_screenshot_2.png
:alt: Screenshot from HMC demo
:class: bg-primary
:width: 450px
:align: center
```

```{image} ./figs/HMC_demo_screenshot_3.png
:alt: Screenshot from HMC demo
:class: bg-primary
:width: 400px
:align: center
```

```{image} ./figs/HMC_demo_screenshot_4.png
:alt: Screenshot from HMC demo
:class: bg-primary
:width: 400px
:align: center
```


* There is a further improvement called NUTS, which stands for "no-U-turn sampler". 
    * The idea is to address the problem that HMV needs to be told how many steps to take before another random flick.
    * Too few steps $\Lra$ samples are too similar
    * Too many steps $\Lra$ also too similar

* NUTS adaptively finds a good number of steps.
    * Simulates in *both$ directions to figure out when the path turns around (U-turns) and stops there.
    * There are other adaptive features - see the documentation.

* Note that NUTS still has trouble with multimodal targets $\Lra$ can explore each high probability area, but has trouble going between them.

## HMC physics

* The basic idea behind HMC is to translate a pdf for the desired distribution into a postential energy function and to add a (fictitious!) momentum variable. In the Markov chain at each iteration, one resamples the momentum (the flick!), creates a proposal using classical Hamiltonian dynamics, and then does a Metropolis update.

* Recall Hamiltonian dynamics, now applied to a $d$-dimensional position vector $q$ and a $d$-dimensional momentum vector $p$ $\Lra$ there is a $2\times d$-dimensional phase space for the Hamiltonian $H(q,p)$.

* The Hamilton equations of motion describe the time evolution:

$$
  \frac{dq_i}{dt} = \frac{\partial H}{\partial p_i},
  \qquad
  \frac{dp_i}{dt} = -\frac{\partial H}{\partial q_i},
  \quad
  i = 1,\ldots d ,
$$

which map states at time $t$ to states at time $t+s$. (Recall the difference between total and partial derivaties; e.g., what is held fixed in each case.)

* We take the form of $H$ to be $H(q,p) = U(q) + K(p)$
    * the potential energy $U(q)$ is minus the log probability density of the distribution for $q$ that we seek to sample.
    * $K(p)$ is the kinetic energy

    $$
        K(p) = \frac{1}{2}p^\intercal M^{-1} p ,
    $$

    where $M$ is a symmetic, positive (what does that mean?) "mass matrix", typically diagonal and even $M\times \mathbb{1}_d$ (proportional to the identity matrix in $d$-dimensions).

    * This is minus the log probability density (plus a constant) of a Gaussian with zero mean and covariance matrix $M$.

* What are we going to do with this? We consider a canonical distribution at temperature $T$:

$$
   P(q,p) = \frac{1}{Z} e^{-H(q,p)/T}
          = \frac{1}{Z} e^{-U(q)/T}e^{-K(p)/T} ,
$$

so $q$ and $p$ are *independent*. We are interested only $q$; $p$ is a fake variable to make things work. Usually $U(q)$ is a posterior: $U(q) = -\log[p(q|D)p(q)]$ where $q \rightarrow \thetavec$.

## HMC algorithm

Two steps of the HMC algorithm:

1. New values for the momentum variables are randomly drawn from their Gaussian distribution, independent of current position values.
    * This means $p_i$ will have mean zero and variance $M_{ii}$ if $M$ is diagonal.
    * $q$ isn't changed, $p$ is from the correct conditional distribution given $q$, so the canonical joint distribution is invariant.

2. Proposal from Hamiltonian dynamics for a new state. Simulate from $(q,p)$ with $L$ steps of size $\epsilon$. At the end, the momenta are flipped in sign and the new proposed step $(q^*,p^*)$ is accepted with probability (cf. $\Delta E$ with $T=1$):

    $$
     \min[1,e^{-H(q^*,p^*) + H(q,p)}] = \min[1,e^{-U(q^*)+U(q)-K(p^*)+K(p)}] .
    $$

    * The momentum flip makes the proposal symmetric, but not done in practice.
    * So the probability distribution for $(q,p)$ *jointly* is (almost) unchanged because energy is conserved, but in terms of $q$ we get a very different probability density.

* You can show that HMC leaves the canonical distribution invariant because detailed balance holds, which is what we need. It will also be *ergodic* $\Lra$ it doesn't get stuck in a subset of phase space but samples all of it.

* Essential features:
    * Reversability needed so that desired distribution is invariant.
    * Conservation of the Hamiltonian (which is the energy here).
    * Volume preservation - preserves volume in $(q,p)$ phase space - this is Liouville's Theorem. (If we take a cluster of points and follow their time evolution, the volume they occupy is unchanged. See [](/notebooks/MCMC_sampling_II/Liouville_theorem_visualization.ipynb) notebook.) $\Lra$ this is critical because a change in volume would mean we would have to make a nontreival adjustment to the proposal (because the normalization $Z$ would change).

* These requirements are satisfied by the exact Hamilton's equations, but we are *approximating* the solution to these differential equations. This necessitates a *symplectic* (symmetry conserving) integration.
    * Ordinary Runge-Kutta-type ODE solvers won't work because they are not time-reversal invariant.
    * E.g., consider the Euler method. Forward and backward integrations are different because the derivatives are calculated from different points.
    * We need something like the Leapfrog algorithm (2nd order version here):

    $$\begin{align}
      p_i(t+\epsilon/2) &= p_i(t) - \frac{\epsilon}{2}\frac{\partial U}{\partial q_i}\bigl(q(t)\bigr) \quad \longleftarrow\text{half step} \\
      q_i(t+\epsilon) &= q_i(t) + \epsilon p_i(t + \epsilon/2)/M_i
      \quad\longleftarrow\text{use intermediate $p$} \\
      p_i(t+\epsilon) &= p_i(t+\epsilon/2) - \frac{\epsilon}{2}\frac{\partial U}{\partial q_i}\bigl(q(t+\epsilon)\bigr) \quad \longleftarrow\text{other half step} \\
    \end{align}$$

    See Figures 1, and 3-6 in ["MCMC using Hamiltonian dynamics"](https://arxiv.org/abs/1206.1901) by Radford Neal.    