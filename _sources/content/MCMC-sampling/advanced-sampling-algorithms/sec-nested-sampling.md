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
\newcommand{\like}{\mathcal{L}}
\newcommand{\threshold}{\like^\star}
\newcommand{\prior}{\pi}
\newcommand{\nlive}{n_{\rm live}}
\newcommand{\evidence}{\mathcal{Z}}  % or just Z

```

(sec:nested-sampling)=
# Nested sampling

## Prelude

Nested sampling (or NS) is a technique invented by John Skilling to estimate the Bayesian *evidence* (and we get a sampling of the posterior as a by-product, see below).
Let us recall the ingredients of Bayes' theorem:

$$
  \overbrace{ \pdf{\thetavec}{\data,I} }^{\textrm{posterior}} =
  \frac{ \color{red}{ \overbrace{ \pdf{\data}{\thetavec,I} }^{\textrm{likelihood}}} 
 \color{black}{\ \times\ } 
  \color{blue}{ \overbrace{ \pdf{\thetavec}{I}}^{\textrm{prior}}}    
 } 
 { \color{darkgreen}{ \underbrace{ \pdf{\data}{I} }_{\textrm{evidence}}} }
 \equiv \frac{\like(\pars)\prior(\pars)}{\evidence} \equiv p(\pars),
$$

where we have introduced a condensed notation for clarity in the following discussion.
We can write $\evidence$, the evidence (or marginal likelihood or normalizing constant), as

$$
   \evidence = \int \like(\pars)\prior(\pars)\, d\pars ,
$$ (eq:evidence_Z)

so, as expressed here, it is an integral in the often high-dimensional space of $\pars$.
You can think of the posterior as the shape of the integrand of this integral while $\evidence$ is the magnitude of the integral.
The usual MCMC sampling techniques based on importance sampling are designed to estimate the relative shape in terms of a representative sampling of points $\pars_i$ found via a Markov chain.
But finding the absolute normalization can be a much greater challenge.

To gain intuition about NS, first recall the standard integration method as a Riemannian sum: we divide space into small volumes (e.g., multi-dimensional cubes) and approximate the integral as a sum over the integrand evaluated in each volume times the volume (see the left panel of {numref}`nested-sampling-intuition-1`).
The cost of such an integral grows exponentially with the dimension of the integral ("the curse of dimensionality"), which is why we turned to Monte Carlo integration in the first place.
To meet this challenge a different way, NS transforms the problem into finding a statistical estimate of a *one-dimensional* integral.

Good references for NS include:
* {cite}`Sivia2006` D.S. Sivia with J. Skilling, *"Data Analysis : A Bayesian Tutorial"*, Oxford University Press (2006). </br>
* {cite}`Ashton:2022grj` G. Ashton et al., *"Nested sampling for physical scientists"*,
 Nature (2022). </br>
* {cite}`buchner2023nested` J. Buchner, *"Nested sampling methods"*, Statistical Surveys (2023). </br>
* {cite}`Martino:2026kzs` L. Martino and L. Fernando, *"Nested Sampling: A Critical and Comprehensive Theoretical Guide"*, arXiv:2606.17916 (2026). </br>
* See also method discussions in the documentation of NS implementations, such as [dynesty](https://dynesty.readthedocs.io/en/stable/overview.html) and [Ultranest](https://johannesbuchner.github.io/UltraNest/method.html).


## Basic idea of NS


```{figure} ../assets/ns_evidence_consistent_combined.png
:alt: Representation of nested sampling identity
:width: 600px
:align: center
:name: nested-sampling-intuition-1

On the left is a schematic for evaluating the evidence integral by summing over uniform small volumes in the multi-dimensional parameter space (here the two-dimensional area is $\Delta \theta_1 \Delta \theta_2$).
On the right is a schematic for evaluating the same integral but now by grouping all points with the same likelihood value into small volumes $\Delta X_i$ and summing over $\mathcal{L}(X_i)\Delta X_i$, which approximates {eq}`eq:evidence_Z`. 
```

A key observation leading to NS is that
we can use other shapes beside cubes to estimate an integral, if
volume elements are such that $p(\pars)$ is almost constant for any shape.
In particular, we can group together into small volumes all points with the same value of the likelihood, as in the right panel of {numref}`nested-sampling-intuition-1`.
To get to an expression taking advantage of this observation, we first split 
the evidence integral into an integration over likelihood values $\threshold$, where for each $\threshold$ we have an integral over the enclosed part of parameter space weighted by the prior:

$$
   \evidence = \int^{+\infty} \biggl[ \int_{\pars:\like(\pars) > \threshold} \prior(\pars)\, d\pars \biggr]\, d\threshold .
$$

Here the integral in square brackets is the volume variable $X$, defined by

$$
   X(\threshold) \equiv \int_{\pars:\like(\pars) > \threshold} \prior(\pars)\, d\pars , 
$$ (eq:definition_of_X)

which is the prior-constrained volume enclosed by contour $\threshold = \like(\pars)$ (which may consist of  disconnected regions).

```{figure} ../assets/oneD_L_vs_theta.png
:alt: One-D schematic of X as function of threshold L-star
:width: 600px
:align: center
:name: nested-sampling-intuition-2

