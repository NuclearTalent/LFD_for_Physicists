---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:2dPDFs)=
# Two-dimensional PDFs

## Visualizing correlated Gaussian distributions

A multivariate Gaussian distribution for $N$ dimensional $\boldsymbol{x} = \{x_1, \ldots, x_N\}$ with $\boldsymbol{\mu} = \{\mu_1, \ldots, \mu_N\}$, with positive-definite *covariance matrix* $\Sigma$ is 

$$
  p(\boldsymbol{x}|\boldsymbol{\mu},\Sigma) = \frac{1}{\sqrt{\det(2\pi\Sigma)}}
    e^{-\frac{1}{2}(\boldsymbol{x}-\boldsymbol{\mu})^\intercal\Sigma^{-1}(\boldsymbol{x}-\boldsymbol{\mu})}
$$

For the one-dimensional case, it reduces to the familiar

$$
  p(x_1|\mu_1,\sigma_1) = \frac{1}{\sqrt{2\pi\sigma_1^2}}
    e^{-\frac{(x_1-\mu_1)^2}{2\sigma_1^2}}
$$

with $\Sigma = \sigma_1^2$.

For the bivariate case (two dimensional), 

$$
  \boldsymbol{x} = \begin{pmatrix} x_1\\ x_2 \end{pmatrix} \quad\mbox{and}\quad
  \boldsymbol{\mu} = \begin{pmatrix} \mu_1\\ \mu_2 \end{pmatrix} \quad\mbox{and}\quad
  \Sigma = \begin{pmatrix}
             \sigma_1^2 & \rho_{12} \sigma_1\sigma_2 \\
             \rho_{12}\sigma_1\sigma_2 & \sigma_2^2
           \end{pmatrix}
        \quad\mbox{with }\ 0 < \rho_{12}^2 < 1            
$$ (eq:bivariate_case)

and $\Sigma$ is positive definite.

**Widget user interface features**:
   * Set the mean position $(\mu_1, \mu_2)$ and variances $(\Sigma_{11}, \Sigma_{22})$ with the sliders
   * Set the correlation $\rho_{12}$ with the slider. This controls the covariance $\Sigma_{12} = \rho_{12} \sqrt{ \Sigma_{11} \Sigma_{22}}$.
   * Four presets are available.
   * The corner plot shows samples from the bivariate PDF and histograms for the two marginal distributions. Control the number of samples with the slider.
   * Dashed lines on the marginals mark the 16th, 50th, and 84th percentiles. This is equivalent to $\pm 1\sigma$ for a one-dimensional Gaussian.


```{raw} html
<iframe src="../../../_static/app_BivariateGaussian_shared-css.html"
    width="100%"
    height="760"
    style="border: none; display: block;"
    scrolling="no">
</iframe>
```

The solid and dashed ellipses in the joint panel are iso-probability levels. These correspond to fixed values of the squared Mahalanobis distance
 
$$
\Delta^2 = (\mathbf{x} - \boldsymbol{\mu})^\top \Sigma^{-1} (\mathbf{x} - \boldsymbol{\mu}).
$$
 
In the widget they are drawn at $\Delta = 1$ and $\Delta = 2$. Their semi-axes are aligned with the eigenvectors of $\Sigma$ and have lengths $\sqrt{\lambda_i}$ (the "$1\sigma$" ellipse) and $2\sqrt{\lambda_i}$ (the "$2\sigma$" ellipse), where $\lambda_i$ are the eigenvalues of $\Sigma$.
 
:::{admonition} A subtlety worth highlighting
:class: note
In one dimension the $\pm 1\sigma$ and $\pm 2\sigma$ intervals contain 68.3% and 95.4% of the probability mass. In two dimensions, the corresponding *ellipses* contain considerably less, because $\Delta^2 \sim \chi^2_2$ and
 
$$
\prob(\Delta^2 \le k^2) = 1 - e^{-k^2/2}.
$$
 
| Ellipse | Probability mass (2D) | For comparison: 1D interval |
|---|---|---|
| $\Delta = 1$ ("$1\sigma$")   | 39.3% | 68.3% |
| $\Delta = 2$ ("$2\sigma$")   | 86.5% | 95.4% |
| $\Delta = 3$ ("$3\sigma$")   | 98.9% | 99.7% |
:::

