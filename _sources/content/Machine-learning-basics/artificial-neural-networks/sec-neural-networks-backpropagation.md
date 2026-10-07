(sec:NeuralNetBackProp)=
# Neural networks: Backpropagation

As we have seen, the final output of a feed-forward network can be expressed in terms of basic matrix-vector multiplications.
The unknown quantities are the weights $w_{ij}^l$ and biases $b_j^l$, and we need an algorithm for changing them so that our errors are as small as possible.
This leads us to the famous back propagation algorithm {cite}`Rumelhart1986`.

## Deriving the back propagation equations for a feed-forward network

The questions we want to ask are how changes in the biases and the
weights of our network change the cost function, and how we can use the
final output to modify the weights.

### Notation

We use the notation of {ref}`sec:NeuralNetFFNN`. Consider an $L$-layer network, i.e., $L-1$ hidden layers and an output layer $l=L$. Node $j$ in layer $l$ has the preactivation

\begin{equation}
z_j^l = \sum_{i=1}^{N_{l-1}} w_{ij}^l y_i^{l-1} + b_j^l,
\end{equation}

and the output $y_j^l = f^l(z_j^l)$. Here $N_{l-1}$ is the number of nodes in layer $l-1$, and $w_{ij}^l$ connects node $i$ in layer $l-1$ to node $j$ in layer $l$. The input layer performs no computation; we simply set $\boldsymbol{y}^0 \equiv \boldsymbol{x}$. The network output is $\boldsymbol{y}^L$.

In matrix-vector form, with signals as row vectors and $\boldsymbol{W}^l$ an $N_{l-1} \times N_l$ matrix,

\begin{equation}
\boldsymbol{z}^l = \boldsymbol{y}^{l-1} \boldsymbol{W}^l + \boldsymbol{b}^l, \qquad \boldsymbol{y}^l = f^l(\boldsymbol{z}^l).
\end{equation}

### Cost function

To derive the equations, let us start with a plain regression problem. For a single data instance with targets $\boldsymbol{t} = (t_1, \ldots, t_{N_L})$ we use the cost function

\begin{equation}
{\cal C} = \frac{1}{2}\sum_{j=1}^{N_L}\left(y_j^L - t_j\right)^2.
\end{equation}

For a batch of training data $\{ (\inputs_i, \targets_i) \}$ (see {ref}`sec:NeuralNetFFNN:learning-algorithm`), the cost is a sum over instances and so are its gradients. Other cost functions can also be considered; only the derivative $\partial {\cal C} / \partial y_j^L$ changes.

### Derivatives and the chain rule

From the definition of the preactivation $z_j^l$ we have

\begin{equation}
\frac{\partial z_j^l}{\partial w_{ij}^l} = y_i^{l-1}, \qquad
\frac{\partial z_j^l}{\partial b_j^l} = 1, \qquad
\frac{\partial z_j^l}{\partial y_i^{l-1}} = w_{ij}^l.
\end{equation}

The output of a node depends only on its own preactivation, $\partial y_j^l / \partial z_j^l = f^{l\prime}(z_j^l)$. For the sigmoid function, $f(z) = 1/(1+e^{-z})$, this derivative is particularly simple

\begin{equation}
f'(z_j^l) = f(z_j^l)\left[1 - f(z_j^l)\right] = y_j^l\left(1-y_j^l\right).
\end{equation}

### The error signal $\delta$

The key quantity is the derivative of the cost function with respect to the preactivation of node $j$ in layer $l$

\begin{equation}
\delta_j^l \equiv \frac{\partial {\cal C}}{\partial z_j^l}.
\end{equation}

Since $w_{ij}^l$ and $b_j^l$ affect the cost only through $z_j^l$, the chain rule immediately gives the gradients

\begin{equation}
\frac{\partial {\cal C}}{\partial w_{ij}^l} = y_i^{l-1}\, \delta_j^l, \qquad
\frac{\partial {\cal C}}{\partial b_j^l} = \delta_j^l.
\end{equation}

The weight gradient is the product of the signal entering the connection and the error signal at its end. In matrix form, $\partial {\cal C} / \partial \boldsymbol{W}^l = (\boldsymbol{y}^{l-1})^T \boldsymbol{\delta}^l$, which is an outer product with the same $N_{l-1} \times N_l$ shape as $\boldsymbol{W}^l$.

### Output layer

At the output layer the error signal follows directly from the cost function

\begin{equation}
\delta_j^L = \frac{\partial {\cal C}}{\partial y_j^L}\frac{\partial y_j^L}{\partial z_j^L} = \left(y_j^L - t_j\right) f^{L\prime}(z_j^L),
\end{equation}

or, using the Hadamard (element-wise) product $\odot$,

\begin{equation}
\boldsymbol{\delta}^L = \frac{\partial {\cal C}}{\partial \boldsymbol{y}^L} \odot f^{L\prime}(\boldsymbol{z}^L).
\end{equation}

The first factor measures how fast the cost changes with output $j$. If the cost does not depend much on a particular output node, then $\delta_j^L$ will be small. The second factor measures how fast the activation function changes at $z_j^L$, which is a cheap by-product of the forward pass.

```{admonition} Linear output for regression
:class: tip
Regression networks usually have a linear output layer, $f^L(z) = z$. Then $f^{L\prime} = 1$ and the output error is simply the residual, $\boldsymbol{\delta}^L = \boldsymbol{y}^L - \boldsymbol{t}$.
```