Schematic example showing how the prior-weighted scalar volume $X$ is determined at a given value of $\threshold$. The vertical dashed lines indicate the limits in $\theta$ for which $\like(\pars) > \threshold$; in one dimensions these define the lengths $\theta_a$ and $\theta_b$. The prior $\pi(\theta)$ is approximately constant (equal to $\pi_0$) in those regions, so the integral defining $X$ is approximately $X \approx \pi_0(\theta_a + \theta_b)$. This piece contributes to the evidence integral as $X \Delta\threshold$.
```

In {numref}`nested-sampling-intuition-2` we show a one-dimensional example of how this works. 
As we step through each value of $\threshold$ in the outer integral, this defines a region in $\theta$ where the likelihood satisfies $\like(\theta) > \threshold$. In the example, the current region, which is disconnected, is defined by lengths $\theta_a$ and $\theta_b$.
In one dimension, the internal integration over $\theta$ for an approximately constant $\prior(\theta) \approx \prior_0$ yields $X \approx \prior_0 (\theta_a + \theta_b)$.
In two dimensions, this region would be the area defined by a slice at height $\threshold$, in three dimensions it would be a 3D volume, and so on.
Note that there is no problem with the likelihood being multimodal.
Note also that $X$ is monotonic in $\threshold$ (this may be easiest to see if you visualize a line at $\threshold$ starting well above the peak and being moved downward; then $X$ always increases, even if $\prior(\pars)$ is not constant).
We multiply $X$ by the width $\Delta\threshold$ to get the contribution to the evidence, and sum this up for all $\threshold$ to get the total evidence.

When the threshold $\threshold$ is zero, $X=1$ (the entire prior space is included, and the prior is normalized).
As the threshold increases toward the peak value, the allowed space shrinks, and $X$ approaches zero.
Because $X$ is monotonic and decreases smoothly from 1 to 0, we can invert $X(\threshold)$ to find $\threshold(X)$.
Integrating the evidence integral by parts yields the NS evidence identity,

$$
  \evidence = \int^{+\infty} X(\threshold)\, d\threshold = \int_0^1 \threshold(X) \,dX ,
$$
    
assuming $\threshold(X)$, the inverse of $X(\threshold)$, exists and $\evidence$ is finite.
If we can evaluate the iso-likelihood contour $\like_i\equiv \like(X_i)$ (dropping the $\star$) associated with samples from the prior volumes

$$
 1 > X_1 > X_2 > \cdots > X_N > 0 ,
$$

then we can compute the evidence $\evidence = \int_0^1 \like(X)\,dX \approx \sum_i \like_i \Delta X_i$ by basic numerical quadrature (e.g., the trapezoid rule). Computing the evidence using these "nested shells" is what gives Nested Sampling its name.
The NS procedure is illustrated schematically in {numref}`schematic-NS-2D`.

```{figure} ../assets/ns_schematic_profile_combined_adjusted_v3.png
:alt: Schematic of NS for a two-dimensional problem
:width: 600px
:align: center
:name: schematic-NS-2D

Schematic representation of NS for a two dimensional problem. The samples $X_i$ from the prior volumes at $\like_i$ satisfy $1 > X_1 > X_2 > X_3 > X_4 > 0$. The corresponding $\Delta X_i$s are multiplied by the $\like_i$s and summed to
approximate the evidence: $\evidence = \int_0^1 \like(X)\,dX \approx \sum_i \like_i \Delta X_i$.  

