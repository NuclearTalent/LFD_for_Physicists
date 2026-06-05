---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:BayesianCredibleIntervals)=
# Bayesian credible intervals

(sec:DefiningCredibleIntervals)=
## Defining credible intervals

For a one-dimensional posterior that is *symmetric*, it is clear how to define the $d\%$ confidence interval. 
The algorithm is: start from the center, step outward on both sides, stop when $d\%$ is enclosed.
For a two-dimensional posterior, we need a way to integrate from the top. (One approach is to lower a plane, as described below for HPD.)

What if the distribution is asymmetic or multimodal? Here are two possible choices.
* **Equal-tailed interval (ETI)**, also known as central interval: define the boundaries of the interval so that the area above and below the interval are equal.
* **Highest posterior density (HPD) region**, also known as highest density region (HDR): the posterior density for
every point is higher than the posterior density for any point
outside the
interval. E.g., lower a horizontal line over the distribution until the desired interval percentage is covered by regions where the distribution is above the line.

Here is a widget showing how ETI and HPD are applied for a variety of distributions.
Some notes on the widget:
* Collapse the left table of contents by toggling the three line icon at the upper left of this middle frame. 
* The starting distribution is bimodal, with a 90% credible interval. In this case, 
the ETI has 5% of the area above and below the blue vertical dashed lines. Note that the HPD leads to two disjoint regions.
* Toggle the checkboxes to see the ETI and HPD regions individually.
* The slider lets you change the size of the credible interval.
* The pulldown menu gives a variety of choices for distributions.


```{raw} html
<iframe src="../../../_static/eti_hpd_credible_regions_widget.html"
    width="100%"
    height="920"
    style="border: none;"
    scrolling="no">
</iframe>
```


<!--
```{code-cell} python3
:label: HPD-visualization-1
:tags: [hide-input]

import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# 1. Define a bimodal Gaussian mixture distribution
np.random.seed(42)
mu1, sigma1, w1 = 2.0, 0.7, 0.45
mu2, sigma2, w2 = 6.5, 1.1, 0.55

x = np.linspace(-1, 10, 2000)
dx = x[1] - x[0]
density = w1 * stats.norm.pdf(x, mu1, sigma1) + w2 * stats.norm.pdf(x, mu2, sigma2)

# 2. Calculate the 90% Equal-Tailed Interval (ETI)
cdf = np.cumsum(density) * dx
cdf /= cdf[-1]  # Normalize
eti_low = x[np.searchsorted(cdf, 0.05)]
eti_high = x[np.searchsorted(cdf, 0.95)]

# 3. Calculate the 90% Highest Posterior Density (HPD) Interval
sorted_indices = np.argsort(density)[::-1]
sorted_density = density[sorted_indices]
cumulative_p = np.cumsum(sorted_density) * dx
threshold_idx = np.searchsorted(cumulative_p, 0.90)
hpd_threshold = sorted_density[threshold_idx]

# 4. Plotting
plt.figure(figsize=(10, 6))
plt.plot(x, density, 'k-', lw=2, label='Probability Density Function (PDF)')

# Draw Equal-Tailed Interval (Single contiguous block)
plt.fill_between(x, 0, density, where=(x >= eti_low) & (x <= eti_high), 
                 color='C0', alpha=0.3, label='90% Equal-Tailed Interval (ETI)')
plt.axvline(eti_low, color='C0', linestyle='--', lw=1.5)
plt.axvline(eti_high, color='C0', linestyle='--', lw=1.5)

# Draw HPD Region (Splits into disjoint blocks around peaks)
plt.fill_between(x, 0, density, where=(density >= hpd_threshold), 
                 color='C1', alpha=0.4, label='90% Highest Posterior Density (HPD)')
plt.axhline(hpd_threshold, color='C1', linestyle=':', lw=2, label='HPD Density Threshold')

plt.title('90% ETI vs HPD Interval for a Multimodal Distribution', fontsize=14)
plt.xlabel('X', fontsize=12)
plt.ylabel('Density', fontsize=12)
plt.tick_params(axis='both', labelsize=12)   
plt.legend(loc='upper right', fontsize=12)
plt.grid(alpha=0.3)
plt.show()
```
-->

See {numref}`sec:point_and_credibility` for further discussion of credible regions.

## Bayesian credible intervals and frequentist confidence intervals

There are important differences between the Bayesian
68% credible (DoB) interval for the most likely value  and a frequentist $1 \sigma$ confidence
interval. 

The first point is that $1 \sigma=68$% assumes a Gaussian distribution
around the maximum of the posterior. While this will
often work out to be roughly correct, it may not. And, as we seek to translate 
$n \sigma$ intervals into DoB statements, assuming a Gaussian
becomes more and more questionable the higher $n$ is. (*Why?*)

But the second point is more philosophical (meta-statistical?). One
  interval is a statement about $p(x|D,I)$, while the other is a
  statement about $p(D|x,I)$.
(Note that because the conversion between the two PDFs requires the
 use of Bayes' theorem, the Bayesian interval may be affected by the
 choice of the prior.)

The Bayesian version of a confidence interval is easy; a 68% credible interval or degree-of-belief (DoB) interval is: given
  some data and some information $I$, there is a 68% chance (probability) that the interval contains the true parameter. 

On the other hand, the frequentist 68% confidence interval is trickier:
assuming the model (contained in $I$) and the value of the
parameter $x$, then if we do the experiment a large number of
times then 68% of them will produce data in that interval.
So the *parameter* is fixed (no PDF) and the confidence
interval is a statement about *data*.
Frequentists will try to make statements about parameters, but
they end up a bit tangled, e.g., "There is a 68% probability
that when I compute a confidence interval from data of this sort
that the true value of $\theta$ will fall within the
(hypothetical) space of observations."