Two consequences of the gradient expressions are worth noting. When the incoming signal $y_i^{l-1}$ is small, the gradient with respect to $w_{ij}^l$ is also small and the weight learns slowly. The same happens when a sigmoid node saturates, i.e., when its output approaches $0$ or $1$, since then $f'(z) \approx 0$.

### Back-propagating the error

We need one more equation: the error signal in layer $l$ expressed in terms of the errors in layer $l+1$. Since $z_j^l$ affects the cost through all preactivations $z_k^{l+1}$ of the next layer, the chain rule gives

\begin{equation}
\delta_j^l = \sum_{k=1}^{N_{l+1}} \frac{\partial {\cal C}}{\partial z_k^{l+1}}\frac{\partial z_k^{l+1}}{\partial z_j^{l}} = \sum_{k=1}^{N_{l+1}} \delta_k^{l+1}\frac{\partial z_k^{l+1}}{\partial z_j^{l}}.
\end{equation}

With $z_k^{l+1} = \sum_{i} w_{ik}^{l+1} y_i^{l} + b_k^{l+1}$ and $y_i^l = f^l(z_i^l)$ we find $\partial z_k^{l+1} / \partial z_j^l = w_{jk}^{l+1} f^{l\prime}(z_j^l)$, so that

\begin{equation}
\delta_j^l = f^{l\prime}(z_j^l) \sum_{k=1}^{N_{l+1}} w_{jk}^{l+1}\, \delta_k^{l+1},
\qquad\text{i.e.,}\qquad
\boldsymbol{\delta}^l = \left(\boldsymbol{\delta}^{l+1} \left(\boldsymbol{W}^{l+1}\right)^T\right) \odot f^{l\prime}(\boldsymbol{z}^l).
\end{equation}

The error signal travels backwards through the same weights as the forward signal, but with the transposed matrix.

## The back-propagation algorithm

The equations above provide the gradient of the cost function with respect to all weights and biases.

*Summary.*
1. Set $\boldsymbol{y}^0 = \boldsymbol{x}$.
2. Forward pass: for $l = 1, 2, \ldots, L$ compute and store $\boldsymbol{z}^l = \boldsymbol{y}^{l-1} \boldsymbol{W}^l + \boldsymbol{b}^l$ and $\boldsymbol{y}^l = f^l(\boldsymbol{z}^l)$.
3. Output error: $\boldsymbol{\delta}^L = \dfrac{\partial {\cal C}}{\partial \boldsymbol{y}^L} \odot f^{L\prime}(\boldsymbol{z}^L)$.
4. Backward pass: for $l = L-1, L-2, \ldots, 1$ compute $\boldsymbol{\delta}^l = \left(\boldsymbol{\delta}^{l+1} (\boldsymbol{W}^{l+1})^T\right) \odot f^{l\prime}(\boldsymbol{z}^l)$.
5. Gradient-descent update for all layers $l = 1, 2, \ldots, L$

\begin{equation}
\boldsymbol{W}^l \leftarrow \boldsymbol{W}^l - \eta \left(\boldsymbol{y}^{l-1}\right)^T \boldsymbol{\delta}^l, \qquad
\boldsymbol{b}^l \leftarrow \boldsymbol{b}^l - \eta\, \boldsymbol{\delta}^l.
\end{equation}

The parameter $\eta$ is the learning rate.
In practice one uses stochastic gradient descent with mini-batches and an outer loop that steps through multiple epochs of training. With $N$ instances stacked as rows of $\boldsymbol{Y}^{l-1}$ and $\boldsymbol{\Delta}^l$, the batch gradients are $\partial {\cal C} / \partial \boldsymbol{W}^l = (\boldsymbol{Y}^{l-1})^T \boldsymbol{\Delta}^l$ and $\partial {\cal C} / \partial \boldsymbol{b}^l = $ the sum of the rows of $\boldsymbol{\Delta}^l$. The matrix product performs the sum over the batch.

```{admonition} Weight conventions in code
:class: tip
The row-vector convention $\boldsymbol{Z} = \boldsymbol{X} \boldsymbol{W} + \boldsymbol{b}$ matches `X @ W + b` in NumPy. Note that PyTorch's `nn.Linear` stores the transposed matrix, with shape $N_l \times N_{l-1}$, such that `layer.weight.T` corresponds to $\boldsymbol{W}^l$.
```

## Learning challenges

The back-propagation algorithm works by going from
the output layer to the input layer, propagating the error gradient. The learning algorithm uses these
gradients to update each parameter with a Gradient Descent (GD) step.

Unfortunately, the gradients often get smaller and smaller as the
algorithm progresses down to the first hidden layers. Each step of the backward pass multiplies by a factor $f^{l\prime}(z^l_j)$, which is at most $1/4$ for the sigmoid. As a result, the
GD update step leaves the lower layer connection weights
virtually unchanged, and training never converges to a good
solution. This is known in the literature as 
**the vanishing gradients problem**. 

In other cases, the opposite can happen, namely that the gradients grow bigger and
bigger. The result is that many of the layers get large updates of the 
weights and the learning algorithm diverges. This is the **exploding gradients problem**, which is mostly encountered in recurrent neural networks. More generally, deep neural networks suffer from unstable gradients, different layers may learn at widely different speeds.
