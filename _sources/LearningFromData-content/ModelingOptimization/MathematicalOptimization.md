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

Mathematical optimization is a large area of research in applied mathematics with many applications in science and technology. Recently, there is a particular focus on this area due to its importance in machine learning and artificial intelligence, and as a potential candidate for quantum computing algorithms.

In a broader context, optimization problems involve maximizing or minimizing a real-valued function by systematically choosing input values from within an allowed set and computing the value of the function.

```{admonition} Discrete or continuous optimization
Optimization problems can be divided into two categories, depending on whether the variables are continuous or discrete:
* An optimization problem is known as discrete if it involves finding an object from a countable set such as an integer, permutation or graph.
* A problem is known as a continuous optimization if arguments from a continuous set must be found.

We will mainly be concerned with continuous optimization problems in scientific modeling for which the input variables $\pars$ are known as model parameters and the allowed set $V$ is some subset of an Euclidean space $\mathbb{R}^{n}$.
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


## Gradient-descent optimization

*Gradient descent* is probably the most popular class of algorithms to perform optimization. It is certainly the most common way to optimize neural networks. Although there are different flavours of gradient descent, as will be discussed, the general feature is an iterative search for a (locally) optimal solution using the gradient of the cost function. Basically, the parameters are tuned in the opposite direction of the gradient of the objective function, thus aiming to follow the direction of the slope downhill until we reach a valley. The evaluation of this gradient at every iteration is often the major computational bottleneck. 

```{prf:algorithm} Gradient descent optimization
:label: algorithm:MathematicalOptimization:gradient-descent
1. Start from a *random initialization* of the parameter vector $\pars_0$.
2. At iteration $n$:
   1. Evaluate the gradient of the cost function at the corrent position $\pars_n$: $\boldsymbol{\nabla} C_n \equiv \left. \boldsymbol{\nabla}_{\pars} C(\pars) \right|_{\pars=\pars_n}$.
   2. Choose a *learning rate* $\eta_n$. This could be the same at all iterations ($\eta_n = \eta$), or it could be given by a learning schedule that typically describes some decreasing function that leads to smaller and smaller steps.
   3. Move in the direction of the negative gradient:
      $\pars_{n+1} = \pars_n - \eta_n \boldsymbol{\nabla} C_n$.
