---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:BasicInfoGPs)=
# Basic info on GPs

## Overview

Here we make use of the paper by Melendez et al., [Phys. Rev. C **100**, 044001 (2019)](https://journals.aps.org/prc/abstract/10.1103/PhysRevC.100.044001), [arXiv:1904.10581](https://arxiv.org/abs/1904.10581) as an introduction to the definition and practical use of GPs.
The reader will also find in this article a novel application of GPs to model discrepancy.

A stochastic *process* is a collection of random variables (RVs) indexed by time or space. I.e., at each time or at each space point there is a random variable.
A *Gaussian* process (GP) is a stochastic process with definite relationships (correlations!) between the RVs.
In particular, any finite subset (say at $x_1$, $x_2$, $x_3$) has a multivariate normal distribution.
Thus, a GP is the natural generalization of multivariate random variables to infinite (countably or continuous) index sets.
They look like random functions, but with characteristic degrees of smoothness, correlation lengths, and ranges.

Gaussian processes (GPs) are often used for *nonparametric regression*. Compare fitting a polynomial, where the basis functions are $1, x, x^2,\ldots, x^d$ and the coefficients are the parameters. This is *parametric regression*. So with GPs we do not have the corresponding set of parameters for basis functions. But there are parameters that specify the GP itself.
Besides regression, the other most common applications of GPs are to *interpolation*. To carry out either of these we need to fit the GP parameters.

## Specifying a GP

A GP is specified by a mean function $m(x)$ [often written $\mu(x)$] and a positive semidefinite covariance function, also called a *kernel*, $\kappa(x,x')$ where $x \in \mathbb{R}^d$ and $d$ is the dimension of the parameter space. (We will generally suppress the $d$ dependence of $\kappa$.)
If we know $m(x)$ and $\kappa(x,x')$, then a GP $f(x)$ is denoted

$$
      f(x) \sim \mathcal{GP}[m(x), \kappa(x,x')]
$$
    
in the same way a normal distribution is $g(x) \sim \mathcal{N(    \mu,\sigma^2)}$.

While the definition has continuous, infinite-dimensional $x$, in practice we use a finite number of points:

$$
   \xvec = \{x_i\}_{i=1}^N \quad\mbox{and}\quad
   \fvec = \{f(x_i)\}_{i=1}^N
$$

where $N$ is the number of input "points" (which are actually vectors in general). Defining

$$
  \mvec = m(\xvec) \in \mathbb{R}^N
  \quad\mbox{and}\quad
  K = \kappa(\xvec,\xvec') \in \mathbb{R}^{N\times N} ,
$$

we can write that any subset of inputs form a multivariate Gaussian:

$$
 \Lra \fvec | \xvec \sim \mathcal{N}(\mvec,K)
$$

which can serve as the definition of a GP, as already mentioned. As usual, we say that "$\fvec$ is conditional on $\xvec$".
The mean function is the *a priori* "best guess" for $f$. If there are no features, this mean function is often taken to be zero.
Our specification of the kernel tells us what $K$ is.



A general multivariate Gaussian distribution with mean vector $\muvec$ and covariance matrix $\Sigma$ has the functional form

$$
  p(\xvec|\muvec,\Sigma) = \frac{1}{\sqrt{\det(2\pi\Sigma)}}
    e^{-\frac{1}{2}(\xvec-\muvec)^\intercal\Sigma^{-1}(\xvec - \muvec)} .
$$

For the bivariate case:

$$
  \muvec = \begin{pmatrix} \mu_x\\ \mu_y \end{pmatrix} \quad\mbox{and}\quad
  \Sigma = \begin{pmatrix}
             \sigma_x^2 & \rho \sigma_x\sigma_y \\
             \rho\sigma_x\sigma_y & \sigma_y^2
           \end{pmatrix}
        \quad\mbox{with}\ 0 \leq \rho^2 < 1 ,           
$$

where $\Sigma$ is manifestly positive definite. The contours of equal probability are ellipses.
You can think of the bivariate case with strong correlations ($|\rho|$ close to one) as belonging to two points sufficiently close together on a single curve: the smoothness of the function tells us that the contour lines in a corner plot  should be close to flat. 

**Kernels** are the covariance functions that, given two points in the $N$-dimensional space, say $\xvec_1$ and $\xvec_2$, return the covariance between $\xvec_1$ and $\xvec_2$.
Consider these vectors to be one-dimensional for simplicity, so we have $x_1$ and $x_2$. Then the commonly used RBF (radial basis function) kernel is

$$
  K_{\rm RBF}(x_1,x_2) = \sigma^2 e^{-(x_1-x_2)^2/2\ell^2}.
$$ 

Compare this to

$$
  \Sigma = \sigma^2 \begin{pmatrix} 1 & \rho \\ \rho & 1 \end{pmatrix} .
$$

The diagonals have $x_1 = x_2$ while $\rho = e^{-(x_1-x_2)^2/2\ell^2}$. 
So when $x_1$ and $x_2$ are close compared to $\ell$ then the values of the sample at $x_1$ and $x_2$ are highly correlated.
When $x_1$ and $x_2$ are far apart, $\rho \rightarrow 0$ and they become independent. **Thus, $\ell$ plays the role of a correlation length.**


## Using the GP


So how do we use this GP? Let's assume we already know $\thetavec$, the set of hyperparameters. And suppose we know the value of the function $f$ at a set of $\xvec_t$ points $\Lra$ this is our *training set*.
Therefore partition the inputs into $N_t$ training and $N_e$ evaluation (test) points; the latter are our predictions:

$$
  \xvec = [\xvec_t\, \xvec_e]^\intercal
  \quad\mbox{and}\quad
  \fvec = f(\xvec) = [\fvec_t\, \fvec_e]^\intercal .
$$

There are corresponding vectors $\mvec_t$ and $\mvec_e$ and covariance matrices.

The *definition* of a GP says the joint distribution of $\fvec_t$, $\fvec_e$ is

$$
 \begin{pmatrix} \fvec_t \\ \fvec_e \end{pmatrix} | \xvec,\thetavec
 \sim \mathcal{N}\biggl[\begin{pmatrix} m_t \\ m_e \end{pmatrix}, 
             \begin{pmatrix}
               K_{tt} & K_{te} \\
               K_{et} & K_{ee}
             \end{pmatrix}
            \biggr] , 
$$ 
    
where
    
$$\begin{align}
   K_{tt} & = \kappa(\xvec_t, \xvec_t) \\
   K_{ee} & = \kappa(\xvec_e, \xvec_e) \\
   K_{te} & = \kappa(\xvec_t, \xvec_e) = K_{et}^\intercal \\
\end{align}$$  

Then manipulation of matrices tells us that

$$
  \fvec_e | \xvec_e, \xvec_t, \fvec_t, \thetavec \sim
    \mathcal{N}(\widetilde m_t, \widetilde K_{tt})
$$ 

where

$$\begin{align}
   \widetilde m_e & = m_e + K_{et}K_{tt}^{-1}(\fvec_t - \mvec_t) \\
   \widetilde K_{ee} & \equiv K_{ee} - K_{et}K_{tt}^{-1}K_{te} .
\end{align}$$
    
So the updated mean function $\widetilde m_e$ is our best prediction for $\xvec_e$ and    $\widetilde K_{ee}$ is the variance (this determines the error band).
    
:::{admonition} This makes sense:
  
$$
 p(\fvec_e,\fvec_t) = p(\fvec_e|\fvec_t) \times p(\fvec_t)
 \quad\Lra\quad
 p(\fvec_e|\fvec_t) = p(\fvec_e,\fvec_t) / p(\fvec_t)
$$

and the ratio of Gaussians is also a Gaussian $\Lra$ we only need to figure out the matrices!

:::   

We can make draws from $\mathcal{N}(\widetilde m_e, \widetilde K_{ee})$ and plot them. With a dense enough grid, we will have lines that go through the $\xvec_t$ points and have bands in between, which grow larger when further from points.
If we have Gaussian white noise at each point, then $K_{tt} \rightarrow K_{tt} + \sigma_n^2 I_{N_t}$ (if the variance of the noise is the same; otherwise it is a diagonal matrix with entries given by the separate variances).  
In general, even if the data is perfect we need to add some noise (called adding a "nugget") for numerical reasons: $K_{tt}^{-1}$ will very probably be unstable without it. 
For predictions with noise, then $K_{ee} \rightarrow K_{ee} + \sigma_n^2 I_{N_e}$.

::::{admonition} Checkpoint question 
:class: my-checkpoint
How do we make draws from a multivariate     Gaussian (normal) distribution if we know how to make draws from     $\mathcal{N}(0,1)$?
:::{admonition} Answer
:class: dropdown, my-answer
Suppose $\xvec \sim \mathcal{N}(\muvec, \Sigmavec)$, where     $\xvec$ and $\muvec$ are dimension $d$ and $\Sigmavec$ is $d\times d$. 
Then we want to make draws with the pdf

$$
  p(\xvec|\muvec,\Sigmavec) = \frac{1}{\sqrt{\det     2\pi\Sigmavec}} e^{-\frac{1}{2}(\xvec-\muvec)^\intercal     \Sigmavec^{-1}(\xvec - \muvec)} .
$$

The procedure is:
* Generate $\uvec \sim \mathcal{N}(0,I_d)$ from $d$     independent draws of $\mathcal{N}(0,1)$. This yields
$\uvec = (u_0, u_1, \ldots, u_{d-1})^\intercal$.
* Find $L$ such that $\Sigmavec = L L^\intercal$ (using a Cholesky decomposition).
* Then $\xvec = \muvec + L\uvec$ has the desired distribution.

Check: What is the expectation value of $\xvec$, given $E[\uvec] = 0$?

$$
 E[\xvec] = E[\muvec + L\uvec] = \mu + L E[\uvec] = \muvec
$$

which is the correct mean. Note that these manipulations used     that expectation values are linear.

Now try for $\Sigmavec$:

$$\begin{align}
 \Sigmavec &\overset{?}{=}
   E[(\xvec - \muvec)(\xvec^\intercal - \muvec^\intercal)]
   = E[(L\uvec)(L\uvec)^T] \\
   &= E[L\uvec\uvec^\intercal L^\intercal]
   = L E[\uvec\uvec^\intercal]
   = L I_d L^\intercal = \Sigmavec
\end{align}$$

so it works!
:::
::::


Let's check that the formulas work for the special case of one training, one evaluation (test) point.
We will also take the mean to be zero to avoid clutter.
Then

$$
  \begin{pmatrix} f_t\\ f_e \end{pmatrix} \sim 
  \mathcal{N}\biggl[\begin{pmatrix} 0\\ 0 \end{pmatrix}, 
             \begin{pmatrix}
                \Sigma_{tt} & \Sigma_{te} \\
                \Sigma_{et} & \Sigma_{ee}
             \end{pmatrix} \biggr] ,
$$

where

$$
  \Sigmavec = \begin{pmatrix}
                \sigma_t^2 & \rho\sigma_t\sigma_e \\
                \rho\sigma_t\sigma_e & \sigma_e^2
              \end{pmatrix} .
$$

The claim is that
    
$$
   f_e | f_t \sim \mathcal{N}(\Sigma_{et}\Sigma_{tt}^{-1}f_t, \Sigma_{ee} - \Sigma_{et}\Sigma_{tt}^{-1}\Sigma_{te})
$$    

i.e., that it is a Gaussian distribution with mean $\Sigma_{et}\Sigma_{tt}^{-1}f_t$ and variance $\Sigma_{ee} - \Sigma_{et}\Sigma_{tt}^{-1}\Sigma_{te}$.
Try it explicitly:
    
$$
 p(f_e|f_t) = p(f_e,f_t)/p(f_e)
  = \frac{\frac{1}{\sqrt{\det(2\pi\Sigmavec)}}e^{-(f_t \ f_e)\,\Sigmavec^{-1}
        \begin{pmatrix} f_t \\ f_e \end{pmatrix} }}
  {\frac{1}{\sqrt{2\pi\Sigma_{tt}}}e^{-f_t^2\Sigma_{tt}^{-1}}}
$$

All of the $\Sigma_{ij}$'s are just scalars now and $\Sigma_{te} = \Sigma_{et}$.

$$
  \Sigmavec^{-1} = \frac{1}{\det\Sigmavec}
    \begin{pmatrix}
       \Sigma_{ee}& -\Sigma_{et} \\ 
       -\Sigma_{te} & \Sigma_{tt}
    \end{pmatrix}
  = \frac{1}{\Sigma_{tt}\Sigma_{ee}-\Sigma_{te}\Sigma_{et}}
     \begin{pmatrix}
       \Sigma_{ee}& -\Sigma_{et} \\ 
       -\Sigma_{te} & \Sigma_{tt}
     \end{pmatrix} ,
$$

which yields

$$
(f_t \ f_e)\,\Sigmavec^{-1} \begin{pmatrix} f_t \\ f_e \end{pmatrix}
 = \frac{(-\Sigma_{ee}f_t^2 + 2\Sigma_{et}f_t f_e - \Sigma_{tt}f_e^2)}{\det\Sigmavec} .
$$

So if we gather the $\Sigma_{ee}$ parts, we find to complete the square we need the combination $(f_e - \Sigma_{et}\Sigma_{tt}^{-1}f_t)$, which identifies the mean, and then the variance part comes out as advertised. 

