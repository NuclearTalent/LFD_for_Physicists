# Gradient-descent optimization

*Gradient descent* is probably the most popular class of algorithms to perform optimization. It is certainly the most common way to optimize neural networks. Although there are different flavours of gradient descent, as will be discussed, the general feature is an iterative search for a (locally) optimal solution using the gradient to the cost function. Basically, the parameters are tuned in the opposite direction of the gradient to the objective function, thus aiming to follow the direction of the slope downhill until we reach a valley. The evaluation of this gradient at every iteration is often the major computational bottleneck. 

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
2. Most cost functions&mdash;in particular in many dimensions&mdash;correspond to very *complicated surfaces with several local minima*. In those cases, gradient descent will likely not find the global minimum.
3. Choosing a proper learning rate can be difficult. A learning rate that is too small leads to painfully slow convergence, while a learning rate that is too large can hinder convergence and cause the parameter updates to fluctuate around the minimum.
4. Standard gradient-descent has particular difficulties to navigate ravines and saddle points for which the gradient is large in some directions and small in others.
```

For the remainder of this chapter we will consider gradient descent methods for the minimization of data-dependent cost functions, for example representing a sum of squared residuals between model predictions and observed data such as Eq. {eq}`eq:LinearRegression:cost-function`. Note that we are interested in general models, not just restricted to linear ones, for which the computational cost for evaluating the cost function and its gradient could be significant (and scale with the number of data that enter the cost function). For situations where data is abundant there are variations of gradient descent that uses only fractions of the data set for computation of the gradient. 