```

This sounds great, but we realize that calculating the $X_i$s directly involves a series of high-dimensional integrals that are exactly what we want to avoid!
So we will estimate the $X_i$s statistically.

## NS in practice

In an implementation of NS one evolves a collection of so-called "live points" through the parameter space.
We start with $\nlive$ points drawn from the prior. 
The prior should cover the full range of parameters being sampled.
The likelihood is calculated for all of the live points, and the least likely (i.e., lowest value of $\like$) is removed and a new draw is made to replace the "dead" point. This lowest value is $\threshold$.
(We keep track of the dead points, which give an estimate of the posterior, see below).

Suppose we could (magically) know the prior volume $X_i$ from {eq}`eq:definition_of_X` associated with each live point $\theta_i$. 
If the current volume is $X_{i-1}$, then the variables $u_j = X_j / X_{i-1}$ would all be uniformly distributed in $[0,1]$.
::::{admonition} Checkpoint question
:class: my-checkpoint
Intuitively, why is $u_j$ uniformly distributed in $[0,1]$? 
:::{admonition} Answer
:class: dropdown, my-answer
Imagine dividing the prior into nested likelihood regions that have prior volumes $X = 0.1, 0.2, 0.3, \ldots, 1$. Then the region with $X(\theta) \equiv X(\like(\theta)) < 0.2$ has, by construction, 20\% of the prior probability. So for a random draw of $\theta$, the cumulative probability of the corresponding $X < 0.2$ is $0.2$. And, generally, the cumulative probability for $X < x$ is $x$. This is the cumulative probability distribution for a uniform distribution of $X$.

If we have already eliminated points so that the current volume is $X_{i-1}$, then the uniform distribution is between $0$ and $X_{i-1}$, so to make it uniform in $[0,1]$ we define $u_j$ with $X_{i-1}$ divided out.

This result is independent of the details of the likelihood or the prior, because $X$ has been defined in terms of enclosed prior probability, so it automatically turns prior draws into uniform random variables.
:::
::::

Removing the point with the lowest likelihood means removing the one with the highest $X$,
so


$$
    t_i \equiv \frac{X_i}{X_{i-1}} = \max(u_1, \ldots, u_{\nlive}),
$$

which means (because the $u_i$s are independent):

$$
   F(t_i < t) = t^{\nlive} \quad\Longrightarrow\quad
   p(t) = \nlive t^{\nlive - 1} \quad\Longrightarrow\quad
   t_i \sim \text{Beta}(\nlive,1) ,
$$

where $F$ is the cumulative distribution and $p(t)$ therefore follows as its derivative.

::::{admonition} Checkpoint question 
:class: my-checkpoint
Why is this a Beta distribution?
:::{admonition} Answer
:class: dropdown, my-answer
The general Beta pdf is

$$
  p(t) = \frac{1}{B(a,b)}t^{a-1}(1-t)^{b-1} , \quad\text{where}\ 
    B(a,b) = \frac{\Gamma(a)\Gamma(b)}{\Gamma(a+b)} ,
$$

and $\Gamma(z)$ is the gamma function.
Here $a=\nlive$ and $b=1$ to match $p(t) = \nlive t^{\nlive - 1}$ and
$B(\nlive,1) = 1/\nlive$. 
:::
::::

::::{admonition} Checkpoint question 
:class: my-checkpoint
Why is $t$ so close to 1? Does this make sense intuitively?
:::{admonition} Hint
:class: dropdown, my-hint
Imagine you are determining $t$ from 50 points uniformly distributed between 0 and 1.
:::
:::{admonition} Answer
:class: dropdown, my-answer
Intuitively it makes sense: with 50 points between 0 and 1 and you are taking the largest one, you expect it to be close to 1.

Mathematically, with $\nlive = 50$, the density is $p(t) = 50 t^{50}$ and any number not close to 1 raised to an exponent of 50 will be close to zero, so the strength is concentrated near 1.
:::
::::



This is the statistical shrinkage rule.
So while there really is a sequence of $X_i$s, they are irregular and random because the live points themselves were randomly drawn.
The NS algorithm doesn't know these while it does know $\like_i$ (as noted above, calculating the $X_i$ would be a difficult multidimensional integral of the type we are trying to avoid).
So, in fact, representative values are used in practice:

$$
  X_i \approx e^{-i/\nlive} \quad \text{or} \quad X_i = t_i X_{i-1}, \text{ with }
  t_i \sim \text{Beta}(\nlive,1).
$$

The process is repeated over many iterations
and the evidence accumulated from

$$
\evidence \approx \sum_{i} \like_i \cdot \Delta X_i ,
$$ 

where $\Delta X_i = X_{i-1} - X_i$.
The iterations are stopped when the remaining evidence is negligible (various stopping criterion are used in different implementations of NS).

As a by-product,
posteriors for $\pars$ are acquired "for free" from the same 
 dead points by assigning each sample its associated importance weight

$$
  \prob(\pars_i) = p(X_i) \approx \frac{\like_i \Delta X_i}{\evidence} .
$$

To determine replacement live points, there are different strategies used by different NS implementations.
For example, to do region sampling, a geometric shape (e.g., an ellipse) is constructed around the live points and a new point is drawn from within the region, rejecting it if it falls outside the region.
Below we examine in detail one such implementation.
 



## Simulation of nested sampling

To establish some intuition about NS in practice, we return to the excellent set of [interactive demos by Chi Feng](https://chi-feng.github.io/mcmc-demo/).
You might want to refresh your memory first on MH and HMC sampling before jumping into the nested sampling demo.

:::{admonition} Controls for the MCMC simulations
:class: note
* The initial simulation uses MH sampling. To switch to an implementation of nested sampling, select `Open Controls` and pull down the `Algorithm` menu and select `RadFriends-NS`.
Note the `Algorithm Options`, where `numLivePoints` $= \nlive$ is set.
* After making changes, use `Close Controls` to avoid obscuring the simulation.
* The initial `Target distribution` should be `banana`, which is a good choice to demonstrate the nested sampling algorithm.
* But for orientation, you might want to first switch the `Target distribution` to `standard`. This distribution is a two-dimensional Gaussian (just the product of two one-dimensional Gaussians).
* If you uncheck the `Autoplay` box, you can use the `Step` button to see the algorithm carried out one step at a time.
* Use the `Reset` button to clear the live points and start again with the full prior.
:::


```{raw} html
<iframe src="../../../_static/chi-feng/app_RandomWalkMH.html"
    width="100%"
    height="600"
    style="border: none;"
    scrolling="no">
