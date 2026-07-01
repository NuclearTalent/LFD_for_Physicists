---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(demo:BiasVarianceTradeoff)=
# The bias-variance trade-off

In the first three sections we'll use a fixed linear regression example to illustrate overfitting and underfitting, the bias-variance trade-off, and ridge regression. (See {numref}`sec:ModelValidation` for more details on these concepts.)
Then in the final section you can play with a widget to explore all three!

## Overfitting and underfitting 

Let us consider some data generated from a cubic polynomial plus some random (Gaussian) noise. These are the blue dots in the figure below (error bars not shown). 
We apply linear regression with three models: polynomials of order 1, order 3, and order 50.

```{code-cell}
:tags: [hide-input]
# Common imports
import numpy as np
import os

# To plot pretty figures
%matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt
# Set the base font size for all elements to 16 (default is usually 10)
plt.rcParams.update({'font.size': 16})


# Let us generate some data from a cubic model with noise
m = 100
minX = -3
maxX = 3
np.random.seed(1)
x = (maxX-minX) * np.random.rand(m, 1) + minX
# up to cubic features, plus random noise
theta_true = np.array([2, 1, 0.5, -0.25])
eps_noise = 1.
y = eps_noise * np.random.randn(m, 1)
for order in range(len(theta_true)):
    y += theta_true[order] * x**order

# For these fits we will employ scaling of the data
# We use the built-in StandardScaler to rescale the data to zero mean and unit variance.
# This will make the fit more stable
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

x_new=np.linspace(minX, maxX, 100).reshape(100, 1)

fig,ax = plt.subplots(1,1,figsize=(10,6))

for style, degree in (("g-", 50), ("b--", 3), ("r-.", 1)):
    polybig_features = PolynomialFeatures(degree=degree, include_bias=False)
    std_scaler = StandardScaler()
    lin_reg = LinearRegression()
    # Here we use a Pipeline that assembles several steps that we
    # also could have applied sequentially:
    # 1. The design matrix is created with the chosen polynomial features.
    # 2. The data is transformed to mean=0 and variance=1 
    #    (usually makes it numerically more stable)
    # 3. Perform the linear regression fit
    polynomial_regression = Pipeline([
            ("poly_features", polybig_features),
            ("std_scaler", std_scaler),
            ("lin_reg", lin_reg),
        ])
    polynomial_regression.fit(x, y)
    y_newbig = polynomial_regression.predict(x_new)
    ax.plot(x_new, y_newbig, style, label=f'{degree:>3}')
    print(f'order {degree:>3}: rms parameter size = ',\
          f'{np.linalg.norm(lin_reg.coef_,ord=None)/order:3.1e}')


ax.plot(x, y, "b.")
ax.legend(loc="best")
ax.set_xlabel("$x$")
ax.set_ylim([-10,20])
ax.set_ylabel("$y$");

```

Observations:
* Note how the high-degree polynomial produces a very wiggly curve that tries very hard to go through the training data. The model explodes near the edges where there is no more training data. This is *overfitting*. A symptom of overfitting is that the size of the fit parameters can get very large.
* The first degree polynomial, in contrast, fails to pick up some trends in the data that are clearly there (despite the noise). This is *underfitting*. The model is not complex enough.

A concise definition of overfitting and underfitting (source unknown):
> A model overfits if it fits noise as much as data and underfits if it considers variability in data to be noise while it is actually not.



## Bias-variance trade-off

An underfit model has a *high bias*, which means that it gives a rather poor fit and the error (as a function of $x$ here) will be rather large in average. 
An overfit model will depend sensitively on the data used for the fit. A different set of (random) data will give very different predictions if the model is overfit. We therefore say that the model displays a *high variance*. While the overfit model usually reproduces training data very well (low bias), it does not generalize well and gives a poor reproduction of new data points. 


