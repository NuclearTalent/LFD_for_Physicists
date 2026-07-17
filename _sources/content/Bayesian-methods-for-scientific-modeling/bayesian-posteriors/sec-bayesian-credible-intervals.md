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

**To do:** *Play with the widget and devise algorithms that can be coded in Python for determining the ETI and HPD regions for a given credible interval percentage.*


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


### Try a couple of checkpoint questions

The following two checkpoint questions show one-dimensional multi-modal PDFs. The smooth curves are approximated by discrete boxes, all of which have the same probability. 
Your task is to establish the intervals for 68% credible intervals using both the equal-tailed interval (ETI) and highest posterior density (HPD) conventions.
You can do this by counting boxes. 
The box width is 0.25 so your intervals should be of the form (-3.25, 1.50).
Note that you may have disconnected intervals.

Because of the discrete size of the boxes, you won't get precisely 68%. Choose your interval to be the closest to 68%, but on the higher side.
There is code available that you can inspect to see how the intervals were calculated here and you can copy it to a Jupyter notebook to change the distributions.

```{code-cell} python3
:label: credible-intervals-1
:tags: [hide-input]

from myst_nb import glue

from dataclasses import dataclass
from typing import Callable, Optional

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.integrate import quad
from scipy.stats import norm

plt.rcParams.update({
    'font.size': 16,           # Global default size
    'axes.titlesize': 20,      # Title of the individual plots
    'axes.labelsize': 18,      # x and y axis labels
    'xtick.labelsize': 14,     # x-axis tick labels
    'ytick.labelsize': 14,     # y-axis tick labels
    'legend.fontsize': 14,     # Legend font size
    'figure.titlesize': 22     # Main figure super-title
})

@dataclass
class BoxHistogram:
    edges: np.ndarray
    counts: np.ndarray
    target_bin_probabilities: np.ndarray
    normalization_on_range: float

    @property
    def n_bins(self) -> int:
        return len(self.counts)

    @property
    def n_boxes(self) -> int:
        return int(self.counts.sum())

    @property
    def bin_width(self) -> float:
        widths = np.diff(self.edges)

        if not np.allclose(widths, widths[0]):
            raise ValueError("The bins must have equal widths.")

        return float(widths[0])

    @property
    def box_height(self) -> float:
        """
        Since each box has area 1/n_boxes,

            bin_width * box_height = 1/n_boxes.
        """
        return 1.0 / (self.n_boxes * self.bin_width)

    @property
    def bin_probabilities(self) -> np.ndarray:
        return self.counts / self.n_boxes

    @property
    def density_heights(self) -> np.ndarray:
        return self.counts * self.box_height

    def probability(self, selected_bins: np.ndarray) -> float:
        """Probability contained in a Boolean selection of whole bins."""
        selected_bins = np.asarray(selected_bins, dtype=bool)

        if selected_bins.shape != self.counts.shape:
            raise ValueError(
                "selected_bins must contain one Boolean value per bin."
            )

        return float(
            self.counts[selected_bins].sum() / self.n_boxes
        )

    def intervals_from_mask(
        self,
        selected_bins: np.ndarray,
    ) -> list[tuple[float, float]]:
        """
        Convert a Boolean bin mask into one or more intervals.

        This is useful for highest-density regions, which may be disconnected.
        """
        selected_bins = np.asarray(selected_bins, dtype=bool)
        intervals = []

        i = 0
        while i < self.n_bins:
            if not selected_bins[i]:
                i += 1
                continue

            j = i
            while (
                j + 1 < self.n_bins
                and selected_bins[j + 1]
            ):
                j += 1

            intervals.append(
                (float(self.edges[i]), float(self.edges[j + 1]))
            )

            i = j + 1

        return intervals

    def plot(
        self,
        selected_bins: Optional[np.ndarray] = None,
        pdf: Optional[Callable[[float], float]] = None,
        ax=None,
        title: Optional[str] = None,
        intervals: Optional[str] = None,
    ):
        """
        Plot every equal-probability box separately.

        Parameters
        ----------
        selected_bins
            Boolean mask indicating which complete bars should be shaded.

        pdf
            Optional target PDF to overlay. It is normalized over the
            displayed x range.

        ax
            Optional matplotlib axis.
        """
        if ax is None:
            _, ax = plt.subplots(figsize=(10, 5))

        if selected_bins is None:
            selected_bins = np.zeros(self.n_bins, dtype=bool)
        else:
            selected_bins = np.asarray(selected_bins, dtype=bool)

        dx = self.bin_width
        dh = self.box_height

        for bin_index, number_of_boxes in enumerate(self.counts):
            for level in range(int(number_of_boxes)):
                rectangle = Rectangle(
                    xy=(
                        self.edges[bin_index],
                        level * dh,
                    ),
                    width=dx,
                    height=dh,
                    facecolor=(
                        "C0"
                        if selected_bins[bin_index]
                        else "white"
                    ),
                    edgecolor="black",
                    linewidth=0.55,
                )

                ax.add_patch(rectangle)

        ax.set_xlim(self.edges[0], self.edges[-1])

        ymax = max(self.density_heights.max(), dh)
        ax.set_ylim(0.0, 1.08 * ymax)

        ax.set_xlabel(r"$x$")
        ax.set_ylabel("probability density")
        ax.set_title(
            title or
            f"{self.n_boxes} equal-probability boxes"
        )
        if intervals:
           answer_text = "intervals = \n" + str(intervals)
           ax.text(
              0.02, 0.97,                      # Coordinates (2% from left, 97% from bottom)
              answer_text,     # The text string
              transform=ax.transAxes,          # Use axes coordinate system (0 to 1)
              verticalalignment='top',         # Align the top of the text to the coordinate
              horizontalalignment='left'       # Align the left of the text to the coordinate
           )

        ax.grid(axis="y", alpha=0.2)

        if pdf is not None:
            x_plot = np.linspace(
                self.edges[0],
                self.edges[-1],
                1200,
            )

            y_plot = np.array(
                [pdf(x) for x in x_plot],
                dtype=float,
            )

            # Normalize the target curve on the displayed range.
            y_plot /= self.normalization_on_range

            ax.plot(
                x_plot,
                y_plot,
                linewidth=2,
                label="target density",
            )
            ax.legend()

        return ax


def make_box_histogram(
    pdf: Callable[[float], float],
    x_range: tuple[float, float],
    n_bins: int = 40,
    n_boxes: int = 200,
) -> BoxHistogram:
    """
    Approximate a PDF using an integer number of equal-area boxes.

    The target PDF is integrated over each equal-width bin. Integer
    box counts are assigned by the largest-remainder method, so that

        sum(counts) == n_boxes

    exactly.

    The PDF is renormalized over x_range.
    """
    xmin, xmax = x_range

    if xmax <= xmin:
        raise ValueError("x_range must satisfy xmax > xmin.")

    if n_bins < 1 or n_boxes < 1:
        raise ValueError("n_bins and n_boxes must be positive.")

    edges = np.linspace(xmin, xmax, n_bins + 1)

    # Integrate the target density over each bin.
    bin_masses = np.array(
        [
            quad(
                pdf,
                edges[i],
                edges[i + 1],
                limit=200,
            )[0]
            for i in range(n_bins)
        ],
        dtype=float,
    )

    if np.any(bin_masses < -1.0e-12):
        raise ValueError(
            "The supplied PDF is negative in at least one bin."
        )

    # Remove insignificant negative roundoff.
    bin_masses = np.maximum(bin_masses, 0.0)

    normalization = float(bin_masses.sum())

    if not np.isfinite(normalization) or normalization <= 0.0:
        raise ValueError(
            "The PDF has no finite positive mass on x_range."
        )

    bin_probabilities = bin_masses / normalization

    # Desired, generally noninteger, box counts.
    raw_counts = n_boxes * bin_probabilities

    # Begin by rounding down.
    counts = np.floor(raw_counts).astype(int)

    # Distribute remaining boxes according to the largest
    # fractional remainders.
    boxes_left = n_boxes - counts.sum()

    if boxes_left > 0:
        fractional_parts = raw_counts - counts

        recipients = np.argsort(
            fractional_parts
        )[::-1][:boxes_left]

        counts[recipients] += 1

    return BoxHistogram(
        edges=edges,
        counts=counts,
        target_bin_probabilities=bin_probabilities,
        normalization_on_range=normalization,
    )


def equal_tailed_bins(
    hist: BoxHistogram,
    level: float = 0.68,
) -> np.ndarray:
    """
    Equal-tailed interval, rounded outward to whole bins.
    """
    if not 0.0 < level < 1.0:
        raise ValueError("level must be between zero and one.")

    tail_probability = 0.5 * (1.0 - level)
    cdf = np.cumsum(hist.counts) / hist.n_boxes

    first_bin = int(
        np.searchsorted(
            cdf,
            tail_probability,
            side="left",
        )
    )

    last_bin = int(
        np.searchsorted(
            cdf,
            1.0 - tail_probability,
            side="left",
        )
    )

    mask = np.zeros(hist.n_bins, dtype=bool)
    mask[first_bin:last_bin + 1] = True

    return mask


def shortest_contiguous_bins(
    hist: BoxHistogram,
    level: float = 0.68,
) -> np.ndarray:
    """
    Narrowest contiguous set of whole bins containing at least
    the requested probability.
    """
    if not 0.0 < level < 1.0:
        raise ValueError("level must be between zero and one.")

    boxes_required = int(
        np.ceil(level * hist.n_boxes)
    )

    cumulative_counts = np.concatenate(
        ([0], np.cumsum(hist.counts))
    )

    best_candidate = None
    right = 0

    for left in range(hist.n_bins):
        right = max(right, left + 1)

        while (
            right <= hist.n_bins
            and cumulative_counts[right]
            - cumulative_counts[left]
            < boxes_required
        ):
            right += 1

        if right > hist.n_bins:
            break

        width = hist.edges[right] - hist.edges[left]

        excess_boxes = (
            cumulative_counts[right]
            - cumulative_counts[left]
            - boxes_required
        )

        candidate = (
            width,
            excess_boxes,
            left,
            right,
        )

        if (
            best_candidate is None
            or candidate < best_candidate
        ):
            best_candidate = candidate

    if best_candidate is None:
        raise RuntimeError(
            "No contiguous interval could be constructed."
        )

    _, _, left, right = best_candidate

    mask = np.zeros(hist.n_bins, dtype=bool)
    mask[left:right] = True

    return mask


def highest_density_bins(
    hist: BoxHistogram,
    level: float = 0.68,
) -> np.ndarray:
    """
    Highest-density set of whole bins.

    Because the bins have equal widths, sorting by histogram
    density is equivalent to sorting by the number of boxes
    in each bar.

    The resulting credible region may be disconnected.
    """
    if not 0.0 < level < 1.0:
        raise ValueError("level must be between zero and one.")

    boxes_required = int(
        np.ceil(level * hist.n_boxes)
    )

    # Tallest bars first.
    order = np.argsort(hist.counts)[::-1]

    mask = np.zeros(hist.n_bins, dtype=bool)
    accumulated_boxes = 0

    for bin_index in order:
        if accumulated_boxes >= boxes_required:
            break

        if hist.counts[bin_index] == 0:
            break

        mask[bin_index] = True
        accumulated_boxes += int(hist.counts[bin_index])

    return mask




##################################################################
#   Boxed pdf #1
##################################################################

weights = np.array([0.42, 0.33, 0.25])
means = np.array([-2.4, 0.3, 2.8])
#standard_deviations = np.array([0.65, 0.35, 0.85])
standard_deviations = np.array([0.65, 0.35, 0.80])


def target_pdf(x):
    return np.sum(
        weights
        * norm.pdf(
            x,
            loc=means,
            scale=standard_deviations,
        )
    )


hist = make_box_histogram(
    pdf=target_pdf,
    x_range=(-5.0, 5.5),
    n_bins=42,
    n_boxes=210,
)


ax = hist.plot(pdf=target_pdf)
fig = ax.figure

# Save the rendered figure for insertion elsewhere.
glue("cred-int-figure-1", fig, display=False)

# Avoid displaying the figure at the original code-cell location.
plt.close(fig)

#print("Boxes in each bar:")
#print(hist.counts)
#print(f"\nProbability per box = {1 / hist.n_boxes:.5f}")

level = 0.68

prescriptions = {
    "Equal-tailed":
        equal_tailed_bins(hist, level),

   # "Shortest contiguous":
   #     shortest_contiguous_bins(hist, level),

    "HPD":
        highest_density_bins(hist, level),
}


fig, axes = plt.subplots(
    2,
    1,
    figsize=(10, 12),
    constrained_layout=True,
)

for ax, (name, selected_bins) in zip(
    axes,
    prescriptions.items(),
):
    enclosed_probability = hist.probability(
        selected_bins
    )

    intervals = hist.intervals_from_mask(
        selected_bins
    )

    hist.plot(
        selected_bins=selected_bins,
        pdf=target_pdf,
        ax=ax,
        title=(
            f"{name}: "
            f"enclosed probability "
            f"= {enclosed_probability:.3f}"
        ),
        intervals=intervals,
    )


#    print(
#        f"{name:22s}: "
#        f"{intervals}; "
#        f"probability = {enclosed_probability:.3f}"
#    )
#    answers = f"{name:22s}: {intervals}; probability = {enclosed_probability:.3f}"
#    answers = f"{name:22s}: {intervals}"
#    glue("cred-int-1ans", answers, display=False)


# Save the rendered figure for insertion elsewhere.
glue("cred-int-figure-1ans", fig, display=False)

# Avoid displaying the figure at the original code-cell location.
plt.close(fig)

#plt.show()


##################################################################
#   Boxed pdf #2
##################################################################

weights = np.array([0.20, 0.30, 0.50])
means = np.array([-2.5, 0.0, 2.5])
standard_deviations = np.array([0.6, 0.5, 0.5])


def target_pdf(x):
    return np.sum(
        weights
        * norm.pdf(
            x,
            loc=means,
            scale=standard_deviations,
        )
    )


hist = make_box_histogram(
    pdf=target_pdf,
    x_range=(-5.0, 5.5),
    n_bins=42,
    n_boxes=210,
)

ax = hist.plot(pdf=target_pdf)
fig = ax.figure

# Save the rendered figure for insertion elsewhere.
glue("cred-int-figure-2", fig, display=False)

# Avoid displaying the figure at the original code-cell location.
plt.close(fig)

#print("Boxes in each bar:")
#print(hist.counts)
#print(f"\nProbability per box = {1 / hist.n_boxes:.5f}")

level = 0.68

prescriptions = {
    "Equal-tailed":
        equal_tailed_bins(hist, level),

   # "Shortest contiguous":
   #     shortest_contiguous_bins(hist, level),

    "HPD":
        highest_density_bins(hist, level),
}


fig, axes = plt.subplots(
    2,
    1,
    figsize=(10, 12),
    constrained_layout=True,
)

for ax, (name, selected_bins) in zip(
    axes,
    prescriptions.items(),
):
    enclosed_probability = hist.probability(
        selected_bins
    )

    intervals = hist.intervals_from_mask(
        selected_bins
    )

    hist.plot(
        selected_bins=selected_bins,
        pdf=target_pdf,
        ax=ax,
        title=(
            f"{name}: "
            f"enclosed probability "
            f"= {enclosed_probability:.3f}"
        ),
        intervals=intervals,
    )

    #print(
    #    f"{name:22s}: "
    #    f"{intervals}; "
    #    f"probability = {enclosed_probability:.3f}"
    #)
#    answers = f"{name:22s}: {intervals}; probability = {enclosed_probability:.3f}"
#    answers = f"{name:22s}: {intervals}"
#    glue("cred-int-2ans", answers, display=False)

# Save the rendered figure for insertion elsewhere.
glue("cred-int-figure-2ans", fig, display=False)

# Avoid displaying the figure at the original code-cell location.
plt.close(fig)

#plt.show()

```

::::{admonition} Checkpoint Question
:class: my-checkpoint

```{glue:figure} cred-int-figure-2
:figwidth: 95%
:align: center
:name: fig-cred-int-2
```

Identify the ETI and HPD credible intervals.



:::{admonition} Answer
:class: dropdown, my-answer
```{glue:figure} cred-int-figure-2ans
:figwidth: 95%
:align: center
:name: fig-cred-int-2ans
```

:::
::::


::::{admonition} Checkpoint Question
:class: my-checkpoint

```{glue:figure} cred-int-figure-1
:figwidth: 95%
:align: center
:name: fig-cred-int-1
```

Identify the ETI and HPD credible intervals.



:::{admonition} Answer
:class: dropdown, my-answer

```{glue:figure} cred-int-figure-1ans
:figwidth: 95%
:align: center
:name: fig-cred-int-1ans
```

:::
::::




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





