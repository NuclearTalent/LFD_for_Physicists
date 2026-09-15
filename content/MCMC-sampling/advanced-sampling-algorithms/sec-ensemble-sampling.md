---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

```{math}

\newcommand\pos{\boldsymbol{x}}
\newcommand\mom{\boldsymbol{p}}
\newcommand\mass{\mathcal{M}}
```

(sec:ensemble-sampling)=
# Ensemble sampling

```{note}
This section is under construction. The motivation below is in place; the description of the stretch move and of the ensemble sampler in practice will be added.
```

## Motivation: sampling from correlated distributions

If our posterior has projections that are slanted, indicating correlations, and we are doing Metropolis-Hastings (MH) sampling, how do we decide on a step size? The problem is that we want to step differently in different directions: a step long enough to explore the long axis will lead to many rejections in the orthogonal direction. *So we do not want an isotropic step proposal!*

If we propose steps by

$$
 p(\xvec) = \frac{1}{\sqrt{(2\pi)^N |\Sigma|}}
   e^{-\xvec^{\intercal}\cdot \Sigma^{-1} \cdot \xvec} ,
$$

then we don't need to take $\Sigma \propto \sigma^2 \mathbb{1}_N$! 
* We have $N(N+1)/2$ parameters in $\Sigma$ to "tune" to reduce the correlation time.
* However, this is increasingly difficult as $N$ increases.

One improvement is to do a linear transformation of $\thetavec \longrightarrow \thetavec' = A\thetavec + B$ such that $\thetavec'$ is uncorrelated with similar $\sigma_i$'s in each direction. Thus effectively to rotate the slanted ellipse.

Or one could use an "affine invariant" sampler such as `emcee`.
An affine transformation is an invertible mapping from $\mathbb{R}^N \rightarrow \mathbb{R}^N$, namely $\yvec = A\xvec + B$, which is a combination of stretching, rotation, and translation. 
"Affine invariant" means that the sampler performs equally well on all affine transformations of a distribution. So `emcee` figures out how to make optimal steps.
It does this by using the many walkers at time $t$, which have sampled the space, to construct an appropriate affine compatible update step for $t+1$. This is one reason to make sure there are plenty of walkers.