```{code-cell}
:tags: [hide-input]

from sklearn.model_selection import train_test_split
from sklearn.utils import resample

np.random.seed(2019)

n_boostraps = 100
maxdegree = 14

error = np.zeros(maxdegree)
bias = np.zeros(maxdegree)
variance = np.zeros(maxdegree)
polydegree = range(maxdegree)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

for degree in range(maxdegree):
    polybig_features = PolynomialFeatures(degree=degree)
    lin_reg = LinearRegression()
    polynomial_regression = Pipeline([
            ("poly_features", polybig_features),
            ("lin_reg", lin_reg),
        ])

    y_pred = np.empty((y_test.shape[0], n_boostraps))
    for i in range(n_boostraps):
        x_, y_ = resample(x_train, y_train)
        # Evaluate the new model on the same test data each time.
        y_pred[:, i] = polynomial_regression.fit(x_, y_).predict(x_test).ravel()

    # Note: Expectations and variances taken w.r.t. different training
    # data sets, hence the axis=1. Subsequent means are taken across the test data
    # set in order to obtain a total value, but before this we have error/bias/variance
    # calculated per data point in the test set.
    # Note 2: The use of keepdims=True is important in the calculation of bias as this 
    # maintains the column vector form. Dropping this yields very unexpected results.
    error[degree] = np.mean( np.mean((y_test - y_pred)**2, axis=1, keepdims=True) )
    bias[degree] = np.mean( (y_test - np.mean(y_pred, axis=1, keepdims=True))**2 )
    variance[degree] = np.mean( np.var(y_pred, axis=1, keepdims=True) )

fig,ax = plt.subplots(1,1,figsize=(10,6))

ax.plot(polydegree, error, label='Error')
ax.plot(polydegree, bias, label='Bias')
ax.plot(polydegree, variance, label='Variance')
ax.legend(loc="best")
ax.set_xlabel("degree")
ax.set_ylabel("Bias-Variance");

```

## Ridge regression

Generally overfitting is characterized by large fit parameters, so we can attempt to avoid overfitting by *regularizing* the model parameters. Ridge regression assigns a penalty function that discourages overly large parameters. 
Larger $\lambda$ in the figures below means a larger penalty.
See {numref}`sec:ModelValidation` for further details.


```{code-cell}
:tags: [hide-input]

from sklearn.linear_model import Ridge

def train_ridge_model(x_train, y_train, alpha, x_predict=None, degree=1, **model_kargs):
    model = Ridge(alpha, **model_kargs) if alpha > 0 else LinearRegression()
    model = Pipeline([
        ("poly_features", PolynomialFeatures(degree=degree, include_bias=False)),
        ("std_scaler", StandardScaler()),
        ("regul_reg", model),
        ])
    model.fit(x_train, y_train)
    if not len(x_predict):
        x_predict=x_train
    return model.predict(x_predict)

fig,axs = plt.subplots(1,2,figsize=(10,6))

lambdas=(0, 1,10, 100)
for i,degree in enumerate((1,6)):
    ax = axs[i]
    for lam, style in zip(lambdas, ("b-", "k:", "g--", "r-.")):
        y_new_regul = train_ridge_model(x, y, lam, x_predict=x_new, \
                                        degree=degree, random_state=42)
        ax.plot(x_new, y_new_regul, style, label=f'$\lambda={lam}$')
    ax.plot(x, y, "b.")
    ax.legend(loc="upper left")
    ax.set_xlabel("$x_1$")
    ax.set_title(f'Ridge regularization; order: {degree}')
    #ax.axis([0, 3, 0, 4])

axs[0].set_ylabel("$y$");    

```

## Widget time!

This interactive widget illustrates one of the central ideas in statistical learning: the bias–variance trade-off. It combines repeated Monte Carlo simulations with polynomial regression to show how increasing model complexity affects prediction error.