::::{admonition} Questions to consider:
:class: my-checkpoint
1. *What does "positive definite" mean and why is this a requirement for the covariance matrix $\Sigma$?*
   :::{admonition} Answer 
   :class: dropdown, my-answer 
   A symmetric matrix (such as a covariance matrix) is positive definite if all of its eigenvalues are greater than zero. This ensures that
   * the variance of any linear combination of random variables is non-negative;
   * that no variable is a linear combination of others (no collinear variables);
   * the covariance matrix is invertible.
   :::
1. *What is plotted in each part of the graph (called a "corner plot")?*
1. *What effect does changing $\mu_1$ or $\mu_2$ have?* 
1. *What effect does changing $\Sigma_{11}$ or $\Sigma_{22}$ have? What if the scales for $x_1$ and $x_2$ were the same?*
1. *What happens if $\rho_{12}$ is equal to $0$ then $+0.7$ then $-0.7$.*
1. *What would happen if you were allowed to set $|\rho_{12}| \leq 1$? Explain what goes wrong.*
1. *So what characterizes independent (uncorrelated) variables versus positively correlated versus negatively correlated?* 


::::

<!--
## Follow-up on correlated posteriors

The first Gaussian 2D PDF in the last section is characterized by elliptical contours of equal probability density whose major axes are aligned with the $x_1$ and $x_2$ axes. 
This is a signature of *independent* random variables.
The second Gaussian 2D PDF had major axes that were slanted with respect to the $x_1$ and $x_2$ axes. 
This is a signature of *correlated* random variables.

Let's look at a case with slanted posteriors and consider analytically (in the next section) what we should expect with correlations.
We'll use the exercise notebook {ref}`exercise:fitting-a-straight-line-i` as a guide.
What are we trying to find? As in other notebooks, we seek $p(\pars|D,I)$, now with $\pars =[b,m]$ (you should review the *statistical model*).

:::{note}
Some comments on the implementation:
* Note that $x_i$ is randomly distributed uniformly.
* Log likelihood gives fluctuating results whose size depend on the # of data points $N$ and the standard deviation of the noise $dy$.
* Note: log(posterior) = log(likelihood) + log(prior)
    * Maximum is set to 1 for plotting
    * Exponentiate: posterior = exp(log(posterior))
:::


:::{admonition} Explore!
Play with the notebook and explore how the results vary with $N$ and $dy$.
:::

::::{admonition} Observation about priors:
Observations about the second set of data: 
* True answers are intercept $b = 25.0$, slope $m=0.5$.
* Flat prior gives $b = -50 \pm 75$, $m = 1.5 \pm 1$, so barely at the $1\sigma$ level.
* Symmetric prior gives $b = 25 \pm 50$, $m = 0.5 \pm 0.75$, so much better.
* Distributions are wide (not surprising since only three points!).

Compare priors on the slope $\Longrightarrow$ uniform in $m$ vs. uniform in angle.
* With the first set of data with $N=20$ points, does the prior matter?
* With the second set of data with $N=3$ points, does the prior matter?
:::{admonition} Answers
:class: dropdown
No!  
Yes!
:::
::::

::::{admonition} Recap: what does it mean that the ellipses are slanted? And why is it expected?
:::{admonition} Answer
:class: dropdown
It means that the slope and intercept are *correlated*. Intuitively, if we want to maintain a good fit when we change the slope, we will need to change the intercept as well. They are not independent!
:::
::::
-->


## 2D PDF with a quadratic approximation

Consider a general two-dimensional log likelihood $L(X,Y)$. We'll analyze it in a quadratic approximation.
We base our discussion on Sivia section 3.3 {cite}`Sivia2006`.

First, find the mode $X_0$, $Y_0$ (which is the best estimate) by differentiating

$$\begin{align}
 L(X,Y) &= \log p(X,Y|\{\text{data}\}, I) \\
  \quad&\Longrightarrow\quad
  \left.\frac{dL}{dX}\right|_{X_0,Y_0} = 0, \ 
  \left.\frac{dL}{dY}\right|_{X_0,Y_0} = 0
