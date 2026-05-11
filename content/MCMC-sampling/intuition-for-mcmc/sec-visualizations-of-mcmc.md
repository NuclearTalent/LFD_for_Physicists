---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:VisualizingMCMC)=
# Visualizations of MCMC

## Chi Feng visualizations

There are excellent javascript visualizations of MCMC sampling available on the web.
A particularly effective set of interactive demos was created by Chi Feng, which are included in this section. 
These demos range from random walk Metropolis-Hastings (MH) to Adaptive MH to Hamiltonian Monte Carlo (HMC) to No-U-Turn Sampler (NUTS) to Metropolis-adjusted Langevin Algorithm (MALA) to Hessian-informed HMC (H2MC), to Stein Variational Gradient Descent (SVGD) to Nested Sampling with RadFriends (RadFriends-NS). 
We'll start with the random walk MH, which is the algorithm discussed in {numref}`sec:BasicStructureMCMC`.


<!--
```{raw} html
<iframe src="../../../_static/chi-feng/index_new.html"
    width="100%"
    height="400"
    style="border: none;"
    scrolling="no">
</iframe>
``` 
-->



## Exploring the Metropolis-Hastings (MH) simulation

```{raw} html
<iframe src="../../../_static/chi-feng/app_RandomWalkMH.html"
    width="100%"
    height="600"
    style="border: none;"
    scrolling="no">
</iframe>
``` 

:::{admonition} Controls for the MCMC simulations
:class: note
Note the various `Simulation options`. For now, switch the `Target distribution` to `standard`. This distribution is a two-dimensional Gaussian (just the product of two one-dimensional Gaussians).
Select `Close Controls` to avoid obscuring the simulation. Use `Open Controls` when you want to make a change to one of the settings.
If you uncheck the `Autoplay` box, you can use the `Step` button to see the algorithm carried out one step at a time.
Use the `Reset` button to clear the sampled points.
:::

When looking at the visualizations, remember the basic structure of the MH algorithm:
1. Make a random proposal for new parameter values.
1. Accept or reject the proposal based on a Metropolis criterion.

::::{admonition} Checkpoint question 
:class: my-checkpoint
Is the distribution correlated?  How do you know from the simulation?
:::{admonition} Answer
:class: dropdown, my-answer
The distribution is uncorrelated. The accumulated joint posterior has horizontally oriented ellipses (circles if the scales are equal). They would be slanted if there were correlations.
:::
::::


Here are some comments and observations on the basic MH simulation:
* An uncolored arrow indicates a proposal, which is accepted (green) or rejected (red).
    ::::{admonition} Checkpoint question 
    :class: my-checkpoint
    What happens when a proposal is rejected? You can see the result by unchecking the `Autoplay` box and using the `Step` button. Look at the histogram as you press the button to get either a green or red arrow. 
    :::
    :::{admonition} Answer
    :class: dropdown, my-answer
    With a rejection, the point should be added to the existing set of samples. This means that
    if the arrow is green (accepted proposal), then the histogram bin at the new point should go up by one. If the arrow is red (rejected proposal), then the histogram bin at the old point should go up by one (this is easy to see if you first `Reset` so there are not many points yet.)
    :::
    ::::
* Notice that the direction and the length of the proposal arrow varies and are, in fact, chosen randomly from a distribution. The direction is sampled uniformly.
* The MH MCMC seems to do ok on sampling such a simple distribution, as indicated by how well the projected posteriors get filled in.
* But it is *diffusing*, i.e., a random walk, which is not so efficient. A more complicated shape can cause problems:
    * MH can spend a lot of time exploring over and over again the same regions;
    * if not specially tuned, many proposals can be rejected (red arrows).
* Try the `donut` target distribution, which is much trickier.
    * Notice that the projected one-dimensional posteriors don't seem to be so complex, but this is a difficult topology.
    * Is this shape realistic? When there are many parameters (a high-dimensional space), this is analogous to a common target distribution. The probability *mass* concentrates in this shape. 
    :::{admonition} Note on donuts in high dimensions
    :class: note
    ```{image} ../assets/bayes_talk.028.png
    :alt: point estimate
    :class: bg-primary
    :width: 300px
    :align: right
    ```
    * Look at the average radius of points sampled from multivariate Gaussians as a function of     the dimension.
    * blue is one dimensional, green is two dimensional, ... , yellow is six dimensional.
    * Imagine yellow as a 6-dimensional *shell* $\Lra$ the *analog* is a two-dimensional donut.
    :::

**Problem:** we are constantly looking for the right step size, which is big enough to explore the space, but small enough to not get rejected too often.
* High dimensions is a big space! It is hard to stay in a region of high probability while also exploring enough of the full space (in a reasonable time).
* Try adjusting the proposal $\sigma$ (there is a Gaussian proposal with variance $\sigma^2$) $\Lra$ try this on donut: to get a reasonable rate of green arrows you need excellent step size tuning.

## Challenges in MCMC sampling

Use the pulldown menu to try the different target distributions available. The `banana` distribution is generally difficult to sample while
the `multimodal` distribution is in general very tough to sample effectively.

::::{admonition} Checkpoint question 
:class: my-checkpoint
What makes the various distributions difficult to sample effectively?
:::{admonition} Hint
:class: dropdown, my-hint
We see several general classes of problematic PDFs:
* Correlated distributions that are very narrow in certain directions.
* Donut or banana shapes.
* Multimodal distributions.

What is the difficulty with each of these?
:::
:::{admonition} Answer
:class: dropdown, my-answer
* Correlated distributions: scaled parameters are needed.
* Donut or banana shapes: very low acceptance ratios.
* Multimodal distributions: might easily get stuck in local region of high probability and completely miss other regions.
:::
::::