The widget has two complementary panels:
* The upper panel shows how the expected prediction error changes with model complexity (here the complexity is the degree of the polynomial). The plotted curves are estimated from repeated simulations.
Throughout, $f(x)$ denotes the true function generating the data, while 
$\hat f(x)$ denotes the function estimated from a single noisy training set. Repeating the experiment produces a different estimate, whose variability gives rise to the bias–variance decomposition.
    *  The blue curve shows the squared bias,  

       $$
          \text{bias}^2(x) = \Bigl(\mathbb{E}[\hat f(x)] - f(x)\Bigr)^2  
       $$

       averaged over the independently generated noisy training sets. The bias measures the systematic error caused by an insufficiently flexible model; it usually decreases as model complexity increases.

    *  The red curve shows the variance of $\hat f(x)$, again averaged over the training sets. Variance measures how much the fitted model changes when a different noisy training set is observed. Variance usually increases with complexity.
    *  The green curve is  

       $$
          \text{Bias}^2 + \text{Variance} + \sigma^2_{\text{noise}},  
       $$

       which approximates the expected test mean-squared error. Its minimum identifies the best compromise between underfitting and overfitting.
    * The blue shaded region indicates the underfitting side of the optimum;
      red shading indicates the overfitting side. The boundaries move as the simulation parameters change.
    * The dashed vertical line indicates the polynomial degree with the smallest estimated prediction error. Changing sample size, observational noise, regularization or underlying function may cause this optimum to move.


* The lower panel illustrates the statistical origin of bias and variance. It explains why those changes occur by displaying many fitted models obtained from different noisy training sets (a representative subset of all Repetitions is shown).
The bias–variance calculations themselves continue to use all Monte Carlo repetitions.
    * Each thin light blue curve is the polynomial obtained from one independently generated noisy training set. The spread of these curves is the visual manifestation of variance.

    * The thick blue curve is the average prediction, $\mathbb{E}[\hat f(x)]$, 
computed over all simulated training sets. Its deviation from the true function represents the bias.

    * The thick black curve is the true underlying function from which the synthetic data are generated.

    * The red points are one representative noisy training set. They illustrate the data that one individual fit is attempting to explain.



**Widget user interface features**:
   * Click the three-horizontal-line-icon at top to expand widget display;
   * select the true underlying function using the pulldown;
   * data sliders select: no. of noisy training points for each simulated data set (**samples**); noise level $\sigma$ for the random samples; 
   * the Repetitions slider determines how many independent training sets are generated.
      Each repetition samples a new noisy data set, fits every polynomial degree, then predicts the function on a dense grid. These repeated simulations are averaged to estimate bias,
      variance, and expected prediction error. Increasing the number of repetitions produces smoother and more stable estimates. 
   * sliders to select settings for the Bias-variance graph: maximum degree displayed; log, linear, or normalized y-scale; the "selected degree" for which the bias, variance, and total error is displayed;
   * other sliders for true and fitted functions in lower graph: selected degree of the fitted polynomial; toggle bottom graph on and off (**show fitted models**);
   * size of ridge regression parameter $\lambda$ (larger means more regularization);
   * press **Resample simulation** to generate new samples.



```{raw} html
<iframe src="../../../_static/bias_variance_refactored_larger_lower_panel_widget.html"
    width="100%"
    height="900"
    style="border: none;"
    scrolling="no">
</iframe>
```

::::{admonition} What happens when you increase the number of sampled training points?
:class: my-checkpoint
Increasing the number of samples generally . . .
:::{admonition} Answer 
:class: dropdown, my-answer
* decreases the variance,
* shifts the optimal model complexity toward larger values,
* improves predictive accuracy.
:::
::::

::::{admonition} What happens when you increase the noise level of each sample?
:class: my-checkpoint
Larger observational noise will . . .
:::{admonition} Answer 
:class: dropdown, my-answer
* increase the variance,
* increase the irreducible error,
* favor simpler models (here that means smaller order polynomials).
:::
::::

::::{admonition} The ridge slider controls the regularization parameter $\lambda$.
:class: my-checkpoint
Increasing ridge regularization will . . .
:::{admonition} Answer 
:class: dropdown, my-answer
* suppress large polynomial coefficients,
* reduce variance,
* increase bias,
* often improve prediction when high-degree polynomials are used (try it!).
:::
::::