</iframe>
``` 

In standard MCMC (like Random Walk or HMC), the histograms accumulate sequentially. Every time a single particle takes a step, the algorithm records its coordinate and adds exactly one tally mark to the corresponding bin.
Nested Sampling, however, does not follow a single particle. It tracks an entire population of active (live) points simultaneously, weighting their contributions based on the prior volume they represent.
* Weighting by Posterior Mass: Because Nested Sampling's goal is to compute the total integral ($\evidence$), every point that gets killed/replaced carries a specific "weight" ($w_i = L_i \cdot \Delta X_i$), which represents how much total probability mass that point occupies.
* The Histogram Addition: In the visualization, the histograms are built by accumulating these weights. When a point is eliminated, its position along the X and Y axes is recorded into the histograms, multiplied by the fractional volume it leaves behind.


Notes for the `RadFriends-NS` simultation:
1. Initially, points are drawn from the entire parameter space (green) weighted by the prior. At any time, the number of points will match the setting of `numLivePoints`.
You might want to first set it to a low number (10 is the least) and switch off autoplay so that you count each of the dots and watch what happens step by step. 

2. In each step, the live point with the lowest likelihood (worst fit) is removed, and a better one sought. At each removal, the volume sampled by the live points shrinks.
If you go step-by-step (`Autoplay` unchecked) with a small number of points, you can identify by eye the point with the lowest likelihood (it is easiest to start with the `standard` target distribution). When you take a step it will disappear.
The green arrow visualizes the birth of a new, valid replacement point; it points from a randomly chosen live point (different from the one about to die) to the sampled next point, which will be added to the set of live points.
There are red points to indicate potential next points that do not have a higher likelihood, and therefore are rejected as candidate live points.

3. To still sample from the prior, RadFriends creates ellipsoids around all live points (not just the one being removed) and samples from them. The ellipsoid size is determined by bootstrapping: Some points are randomly left out, and the ellipsoids have to be large enough so that they could have been sampled. This is repeated several times. In [Ultranest](https://johannesbuchner.github.io/UltraNest/method.html), the ellipsoid shape is learnt as well.
Other NS algorithms have other ways to do the sampling.

4. Nested sampling proceeds to the peak, keeping track of the likelihood. The volume becomes smaller and smaller. At some point, the remainder does not contribute any probability mass, and the exploration is finished.

5. The removed points are weighted by their likelihood and the volume they represent. These are the posterior samples (histograms).


:::{admonition} Why do so many points appear initially in the histograms?
:class: note
The instant appearance of many bins on Step 1 of the Rad-Friends-NS simulation is the result of a specific programmatic sequence in the rendering engine.
Before the simulation officially begins iterating, the code checks the likelihood of all 40 randomly scattered points (assuming you are using the default $\nlive=40$. The visualization code treats this entire initial batch of 40 points as the starting baseline.
Because a histogram cannot show "live" floating points (it can only record permanent data data-points), the code takes all $\nlive$ initial locations and puts them into the histogram array simultaneously as a single initialization event. You are seeing the birth of the entire population rendering all at once, not a single particle moving.
Thus, the code pushes the coordinates of all $\nlive$ points into the histogram bin counters in a single clock cycle. If you have 40 points, up to 40 different bins across the X and Y axes instantly receive a value.

Once that initial batch of $\nlive$ points is registered into the visualization framework, the simulation settles into its actual loop:
* Step 2: One single worst point is removed. One new green arrow finds one replacement point. Therefore, only one new coordinate is added to the histogram.
* Step 3: Only one point is replaced. Only one contribution is added to a single bin.
* The massive burst of bins is a one-time initialization dump required to set up the population ecosystem on screen. Every step after that will only modify a single point at a time, making the progress look slow and incremental from that moment forward.
:::

:::{admonition} The Life Cycle of a Green Arrow in RadFriends-NS
:class: note
* **The Replacement Goal:** The algorithm identifies the "worst" active point in the entire population (the point with the lowest likelihood density) and marks it to be destroyed.
* **The Originating End (The Tail):** To find a replacement, the algorithm randomly selects one of the other, surviving active points to act as a parent. The tail of the green arrow sits exactly on this surviving parent point.
* **The "Friend" Ball:** The algorithm draws a radius (the "Rad" in RadFriends) around that parent point to define a local neighborhood.
* **The Pointy End (The Tip):** The algorithm randomly samples a new coordinate inside that neighborhood. If this new coordinate has a higher likelihood than the "worst" point, it is accepted. The tip of the green arrow lands on this new location.


**Summary of the Visual Mechanics**
* **The Tail:** The surviving point chosen to spawn a new candidate.
* **The Tip:** The successful new point that instantly takes the place of the dead, lowest-likelihood point.
* **The Deleted Point:** The actual point being replaced vanishes from the screen elsewhere in the cluster without an arrow drawn directly to it.

Other notes:
* The RadFriends algorithm determines the radius of the proposal region dynamically. This resulting radius builds a local bounding region around each surviving point. By overlapping these regions across all active points, a collective "friend" zone envelope is formed that wraps around the entire high-density target landscape.

* A red arrow represents a failed proposal where a newly sampled point is rejected. This occurs because the algorithm failed to meet the strict criterion of Nested Sampling: every new point must have a higher likelihood density than the worst point in the current population. Just like a green arrow, a red arrow starts at the randomly selected parent point. The population remains unchanged, no points are replaced, and the algorithm tries again from a new random parent.
:::

### Multimodal sampling

Now switch the `Target distribution` to `multimodal`. Compare the performance of nested sampling to MH or HMC.
We will compare several sampling techniques in finding multimodal posteriors and calculating evidence integrals in demo notebooks in the next chapter.


## Summary of Nested Sampling 

:::{admonition} Comparison of Nested Sampling, Metropolis-Hastings, and HMC simulations
:class: note

RadFriends-NS (Nested Sampling) differs fundamentally from algorithms like Metropolis-Hastings (MH) and Hamiltonian Monte Carlo (HMC) because it is designed to calculate a total volume (the Bayesian evidence) rather than just exploring a continuous path (or multiple paths in parallel).

| Algorithm | Exploration Strategy | Behavior of Arrows | Best Used For |
|   ---     |       ---            |      ---           |    ---        |
| **RadFriends-NS** (RadFriends Nested Sampling)| Shrinks a contour to isolate high-density zones while keeping a population of active points. | **Radial clusters.** Green arrows radiate outward inside an adaptive bounding region (a "friend" ball) to replace the lowest-likelihood point. | Multi-modal distributions and calculating Bayesian evidence. |
| **Random Walk MH** (Metropolis-Hastings) | Takes blind, random steps in any direction from a single active point. | **Jagged, local paths.** Shows many red arrows (rejections) because random steps frequently land in low-probability areas. | Simple, low-dimensional distributions. |
| **HMC** (Hamiltonian Monte Carlo) | Uses physics simulation (gradient/slope) to glide smoothly across the distribution. | **Long, sweeping curves.** Green arrows form long, elegant trajectories with very few red arrows, easily moving between distant peaks. | Complex, high-dimensional, and continuous distributions. |

<!--
Appearance of each:
1. **RadFriends-NS: The Adaptive Bounding Box**  
  Instead of a single particle walking around, Nested Sampling maintains a population of points. It identifies the worst point (lowest value of the likelihood), throws it away, and tries to generate a new, better point to replace it.
    * **The "RadFriends" Trick:** To avoid guessing blindly, the algorithm draws an adaptive envelope around the surviving points (the "friend" zone).
    * **The Visual Result:** You see green arrows popping up dynamically within this specialized cluster. As time goes on, the allowed boundary shrinks, tightening around the peaks like a lasso.

2. **Random Walk Metropolis-Hastings: The Blind Explorer**  
  This algorithm is a single particle that tosses a coin to choose a random direction and distance. If the new spot has higher density, it moves there (green arrow). If it has lower density, it usually (but not always) stays put (red arrow).
    * **The Visual Result:** The trail looks like a chaotic, jagged "drunkard's walk." It spends a massive amount of time generating red arrows because blind guesses often hit poor zones.

3. **Hamiltonian Monte Carlo: The Orbiting Satellite**  
  HMC treats the particle like a hockey puck sliding on a frictionless, curved surface where the high-density areas are deep valleys. It gives the particle a random push (momentum) and lets gravity simulate a smooth path.
    * **The Visual Result:** Beautiful, sweeping green arcs that effortlessly trace the contours of the shape. Because it uses math gradients to guide its path, almost every single proposal is accepted, resulting in almost zero red arrows.
-->
:::



<!--
### Code demo

```{code-cell} python3
:label: Nested-sampling-1
:tags: [hide-input]