\end{align}$$

To check reliability, Taylor expand around $L(X_0,Y_0)$:

$$\begin{align}
 L &= L(X_0,Y_0) + \frac{1}{2}\biggl[
   \left.\frac{\partial^2L}{\partial X^2}\right|_{X_0,Y_0}(X-X_0)^2
  + \left.\frac{\partial^2L}{\partial Y^2}\right|_{X_0,Y_0}(Y-Y_0)^2 \\
  & \qquad\qquad\qquad + 2 \left.\frac{\partial^2L}{\partial X\partial Y}\right|_{X_0,Y_0}(X-X_0)(Y-Y_0)
   \biggr] + \ldots \\
   &\equiv L(X_0, Y_0) + \frac{1}{2}Q + \ldots
\end{align}$$

It makes sense to do this in (symmetric) matrix notation:

$$
  Q = 
  \begin{pmatrix} X-X_0 & Y-Y_0 
  \end{pmatrix}
  \begin{pmatrix} A & C \\
                  C & B 
  \end{pmatrix}
  \begin{pmatrix} X-X_0 \\
                  Y-Y_0 
  \end{pmatrix}
$$  (eq:Qmatrix)

$$
 \Longrightarrow
 A = \left.\frac{\partial^2L}{\partial X^2}\right|_{X_0,Y_0},
 \quad
 B = \left.\frac{\partial^2L}{\partial Y^2}\right|_{X_0,Y_0},
 \quad
 C = \left.\frac{\partial^2L}{\partial X\partial Y}\right|_{X_0,Y_0}
$$


```{image} ../assets/posterior_ellipse.png
:alt: posterior ellipse
:class: bg-primary
:width: 400px
:align: center
```

So in a quadratic approximation, the contour $Q=k$ for some $k$ is an ellipse centered at $X_0, Y_0$ (as in the figure). The orientation and eccentricity of the ellipse are determined by $A$, $B$, and $C$.
The principal axes are found from the eigenvectors of the Hessian matrix $\begin{pmatrix} A & C \\ C & B  \end{pmatrix}$:

$$
\begin{pmatrix}
     A & C \\
     C & B
\end{pmatrix}
\begin{pmatrix}
 x \\ y
\end{pmatrix}
=
\lambda
\begin{pmatrix}
 x \\ y
\end{pmatrix}
\quad\Longrightarrow\quad
\lambda_1,\lambda_2 < 0 \ \ \mbox{so $(X_0,Y_0)$ is a maximum}
$$

:::{admonition} Conditions on $A$, $B$, $C$
:class: note
The condition $\lambda_1,\lambda_2 < 0$ for the point $(X_0,Y_0)$ to be a maximum implies that we must have

$$
   A < 0, \qquad B < 0, \qquad AB > C^2 .
$$
:::

If the major and minor axes of the ellipse are aligned with the $x$-axis and $y$-axis (so $C=0$), the analysis is simple: the eigenvalues are $A$ and $B$ and the error-bars (standard deviations) for $X$ and $Y$ will be inversely proportional to the modulus of their square roots.
What if the ellipse is skewed?


If we compare $Q$ in {eq}`eq:Qmatrix` to the bivariate Gaussian exponent {eq}`eq:bivariate_case`, we can identify the covariance matrix {eq}`eq:covariance_Sigma_XY` in terms of the inverse of $Q$:

$$
 \Sigma_{XY} 
  = 
   \begin{pmatrix}
    \sigma_X^2 &  \sigma_{XY}^2 \\
    \sigma_{XY}^2 & \sigma_Y^2
   \end{pmatrix}
 = - \begin{pmatrix}
     A & C \\
     C & B
     \end{pmatrix}^{-1} 
  = \frac{1}{AB - C^2}
    \begin{pmatrix}
      -B & C \\
      C  & -A
    \end{pmatrix}
     ,
$$

