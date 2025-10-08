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

(sec:AdvancedMCMC:HMC)=
# Introduction to Hamilton Monte Carlo

```{epigraph}
> "Why walk when you can flow."

-- Richard McElreath
```


The Hamiltonian Monte Carlo Method (HMC) is a Metropolis method that uses gradient information to reduce the random-walk behavior and to collect effectively independent samples. It was introduced in lattice QCD by Duane et al. {cite}`Duane:1987de`and was originally named Hybrid Monte Carlo as they were combining molecular dynamics with the Metropolis MCMC algorithm. A very good and detailed review of HMC is written by Radford Neal and is contained in the Handbook of Markov Chain Monte Carlo {cite}`brooks2011handbook`.

In HMC, the state space $\pos$ is augmented by a conjugate momentum $\mom$. Note that $\pos$ will be the model parameters $\pars$ in our applications but here we will stick to $\pos,\mom$ to make the connection with Hamiltonian dynamics explicit. Let us define a *Hamiltonian*

$$
H(\pos,\mom) = K(\mom) + U(\pos),
$$ (eq:AdvancedMCMC:hamiltonian)

where the kinetic energy function $K(\mom)$ is a design choice while the potential energy function $U(\pos)$ will be defined as minus the log probability of the density that we wish to sample

$$
\begin{aligned}
  K(\mom) &= \frac{1}{2} \mom^T \mass^{-1} \mom, \\
  U(\pos) &= -\ln\left( \p{\pos} \right),
\end{aligned}
$$ (eq:AdvancedMCMC:kinetic-potential)

where $\mass$ is a user-defined mass matrix (positive definite and symmetric) and where we use $\p{\pos}$ to denote the PDF that we want to sample. It could for example be a posterior distribution for some model parameters. 

We can link $H(\pos,\mom)$ to a probability distribution for $(\pos,\mom)$ using the canonical Boltzmann distribution

\begin{equation}
\p{\pos,\mom} = \frac{1}{Z} \exp\left( \frac{-H(\pos,\mom)}{T}\right),
\end{equation}

where $Z$ is the normalization and $T$ is a temperature (here serving to render the exponents dimensionless). Let us set $T=1$ and use the expressions {eq}`eq:AdvancedMCMC:kinetic-potential` to obtain the separable joint distribution

$$
\p{\pos,\mom} \propto \p{\pos} \exp \left( \frac{\mom^T \mass^{-1} \mom}{2} \right).
$$ (eq:AdvancedMCMC:joint-distribution)

Since we will use the Metropolis ratio during sampling, the normalization factor becomes irrelevant. The joint distribution is a produce of two (independent) distributions, the one for $\mom$ becomes a Gaussian with our design choices and the one for $\pos$ is the one that we are seeking. If we manage to efficiently sample from $\p{\pos,\mom}$ then we can just ignore the $\mom$ samples and  we will be left with samples from $\p{\pos}$.

How do we sample from $\p{\pos,\mom}$? Well, naturally we simulate Hamiltonian dynamics for a finite period of time. For Metropolis updates, using a proposal found by Hamiltonian dynamics, the acceptance probability will be one since $H$ is kept invariant. Unfortunately, we will only be able to solve Hamilton's equations approximately and in practice we might not end up with perfect energy conservation.

Apart from energy conservation, two additional key properties of Hamiltonian dynamics---in the context of using it for MCMC sampling---are that it is time reversibile and that it preserves the volume in $(\pos,\mom)$-space (a result known as Liouville's theorem).

Hamilton's equations are

$$
\begin{aligned}
\frac{d x_i}{d t} &= \frac{\partial H}{\partial p_i} = \left( \mass^{-1}\mom\right)_i\\
\frac{d p_i}{d t} &= -\frac{\partial H}{\partial x_i} = \frac{\partial \ln(\p{\pos})}{\partial x_i}.
\end{aligned}
$$ (eq:AdvancedMCMC:hamiltons-equations)

Every HMC iteration begins with a sample of the momentum $\mom$ and continues with the integration of Hamilton's equations for some total time $t$ before the final Metropolis update and the (likely) acceptance of the new position.

In order to maintain energy conservation it is important to simulate the Hamiltonian dynamics using a short time step and to perform the integration such that the accumulation of numerical errors is avoided. The standard method in HMC is known as leapfrog integration and is a symplectic integrator where the discretization error for each time step is equally likely to be positive and negative, thus helping to preserve the total energy throughout the simulation. Leapfrog integration works as an update of the momentum with half a time step, followed by a full step for the position (using the new values for the momentum variables), and finally another half time step for the momentum using the newly updated position variables.

```{prf:algorithm} The Hamiltonian Monte Carlo method
:label: algorithm:AdvancedMCMC:HMC
HMC can be used to sample from continuous distributions pn $\mathbb{R}^d$ for which both the density and the partial derivatives of the log of the density can be evaluated.
1. In the first step, new values for the momentum variables $\mom$ are randomly drawn from their Gaussian distribution (independently of the current values of the position variables). The result is a state $(\pos_i,\mom_i)$.
2. In the second step, a Metropolis update is performed, simulating Hamiltonian dynamics to propose a new state. 
   - Starting at the current state $(\pos_i,\mom_i)$, Hamilton's equations are integrated for $L$ timesteps of length $\varepsilon$ using the leapfrog method (or some other reversible method that preserves volume). 
   - The momentum variable at the end of this $L$-step trajectory are then negated, giving a proposed state $(\pos^*_i,\mom^*_i)$. The negation is is needed to make the Metropolis proposal symmetric, but does not matter in practice since $K(-\mom) = K(\mom)$ and the momentum will be replaced before it is used again.
   - The proposed state is accepted as the new state $(\pos_{i+1},\mom_{i+1})$ with probability
   
     $$
     \min\left( 1, -\exp(-H(\pos^*_i,\mom^*_i)) +H\exp(-H(\pos_i,\mom_i)) \right).
     $$
     
     Otherwise, the new state is a copy of the current state. 
```


For succesful application of HMC there are three hyperparameters that need to be tuned by the user:

1. The mass matrix $\mass$;
2. The integration timestep $\varepsilon$;
3. The number of timesteps $L$.

The MontePython implementation of HMC, by Isak Svensson, was published in Ref. {cite}`Svensson:2021lzs` and is publicly available at: https://github.com/svisak/montepython.git

More advanced versions, such as the No-U-Turn Samplers (NUTS) {cite}`hoffman2014no`, are also available and aims to simplify the process of tuning the hyperparameters.