import numpy as np
import matplotlib.pyplot as plt

# 1. Setup target distribution (2D Gaussian landscape)
def log_likelihood(x, y):
    # Peak is at (0,0)
    return -0.5 * (x**2 + y**2)

# 2. Simulation parameters
np.random.seed(42)
num_points = 20
num_iterations = 150
expansion_factor = 1.5  # Scale factor (F) for the friend ball

# Initialize random population uniformly distributed between -3 and 3
population = np.random.uniform(-3, 3, (num_points, 2))
likelihoods = np.array([log_likelihood(p[0], p[1]) for p in population])

# Track historical metrics for plotting
history_worst_lh = []
history_rejection_rate = []

# Data structures to store arrows for visualization
green_arrows = [] # (start_x, start_y, dx, dy)
red_arrows = []

print("Running RadFriends Nested Sampling Simulation...")

for idx in range(num_iterations):
    # Find the current worst point (lowest likelihood)
    worst_idx = np.argmin(likelihoods)
    worst_lh = likelihoods[worst_idx]
    history_worst_lh.append(worst_lh)
    
    # Calculate adaptive radius (distance to nearest surviving neighbor)
    radii = []
    for i, p1 in enumerate(population):
        if i == worst_idx:
            continue
        distances = [np.linalg.norm(p1 - p2) for j, p2 in enumerate(population) if j != i and j != worst_idx]
        radii.append(min(distances) * expansion_factor)
    avg_radius = np.mean(radii)
    
    # Try to propose a valid replacement point
    attempts = 0
    accepted = False
    
    while not accepted:
        attempts += 1
        # Pick a random surviving parent point
        parent_idx = np.random.choice([i for i in range(num_points) if i != worst_idx])
        parent = population[parent_idx]
        
        # Sample uniformly within a circular "friend ball" around the parent
        r = avg_radius * np.sqrt(np.random.rand())
        theta = np.random.rand() * 2 * np.pi
        dx, dy = r * np.cos(theta), r * np.sin(theta)
        proposal = parent + np.array([dx, dy])
        
        # Check acceptance criteria
        prop_lh = log_likelihood(proposal[0], proposal[1])
        if prop_lh > worst_lh:
            # Success: Accept proposal and replace the worst point
            population[worst_idx] = proposal
            likelihoods[worst_idx] = prop_lh
            accepted = True
            # Store sample arrow from early, middle, or late phase to visualize
            if len(green_arrows) < 15 and idx % 10 == 0:
                green_arrows.append((parent[0], parent[1], dx, dy))
        else:
            # Failure: Record rejection arrow location
            if len(red_arrows) < 30 and idx % 5 == 0:
                red_arrows.append((parent[0], parent[1], dx, dy))
                
    history_rejection_rate.append((attempts - 1) / attempts)

