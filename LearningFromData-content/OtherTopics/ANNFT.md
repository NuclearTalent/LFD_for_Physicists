(sec:ANNFT)=
# ANNs in the large-width limit

Machine learning methods such as artificial neural networks (ANNs) are offering physicists new ways to explore and understand a wide range of physics systems, as well as improving existing solution methods {cite}`Mehta2019`.
ANNs are commonly treated as black boxes that are empirically optimized. Given their growing prominence as a tool for physics research, it is desirable to have a framework that allows for a more structured analysis based on an understanding of how they work. 
Several authors have proposed a field theory approach to analyze and optimize neural networks using a combination of methods from quantum field theory and Bayesian statistics {cite}`Roberts:2021lll,Roberts:2021fes,Halverson:2020trp,Halverson:2021aot`. It is based on expanding about the large-width limit of ANNs and is known as ANNFT.


Dan Roberts, in an essay entitled "Why is AI hard and Physics simple?" {cite}`Roberts:2021lll`, claims that the principle of *sparsity* means that methods of theoretical physics and associated physical intuition can be powerful in understanding machine learning..
Roberts interprets Wigner’s observations
about "The Unreasonable Effectiveness of Mathematics in the Natural Sciences" as "the laws
of physics have an (unreasonable?) lack of algorithmic complexity".
The key idea is that many neural network architectures (including the common ones) have a well-defined limit when the network width (which is the number of neurons in each layer) is taken to infinity. In particular, they reduce to Gaussian processes (GPs), and with gradient-based training they evolve as linear models according to the neural tangent kernel (or NTK). This infinite width limit by itself is not an accurate model for actual deep-learning networks, but there is a way to describe finite-width effects systematically using the correspondence with field theories (statistical or quantum). In this correspondence, the infinite-width limit is associated with free (non-interacting) theories that can be corrected perturbatively for finite width as weakly interacting theories. The concepts of effective (field) theories carry over as well, as the information propagation through the layers of a deep neural network can be understood in terms of a renormalization group (RG) flow. A fixed point analysis motivates strategies for tuning the network to criticality, which deals with gradient problems (blowing up and going to zero).

## Sparsity

Roberts argues how the most generic theory in a quantum field theory framework without guiding principles would start with all combinations of interactions between the particles in the theory but that applying several guiding principles of sparsity will drastically reduce the algorithmic complexity.
He first discusses why AI is hard by considering all possible $n$-pixel images that take on two values (e.g., black or white), so that there are $2^n$ different images. 
If each of these images has one of two possible labels (e.g., cat/not-cat or spin-up/spin-down), then the images can be labeled $2^{2^n}$ ways. This is a really big number. If the labels don't correlate with image *features*, then you can't do better than memorizing images with their labels.

Roberts follows by discussing why physics is simple; these are the arguments that lead him to paraphrase Wigner.
In particular, he analyzes the degrees of freedom (dofs) within a QFT-like framework. When thinking about the associated counting, it is convenient to have the Ising model in mind as a concrete and familiar example.
The starting point is a generic theory with all interactions between all spins; two at a time, three at a time, and so on. Generically the strength of the couplings for these interactions would all be different.

A summary of the sparsity counting of dofs is:

$$
 2^{\mathcal{O}(N)} \xrightarrow[\text{locality}]{k}
 \mathcal{O}(N^k) \xrightarrow[\text{locality}]{\text{spatial}}
 \mathcal{O}(N) \xrightarrow[\text{invariance}]{\text{translational}}
\mathcal{O}(1) .
$$

The big picture is that the neural network acts like a parameterized function

$$
    f(x; \pars) ,
$$

