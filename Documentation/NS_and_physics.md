There is a very direct statistical-mechanics analogy, and in fact it is one of the cleanest ways to understand nested sampling.

Start from the Bayesian evidence

[
Z=\int d\theta,\pi(\theta)L(\theta).
]

Define an “energy”

[
E(\theta)\equiv -\log L(\theta),
]

so that

[
L(\theta)=e^{-E(\theta)}.
]

Then

[
Z=\int d\theta,\pi(\theta)e^{-E(\theta)}.
]

This has exactly the form of a **canonical partition function at (\beta=1)**, with the prior (\pi(\theta)d\theta) playing the role of the underlying phase-space measure.

More generally, introduce a temperature parameter,

[
Z(\beta)
========

\int d\theta,\pi(\theta)
e^{-\beta E(\theta)}
====================

\int d\theta,\pi(\theta)L(\theta)^\beta.
]

Then ordinary Bayesian inference corresponds to (\beta=1), while

[
\beta=0
]

is just the prior.

### Prior volume is a cumulative density of states

This is where nested sampling becomes particularly natural from a statistical-mechanics viewpoint.

Nested sampling defines

[
X(\lambda)
==========

\int_{L(\theta)>\lambda}
\pi(\theta),d\theta.
]

Since (E=-\log L), the condition (L>\lambda) is equivalent to

[
E<E_\lambda.
]

Therefore

[
\boxed{
X(E)=
\int_{E(\theta)<E}
\pi(\theta),d\theta
}
]

is the **cumulative phase-space volume below energy (E)**.

That is extremely close to the integrated density of states familiar from statistical mechanics,

[
\Omega(E)=
\int d\Gamma,
\Theta(E-H(\Gamma)).
]

Thus the correspondences are

[
\begin{array}{c|c}
\text{Bayesian inference} & \text{Statistical mechanics}\
\hline
\theta & \text{configuration / microstate}\
-\log L(\theta) & E(\theta)\
\pi(\theta)d\theta & \text{reference phase-space measure}\
X(E) & \text{cumulative density of states}\
L=e^{-E} & \text{Boltzmann factor at }\beta=1\
Z & \text{partition function}\
-\log Z & \text{free energy at }\beta=1
\end{array}
]

(up to the usual factors of (\beta) and units).

### The density-of-states formulation

If

[
g(E)=\frac{dX}{dE},
]

then

[
Z(\beta)
========

\int g(E)e^{-\beta E},dE.
]

This is precisely the usual density-of-states expression for the canonical partition function.

Nested sampling doesn't normally estimate (g(E)) directly. Instead, it estimates the inverse relation

[
E(X)
]

or equivalently

[
L(X)=e^{-E(X)},
]

and computes

[
Z
=

\int_0^1 L(X),dX.
]

So one particularly good description is:

[
\boxed{
\text{Nested sampling is a way of reconstructing the density-of-states information needed for a partition function.}
}
]

### What are the live points physically analogous to?

At iteration (i), nested sampling has imposed the constraint

[
L>L_i,
]

which is

[
E<E_i.
]

The live points are therefore samples from the prior measure **restricted to the region below a specified energy ceiling**.

That looks much more like a **microcanonical-type construction** than a canonical one. It is not exactly the conventional thin-shell microcanonical ensemble (E<E_i+\delta E), because nested sampling samples the entire interior

[
E<E_i.
]

But the analogy is strong:

[
\boxed{
\text{nested sampling repeatedly measures the phase-space volume inside successively lower energy surfaces.}
}
]

In the schematic figures we have been discussing, those shrinking likelihood contours are therefore literally analogous to **constant-energy surfaces**, with the algorithm progressively moving toward lower (E), or equivalently higher likelihood.

### Entropy makes the analogy even stronger

Because (X(E)) measures available volume, one can define an entropy-like quantity

[
S(E)=\log X(E).
]

More conventionally one might use

[
S_{\rm micro}(E)=\log g(E),
]

but (\log X) is especially natural for nested sampling.

Recall the characteristic shrinkage

[
X_i\sim e^{-i/N_{\rm live}}.
]

Therefore

[
\log X_i\simeq-\frac{i}{N_{\rm live}}.
]

So nested sampling is effectively stepping almost uniformly in an **entropy-like variable**,

[
\Delta \log X\simeq-\frac{1}{N_{\rm live}},
]

