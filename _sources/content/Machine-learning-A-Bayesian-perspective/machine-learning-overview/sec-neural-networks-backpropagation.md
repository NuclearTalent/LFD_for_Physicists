(sec:NeuralNetBackProp)=
# \*Neural networks: Backpropagation

<div class="highlight-section">

As we have seen the final output of a feed-forward network can be expressed in terms of basic matrix-vector multiplications.
The unknowwn quantities are our weights $w_{ij}$ and we need to find an algorithm for changing them so that our errors are as small as possible.
This leads us to the famous back propagation algorithm {cite}`Rumelhart1986`.

## Deriving the back propagation code for a multilayer perceptron model

The questions we want to ask are how do changes in the biases and the
weights in our network change the cost function and how can we use the
final output to modify the weights?

To derive these equations let us start with a plain regression problem
and define our cost function as

\begin{equation}

{\cal C}(\boldsymbol{W})  =  \frac{1}{2}\sum_{i=1}^n\left(y_i - t_i\right)^2, 

\end{equation}

where the $t_i$s are our $n$ targets (the values we want to
reproduce), while the outputs of the network after having propagated
all inputs $\boldsymbol{x}$ are given by $y_i$.  Other cost functions can also be considered.

### Definitions

With our definition of the targets $\boldsymbol{t}$, the outputs of the
network $\boldsymbol{y}$ and the inputs $\boldsymbol{x}$ we
define now the activation $z_j^l$ of node/neuron/unit $j$ of the
$l$-th layer as a function of the bias, the weights which add up from
the previous layer $l-1$ and the forward passes/outputs
$\boldsymbol{a}^{l-1}$ from the previous layer as


\begin{equation}

z_j^l = \sum_{i=1}^{M_{l-1}}w_{ij}^la_i^{l-1}+b_j^l,

\end{equation}

where $b_j^l$ are the biases from layer $l$.  Here $M_{l-1}$
represents the total number of nodes/neurons/units of layer $l-1$. 

```{admonition} Activation outputs
:class: tip
In this derivation we will denote the output of neuron $j$ in layer $l$ as a_j^{l}. Collectively, all outputs from layer $l$ corresponds to the vector $\boldsymbol{a}^l$.
```

```{admonition} Final outputs
:class: tip
We will reserve the output notation $y$ exclusively for the final layer such that an $L$-layer network has final output $\boldsymbol{y} \equiv \boldsymbol{a}^L$. Note that it is quite common to use a different activation function for the final outputs as compared with the inner layers.
```

We can rewrite this *(figure to be inserted)* in a more
compact form as the matrix-vector products we discussed earlier,

\begin{equation}

\boldsymbol{z}^l = \left(\boldsymbol{W}^l\right)^T\boldsymbol{a}^{l-1}+\boldsymbol{b}^l.

\end{equation}

With the activation values $\boldsymbol{z}^l$ we can in turn define the
output of layer $l$ as $\boldsymbol{a}^l = f(\boldsymbol{z}^l)$ where $f$ is our
activation function. In the examples here we will use the sigmoid
function discussed in the logistic regression lecture. We will also use the same activation function $f$ for all layers
and their nodes.  It means we have

\begin{equation}

a_j^l = f(z_j^l) = \frac{1}{1+\exp{-(z_j^l)}}.

\end{equation}


### Derivatives and the chain rule

From the definition of the activation $z_j^l$ we have

\begin{equation}

\frac{\partial z_j^l}{\partial w_{ij}^l} = a_i^{l-1},

\end{equation}

and

\begin{equation}

\frac{\partial z_j^l}{\partial a_i^{l-1}} = w_{ji}^l. 

\end{equation}

With our definition of the activation function we have (note that this function depends only on $z_j^l$)

\begin{equation}

\frac{\partial a_j^l}{\partial z_j^{l}} = a_j^l(1-a_j^l)=f(z_j^l) \left[ 1-f(z_j^l) \right]. 

\end{equation}


### Derivative of the cost function

With these definitions we can now compute the derivative of the cost function in terms of the weights.

Let us specialize to the output layer $l=L$. Our cost function is

\begin{equation}