# 3. Plotting results
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Left Plot: The Population and Arrow Vectors
# Draw contours of the target landscape
X, Y = np.meshgrid(np.linspace(-3, 3, 100), np.linspace(-3, 3, 100))
Z = log_likelihood(X, Y)
ax1.contourf(X, Y, Z, cmap='Blues', alpha=0.6)

# Plot final converged point cloud
ax1.scatter(population[:, 0], population[:, 1], c='black', label='Final Active Points', zorder=5)

# Overlay Green Arrows (Accepted Steps)
for arrow in green_arrows:
    ax1.arrow(arrow[0], arrow[1], arrow[2], arrow[3], head_width=0.08, head_length=0.08, fc='g', ec='g', alpha=0.8)
# Overlay Red Arrows (Rejected Steps)
for arrow in red_arrows:
    ax1.arrow(arrow[0], arrow[1], arrow[2], arrow[3], head_width=0.06, head_length=0.06, fc='r', ec='r', alpha=0.4)

ax1.set_title("RadFriends Particle Field & Proposals")
ax1.set_xlabel("X coordinate")
ax1.set_ylabel("Y coordinate")
# Proxy artists for legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='g', edgecolor='g', label='Accepted Proposal (Green)'),
                   Patch(facecolor='r', edgecolor='r', alpha=0.5, label='Rejected Proposal (Red)'),
                   plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=8, label='Active Points')]
ax1.legend(handles=legend_elements, loc='upper right')

# Right Plot: The Shrinking Boundary Effects
ax2.plot(history_worst_lh, color='darkblue', linewidth=2, label='Worst Likelihood Threshold')
ax2.set_xlabel("Iteration")
ax2.set_ylabel("Log Likelihood Value (Higher = Closer to Peak)")
ax2.set_title("Convergence & Threshold Tightening")
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend(loc='lower right')

plt.tight_layout()
plt.show()

print("\nSimulation complete. Plot window displayed.")


```


* The Vector Clusters: On the left map, you will see green arrows moving directly toward the higher-density core.
* The Red Chaos: Scattered red arrows map out where the "friend" ball overstepped the threshold boundaries, illustrating how the algorithm wastes steps guessing outside the valid contour line.
* The Threshold Slope: The right graph shows how the minimum allowable likelihood value climbs higher over time, squeezing the target volume exactly like the animation behaves in the interactive gallery.


```{code-cell} python3
:label: Nested-sampling-2
:tags: [hide-input]

import numpy as np
import matplotlib.pyplot as plt

# 1. Setup multi-modal target distribution (Two distinct Gaussian peaks)
def log_likelihood_multimodal(x, y):
    # Peak 1 centered at (-1.5, -1.5)
    peak1 = -0.5 * ((x + 1.5)**2 + (y + 1.5)**2)
    # Peak 2 centered at (1.5, 1.5)
    peak2 = -0.5 * ((x - 1.5)**2 + (y - 1.5)**2)
    
    # Use log-sum-exp trick to safely add probabilities in log space
    # This represents a mixture of two separate density islands
    max_p = np.maximum(peak1, peak2)
    return max_p + np.log(np.exp(peak1 - max_p) + np.exp(peak2 - max_p))

# 2. Simulation parameters
np.random.seed(101) # Seed chosen to highlight the split behavior well
num_points = 30     # Increased point pool to adequately cover both peaks
num_iterations = 200
expansion_factor = 1.3 

# Initialize random population uniformly across the entire grid
population = np.random.uniform(-4, 4, (num_points, 2))
likelihoods = np.array([log_likelihood_multimodal(p, p) for p in population])