rather than uniformly in energy or likelihood.

This is one reason it is so effective at moving through enormous ranges of phase-space volume.

### Evidence is an energy–entropy competition

This also gives a nice statistical-mechanics interpretation of the Bayesian Occam factor.

Write schematically

[
Z
=

\int dE,
e^{S(E)-\beta E},
]

where (S(E)\sim\log g(E)).

The dominant contribution balances

[
\underbrace{-\beta E}_{\text{favor low energy/high likelihood}}
]

against

[
\underbrace{S(E)}_{\text{favor large phase-space volume}}.
]

That is exactly the same competition that determines equilibrium in statistical mechanics.

In Bayesian language:

* high likelihood favors a small region around an excellent fit;
* prior volume favors broader regions that fit reasonably well.

Thus the Bayesian tradeoff between **fit and Occam penalty** is the analogue of the statistical-mechanical tradeoff between **energy and entropy**.

This is more than a metaphor. Mathematically they are the same structure.

### Posterior and canonical ensemble

The tempered posterior is

[
p_\beta(\theta)
===============

\frac{\pi(\theta)L(\theta)^\beta}
{Z(\beta)}
==========

\frac{\pi(\theta)e^{-\beta E(\theta)}}
{Z(\beta)}.
]

This is the canonical distribution.

At

[
\beta=0,
]

[
p_0(\theta)=\pi(\theta),
]

while at

[
\beta=1
]

you have the ordinary posterior.

As (\beta\rightarrow\infty), the distribution concentrates on the maximum-likelihood/minimum-energy configurations.

So Bayesian tempering has the literal interpretation of **cooling a statistical-mechanical system**.

### Thermodynamic integration versus nested sampling

This also clarifies the connection to another evidence method, thermodynamic integration. Since

[
Z(\beta)
========

\int \pi(\theta)L(\theta)^\beta d\theta,
]

we have

[
\frac{d\log Z}{d\beta}
======================

# \langle \log L\rangle_\beta

-\langle E\rangle_\beta.
]

Hence

[
\log Z(1)-\log Z(0)
===================

\int_0^1
\langle\log L\rangle_\beta,d\beta.
]

Since (Z(0)=1),

[
\boxed{
\log Z
======

\int_0^1
\langle\log L\rangle_\beta,d\beta.
}
]

That is essentially a **free-energy calculation by thermodynamic integration**.

So there are two complementary physics pictures:

[
\begin{array}{ll}
\textbf{Thermodynamic integration:}
&
\text{change the temperature } \beta
[1ex]
\textbf{Nested sampling:}
&
\text{change the accessible phase-space volume }X.
\end{array}
]

Nested sampling is thus closer in spirit to a **density-of-states / microcanonical method**, while thermodynamic integration is directly a **canonical-ensemble free-energy method**.

### Phase transitions and multimodal posteriors

The analogy becomes particularly interesting for difficult Bayesian problems.

Suppose the likelihood has two separated modes. In statistical mechanics these can resemble competing phases. As (\beta) changes, the dominant contribution to

[
Z(\beta)
]

may move from one region to another.

Then quantities such as

[
\langle E\rangle_\beta
]

and

[
C(\beta)
========

\beta^2
\left(
\langle E^2\rangle_\beta
------------------------

\langle E\rangle_\beta^2
\right)
]

can show behavior analogous to thermodynamic transitions.

In nested-sampling language, abrupt changes in the structure of (L(X)) can signal transitions between large-volume/low-likelihood and small-volume/high-likelihood regions.

So multimodality, metastability, and phase coexistence have quite literal Bayesian analogues.

### The interpretation I find most useful

For the figures we have just constructed, I would explain the analogy this way:

> **Treat (-\log L) as an energy. Each likelihood contour is then an energy contour. The prior volume (X) is the cumulative phase-space volume enclosed by that contour. Nested sampling systematically compresses this accessible phase-space volume, thereby reconstructing the density-of-states information needed to calculate the partition function—i.e. the Bayesian evidence.**

And the particularly elegant chain is

[
\boxed{
L(\theta)
\longleftrightarrow
E(\theta)=-\log L(\theta)
\longleftrightarrow
X(E)
\longleftrightarrow
g(E)
\longleftrightarrow
Z.
}
]

That is much closer than a loose analogy: nested sampling can genuinely be viewed as a statistical-mechanics **density-of-states/free-energy algorithm**.