from which we can read off the variances and covariance in terms of $A$, $B$, $C$.
When $C=0$, the covariance $\sigma_{XY} = 0$ and the values of $X$ and $Y$ are uncorrelated.
As $|C|$ increases from zero, the ellipse becomes increasingly skewed and elongated; this corresponds to greater correlation (with $C>0$ correlated and $C<0$ anti-correlated).


<!--
## Sivia example on "signal on top of background"

See {cite}`Sivia2006` for further details. The figure shows the set up:
```{image} ../assets/signal_on_background_handdrawn.png
:alt: signal on background
:class: bg-primary
:width: 500px
:align: center
```
The level of the background is $B$, the peak height of the signal above the background is $A$ and there are $\{N_k\}$ counts in the bins $\{x_k\}$. 
The distribution is

$$
  D_k = n_0 [A e^{-(x_k-x_0)^2/2w^2} + B]
$$


**Goal:** Given $\{N_k\}$, find $A$ and $B$.

So what is the posterior we want?

$$
  p(A,B | \{N_k\}, I) \ \mbox{with $I=x_0, w$, Gaussian, flat background}  
$$

The actual counts we get will be integers, and we can expect a *Poisson distribution*:

$$
   p(n|\mu) = \frac{\mu^n e^-\mu}{n!} \ \mbox{$n\geq 0$ integer}
$$

or, with $n\rightarrow N_k$, $\mu \rightarrow D_k$,

$$
  p(N_k|D_k) = \frac{D_k e^{-D_k}}{N_k!}
$$

for the $k^{\text{th}}$ bin at $x_k$.

What do we learn from the plots of the Poisson distribution?

$$\begin{align}
  p(A,B | \{N_k\}, I) &\propto p(\{N_k\}|A,B,I) \times p(A,B|I) \\
  \textit{posterior}\qquad &\propto \quad\textit{likelihood}\quad \times \quad\textit{prior}
\end{align}$$

which means that 

$$
  L = \log[p(A,B)|\{N_k\,I\})] = \text{constant} + \sum_{k=1}^M [N_k \log(D_k) - D_k]
$$


* Choose the constant for convenience; it is independent of $A,B$.
* Best *point estimate*: maximize $L(A,B)$ to find $A_0,B_0$
* Look at code for likelihood and prior
* Uniform (flat) prior for $0 \leq A \leq A_{\text{max}}$, $0 < B \leq B_{\text{max}}$
    * Not sensitive to $A_{\text{max}}$, $B_{\text{max}}$ if larger than support of likelihood

:::{admonition} Table of results

| Fig. # | data bins  | $\Delta x$  | $(x_k)_{\text{max}}$ | $D_{\text{max}}$ |
|:----:|:----:|:----:|:----:|:----:|
|  1  |  15  |  1   |   7   | 100  |
|  2  |  15  |  1   |   7   | 10   |
|  3  |  31  |  1   |  15   | 100  |
|  4  |   7  |  1   |   3   | 100  |

:::

Comments on figures:
* Figure 1: 15 bins and $D_{\text{max}} = 100$
    * Contours are at 20% intervals showing *height*
    * Read off best estimates and compare to true
        * does find signal is about half background
    * Marginalization of $B$
        * What if we don't care about $B$? ("nuisance parameter")

        $$
         p(A | \{N_k\}, I) \int_0^\infty p(A,B|\{N_k\},I)\, dB
        $$
 
        * compare to $p(A | \{N_k\}, B_{\text{true}}, I)$
          $\Longrightarrow$ plotted on graph
    * Also can marginalize over $A$

        $$
         p(B | \{N_k\}, I) \int_0^\infty p(A,B|\{N_k\},I)\, dA
        $$

    * Note how these are done in code: `B_marginalized` and `B_true_fixed`, and note the normalization at the end.

* Set extra plots to true
    * different representations of the same info and contours in the first three. The last one is an attempt at 68%, 95%, 99.7% (but looks wrong).
    * note the difference between contours showing the PDF *height* and showing the integrated volume.

* Look at the other figures and draw conclusions.

* How should you design your experiments?
    * E.g., how should you bin data, how many counts are needed, what $(x_k)_{\text{max}}$, and so on.    
-->