history_worst_lh = []
green_arrows = [] 
red_arrows = []

print("Running Multi-Modal RadFriends Nested Sampling Simulation...")

for idx in range(num_iterations):
    # Find the current worst point to destroy
    worst_idx = np.argmin(likelihoods)
    worst_lh = likelihoods[worst_idx]
    history_worst_lh.append(worst_lh)
    
    # Calculate adaptive radius based on nearest neighbors
    radii = []
    for i, p1 in enumerate(population):
        if i == worst_idx:
            continue
        distances = [np.linalg.norm(p1 - p2) for j, p2 in enumerate(population) if j != i and j != worst_idx]
        radii.append(min(distances) * expansion_factor)
    avg_radius = np.mean(radii)
    
    accepted = False
    while not accepted:
        # Pick a random surviving parent point
        parent_idx = np.random.choice([i for i in range(num_points) if i != worst_idx])
        parent = population[parent_idx]
        
        # Sample uniformly within the local "friend ball"
        r = avg_radius * np.sqrt(np.random.rand())
        theta = np.random.rand() * 2 * np.pi
        dx, dy = r * np.cos(theta), r * np.sin(theta)
        proposal = parent + np.array([dx, dy])
        
        # Evaluate proposal
        prop_lh = log_likelihood_multimodal(proposal, proposal)
        if prop_lh > worst_lh:
            population[worst_idx] = proposal
            likelihoods[worst_idx] = prop_lh
            accepted = True
            # Sample arrows periodically for clean visualization
            if idx % 8 == 0:
                green_arrows.append((parent, parent, dx, dy))
        else:
            if len(red_arrows) < 40 and idx % 4 == 0:
                red_arrows.append((parent, parent, dx, dy))

# 3. Plotting multi-modal results
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Left Plot: Multi-modal Contour and Clustering
X, Y = np.meshgrid(np.linspace(-4, 4, 100), np.linspace(-4, 4, 100))
Z = log_likelihood_multimodal(X, Y)
ax1.contourf(X, Y, Z, cmap='Blues', alpha=0.6)

# Plot final active points (you'll see them split between both islands)
ax1.scatter(population[:, 0], population[:, 1], c='black', label='Final Active Points', zorder=5)

# Overlay Arrows
for arrow in green_arrows:
    ax1.arrow(arrow, arrow, arrow, arrow, head_width=0.08, head_length=0.08, fc='g', ec='g', alpha=0.7)
for arrow in red_arrows:
    ax1.arrow(arrow, arrow, arrow, arrow, head_width=0.06, head_length=0.06, fc='r', ec='r', alpha=0.3)

ax1.set_title("RadFriends Splitting on Multi-Modal Distribution")
ax1.set_xlabel("X coordinate")
ax1.set_ylabel("Y coordinate")

from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='g', edgecolor='g', label='Accepted Steps (Green)'),
                   Patch(facecolor='r', edgecolor='r', alpha=0.5, label='Rejected Steps (Red)'),
                   plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=8, label='Active Points')]
ax1.legend(handles=legend_elements, loc='upper left')

# Right Plot: Sharp threshold jumps as valleys are cleared
ax2.plot(history_worst_lh, color='darkblue', linewidth=2, label='Worst Likelihood Threshold')
ax2.set_xlabel("Iteration")
ax2.set_ylabel("Log Likelihood Value")
ax2.set_title("Threshold Progression Over Valleys")
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend(loc='lower right')

plt.tight_layout()
plt.show()

print("\nSimulation complete. Multi-modal plot window displayed.")