where the input vector is $x$ (we don't use boldface or arrows for this vector) and $\pars$ is the collective vector of all the parameters (weights and biases).


## Large-width limit

:::{figure} ./figs/network_schematic_2.png
:height: 400px
:name: fig-ANNFT-network_schematic

Schematic of a feed-forward neural network with two inputs $x_{\alpha}$ and one output $z_{\alpha}^{(L+1)}$, where $\alpha$ is an index running over the dataset $\mathcal{D}$. The width is $n$ and the depth is $L+1$, with $L$ being the number of hidden layers. The neurons are totally connected (some lines are omitted here for clarity).
:::

:::{figure} ./figs/neuron_schematic_4.png
:height: 150px
:name: fig-ANNFT-neuron_schematic

Schematic of a neuron within a neural network. In the layer $\ell$, the product between the weight matrix $W^{(\ell)}$ and the previous layers' output $\sigma^{(\ell-1)}$ is summed over the width of the prior layer $n_{\ell-1}$, and a bias vector $b^{(\ell)}$ is added, forming the preactivation $z^{(\ell)}$. The activation function $\sigma$ acts on the preactivation to yield the output $\sigma \bigl(z^{(\ell)}\bigr)$ (also notated $\sigma^{(\ell)}$) to be passed to the next layer.
:::


For a given initialization of the network parameters $\pars$, the preactivations and the output function $f$ are uniquely determined.
However, a repeated random initialization of $\pars$ induces a probability distribution on preactivations and $f$.
Explicit expressions for these probability distributions in the limit of large width $n$ can be derived, with the ratio of depth to width revealed as an expansion parameter for the distribution's action. 
The output distribution in a given layer $\ell$ refers to the distribution of preactivations $z^{(\ell)}_{j,\alpha}$. 
This choice allows for parallel treatment of all other layers with the function distribution in the output layer. 

To achieve the desired functional relationship between $x_{i,\alpha}$ and $y_{j,\alpha}$, a neural network is trained by adjusting the weights and biases in each layer according to the gradients of the loss function $\mathcal{L}\bigl(f(x,\pars),y\bigr)$. 
The loss function quantifies the difference between the network output $f(x,\pars)$ and the output data $y$, and the goal of training is to minimize $\mathcal{L}\bigl(f(x,\pars),y\bigr)$. 
The gradients of $\mathcal{L}\bigl(f(x,\pars),y\bigr)$ with respect to the network parameters $\pars$ depend on the size of the output, as well as the architecture hyperparameters. 
It is known empirically that poor choices of architecture and/or initialization lead to exploding/vanishing gradients in the absence of adaptive learning algorithms, and this was problematic for training networks for many years.

The ANN output function $f(x,\pars)$ for any fixed $\pars$ (that is, specified weights and biases) is a deterministic function.
But, as already stressed, with repeated initializations of the ANN with $\pars$ drawn from random distributions, the network acquires a probability distribution over functions $p\left(f(x)|\mathcal{D}\right)$. 
Again, $\mathcal{D}$ is used to represent the data set of inputs and outputs that the network is finding a relationship between.
In the pre-training case, this quantity simply refers to the inputs $x_\alpha$ for the network.

:::{figure} ./figs/ANNFT_CLT_plots.png
:height: 600px
:name: fig-ANNFT_CLT_plots
Output distributions from repeated sampling at the same input point, each plot being a different width. ReLU activation is on the left; Softplus activaiton is on the right.
:::

:::{figure} ./figs/ANNFT_corner_plots.png
:height: 750px
:name: fig-ANNFT_corner_plots

:::

:::{figure} ./figs/ANNFT_variance_plots.png
:height: 750px
:name: fig-ANNFT_variance_plots

:::

:::{figure} ./figs/ANNFT_kurtosis_plots.png
:height: 750px
:name: fig-ANNFT_kurtosis_plots

:::

:::{figure} ./figs/ANNFT_ReLU_MAE_loss.png
:height: 350px
:name: fig-ANNFT_ReLU_MAE_loss

:::

:::{figure} ./figs/ANNFT_Tanh_MAE_loss.png
:height: 350px
:name: fig-ANNFT_Tanh_MAE_loss

:::

:::{figure} ./figs/ANNFT_mean_RMSD_vs_width.png
:height: 150px
:name: fig-ANNFT_mean_RMSD_vs_width

:::

:::{figure} ./figs/ANNFT_mean_Frobenius_norm_vs_width.png
:height: 150px
:name: fig-ANNFT_mean_Frobenius_norm_vs_width

:::

:::{figure} ./figs/ANNFT_mean_Frobenius_norm_vs_depth.png
:height: 150px
:name: fig-ANNFT_mean_Frobenius_norm_vs_depth

:::

:::{figure} ./figs/ANNFT_mean_rms_vs_r.png
:height: 150px
:name: fig-ANNFT_mean_rms_vs_r

:::

:::{figure} ./figs/ANNFT_residual_heatmap.png
:height: 150px
:name: fig-ANNFT_residual_heatmap

:::


