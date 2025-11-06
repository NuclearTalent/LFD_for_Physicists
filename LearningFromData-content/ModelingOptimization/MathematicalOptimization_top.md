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

(sec:MathematicalOptimization)=
# Mathematical optimization

```{epigraph}
> "With four parameters I can fit an elephant, and with five I can make him wiggle his trunk."

-- John von Neumann 
```
(see https://en.wikipedia.org/wiki/Von_Neumann%27s_elephant for the historical context of this quote.)

Mathematical optimization is a large area of research in applied mathematics. There are many applications in science and technology. Recently, there is a particular focus on this area due to its importance in machine learning and artificial intelligence, and as a potential candidate application for quantum computing algorithms.

In a broader context, optimization problems involve maximizing or minimizing a real-valued function by systematically choosing input values from within an allowed set and computing the value of the function.

```{admonition} Discrete or continuous optimization
Optimization problems can be divided into two categories, depending on whether the variables are continuous or discrete:
* An optimization problem is known as discrete if it involves finding an argument from a countable set such as an integer, permutation or graph.
* A problem is known as a continuous optimization if arguments from a continuous set must be found.

We will mainly be concerned with continuous optimization problems in scientific modeling for which the input variables $\pars$ are known as model parameters and the allowed set $V$ is some subset of an Euclidean space $\mathbb{R}^{p}$.
```

Mathematically, we want to consider the following *minimization* problem

```{prf:definition} Global minimization
:label: definition:MathematicalOptimization:global-minimization

Given a function $C : V \to \mathbb{R}$, where $V$ is a search space that possibly involves various constraints, we seek the element $\optpars \in V$ such that $C(\optpars) \leq C(\pars), \; \forall \pars \in V$.
```

We will often use the shorthand notation

\begin{equation}
\optpars = \underset{\pars \in V}{\operatorname{argmin}} C(\pars)
\end{equation}

to indicate the solution of a minimization problem.

The identification of $\optpars \in V$ such that $C(\optpars) \geq C(\pars), \; \forall \pars \in V$, is known as *maximization*. However, since the following is valid,

$$
C(\optpars) \leq C(\pars) \Leftrightarrow -C(\optpars) \geq -C(\pars),
$$ (eq:MathematicalOptimization:max-min)

a maximization problem can be recast as a minimization one and we will restrict ourselves to consider only minimization problems. 

The function $C$ has various names in different applications. It can be called a cost function, objective function or loss function (minimization), a utility function or fitness function (maximization), or, in certain fields, an energy function or energy functional. A feasible solution that minimizes (or maximizes, if that is the goal) the objective function is in general called an optimal solution.

```{prf:definition} Local minimization
:label: definition:MathematicalOptimization:local-minimization

A solution $\optpars \in V$ that fulfills 

$$
C(\optpars) \leq C(\pars), \; \forall \pars \in V, \; \text{where} \, \lVert \pars - \optpars \rVert \leq \delta,  
$$

for some $\delta > 0$ is known as a *local minimum*.
```

Generally, unless the cost function is convex in a minimization problem, there may be several local minima within $V$. In a convex problem, if there is a local minimum that is interior (not on the edge of the set of feasible elements), it is also the global minimum, but a nonconvex problem may have more than one local minimum not all of which need be global minima.

With the linear regression model we could find the best fit parameters by solving the normal equation. Although we could encounter problems associated with inverting a matrix, we do in principle have a closed-form expression for the model parameters. In general, however, the problem of optimizing the model parameters is a very difficult one. 

It is important to understand that the majority of available optimizers are not capable of making a distinction between locally optimal and globally optimal solutions. They will therefore, erroneously, treat the former as actual solutions to the global optimization problem. 