```

* The Valley of Rejection: In the space between the two islands (near 0,0), you will see highly concentrated red arrows. As the threshold tightens, proposals that drop into this empty valley are fiercely rejected.
* Independent Neighborhoods: Because avg_radius continuously shrinks as clusters tighten, the points on the top-right peak stop generating proposals that land on the bottom-left peak. The populations become visually and functionally isolated.
* The Threshold Step-Function: On the right-hand graph, you may notice a sudden sharp inflection or "jump" in the log-likelihood curve. This represents the precise moment the algorithm completely purged the last point stuck in the dead-zone valley, leaving only points securely resting on the two high-density summits.
-->



### Visualizing the Difference: NS vs. MCMC  

  | Aspect | Traditional MCMC (e.g., HMC, Metropolis) | Nested Sampling (e.g., RadFriends-NS) |
  |---|---|---|
  | Mathematical Goal | Samples proportionally to the target density to map the shape of the   posterior. | Directly calculates the absolute volume under the likelihood curve. |
  | The Integration Issue | Cannot easily compute $\evidence$ because it does not track the total   volume of unvisited spaces. | Explicitly solves $\evidence$ by systematically compressing the known   prior volume. |
  | Handling Phase Transitions | Often gets trapped on a single peak, missing entire "islands"   of probability. | Compresses all modes uniformly, naturally isolating multiple peaks as the   volume shrinks. |
  
  Every time you see a green arrow replace a point in the RadFriends simulation, the algorithm   is taking one more step down the $X$-axis (from 1 toward 0). It locks in the likelihood of   the rejected point ($\like_i$), shrinks the remaining volume estimate ($X_i$), and adds another   rectangle to the grand total of the Bayesian Evidence ($\evidence$).


:::{admonition} Advantages of nested sampling
:class: note
* Returns results for both model comparison and parameter inference at the same time.
* Successful in multi-model problems.
* Naturally self-tuning.
:::


## Physics connection: statistical mechanics

[This discussion is based on {cite}`Ashton:2022grj`]

We can make a connection between the evidence and the canonical ensemble partition function in statistical mechanics by defining an "energy"

$$
          E(\pars) = -\log \like(\pars) \quad\Longrightarrow\quad \like(\pars)= e^{-E(\pars)},
$$

where we think of $\pars$ as defining a microstate.
Then the partition function at inverse temperature $\beta$ is

$$
   Z(\beta) = \int e^{-\beta E(\pars)} \prior(\pars)\, d\pars
   = \int \like(\pars)^\beta\prior(\pars) \, d\pars,
$$

where $\prior(\pars)\,d\pars$ is the underlying phase-space measure.
For $\beta=1$ this is the evidence and with $\beta=0$ the integrand is just the prior.
In parallel tempering, we find a differential equation in $\beta$ for $Z(\beta)$.

Nested sampling of parameters $\pars$ presents a different perspective, which is also well aligned with statistical mechanics, but the analogies are to the *microcanonical ensemble*.
The microcanonical ensemble has all states with $E(\pars) = \epsilon$ where $\epsilon$ is a constant energy level.
The volume of state space corresponding to a given energy $\epsilon$ is given by the density of states,

$$
g(\epsilon) = \int \delta(E(\pars) - \epsilon)\prior(\pars) \, d\pars .
$$

<!--
Taking the prior to be uniform corresponds to the  *ergodic hypothesis*, namely that each microstate that is allowed by applicable conservation laws is equally likely to be observed. 
-->
Taking the Laplace transform of the density of states $g$ is the canonical partition function $\evidence(\beta) = \int e^{-\beta E} g(E) d E$, which corresponds to the generalized evidence $\evidence(\beta)$. 
As noted, the canonical ensemble describes thermodynamic states based on the inverse temperature $\beta$ rather than the energy level $\epsilon.$ 
In the canonical ensemble, the Boltzmann distribution $p(\pars\mid\beta) = \exp\{-\beta E(\pars)\} / \evidence(\beta)$ characterizes the distribution of states. 

NS in essence tracks the cumulative density of states via:

$$
  X(\like) = \int\limits_{E \le -\log \like} g(E) \, d E,
$$

Thus, NS is a way of reconstructing the density-of-states information.
Note that in NS, we don't have a microcanonical *shell*, but rather the entire interior below a given $E$.
The practical approximation to the evidence follows as

$$
\evidence(\beta) \approx \sum_i {e^{-\beta E_i} \left(X_{i-1}  -  X_{i+1} \right)/2}.
$$

:::{admonition} Correspondence between Bayesian inference and stat mech
:class: note
|  Bayesian inference (NS) | Statistical mechanics |
|    :-----------:      |  :-----------:         |
| $\pars$             | configuration / microstate |
| $-\log\like(\pars)$   |  $E(\pars)$  |
| $\prior(\pars)\,d\pars$ |  reference phase-space measure |
|  $X(\like)$   | cumulative density of states |
| $\like = e^{-E}$     |  Boltzmann factor at $\beta = 1$ |
|   $\evidence$       | partition function  |
|  $-\log\evidence$    |   free energy at $\beta = 1$    |
:::

During NS, states are generated from the prior constrained by an upper energy limit $\epsilon = -\log \threshold$, which can be achieved with various techniques (see references).
The information entropy of the constrained prior is the *volume entropy* $\log X(\epsilon)$.
As NS progresses from one energy limit $\epsilon$ to the next $\epsilon' < \epsilon$, the volume entropy changes by $\Delta H = \log[X(\epsilon) / X(\epsilon')]$ at a rate that is constant on average: $\langle \Delta H \rangle = 1 / \nlive$.



The evidence is an energy-entropy competition, which is what determines equilibrium in statistical mechanics. In Bayesian terms, high likelihood favors a small region around an excellent fit while prior volume favors broader regions fit reasonably well.
We recognize this as the tradeoff between better fit and the Occam penalty.

:::{admonition} NS vs. thermodynamic integration
:class: note
The NS procedure with energy as a control parameter can be contrasted with thermodynamic integration (see {ref}`sec:parallel-tempering`), which works in the canonical ensemble and uses the inverse temperature $\beta$ as a control parameter to weight each microstate.
In contrast to the ensemble property $\beta$, a key advantage of $E(\pars)$ is that it can be evaluated for a single microstate $\pars$.
NS constructs a sequence of energy levels at runtime.
The sequence is optimal in that it achieves constant thermodynamic speed because changes in the volume entropy are constant on average.
Therefore, NS avoids having to design a good temperature schedule, as must be done in thermodynamic integration.
:::
 