{\cal C}(\boldsymbol{W^L})  =  \frac{1}{2}\sum_{i=1}^n\left(y_i - t_i\right)^2=\frac{1}{2}\sum_{i=1}^n\left(a_i^L - t_i\right)^2, 

\end{equation}

The derivative of this function with respect to the weights is

\begin{equation}

\frac{\partial{\cal C}(\boldsymbol{W^L})}{\partial w_{jk}^L}  =  \left(a_j^L - t_j\right)\frac{\partial a_j^L}{\partial w_{jk}^{L}}, 

\end{equation}

The last partial derivative can easily be computed and reads (by applying the chain rule)

\begin{equation}

\frac{\partial a_j^L}{\partial w_{jk}^{L}} = \frac{\partial a_j^L}{\partial z_{j}^{L}}\frac{\partial z_j^L}{\partial w_{jk}^{L}}=a_j^L(1-a_j^L)a_k^{L-1},  

\end{equation}



### Bringing it together, first back propagation equation

We have thus

\begin{equation}

\frac{\partial{\cal C}(\boldsymbol{W^L})}{\partial w_{jk}^L}  =  \left(a_j^L - t_j\right)a_j^L(1-a_j^L)a_k^{L-1}, 

\end{equation}

Defining

\begin{equation}

\delta_j^L = a_j^L(1-a_j^L)\left(a_j^L - t_j\right) = f'(z_j^L)\frac{\partial {\cal C}}{\partial (a_j^L)},

\end{equation}

and using the Hadamard product of two vectors we can write this as

\begin{equation}

\boldsymbol{\delta}^L = f'(\boldsymbol{z}^L)\circ\frac{\partial {\cal C}}{\partial (\boldsymbol{a}^L)}.

\end{equation}

This is an important expression. The second term on the right handside
measures how fast the cost function is changing as a function of the $j$th
output activation.  If, for example, the cost function doesn't depend
much on a particular output node $j$, then $\delta_j^L$ will be small,
which is what we would expect. The first term on the right, measures
how fast the activation function $f$ is changing at a given activation
value $z_j^L$.

Notice that everything in the above equations is easily computed.  In
particular, we compute $z_j^L$ while computing the behaviour of the
network, and it is only a small additional overhead to compute
$f'(z^L_j)$.  The exact form of the derivative with respect to the
output depends on the form of the cost function.
However, provided the cost function is known there should be little
trouble in calculating

\begin{equation}

\frac{\partial {\cal C}}{\partial (a_j^L)}

\end{equation}

With the definition of $\delta_j^L$ we have a more compact definition of the derivative of the cost function in terms of the weights, namely

\begin{equation}

\frac{\partial{\cal C}(\boldsymbol{W^L})}{\partial w_{jk}^L}  =  \delta_j^La_k^{L-1}.

\end{equation}

### Derivatives in terms of $z_j^L$

It is also easy to see that our previous equation can be written as

\begin{equation}

\delta_j^L =\frac{\partial {\cal C}}{\partial z_j^L}= \frac{\partial {\cal C}}{\partial a_j^L}\frac{\partial a_j^L}{\partial z_j^L},

\end{equation}

which can also be interpreted as the partial derivative of the cost function with respect to the biases $b_j^L$, namely

\begin{equation}

\delta_j^L = \frac{\partial {\cal C}}{\partial b_j^L}\frac{\partial b_j^L}{\partial z_j^L}=\frac{\partial {\cal C}}{\partial b_j^L},

\end{equation}
That is, the error $\delta_j^L$ is exactly equal to the rate of change of the cost function as a function of the bias. 

<!-- !split -->

We have now three equations that are essential for the computations of the derivatives of the cost function at the output layer. These equations are needed to start the algorithm and they are

*The starting equations.* 


\begin{equation}
\frac{\partial{\cal C}(\boldsymbol{W^L})}{\partial w_{jk}^L}  =  \delta_j^La_k^{L-1},
\end{equation}

and

\begin{equation}
\delta_j^L = f'(z_j^L)\frac{\partial {\cal C}}{\partial (a_j^L)},
\end{equation}

and


\begin{equation}
\delta_j^L = \frac{\partial {\cal C}}{\partial b_j^L},
\end{equation}





