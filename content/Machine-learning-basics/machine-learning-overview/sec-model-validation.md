---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.0
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

(sec:ModelValidation)=
# Model validation

In this section we will encounter several concepts that are common to machine learning methods. These concepts are:
  * Overfitting and underfitting
  * Model validation and model hyperparameters
  * Bias-variance tradeoff
  * Regularization
  * Cross-validation

Throughout this section we use a simple running example. The data-generating process is $f(x) = \sin(\pi x) + x/2$ for $x \in [-1, 1]$, and observations $\output_i = f(x_i) + \epsilon_i$ include independent, normally distributed noise with standard deviation $\sigma_\epsilon = 0.3$. We have a training set of $N_\mathrm{train} = 20$ observations and a validation set of $N_\mathrm{val} = 50$ observations, and we use linear regression with polynomial models of different degrees (see {ref}`sec:ols_in_practice`). The code that produces the figures is available in hidden code cells (click on "Show code cell content"). While linear regression is used for demonstration purposes, the concepts are general and carry over to more complex models such as neural networks. 

The section is based on and inspired by material in several good textbooks: in particular chapter 4 in [Hands‑On Machine Learning with Scikit‑Learn and TensorFlow](http://shop.oreilly.com/product/0636920052289.do) {cite}`Geron2017` by Aurelien Geron, chapter 5 in the 
[Python Data Science Handbook](http://shop.oreilly.com/product/0636920034919.do) {cite}`Vanderplas2016` by Jake VanderPlas and chapters 2-4 in [The Elements of
Statistical Learning](https://link.springer.com/book/10.1007/978-0-387-84858-7) {cite}`Hastie2009` by Trevor Hastie et al.

## Over- and underfitting

Overfitting and underfitting are common problems in data analysis and machine learning. Both extremes are illustrated in {numref}`fig-over_under_fitting`.

```{code-cell} python3
:tags: [hide-cell]

import numpy as np
import matplotlib.pyplot as plt
from myst_nb import glue

plt.rcParams.update({'font.size': 13, 'axes.titlesize': 13, 'legend.fontsize': 11})

# The data-generating process: a smooth, non-polynomial function
def f_true(x):
    return np.sin(np.pi * x) + 0.5 * x

# Observations with additive, normally distributed noise
sigma_eps = 0.3
def generate_data(N, rng, xlim=(-1, 1)):
    x = np.sort(rng.uniform(*xlim, N))
    y = f_true(x) + rng.normal(0, sigma_eps, N)
    return x, y

# Training and validation data
N_train, N_val = 20, 50
rng = np.random.default_rng(1)
x_train, y_train = generate_data(N_train, rng)
x_val, y_val = generate_data(N_val, rng, xlim=(x_train.min(), x_train.max()))

# Linear regression with a polynomial model: the design matrix has
# the columns 1, x, x^2, ..., x^degree
def design_matrix(x, degree):
    return np.vander(x, degree + 1, increasing=True)

# Least-squares fit (lam = 0) or Ridge regression (lam > 0)
def fit(x, y, degree, lam=0.0):
    X = design_matrix(x, degree)
    if lam == 0.0:
        return np.linalg.lstsq(X, y, rcond=None)[0]
    return np.linalg.solve(X.T @ X + lam * np.eye(degree + 1), X.T @ y)

def predict(theta, x):
    return design_matrix(x, len(theta) - 1) @ theta

def mse(theta, x, y):
    return np.mean((predict(theta, x) - y)**2)

def theta_rms(theta):
    return np.linalg.norm(theta) / np.sqrt(len(theta))

# Fit polynomial models of degree 0, 1, ..., 14 to the training data
max_degree = 14
degrees = np.arange(max_degree + 1)
thetas = [fit(x_train, y_train, degree) for degree in degrees]
rms = np.array([theta_rms(theta) for theta in thetas])

# Plot the true function and the data (also used in later figures)
x_grid = np.linspace(-1, 1, 400)
colors = {'train': 'C0', 'val': 'C1', 'true': '0.25'}
def plot_data(ax):
    ax.plot(x_grid, f_true(x_grid), ls='-', color=colors['true'], lw=1, label='true $f(x)$')
    ax.plot(x_train, y_train, 'o', color=colors['train'], ms=5, label='training data')
    ax.plot(x_val, y_val, 'o', mfc='none', color=colors['val'], ms=4, label='validation data')

# Create a visualization
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6.5, 5))
plot_data(ax)
for degree, ls, color in [(1, ':', 'C3'), (4, '--', 'C2'), (14, '-.', 'C4')]:
    ax.plot(x_grid, predict(thetas[degree], x_grid), ls=ls, color=color, lw=2, label=f'degree {degree}')
ax.set_ylim(-2.5, 2.5)
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=3, frameon=False)
fig.tight_layout()

glue('ModelValidation_over_under_fig', fig, display=False)
plt.close(fig)
for degree in (1, 4, 14):
    glue(f'ModelValidation_rms_deg{degree}', float(rms[degree]), display=False)
```

```{glue:figure} ModelValidation_over_under_fig
:name: fig-over_under_fitting

Polynomial models of degree 1, 4 and 14 trained on the training data (filled circles). The validation data (open circles) are not used for training. The first-order polynomial model is clearly underfitting the data, while the very high degree model is overfitting it trying to reproduce variations that are clearly noise. The degree-4 model is close to the true function $f(x)$ (thin solid line).
```

The following quote from an unknown source provides a concise definition of overfitting and underfitting:
> A model overfits if it fits noise as much as data and underfits if it considers variability in data to be noise while it is actually not.

A sign of overfitting is the appearance of very large fit parameters that are needed for the fine tunings of cancellations of different terms in the model. Polynomial fits of different orders to the data in {numref}`fig-over_under_fitting` give the following root-mean-square parameter values

\begin{equation}
\para_\mathrm{rms} \equiv \sqrt{ \frac{1}{N_p} \sum_{i=0}^{N_p-1} \theta_i^2 } = \| \pars \|_2 / \sqrt{N_p},
\end{equation}

where $N_p$ is the number of parameters (the degree of the polynomial plus one).

| order  | $\para_\mathrm{rms}$  |
| :----- | :--------------------- | 
|    1   | {glue:text}`ModelValidation_rms_deg1:.1e` |
|    4   | {glue:text}`ModelValidation_rms_deg4:.1e` |
|   14   | {glue:text}`ModelValidation_rms_deg14:.1e` |

:::{note} 
 In some cases a learning algorithm makes good predictions despite fitting to the noise in training data. This is called "benign overfitting". See, for example, [Bartlett et al., *Benign Overfitting in Linear Regression*](https://arxiv.org/abs/1906.11300). A recent explanation of this is [Chatterji and Long, *Foolish Crowds Support Benign Overfitting*](https://arxiv.org/abs/2110.02914). From their abstract: "Our analysis exposes the benefit of an effect analogous to the 'wisdom of the crowd', except here the harm arising from fitting the *noise* is ameliorated by spreading it among many directions - the variance reduction arises from a *foolish* crowd."
:::

The questions are: (i) How do we detect these problems? and (ii) How can we reduce them?

(sec:ModelValidation:validation)=
## Model validation

We can detect over- and underfitting by employing a holdout set, also known as *validation* set. This means that we only use a fraction of the data for training the model, and save the rest for validation purposes. 

This implies that we optimize the model parameters to best fit the training data, and then measure, e.g., the mean-squared error (MSE) of the model predictions for the validation set. The function that is used for measuring the performance of the model prediction is called an error function, and is here denoted $E(\MLoutputs, \outputs)$. We stress that this function does not necessarily have to be the same as the cost function that is used for learning. The latter can incorporate other desirable features such as regularization to avoid overfitting (see below), or some domain-specific constraints. The error function, on the other hand, should focus on measuring the property of the prediction that is most important for the application at hand. Default choices for regression and classification tasks, respectively, are

| Task             | Error function  | Measures  |
| :--------------- | :--------------------- | :--------------------- | 
|  Regression      |   $E(\MLoutput, \output) = (\MLoutput - \output)^2 $    | Squared error |
|  Classification  |    $E(\MLoutput, \output) =  1 - \delta_{\MLoutput, \output}$   | Misclassification |

where $1 - \delta_{\MLoutput, \output} = 0$ if $\MLoutput = \output$ (i.e. correct classification) and $= 1$ if $\MLoutput \neq \output$ (misclassified).

Evaluating the error function on either the training set, or the validation set, gives relevant metrics that can be used to monitor under- or overfitting

$$
E_\mathrm{train} &= \frac{1}{N_\mathrm{train}} \sum_{i=1}^{N_\mathrm{train}} E(\MLoutput(\inputs_i), \output_i), \quad\text{for } (\inputs_i, \output_i) \in \data_\mathrm{train} \\
E_\mathrm{val} &= \frac{1}{N_\mathrm{val}} \sum_{i=1}^{N_\mathrm{val}} E(\MLoutput(\inputs_i), \output_i), \quad\text{for } (\inputs_i, \output_i) \in \data_\mathrm{val}. 
$$ (eq:ModelValidation:Etrain-Eval)

```{admonition} Training and validation scores
Several training and validation scores are commonly used in machine learning applications.  First we have the **Mean-Squared Error** (MSE)

$$
\mathrm{MSE} = \frac{1}{N} \sum_{i=1}^N \left( \MLoutput(\inputs_i) - \output_i \right)^2,
$$ (eq:ModelValidation:MSE)

where we have $N$ data and our model is a function of the parameter vector $\pars$. Note that this is the metric that we are minimizing when solving the normal equation Eq. {eq}`eq:NormalEquation`.

Furthermore, we have the **mean absolute error** (MAE) defined as.

$$
\mathrm{MAE} = \frac{1}{N} \sum_{i=1}^N \left| \MLoutput(\inputs_i) - \output_i \right|,
$$ (eq:ModelValidation:MAE)

And the $R2$ score, also known as *coefficient of determination* is

$$
\mathrm{R2} = 1 - \frac{\sum_{i=1}^N \left( \MLoutput(\inputs_i) - \output_i \right)^2}{\sum_{i=1}^N \left( \output_i - \bar{\output} \right)^2},
$$ (eq:ModelValidation:R2)

where $\bar{\output} = \frac{1}{N} \sum_{i=1}^N \output_i$ is the mean of the data. This metric therefore represents the proportion of variance (of $\data$) that has been explained by the independent variables in the model.
  ```

{numref}`fig:ModelValidation:validation-curve` shows $E_\mathrm{train}$ and $E_\mathrm{val}$ (using the squared error) for polynomial models of increasing degree. The training error decreases steadily with the degree, since a more flexible model can always fit the training data at least as well as a less flexible one. The validation error, on the other hand, first decreases and then increases. It has a minimum for degree {glue:text}`ModelValidation_best_degree`. The growing difference between the two curves for high degrees is known as the *generalization gap*. It signals that the model has learned features of the training data that do not generalize to new data.

```{code-cell} python3
:tags: [hide-cell]

# Training and validation errors for all polynomial degrees
E_train = np.array([mse(theta, x_train, y_train) for theta in thetas])
E_val = np.array([mse(theta, x_val, y_val) for theta in thetas])
best_degree = degrees[np.argmin(E_val)]

# Create a visualization
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 4))
ax.semilogy(degrees, E_train, 'o-', color=colors['train'], label=r'$E_\mathrm{train}$')
ax.semilogy(degrees, E_val, 's-', color=colors['val'], label=r'$E_\mathrm{val}$')
ax.axhline(sigma_eps**2, ls=':', color='k', label=r'$\sigma_\epsilon^2$')
ax.axvline(best_degree, color='0.7', lw=6, alpha=0.4, zorder=0)
ax.text(best_degree + 0.2, 0.05, f'min $E_\\mathrm{{val}}$\n(degree {best_degree})', fontsize=12, va='top')
ax.text(0.5, 0.012, 'underfitting', fontsize=12, color='0.3')
ax.text(10.0, 0.012, 'overfitting', fontsize=12, color='0.3')
ax.set_ylim(0.01, 20)
ax.set_xlabel('polynomial degree')
ax.set_ylabel('mean-squared error')
ax.legend(loc='upper left', bbox_to_anchor=(0.3, 1.0))
fig.tight_layout()

glue('ModelValidation_validation_curve_fig', fig, display=False)
plt.close(fig)
glue('ModelValidation_best_degree', int(best_degree), display=False)
```

```{glue:figure} ModelValidation_validation_curve_fig
:name: fig:ModelValidation:validation-curve

Training and validation errors versus polynomial degree for the running example. The training error decreases monotonically, while the validation error has a minimum at an intermediate degree (shaded). The dotted line shows the variance $\sigma_\epsilon^2$ of the noise.
```

An underfit model has a *high bias*, which means that it gives a rather poor fit and the error function will be rather large in average. This will be true for both the training and the validation sets. In {numref}`fig:ModelValidation:validation-curve` this is the case for polynomial degrees 0–2: the training and validation errors are similar, and both are well above the noise level $\sigma_\epsilon^2$.

An overfit model will depend sensitively on the choice of training data. A different split into training and validation sets will give very different predictions. We therefore say that the model displays a *high variance*. While the overfit model usually reproduces training data very well (low bias), it does not generalize well and gives a poor reproduction of validation data. The average values for the error function are therefore very different for the training and validation sets. For degrees 10 and higher in {numref}`fig:ModelValidation:validation-curve`, the validation error is one to two orders of magnitude larger than the training error. Note also that the training error drops below $\sigma_\epsilon^2$. Since no model can predict new observations better than the irreducible noise allows, a training error well below $\sigma_\epsilon^2$ is a clear sign that the model has adapted to the noise in the training data. (The validation error, on the other hand, can dip slightly below $\sigma_\epsilon^2$ since it is itself a noisy estimate based on only $N_\mathrm{val} = 50$ observations.) The wiggles of the degree-14 model in {numref}`fig-over_under_fitting` show how this happens. The concepts of bias and variance are made precise in {numref}`sec:ModelValidation:bias-variance`.

The polynomial degree is an example of a model *hyperparameter*. Hyperparameters are not determined by the training (the minimization of the cost function) but must be chosen beforehand. Other examples are the regularization strength introduced below, and the learning rate, the mini-batch size and the number of epochs of an iterative training algorithm. In order to make an informed choice for these hyperparameters we need to validate that our model provides a good fit to the training data while not becoming overfit. This important process is known as *model validation*. It most often involves splitting the data into two sets: the training set and the validation set. 

The model is then trained on the first set of data, while its performance is monitored on the validation set (by computing your choice of performance score/error function).

```{caution} 
Why is it important not to train and evaluate the model on the same data?
```

Note that the validation set is used to make choices, e.g., to select the polynomial degree with the smallest validation error. The validation error of the selected model is therefore an optimistic estimate of its performance on new data. If an unbiased estimate of the prediction error is needed, a third data set, called the *test set*, should be held back. The test set is used only once, to evaluate the final model after all choices have been made.

```{code-cell} python3
:tags: [remove-cell]

# Helper function that creates the interactive figures (HTML and JavaScript).
# The data is computed in Python and embedded in the page.
import json
from IPython.display import HTML

def slider_widget(wid, title, intro, params, param_labels, fits, E_tr, E_va, rms, xlabel, logx=False, init=0):
    """Return HTML/JS for an interactive figure with a slider over model fits.
    Left panel: data, true f(x) and the selected fit. Right panel: training and
    validation errors versus the slider parameter."""
    xg = x_grid[::2]  # coarser grid keeps the embedded data small
    data = dict(xg=np.round(xg, 3).tolist(), fg=np.round(f_true(xg), 3).tolist(),
                xtr=np.round(x_train, 4).tolist(), ytr=np.round(y_train, 4).tolist(),
                xva=np.round(x_val, 4).tolist(), yva=np.round(y_val, 4).tolist(),
                p=[float(np.log10(p)) if logx else float(p) for p in params],
                labels=param_labels, fits=[np.round(np.clip(fi[::2], -10, 10), 3).tolist() for fi in fits],
                Etr=[float(e) for e in E_tr], Eva=[float(e) for e in E_va],
                rms=[float(r) for r in rms], xlabel=xlabel, logx=logx, sig2=sigma_eps**2)
    return HTML(f"""
<div id="{wid}" style="font-family:sans-serif;font-size:15px;max-width:780px;margin:1.5em 0;border:2px solid #4a7fb5;border-radius:6px;overflow:hidden;">
  <div style="background:#4a7fb5;color:#fff;font-weight:bold;padding:6px 12px;">&#9654; Interactive figure: {title}</div>
  <div style="padding:10px 12px;">
  <p style="margin:0 0 10px 0;">{intro}</p>
  <div style="display:flex;flex-wrap:wrap;align-items:center;gap:12px;margin-bottom:8px;">
    <label style="font-weight:bold;">{xlabel}: <input type="range" min="0" max="{len(params)-1}" step="1" value="{init}" style="width:260px;vertical-align:middle;"></label>
    <span class="param" style="font-weight:bold;font-size:17px;"></span>
  </div>
  <div class="scores" style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:8px;"></div>
  <svg viewBox="0 0 780 320" style="width:100%;height:auto;background:#fff;"></svg>
  </div>
</div>
<script>
(function() {{
  const D = {json.dumps(data)};
  const root = document.getElementById("{wid}");
  const svg = root.querySelector("svg"), slider = root.querySelector("input"), outP = root.querySelector(".param"), outS = root.querySelector(".scores");
  const NS = "http://www.w3.org/2000/svg";
  function el(tag, attrs, parent) {{
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    (parent || svg).appendChild(e); return e;
  }}
  function txt(s, x, y, attrs) {{ const t = el("text", Object.assign({{x: x, y: y, "font-size": 15}}, attrs || {{}})); t.textContent = s; return t; }}
  // Panel geometry
  const L = {{x0: 62, x1: 372, y0: 10, y1: 262, xmin: -1, xmax: 1, ymin: -2.5, ymax: 2.5}};
  const R = {{x0: 490, x1: 755, y0: 10, y1: 262, xmin: Math.min(...D.p), xmax: Math.max(...D.p), ymin: -2, ymax: Math.log10(20)}};
  const sx = (P, v) => P.x0 + (v - P.xmin) / (P.xmax - P.xmin) * (P.x1 - P.x0);
  const sy = (P, v) => P.y1 - (Math.min(Math.max(v, P.ymin - 1), P.ymax + 1) - P.ymin) / (P.ymax - P.ymin) * (P.y1 - P.y0);
  const ly = v => Math.log10(Math.max(v, 1e-6));
  function axes(P, xticks, yticks, xl, yl) {{
    el("rect", {{x: P.x0, y: P.y0, width: P.x1 - P.x0, height: P.y1 - P.y0, fill: "none", stroke: "#444"}});
    xticks.forEach(([v, s]) => {{ el("line", {{x1: sx(P, v), x2: sx(P, v), y1: P.y1, y2: P.y1 + 4, stroke: "#444"}}); txt(s, sx(P, v), P.y1 + 20, {{"text-anchor": "middle"}}); }});
    yticks.forEach(([v, s]) => {{ el("line", {{x1: P.x0 - 4, x2: P.x0, y1: sy(P, v), y2: sy(P, v), stroke: "#444"}}); txt(s, P.x0 - 7, sy(P, v) + 5, {{"text-anchor": "end"}}); }});
    txt(xl, (P.x0 + P.x1) / 2, P.y1 + 44, {{"text-anchor": "middle", "font-size": 17}});
    txt(yl, 0, 0, {{"text-anchor": "middle", transform: `translate(${{P.x0 - 46}},${{(P.y0 + P.y1) / 2}}) rotate(-90)`, "font-size": 17}});
  }}
  const clipL = el("clipPath", {{id: "{wid}-clip"}}); el("rect", {{x: L.x0, y: L.y0, width: L.x1 - L.x0, height: L.y1 - L.y0}}, clipL);
  const clipR = el("clipPath", {{id: "{wid}-clipR"}}); el("rect", {{x: R.x0, y: R.y0, width: R.x1 - R.x0, height: R.y1 - R.y0}}, clipR);
  axes(L, [[-1, "-1"], [-0.5, "-0.5"], [0, "0"], [0.5, "0.5"], [1, "1"]], [[-2, "-2"], [-1, "-1"], [0, "0"], [1, "1"], [2, "2"]], "x", "y");
  function path(P, xs, ys, attrs, clip) {{
    const d = xs.map((x, i) => (i ? "L" : "M") + sx(P, x).toFixed(1) + "," + sy(P, ys[i]).toFixed(1)).join("");
    return el("path", Object.assign({{d: d, fill: "none", "clip-path": `url(#${{clip}})`}}, attrs));
  }}
  path(L, D.xg, D.fg, {{stroke: "#333", "stroke-width": 1.2}}, "{wid}-clip");
  D.xtr.forEach((x, i) => el("circle", {{cx: sx(L, x), cy: sy(L, D.ytr[i]), r: 3.5, fill: "#1f77b4"}}));
  D.xva.forEach((x, i) => el("circle", {{cx: sx(L, x), cy: sy(L, D.yva[i]), r: 3, fill: "none", stroke: "#ff7f0e"}}));
  const fitPath = el("path", {{fill: "none", stroke: "#9467bd", "stroke-width": 2.5, "stroke-dasharray": "8,4", "clip-path": "url(#{wid}-clip)"}});
  // legend left
  [["training data", "#1f77b4", "dot"], ["validation data", "#ff7f0e", "ring"], ["true f(x)", "#333", "line"], ["model", "#9467bd", "dash"]].forEach(([s, c, k], i) => {{
    const y = L.y1 - 62 + 18 * i, x = L.x1 - 150;
    if (k === "dot") el("circle", {{cx: x + 9, cy: y - 5, r: 3.5, fill: c}});
    else if (k === "ring") el("circle", {{cx: x + 9, cy: y - 5, r: 3, fill: "none", stroke: c}});
    else el("line", {{x1: x, x2: x + 18, y1: y - 5, y2: y - 5, stroke: c, "stroke-width": k === "dash" ? 2.5 : 1.2, "stroke-dasharray": k === "dash" ? "6,3" : ""}});
    txt(s, x + 24, y, {{"font-size": 14}});
  }});
  // right panel
  const xt = D.logx ? D.p.filter(v => Math.abs(v - Math.round(v)) < 1e-9 && Math.round(v) % 2 === 0).map(v => [v, "1e" + Math.round(v)])
                    : D.p.filter(v => v % 2 === 0).map(v => [v, String(v)]);
  axes(R, xt, [[-2, "0.01"], [-1, "0.1"], [0, "1"], [1, "10"]], D.xlabel, "mean-squared error");
  el("line", {{x1: R.x0, x2: R.x1, y1: sy(R, ly(D.sig2)), y2: sy(R, ly(D.sig2)), stroke: "#000", "stroke-dasharray": "2,3"}});
  path(R, D.p, D.Etr.map(ly), {{stroke: "#1f77b4", "stroke-width": 2}}, "{wid}-clipR");
  path(R, D.p, D.Eva.map(ly), {{stroke: "#ff7f0e", "stroke-width": 2}}, "{wid}-clipR");
  const mTr = el("circle", {{r: 5, fill: "#1f77b4"}}), mVa = el("circle", {{r: 5, fill: "#ff7f0e"}});
  const vline = el("line", {{y1: R.y0, y2: R.y1, stroke: "#999", "stroke-width": 1}});
  [["E_train", "#1f77b4"], ["E_val", "#ff7f0e"], ["σ²_ε", "#000"]].forEach(([s, c], i) => {{
    const y = R.y0 + 18 + 18 * i, x = R.x1 - 92;
    el("line", {{x1: x, x2: x + 18, y1: y - 5, y2: y - 5, stroke: c, "stroke-width": 2, "stroke-dasharray": i === 2 ? "2,3" : ""}});
    txt(s, x + 24, y, {{"font-size": 14}});
  }});
  function update() {{
    const k = +slider.value;
    fitPath.setAttribute("d", D.xg.map((x, i) => (i ? "L" : "M") + sx(L, x).toFixed(1) + "," + sy(L, D.fits[k][i]).toFixed(1)).join(""));
    const X = sx(R, D.p[k]);
    vline.setAttribute("x1", X); vline.setAttribute("x2", X);
    mTr.setAttribute("cx", X); mTr.setAttribute("cy", sy(R, ly(D.Etr[k])));
    mVa.setAttribute("cx", X); mVa.setAttribute("cy", sy(R, ly(D.Eva[k])));
    const fmt = v => v < 100 ? v.toFixed(3) : v.toExponential(1);
    outP.textContent = D.labels[k];
    const box = (name, val, c) => `<div style="border:2px solid ${{c}};border-radius:5px;padding:4px 12px;min-width:120px;text-align:center;"><span style="font-size:14px;">${{name}}</span><br><span style="font-size:20px;font-weight:bold;">${{fmt(val)}}</span></div>`;
    outS.innerHTML = box("E<sub>train</sub>", D.Etr[k], "#1f77b4") + box("E<sub>val</sub>", D.Eva[k], "#ff7f0e") + box("θ<sub>rms</sub>", D.rms[k], "#9467bd");
  }}
  slider.addEventListener("input", update); update();
}})();
</script>
""")
```

```{code-cell} python3
:tags: [remove-input, web-only]

# Interactive figure (only in the web version of the book)
slider_widget("mv-degree-widget", "polynomial degree",
    "Vary the degree of the polynomial model. The left panel shows the model trained on the training data, and the right panel shows the training and validation errors versus degree.",
    degrees, [f"degree {d}" for d in degrees],
    [predict(theta, x_grid) for theta in thetas], E_train, E_val, rms,
    xlabel="polynomial degree", init=1)
```

(sec:ModelValidation:learning-curves)=
### Learning curves

The performance of the model will depend on the amount of data that is used for training. When using iterative optimization approaches, such as gradient descent, it will also depend on the number of training iterations. In order to monitor this dependence one usually plots a *learning curve*.

Learning curves are plots of the model performance on both the training and the validation sets, measured by some performance metric such as the mean squared error. This measure is plotted as a function of the size of the training set, or alternatively as a function of the number of training iterations. One defines an *epoch* of training as an update of the model parameters where the entire batch of training data has been used exactly once. An epoch can therefore consist of multiple updates via a random traverse of all training data one by one, or split into mini-batches.

The general steps of an iterative learning algorithm, in which both errors are monitored during the training, are summarized in {prf:ref}`algorithm:ModelValidation:training-loop`.

```{prf:algorithm} Iterative training with monitoring of training and validation errors
:label: algorithm:ModelValidation:training-loop

1. Split the data into a training set $\data_\mathrm{train}$ and a validation set $\data_\mathrm{val}$.
2. Choose the hyperparameters of the model and of the training algorithm, e.g., the learning rate $\eta$, the momentum parameter $\gamma$, the mini-batch size $N_\mathrm{mb}$ and the number of epochs $N_\mathrm{epochs}$.
3. Initialize the model parameters $\pars$ (for a neural network: all weights $\weights$ and biases) and the velocity $\boldsymbol{v} = \boldsymbol{0}$. The parameters are often initialized randomly.
4. For each epoch $t = 1, \ldots, N_\mathrm{epochs}$:
   1. Shuffle the training data and divide it into mini-batches.
   2. Loop through the mini-batches. For each one: evaluate the gradient of the cost function for the mini-batch and update the parameters, e.g., with momentum gradient descent (see {numref}`sec:MathematicalOptimization:adaptive-gd`).
   3. Evaluate $E_\mathrm{train}$ and $E_\mathrm{val}$, Eq. {eq}`eq:ModelValidation:Etrain-Eval`, with the current parameters and store the results.
5. Plot $E_\mathrm{train}$ and $E_\mathrm{val}$ versus epoch (the learning curve). Keep the parameters from the epoch with the smallest $E_\mathrm{val}$ (known as *early stopping*), or change the hyperparameters and repeat the training.
```

```{code-cell} python3
:tags: [hide-cell]

# (a) Train a degree-14 model with mini-batch gradient descent with momentum
# and store the training and validation errors after each epoch
degree = 14
X_train, X_val = design_matrix(x_train, degree), design_matrix(x_val, degree)
learning_rate, momentum, batch_size, N_epochs = 0.03, 0.9, 10, 5000
rng_lc = np.random.default_rng(0)
theta = np.zeros(degree + 1)     # initial parameters
velocity = np.zeros(degree + 1)
lc_train, lc_val = [], []
for epoch in range(N_epochs):
    idx = rng_lc.permutation(N_train)     # shuffle the training data
    for start in range(0, N_train, batch_size):
        batch = idx[start:start + batch_size]
        # gradient of the MSE cost function for the mini-batch
        gradient = 2 * X_train[batch].T @ (X_train[batch] @ theta - y_train[batch]) / len(batch)
        velocity = momentum * velocity + gradient
        theta = theta - learning_rate * velocity
    lc_train.append(np.mean((X_train @ theta - y_train)**2))
    lc_val.append(np.mean((X_val @ theta - y_val)**2))
epochs = np.arange(1, N_epochs + 1)
i_stop = int(np.argmin(lc_val))    # early stopping

# (b) Errors versus the size of the training set (median over many training sets)
sizes = np.arange(5, 101, 5)
rng_size = np.random.default_rng(2)
x_big_val, y_big_val = generate_data(1000, rng_size)
def size_curve(degree, N_repeat=50):
    Etr, Eva = [], []
    for N in sizes:
        tr, va = [], []
        for _ in range(N_repeat):
            x, y = generate_data(N, rng_size)
            theta = fit(x, y, degree)
            tr.append(mse(theta, x, y))
            va.append(mse(theta, x_big_val, y_big_val))
        Etr.append(np.median(tr))
        Eva.append(np.median(va))
    return np.array(Etr), np.array(Eva)

# Create a visualization
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(11, 4.6))
ax = axs[0]
ax.loglog(epochs, lc_train, color=colors['train'], label=r'$E_\mathrm{train}$')
ax.loglog(epochs, lc_val, color=colors['val'], label=r'$E_\mathrm{val}$')
ax.axhline(sigma_eps**2, ls=':', color='k', label=r'$\sigma_\epsilon^2$')
ax.plot(epochs[i_stop], lc_val[i_stop], 'v', color='k', ms=8, label=f'min $E_\\mathrm{{val}}$ (epoch {epochs[i_stop]})')
ax.set_xlabel('epoch')
ax.set_ylabel('mean-squared error')
ax.set_title(f'(a) degree {degree}, GD with momentum')
ax.legend()
ax = axs[1]
for degree, ls in [(1, '--'), (8, '-')]:
    Etr, Eva = size_curve(degree)
    ax.semilogy(sizes, Etr, ls=ls, color=colors['train'], label=f'$E_\\mathrm{{train}}$, degree {degree}')
    ax.semilogy(sizes, Eva, ls=ls, color=colors['val'], label=f'$E_\\mathrm{{val}}$, degree {degree}')
ax.axhline(sigma_eps**2, ls=':', color='k')
ax.set_ylim(0.01, 10)
ax.text(62, 0.4, 'degree 1: high bias', fontsize=12)
ax.text(45, 0.025, 'degree 8: high variance', fontsize=12)
ax.set_xlabel('size of training set')
ax.set_ylabel('mean-squared error')
ax.set_title('(b) error versus training-set size')
ax.legend(ncol=2)
fig.tight_layout()

glue('ModelValidation_learning_curves_fig', fig, display=False)
plt.close(fig)
glue('ModelValidation_early_stop_epoch', int(epochs[i_stop]), display=False)
```

```{glue:figure} ModelValidation_learning_curves_fig
:name: fig:ModelValidation:learning-curve

Learning curves for the running example. (a) Training and validation errors versus epoch when a degree-14 polynomial model is trained with mini-batch gradient descent with momentum ({prf:ref}`algorithm:ModelValidation:training-loop`). The triangle marks the smallest validation error. (b) Training and validation errors versus the size of the training set for a degree-1 (dashed) and a degree-8 (solid) model. The curves show the median over 50 randomly drawn training sets for each size, and the validation errors are evaluated on a large validation set.
```

Several features in the learning curves shown in {numref}`fig:ModelValidation:learning-curve`(a) deserve to be mentioned:

1. The performance on both training and validation sets is very poor in the beginning of the training.
2. The error on the training set then decreases steadily as more training iterations are performed. 
3. The training error decreases quickly in the beginning, and much more slowly as the model parameters are getting closer to an optimum.
4. The validation error is initially very high but decreases as the model becomes better.
5. The validation error eventually reaches a plateau. If the training proceeds much longer than this, the model can become overfit and the validation error will eventually start increasing.

In panel (a), the validation error is smallest after {glue:text}`ModelValidation_early_stop_epoch` epochs. Stopping the training at this point gives a model that generalizes better than the fully converged one. Early stopping thereby acts as a form of regularization (see {numref}`sec:ModelValidation:regularization`).

For models with a high degree of complexity there will usually be a gap between the curves which implies that the model performs significantly better on the training data than on the validation set. This is a sign of high variance, see the discussion of the *bias-variance tradeoff* below.

The learning curves versus the size of the training set in {numref}`fig:ModelValidation:learning-curve`(b) show two typical patterns:
- *High bias* (degree 1): the training and validation errors quickly approach each other and level out at a value well above $\sigma_\epsilon^2$. Adding more training data does not help. A more flexible model is needed.
- *High variance* (degree 8): for small training sets there is a large gap between the very small training error and the large validation error. The gap closes slowly as the training set grows, and both errors approach $\sigma_\epsilon^2$. Here, more training data (or regularization) does help.

(sec:ModelValidation:bias-variance)=
## The bias-variance tradeoff

We will discuss the bias-variance tradeoff in the context of continuous predictions such as regression. However, many of the intuitions and ideas discussed here also carry over to classification tasks. 

Consider observations that are related to the true data-generating process $f$ via experimental noise. For a specific observation $i$ we can write

\begin{equation}
\output_i = f({\inputs_i}) + {\epsilon}_{i},
\end{equation}

where ${\epsilon}_{i}$ is an irreducible error described by a random variable. That is, even if we could find the data-generating process $f$ we would not reproduce the data more accurately than $\epsilon$ permits. Let us assume that these errors are i.i.d. with expectation value $\expect{\epsilon} = 0$ and variance $\var{\epsilon} = \sigma^2_\epsilon$[^variance]. 
[^variance]: Remember that $\expect{t}$ denotes the expectation value for the random variable $t$. Furthermore, the variance is given by $\var{t} = \expect{\left(t -  \expect{t}\right)^2}$.

Our model $\MLoutput(\inputs)$ is an approximation to the function $f(\inputs)$. We will arrive at the final model after calibration (training) and there is always a risk of either under- or overfitting. Let us now consider the following scenario:
 
- We make a prediction with our trained model at a new point $\testinputs$. We use the shorthand notation $\MLtestoutput \equiv {\MLoutput}(\testinputs)$. 
- This prediction should eventually be compared with a future observation $\testoutput \equiv y(\testinputs) = f(\testinputs)+\epsilon^\odot \equiv f^\odot+\epsilon^\odot$
- Specifically, we are interested in the prediction error, $\testoutput - \MLtestoutput = f^\odot+\epsilon^\odot - \MLtestoutput$, to judge the predictive power of our model.

What can we say about this prediction error? It obviously depends on the inherent noise ($\epsilon$), which is random, but also on the model complexity and how it was calibrated.
Imagine the following repeated model calibrations:

1. Draw a size $n$ sample, $\trainingdata_n = \{(\inputs_j, y_j), j=1\ldots n\}$
   - Train our model ${\MLoutput}$ using $\trainingdata_n$.
   - Make the prediction at $\testinputs$ and evaluate $\testoutput - \MLtestoutput$
2. Repeat this multiple times, using different sets of data $\trainingdata_n$ to fit your model. What is the expectation value $\expect{\left(\testoutput-\MLtestoutput\right)^2}$?

````{prf:theorem} The bias-variance tradeoff
:label: theorem:ModelValidation:bias-variance

Consider a fixed input $\testinputs$ and the prediction $\MLtestoutput$ of a model that has been trained on a randomly drawn training set. The prediction is compared with a future observation $\testoutput = f^\odot + \epsilon^\odot$, where the noise $\epsilon^\odot$ has zero mean and variance $\sigma^2_\epsilon$, and is independent of the training data. The bias-variance tradeoff theorem states that the expected squared prediction error (with the expectation taken over the randomness in both training sets and the noise $\epsilon^\odot$) can be expressed as a sum

$$
\expect{\left(\testoutput-\MLtestoutput\right)^2} = \left(f^\odot-\expect{\MLtestoutput}\right)^2 + \var{ \MLtestoutput} + \sigma^2_\epsilon.
$$ (eq:ModelValidation:bias-variance)

The first of the three terms represents the square of the bias of the machine-learning model, which can be thought of as the error caused by a lack of flexibility (underfitting) that inhibits our model to fully recreate $f$. The second term represents the variance of the model predictions, which can be thought of as its sensitivity to the choice of training data (overfitting). Finally, the last term comes from the irreducible error $\epsilon$ that is inherent in the observations. 
````

````{prf:proof}
There are two sources of randomness: the training set, which makes the prediction $\MLtestoutput$ a random variable, and the noise $\epsilon^\odot$ of the future observation. The true value $f^\odot = f(\testinputs)$ is a fixed number, and so is the expected prediction $\expect{\MLtestoutput}$.

1. *Split the error.* Subtracting and adding $\expect{\MLtestoutput}$, we write the prediction error as a sum of two terms

   $$
   \testoutput - \MLtestoutput = \underbrace{\left( f^\odot - \expect{\MLtestoutput} + \epsilon^\odot \right)}_{a} + \underbrace{\left( \expect{\MLtestoutput} - \MLtestoutput \right)}_{b}.
   $$

   Squaring and using the linearity of expectation values gives

   $$
   \expect{\left(\testoutput-\MLtestoutput\right)^2} = \expect{a^2} + \expect{b^2} + 2\expect{ab}.
   $$

2. *First term.* Since $f^\odot - \expect{\MLtestoutput}$ is a fixed number, we have

   $$\begin{align}
   \expect{a^2} &= \left(f^\odot-\expect{\MLtestoutput}\right)^2 + 2\left(f^\odot-\expect{\MLtestoutput}\right)\expect{\epsilon^\odot} + \expect{(\epsilon^\odot)^2} \\
      &= \left(f^\odot-\expect{\MLtestoutput}\right)^2 + \sigma^2_\epsilon,
   \end{align}$$

   where we used $\expect{\epsilon^\odot} = 0$, which also implies that $\expect{(\epsilon^\odot)^2} = \var{\epsilon^\odot} = \sigma^2_\epsilon$. This term is the squared bias plus the irreducible error.

3. *Second term.* By the definition of the variance,

   $$
   \expect{b^2} = \expect{\left(\MLtestoutput - \expect{\MLtestoutput}\right)^2} = \var{\MLtestoutput}.
   $$

4. *Mixing term.* Splitting $a$ into its fixed and random parts gives

   $$
   \expect{ab} = \left(f^\odot-\expect{\MLtestoutput}\right) \expect{\expect{\MLtestoutput} - \MLtestoutput} + \expect{\epsilon^\odot \left(\expect{\MLtestoutput} - \MLtestoutput\right)}.
   $$

   The first part vanishes since $\expect{\expect{\MLtestoutput} - \MLtestoutput} = \expect{\MLtestoutput} - \expect{\MLtestoutput} = 0$. The second part vanishes because the noise $\epsilon^\odot$ of the future observation is independent of the training data, and therefore of $\MLtestoutput$. The expectation value then factorizes into $\expect{\epsilon^\odot} \expect{\expect{\MLtestoutput} - \MLtestoutput} = 0$.

Adding the three terms gives Eq. {eq}`eq:ModelValidation:bias-variance`.
````


The tradeoff between bias and variance is illustrated in {numref}`fig-bias_variance_resample` and {numref}`fig-bias_variance`. Note the similarity between the expected prediction error in {numref}`fig-bias_variance` and the validation error in {numref}`fig:ModelValidation:validation-curve`. The latter is a noisy estimate of the former, based on a single training set and a single validation set.

```{code-cell} python3
:tags: [hide-cell]

# Train polynomial models on many different training sets and evaluate
# the predictions at fixed test inputs x^\odot
N_resample = 200
rng_bv = np.random.default_rng(3)
x_test = np.linspace(-0.9, 0.9, 19)
bins = np.linspace(-1, 1, N_train + 1)   # one training input drawn in each bin (stratified sampling)
bv_degrees = np.arange(0, 15)
pred_grid = {degree: [] for degree in bv_degrees}
pred_test = {degree: [] for degree in bv_degrees}
for _ in range(N_resample):
    x = rng_bv.uniform(bins[:-1], bins[1:])
    y = f_true(x) + rng_bv.normal(0, sigma_eps, N_train)
    for degree in bv_degrees:
        theta = fit(x, y, degree)
        pred_grid[degree].append(predict(theta, x_grid))
        pred_test[degree].append(predict(theta, x_test))

# Squared bias and variance, averaged over the test inputs
bias2 = np.array([np.mean((f_true(x_test) - np.mean(pred_test[degree], axis=0))**2) for degree in bv_degrees])
variance = np.array([np.mean(np.var(pred_test[degree], axis=0)) for degree in bv_degrees])

# Create a visualization of individual models and their mean
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(12, 4.2), sharey=True)
for ax, degree in zip(axs, (1, 5, 14)):
    preds = np.array(pred_grid[degree])
    for pred in preds[:30]:
        ax.plot(x_grid, pred, color='C0', alpha=0.15, lw=1)
    ax.plot(x_grid, np.mean(preds, axis=0), color='C3', ls='--', lw=2.5, label=r'mean prediction $\mathbb{E}[\hat{y}]$')
    ax.plot(x_grid, f_true(x_grid), ls='-', color='k', lw=1, label='true $f(x)$')
    ax.set_title(f'degree {degree}')
    ax.set_xlabel('$x$')
    ax.set_ylim(-2.5, 2.5)
axs[0].set_ylabel(r'$\hat{y}$')
axs[0].plot([], [], color='C0', alpha=0.4, label='individual models')
axs[0].legend(loc='upper left')
fig.tight_layout()

glue('ModelValidation_bias_variance_resample_fig', fig, display=False)
plt.close(fig)

# Create a visualization of the bias-variance decomposition
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6.5, 4.5))
ax.semilogy(bv_degrees, bias2 + variance + sigma_eps**2, 'o-', color='k', label=r'$\mathbb{E}[(y^\odot - \hat{y}^\odot)^2]$')
ax.semilogy(bv_degrees, bias2, 's--', color='C3', label=r'bias$^2$: $(f^\odot - \mathbb{E}[\hat{y}^\odot])^2$')
ax.semilogy(bv_degrees, variance, '^-.', color='C0', label=r'variance: $\mathrm{Var}[\hat{y}^\odot]$')
ax.axhline(sigma_eps**2, ls=':', color='0.4', label=r'$\sigma_\epsilon^2$')
ax.set_ylim(1e-7, 5)
ax.set_xlabel('polynomial degree')
ax.set_ylabel('mean over test inputs')
ax.legend(loc='lower left')
fig.tight_layout()

glue('ModelValidation_bias_variance_means_fig', fig, display=False)
plt.close(fig)
```

```{glue:figure} ModelValidation_bias_variance_resample_fig
:name: fig-bias_variance_resample

The bias-variance tradeoff illustrated for polynomial models of low (degree 1), intermediate (degree 5) and high (degree 14) complexity. For each degree we have trained the model on 200 different training sets, each with $N_\mathrm{train} = 20$ observations. Thin blue lines show 30 of these models and the thick dashed line shows the mean prediction. The degree-1 models are similar to each other but their mean deviates from the true function $f(x)$ (thin black line). These models have a large bias and small variance. The degree-14 models have a mean close to $f(x)$ but vary a lot between training sets. They have a small bias and large variance.
```

```{glue:figure} ModelValidation_bias_variance_means_fig
:name: fig-bias_variance

The three terms of the bias-variance decomposition, Eq. {eq}`eq:ModelValidation:bias-variance`, versus polynomial degree. The squared bias and the variance are estimated from the 200 training sets of {numref}`fig-bias_variance_resample` and averaged over 19 test inputs $\testinputs \in [-0.9, 0.9]$. The expected squared prediction error is their sum plus the irreducible error $\sigma_\epsilon^2$.
```

### Remarks on bias and variance


The bias-variance tradeoff summarizes the fundamental tension in
machine learning, particularly supervised learning, between the
complexity of a model and the amount of training data needed to train
it.  Since data is often limited, in practice it is often useful to
use a less-complex model with higher bias, that is  a model whose asymptotic
performance is worse than another model because it is easier to
train and less sensitive to sampling noise arising from having a
finite-sized training dataset (smaller variance). In general, more
flexible statistical methods have higher variance.

The above equations tell us that in
order to minimize the expected validation error, we need to select a
statistical learning method that simultaneously achieves low variance
and low bias. Note that variance is inherently a nonnegative quantity,
and squared bias is also nonnegative. Hence, we see that the prediction error can never lie below $\var{\epsilon} \equiv \sigma^2_\epsilon$, the irreducible error.


(sec:ModelValidation:regularization)=
## Regularization: Ridge and Lasso

Let us now consider an approach to reduce the risk of overfitting. Assuming that overfitting is characterized by large fit parameters, we can attempt to avoid this scenario by *regularizing* the model parameters. We will introduce two kinds of regularization: Ridge and Lasso. So called elastic net regularization is also used in the literature and basically corresponds to a linear combination of the Ridge and Lasso penalty functions.

Let us remind ourselves about the expression for the standard Mean Squared Error (MSE) which we used to define our cost function and the equations for the ordinary least squares (OLS) method. That is our optimization problem is

\begin{equation}
\pars^* = \underset{\pars\in {\mathbb{R}}^{N_p}}{\operatorname{argmin}} \frac{1}{N_d}\left\{\left(\data-\dmat\pars\right)^T\left(\data-\dmat\pars\right)\right\}
= \underset{\pars\in {\mathbb{R}}^{N_p}}{\operatorname{argmin}}
\frac{1}{N_d}\vert\vert \data-\dmat\pars\vert\vert_2^2,
\end{equation}

where $N_d$ is the number of training data.

By minimizing the above equation with respect to the parameters
$\pars$ we could then obtain an analytical expression for the
parameters $\pars$.  Let us add a penalty term, with a regularization parameter $\lambda$, to define a new cost function

\begin{equation}
C_{\lambda,2} \left( \pars \right) \equiv
\vert\vert \data-\dmat\pars\vert\vert_2^2+\lambda\vert\vert \pars\vert\vert_2^2 
\end{equation}

(the normalization factor $1/N_d$ of the MSE has been absorbed into $\lambda$). This leads to the *Ridge regression* minimization problem where we
constrain the parameters via $\vert\vert \pars\vert\vert_2^2$ and the optimization equation becomes

\begin{equation}
\pars^* = \underset{\pars\in {\mathbb{R}}^{N_p}}{\operatorname{argmin}}
C_{\lambda,2}\left( \pars \right)
.
\end{equation}

Alternatively, *Lasso regularization* can be performed by defining

\begin{equation}
C_{\lambda,1} \left( \pars \right) \equiv
\vert\vert \data-\dmat\pars\vert\vert_2^2+\lambda\vert\vert \pars\vert\vert_1.
\end{equation}

Here we have defined the norm-1 as 

\begin{equation}
\vert\vert \pars\vert\vert_1 = \sum_i \vert \theta_i\vert. 
\end{equation}

Lasso stands for least absolute shrinkage and selection operator. In contrast to Ridge regression, which makes all parameters smaller but rarely exactly zero, Lasso tends to set some parameters exactly to zero. It therefore also performs a selection of the most relevant basis functions (features).

The effect of Ridge regularization on the running example is shown in {numref}`fig-ridge_reg`. Without regularization ($\lambda = 0$) the degree-14 model is overfitting, while a very large $\lambda$ forces all parameters towards zero and the model underfits. The training error increases monotonically with $\lambda$, while the validation error has a minimum at an intermediate value. The regularization strength $\lambda$ is therefore a hyperparameter that should be determined using a validation set, or with cross-validation as described in {numref}`sec:ModelValidation:cross-validation`.

```{code-cell} python3
:tags: [hide-cell]

# Ridge regression of a degree-14 polynomial model for a range of lambda values
degree_ridge = 14
lambdas = np.logspace(-8, 2, 41)
ridge_thetas = [fit(x_train, y_train, degree_ridge, lam) for lam in lambdas]
R_train = np.array([mse(theta, x_train, y_train) for theta in ridge_thetas])
R_val = np.array([mse(theta, x_val, y_val) for theta in ridge_thetas])
lam_best = lambdas[np.argmin(R_val)]

# Create a visualization
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 4.8))
ax = axs[0]
plot_data(ax)
for lam, color, ls in [(0.0, 'C4', '-.'), (1e-4, 'C2', '--'), (1e-1, 'C3', (0, (1, 1))), (10.0, 'C5', (0, (6, 2, 1, 2, 1, 2)))]:
    theta = fit(x_train, y_train, degree_ridge, lam)
    label = r'$\lambda = 0$' if lam == 0 else f'$\\lambda = 10^{{{int(np.log10(lam))}}}$'
    ax.plot(x_grid, predict(theta, x_grid), color=color, ls=ls, lw=2, label=label)
ax.set_ylim(-2.5, 2.5)
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_title(f'(a) degree-{degree_ridge} model, Ridge penalty')
ax.legend(ncol=2, loc='lower right', fontsize=10)
ax = axs[1]
ax.loglog(lambdas, R_train, color=colors['train'], label=r'$E_\mathrm{train}$')
ax.loglog(lambdas, R_val, color=colors['val'], label=r'$E_\mathrm{val}$')
ax.axhline(sigma_eps**2, ls=':', color='k', label=r'$\sigma_\epsilon^2$')
ax.axvline(lam_best, color='0.7', lw=6, alpha=0.4, zorder=0)
ax.text(1e-7, 0.02, 'overfitting\n(small $\\lambda$)', fontsize=12, color='0.3')
ax.text(1.5e-1, 0.02, 'underfitting\n(large $\\lambda$)', fontsize=12, color='0.3')
ax.set_ylim(0.01, 10)
ax.set_xlabel(r'$\lambda$')
ax.set_ylabel('mean-squared error')
ax.set_title('(b) error versus regularization strength')
ax.legend(loc='upper center')
fig.tight_layout()

glue('ModelValidation_ridge_fig', fig, display=False)
plt.close(fig)
```

```{glue:figure} ModelValidation_ridge_fig
:name: fig-ridge_reg

Ridge regularization of a degree-14 polynomial model of the running example. (a) The model trained with different penalty parameters $\lambda$. (b) Training and validation errors versus $\lambda$. The shaded band marks the $\lambda$ with the smallest validation error.
```

```{code-cell} python3
:tags: [remove-input, web-only]

# Interactive figure (only in the web version of the book)
slider_widget("mv-ridge-widget", "Ridge regularization",
    "Vary the Ridge regularization strength λ of a degree-14 polynomial model. The left panel shows the trained model, and the right panel shows the training and validation errors versus λ.",
    lambdas, [f"λ = {lam:.1e}" for lam in lambdas],
    [predict(theta, x_grid) for theta in ridge_thetas], R_train, R_val,
    [theta_rms(theta) for theta in ridge_thetas], xlabel="λ", logx=True, init=0)
```

### More on Ridge Regression

Using the matrix-vector expression for Ridge regression,

\begin{equation}
C_{\lambda,2}(\pars)=(\data-\dmat\pars)^T(\data-\dmat\pars)+\lambda\pars^T\pars,
\end{equation}

by taking the derivatives with respect to $\pars$ we obtain then
a slightly modified matrix inversion problem which for finite values
of $\lambda$ does not suffer from singularity problems. We obtain

\begin{equation}
\pars^{\mathrm{Ridge}} = \left(\dmat^T\dmat+\lambda\boldsymbol{I}\right)^{-1}\dmat^T\data,
\end{equation}

with $\boldsymbol{I}$ being a $N_p\times N_p$ identity matrix 

We see that Ridge regression is nothing but the standard
OLS with a modified diagonal term added to $\dmat^T\dmat$. The
consequences, in particular for our discussion of the bias-variance
are rather interesting. Increasing $\lambda$ reduces the variance of the model predictions at the price of an increased bias, as seen in {numref}`fig-ridge_reg`. Ridge regression can also be formulated as a constraint on the model parameters

\begin{equation}
\sum_{i=0}^{N_p-1} \theta_i^2 \leq t,
\end{equation}

with $t$ a finite positive number. Minimizing $\vert\vert \data-\dmat\pars\vert\vert_2^2$ subject to this constraint is equivalent to minimizing $C_{\lambda,2}(\pars)$, with a one-to-one correspondence between $t$ and $\lambda$ (as follows from the method of Lagrange multipliers). A larger $\lambda$ corresponds to a smaller $t$.

For more discussions of Ridge and Lasso regression, see: [Wessel van Wieringen's](https://arxiv.org/abs/1509.09169) {cite}`Vanwieringen2015` article or [Mehta et al's](https://arxiv.org/abs/1803.08823) {cite}`Mehta2019` article.

(sec:ModelValidation:cross-validation)=
## Cross-validation

Cross-validation is a strategy to find model hyperparameters that yield a model with good prediction
performance. A common practice is to hold back some subset of the data from the training of the model and then use this holdout set to check the model performance. 

One of these two data sets, called the 
*training set*, plays the role of **original** data on which the model is
built. The second of these data sets, called the *validation set*, plays the
role of the **novel** data and is used to evaluate the prediction
performance (often operationalized as the log-likelihood or the
prediction error: MSE or R2 score) of the model built on the training data set. This
procedure (model building and prediction evaluation on training and
validation set, respectively) is done for a collection of possible choices for the hyperparameters. The hyperparameter value that yields the model with
the best prediction performance is to be preferred. 

The validation set approach is conceptually simple and is easy to implement. But it has two potential drawbacks:

* The validation estimate of the test error rate can be highly variable, depending on precisely which observations are included in the training set and which observations are included in the validation set. There might be data points that are critical for training the model, and the performance metric will be very bad if those happen to be excluded from the training set.
* In the validation approach, only a subset of the observations, those that are included in the training set rather than in the validation set are used to fit the model. Since statistical methods tend to perform worse when trained on fewer observations, this suggests that the validation set error rate may tend to overestimate the test error rate for the model fit on the entire data set.

To reduce the sensitivity on a particular data split, one can perform several different splits. For each split the model is fit using the training data and
evaluated on the corresponding validation set. The hyperparameter that performs best on average (in some sense) is then selected.

To avoid unbalanced influence of important training samples one can use $K$-fold cross-validation to structure the data splitting. The $N_d$ samples are divided into $K$ more or less equally sized, exhaustive and mutually exclusive subsets (folds). At each fold one of these subsets plays the role of the validation set while the union of the remaining subsets constitutes the training set. Such a splitting warrants a balanced representation of each sample in both training and validation set over the splits. Still the division into the $K$ subsets involves a degree of randomness. This may be fully excluded when choosing $K=N_d$. This particular case is referred to as leave-one-out cross-validation (LOOCV). Note that any test set should be held back before the cross-validation is performed.

```{prf:algorithm} $K$-fold cross-validation
:label: algorithm:ModelValidation:cross-validation

1. Define a range of interest for the  model hyperparameter(s) $\boldsymbol{\lambda}$ and create a set $\{ \boldsymbol{\lambda}_m \}_{m=1}^M$ that spans this range. Here, $\boldsymbol{\lambda}$ denotes any hyperparameter(s), e.g., the polynomial degree or the Ridge regularization strength.
2. Divide the data set $\data$ (with $N_d$ data, not including any test set) into $K$ exhaustive and mutually exclusive subsets $\data_{k} \subset \data$ for $k=1,\ldots,K$, with $\data_{k} \cap \data_{l} = \emptyset$ for $k \neq l$.
3. For $m \in \{1, \ldots, M\}$:
   1. For $k \in \{1, \ldots, K\}$:
      - Use $\data_{k}$ as the validation set and all other data $\data_{-k} = \data \setminus \data_k$ as the training set.
      - Train the model with hyperparameter(s) $\boldsymbol{\lambda}_m$ using the training set $\data_{-k}$, which will give a best fit $\pars^*_{-k}(\boldsymbol{\lambda}_m)$.
      - Evaluate the error function for all data in the validation set $\data_k$.
   2. Average the errors over all folds. This is known as the *cross-validated error*

      $$
      \mathrm{CV}_K(\boldsymbol{\lambda}_m) = \frac{1}{N_d} \sum_{k=1}^{K} \sum_{(\inputs_i, \output_i) \in \data_k} E\left( \MLoutput(\inputs_i; \pars^*_{-k}(\boldsymbol{\lambda}_m)), \output_i \right),
      $$

      where $\MLoutput(\inputs_i; \pars^*_{-k}(\boldsymbol{\lambda}_m))$ is the prediction of the model trained without fold $k$. Each datum is used for validation exactly once.
4. The hyperparameter(s) that minimizes the cross-validated error is the best choice. 

   $$
   \boldsymbol{\lambda}^* = \underset{\boldsymbol{\lambda}_m}{\operatorname{argmin}}
    \mathrm{CV}_K(\boldsymbol{\lambda}_m).
   $$
   
5. Fix $\boldsymbol{\lambda} = \boldsymbol{\lambda}^*$ and train the model on all data $\data$.
```

## Exercises

```{exercise} $k=1$ NN training error
:label: exercise:ModelValidation:kNN-training-error

What is $E_\mathrm{train}$ {eq}`eq:ModelValidation:Etrain-Eval` for binary classification using $k$NN with $k=1$? 
```

```{exercise} $k$NN model complexity
:label: exercise:ModelValidation:kNN-model-complexity

Draw a simple figure to illustrate the under-and overfitting regions of a $k$NN model. With model complexity on the $x$-axis, where would you put the extremes $k=1$ and $k=N$ (with $N$ being the number of training data)? In other words, what would be the effective number of parameters in this model?
```

```{exercise} Study of model bias and variance
:label: exercise:ModelValidation:study-model-bias-variance

Perform your own study of the bias-variance tradeoff by revisiting the linear regression problem in [](sec:ols_in_practice). 

- Create one validation set and ten different training sets using different random number generators (`rng` argument) in the `data_generating_process_measurement()` function. 
- Train linear regression models of different polynomial degrees for each training set. Evaluate both the training error and the validation error for each model.
- Plot all ten degree-0 models in a single figure (using the same color for each line, but make them slightly transparent such that they don't block the view) together with the validation data and with the true, underlying model. Plot also the ten degree-5 models in the same figure (in a different color). Now try to understand why the former family can be described as having large bias but small variance, whereas the latter has large variance.

Connect these findings to the concept of predictive power.
```

```{exercise} Implement $K$-fold cross validation
:label: exercise:ModelValidation:kfold-cross-validation

Use either the linear regression example, or the binary classification one, to implement $K$-fold cross validation. Try to use the results to determine an optimal degree of the polynomial for linear regression, or the choice of $k$ for the $k$NN classifier.
```

```{exercise} Large training error
:label: exercise:ModelValidation:large-training-error

- Explain why $E_\mathrm{train}$ is a poor metric for estimating the prediction error.
- Consider the situation when $E_\mathrm{train}$ is larger than the prediction error that you are aiming for. Explain why it then becomes a waste of time to implement cross validation or other techniques to estimate the actual prediction error.
- What could help to reduce the training error?
```

## Solutions to exercises

```{solution} exercise:ModelValidation:kNN-training-error
:label: solution:ModelValidation:kNN-training-error
:class: dropdown

$E_\mathrm{train} = 0$ for $k$NN models with $k=1$.
```

```{solution} exercise:ModelValidation:kNN-model-complexity
:label: solution:ModelValidation:kNN-model-complexity
:class: dropdown

The effective number of parameters in a $k$NN model goes something like $N/k$. Think about how many effective parameters the training data corresponds to in the extreme situations with $k=1$ and $k=N$. In between, you can imagine non-overlapping regions of $k$ sized clusters.

In effect, this implies that the $k=1$ model is the one with the largest number of effective parameters and hence the most complex one (explaining the overfitting), whereas the $k=N$ model has effectively a single parameter and will underfit.
```

```{solution} exercise:ModelValidation:study-model-bias-variance
:label: solution:ModelValidation:study-model-bias-variance
:class: dropdown

You should see small variations between the degree-0 models since they just capture the  means of the respective training sets. However, it also implies that they in average reproduce both training and validation data poorly.

The higher degree models will show much larger variations (since they will be overfitting to the different sets of training data). They will all perform well on their respective training set, but poorly on the validation set. 
```

```{solution} exercise:ModelValidation:kfold-cross-validation
:label: solution:ModelValidation:kfold-cross-validation
:class: dropdown

Note you are interested in the cross-validated error $\mathrm{CV}_K(\lambda)$ (see {prf:ref}`algorithm:ModelValidation:cross-validation`), where the hyperparameter $\lambda$ is the polynomial degree for the linear regression example, or the number of neighbors $k$ for the $k$NN classifier.
```

```{solution} exercise:ModelValidation:large-training-error
:label: solution:ModelValidation:large-training-error
:class: dropdown

- $E_\mathrm{train}$ will always decrease with increasing model complexity as it is tuned to the data (and higher model complexity implies more model flexibility).
- The error on new data, $E_\mathrm{new}$, is in general larger than $E_\mathrm{train}$. This is the generalization gap. So it is better to invest your time in improving the model, or collecting more data, before actually attempting to estimate the prediction error.
- See the above answer.
```