3. Continue for a fixed number of iterations, or until the gradient vector $\boldsymbol{\nabla} C_n$ is smaller than some chosen precision $\epsilon$.
```

Gradient descent is a general optimization algorithm. However, there are several important issues that should be considered before using it.

```{admonition} Challenges for gradient descent
1. It requires the computation of partial derivatives of the cost function. This might be straight-forward for the linear regression method, see Eq. {eq}`eq:LinearRegression:gradient`, but can be very difficult for other models. Numerical differentiation can be computationally costly. Instead, *automatic differentiation* has become an important tool and there are software libraries for different programming languages. See, e.g., [JAX](https://jax.readthedocs.io/en/latest/) for Python, which is well worth exploring. 
2. Most cost functions&mdash;in particular in many dimensions&mdash;correspond to very *complicated surfaces with several local minima*. In those cases, gradient descent will not likely not find the global minimum.
3. Choosing a proper learning rate can be difficult. A learning rate that is too small leads to painfully slow convergence, while a learning rate that is too large can hinder convergence and cause the parameter updates to fluctuate around the minimum.
4. Standard gradient-descent has particular difficulties to navigate ravines and saddle points for which the gradient is large in some directions and small in others.
```

For the remainder of this chapter we will consider gradient descent methods for the minimization of data-dependent cost functions, for example representing a sum of squared residuals between model predictions and observed data such as Eq. {eq}`eq:LinearRegression:cost-function`. Note that we are interested in general models, not just restricted to linear ones, for which the computational cost for evaluating the cost function and its gradient could be significant (and scale with the number of data that enter the cost function). For situations where data is abundant there are variations of gradient descent that uses only fractions of the data set for computation of the gradient. 

## Batch, stochastic and mini-batch gradient descent

{{ sub_extra_tif385_admonition }}

The use of the full data set in the cost function for every parameter update would correspond to *batch gradient descent* (BGD). The gradient of the cost function then has the following generic form

\begin{equation}
\boldsymbol{\nabla} C_n \equiv \left. \boldsymbol{\nabla}_{\pars} C(\pars) \right|_{\pars=\pars_n}
= \sum_{i=1}^{N_d} \left. \boldsymbol{\nabla}_{\pars} C^{(i)}(\pars) \right|_{\pars=\pars_n},
\end{equation}

where the sum runs over the data set (of length $N_d$) and $C^{(i)}(\pars)$ is the cost function evaluated for a single data instance $\data_i = (\inputs_i, \outputs_i)$.

A typical Python implementation of batch gradient descent would look something like the following:

```python
# Pseudo-code for batch gradient descent
for i in range(N_epochs):
  params_gradient = evaluate_gradient(cost_function, data, params)
  params = params - learning_rate * params_gradient
```
for a fixed numer of epochs `N_epochs` and a function `evaluate_gradient` that returns the gradient vector of the cost function (that depends on the data `data` and the model parameters `params`) with respect to the parameters. The update step depends on the `learning_rate` hyperparameter.

Depending on the size of the data set, batch gradient descent can be rather inefficient since the evaluation of the gradient depends on all data. Instead, one often employs *stochastic gradient descent* (SGD) for which parameter updates are performed for every data instance $\data_i = (\inputs_i, \outputs_i)$ at a time. Note that the total number of iterations for SGD is $N_\mathrm{epochs} \times N_d$.

SGD performs frequent updates that can be performed fast. The updates are often characterized by a high variance that can cause the cost function to fluctuate heavily during the iterations. This ultimately complicates convergence to the exact minimum, as SGD will keep overshooting. However, employing a learning rate that slowly decreases with iterations, SGD can be much more efficient than BGD. A typical Python implementation would look something like the following:

```python
# Pseudo-code for stochastic gradient descent
for i in range(N_epochs):
  np.random.shuffle(data)
  for data_instance in data:
    params_gradient = evaluate_gradient(cost_function, data_instance, params)
    params = params - learning_rate * params_gradient
```

where you should note the loop over all data instances for each epoch. Note that we shuffle the training data at every epoch.

Finally, *mini-batch gradient descent* (MBGD) combines the best of the previous algorithms and performs an update for every mini-batch of data

\begin{equation}
\pars \mapsto \pars - \eta \boldsymbol{\nabla} C_{i*N_{mb}:(i+1)*N_{mb}}(\pars),
\end{equation}

where $N_{mb}$ is the mini-batch size. This way one can make use of highly optimized matrix optimizations for the reasonably sized mini-batch evaluations, and one usually finds much reduced variance of the parameter updates which can lead to more stable convergence. Mini-batch gradient descent is typically the algorithm of choice when training a neural network. The total number of iterations for MBGD is $N_\mathrm{epochs} \times N_d / N_{mb}$.

```python
# Pseudo-code for mini-batch gradient descent
for i in range(N_epochs):
  np.random.shuffle(data)
  for data_batch in get_batches(data, batch_size=50):
    params_gradient = evaluate_gradient(cost_function, data_batch, params)
    params = params - learning_rate * params_gradient
```

Be aware that the terms SGD or BGD can both be used to denote mini-batch gradient descent. 

## Adaptive gradient descent algorithms

{{ sub_extra_tif385_admonition }}

As outlined above, there are several convergence challenges for the standard gradient-descent methods. These are in general connected with the difficulty of navigating complicated cost function surfaces using only pointwise information on the gradient. The use of the history of past updates can help to adapt the learning schedule and has been shown to significantly increase the efficiency of gradient descent. Somewhat simplified, the adaptive versions improves the parameter update by adding a fraction of the past update vector to the current one.

Some examples of commonly employed, adaptive methods are Adagrad {cite}`Duchi:2011`, Adadelta {cite}`Zeiler:2012`, RMSprop, and Adam {cite}`Kingma:2014`. 

### Adagrad

Adagrad {cite}`Duchi:2011` is a simple algorithm that uses the history of past updates to adapt the learning rate to the different parameters. Let us introduce a shorthand notation $j_{n,i}$ for the partial derivative of the cost function with respect to parameter $\para_i$ at the position $\pars_n$ corresponding to iteration $n$

\begin{equation}
j_{n,i} \equiv \left. \frac{\partial C}{\partial \para_i} \right|_{\pars = \pars_n}.
\end{equation}

We also introduce a diagonal matrix $J^2_n \in \mathbb{R}^{N_p \times N_p}$ where the $i$th diagonal element 

\begin{equation}
J^2_{n,ii} \equiv \sum_{k=1}^{n} j_{k,i}^2
\end{equation}

is the sum of the squares of the gradients with respect to $\para_i$ up to iteration $n$. In its update rule, at iteration $n$, Adagrad modifies the general learning rate $\eta_n$ for every parameter $\para_i$ based on the past gradients that have been computed as described by $J^2_{n,ii}$. The parameter $\para_i$ at the next iteration $n+1$ is then given by

$$
\para_{n+1,i} = \pars_{n,i} - \frac{\eta}{\sqrt{J^2_{n,ii} + \varepsilon}} j_{n,i},
$$ (eq:MathematicalOptimization:adagrad)

with $\varepsilon$ a small, positive number to avoid division by zero.

Using Eq. {eq}`eq:MathematicalOptimization:adagrad` the learning schedule does not have to be tuned by the user as it is adapted by the history of past gradients. This is the main advantage of this algorithm. At the same time, its main weakness is the accumulation of the squared gradients in the denominator which implies that the learning rate eventually becomes infinitesimally small, at which point the convergence halts.

### RMSprop

RMSprop is an extension of Adagrad that seeks to reduce its aggressive, monotonically decreasing learning rate. Instead of storing the sum of past squared gradients, the denominator is defined as a decaying average of past squared gradients. Labeling the decaying average at iteration $n$ by $\bar{{J}^2}_{n,ii}$, we introduce a decay variable $\gamma$ and define

\begin{equation}
\bar{J}^2_{n,ii} = \gamma \bar{J}^2_{n-1,ii} + (1-\gamma) j_{n,i}^2.
\end{equation}

The inventor of RMSprop, Geoff Hinton, suggests setting the decay variable $\gamma=0.9$ , while a good default value for the learning rate $\eta$ is 0.001. The update rule in RMSprop is then

\begin{equation}
\para_{n+1,i} = \pars_{n,i} - \frac{\eta}{\sqrt{\bar{J}^2_{n,ii} + \varepsilon}} j_{n,i}.
\end{equation}

### Adam

Adaptive Moment Estimation (Adam) {cite}`Kingma:2014` also computes adaptive learning rates for each parameter. However, in addition to storing an exponentially decaying average of past squared gradients like Adagrad and RMSprop, Adam also keeps an exponentially decaying average of past gradients similar to a momentum. Describing this latter quantity by the diagonal matrix $\hat{M}_n$ (at iteration $n$) we have

\begin{align}
\bar{M}_{n,ii} &= \gamma_1 \bar{M}_{n-1,ii} + (1-\gamma_1) j_{n,i}, \\
\bar{J}^2_{n,ii} &= \gamma_2 \bar{J}^2_{n-1,ii} + (1-\gamma_2) j_{n,i}^2.
\end{align}

Both of these quantities are initialized with zero vectors ($\bar{M}_{0,ii}=0$ and $\bar{J}^2_{0,ii}=0$ for all $i$) which tends to introduce a bias for early time steps. This bias can be large if $\gamma_1$ and $\gamma_2$ are close to one. It was therefore proposed to use bias-corrected first and second moment estimates

\begin{align}
\hat{M}_{n,ii} &= \frac{\bar{M}_{n,ii}}{1 - (\gamma_1)^n}, \\
\hat{J}^2_{n,ii} &= \frac{\bar{J}^2_{n,ii}}{1 - (\gamma_2)^n}.
\end{align}

The update rule then becomes

\begin{equation}
\para_{n+1,i} = \pars_{n,i} - \frac{\eta}{\sqrt{\hat{J}^2_{n,ii}} + \varepsilon} \hat{M} _{n,ii}.
\end{equation}


Default, recommended values are $\gamma_1=0.9$, $\gamma_2=0.999$, and $\varepsilon=10^{-8}$. 

Adam has become the method of choice in many machine-learning implementations. An explanation and comparison of different gradient-descent algorithms is presented in a [blog post](https://www.ruder.io/optimizing-gradient-descent) by Sebastian Ruder.