An interesting consequence of the above equations is that when the
activation $a_k^{L-1}$ is small, the gradient term, that is the
derivative of the cost function with respect to the weights, will also
tend to be small. We say then that the weight learns slowly, meaning
that it changes slowly when we minimize the weights via say gradient
descent. In this case we say the system learns slowly.

Another interesting feature is that is when the activation function,
represented by the sigmoid function here, is rather flat when we move towards
its end values $0$ and $1$. In these
cases, the derivatives of the activation function will also be close
to zero, meaning again that the gradients will be small and the
network learns slowly again.



We need a fourth equation and we are set. We are going to propagate
backwards in order to determine the weights and biases. In order
to do so we need to represent the error in the layer before the final
one $L-1$ in terms of the errors in the final output layer.

### Final back-propagating equation

We have that (replacing $L$ with a general layer $l$)

\begin{equation}

\delta_j^l =\frac{\partial {\cal C}}{\partial z_j^l}.

\end{equation}

We want to express this in terms of the equations for layer $l+1$. Using the chain rule and summing over all $k$ entries we have

\begin{equation}

\delta_j^l =\sum_k \frac{\partial {\cal C}}{\partial z_k^{l+1}}\frac{\partial z_k^{l+1}}{\partial z_j^{l}}=\sum_k \delta_k^{l+1}\frac{\partial z_k^{l+1}}{\partial z_j^{l}},

\end{equation}

and recalling that

\begin{equation}

z_j^{l+1} = \sum_{i=1}^{M_{l}}w_{ij}^{l+1}a_i^{l}+b_j^{l+1},

\end{equation}

with $M_l$ being the number of nodes in layer $l$, we obtain

\begin{equation}

\delta_j^l =\sum_k \delta_k^{l+1}w_{kj}^{l+1}f'(z_j^l),

\end{equation}

This is our final equation.

We are now ready to set up the algorithm for back propagation and learning the weights and biases.

## Setting up the back-propagation algorithm



The four equations  provide us with a way of computing the gradient of the cost function. Let us write this out in the form of an algorithm.

*Summary.* 
* First, we set up the input data $\boldsymbol{x}$ and the activations $\boldsymbol{z}_1$ of the input layer and compute the activation function and the outputs $\boldsymbol{a}^1$.
* Secondly, perform the feed-forward until we reach the output layer. I.e., compute all activation functions and the pertinent outputs $\boldsymbol{a}^l$ for $l=2,3,\dots,L$.
* Compute the ouput error $\boldsymbol{\delta}^L$ by

\begin{equation}

\delta_j^L = f'(z_j^L)\frac{\partial {\cal C}}{\partial (a_j^L)}.

\end{equation}

* Back-propagate the error for each $l=L-1,L-2,\dots,2$ as

\begin{equation}

\delta_j^l = \sum_k \delta_k^{l+1}w_{kj}^{l+1}f'(z_j^l).

\end{equation}

* Finally, update the weights and the biases using gradient descent for each $l=L-1,L-2,\dots,2$ and update the weights and biases according to the rules

\begin{equation}

w_{jk}^l\leftarrow  w_{jk}^l- \eta \delta_j^la_k^{l-1},

\end{equation}

\begin{equation}

b_j^l \leftarrow b_j^l-\eta \frac{\partial {\cal C}}{\partial b_j^l}=b_j^l-\eta \delta_j^l,

\end{equation}



The parameter $\eta$ is the learning rate.
Here it is convenient to use stochastic gradient descent with mini-batches and an outer loop that steps through multiple epochs of training.


## Learning challenges

The back-propagation algorithm works by going from
the output layer to the input layer, propagating the error gradient. The learning algorithm uses these
gradients to update each parameter with a Gradient Descent (GD) step.

Unfortunately, the gradients often get smaller and smaller as the
algorithm progresses down to the first hidden layers. As a result, the
GD update step leaves the lower layer connection weights
virtually unchanged, and training never converges to a good
solution. This is known in the literature as 
**the vanishing gradients problem**. 

In other cases, the opposite can happen, namely that the gradients grow bigger and
bigger. The result is that many of the layers get large updates of the 
weights and the learning algorithm diverges. This is the **exploding gradients problem**, which is mostly encountered in recurrent neural networks. More generally, deep neural networks suffer from unstable gradients, different layers may learn at widely different speeds.

</div>