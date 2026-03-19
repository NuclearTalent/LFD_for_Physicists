# Adaptive gradient descent algorithms

{{ sub_extra_tif385_admonition }}

As outlined above, there are several convergence challenges for the standard gradient-descent methods. These are in general connected with the difficulty of navigating complicated cost function surfaces using only pointwise information on the gradient. The use of the history of past updates can help to adapt the learning schedule and has been shown to significantly increase the efficiency of gradient descent. Somewhat simplified, the adaptive versions improves the parameter update by adding a fraction of the past update vector to the current one.

Some examples of commonly employed, adaptive methods are Adagrad {cite}`Duchi:2011`, Adadelta {cite}`Zeiler:2012`, RMSprop, and Adam {cite}`Kingma:2014`. 

## Adagrad

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

## RMSprop

RMSprop is an extension of Adagrad that seeks to reduce its aggressive, monotonically decreasing learning rate. Instead of storing the sum of past squared gradients, the denominator is defined as a decaying average of past squared gradients. Labeling the decaying average at iteration $n$ by $\bar{{J}^2}_{n,ii}$, we introduce a decay variable $\gamma$ and define

\begin{equation}
\bar{J}^2_{n,ii} = \gamma \bar{J}^2_{n-1,ii} + (1-\gamma) j_{n,i}^2.
\end{equation}

The inventor of RMSprop, Geoff Hinton, suggests setting the decay variable $\gamma=0.9$ , while a good default value for the learning rate $\eta$ is 0.001. The update rule in RMSprop is then

\begin{equation}
\para_{n+1,i} = \pars_{n,i} - \frac{\eta}{\sqrt{\bar{J}^2_{n,ii} + \varepsilon}} j_{n,i}.
\end{equation}

## Adam

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