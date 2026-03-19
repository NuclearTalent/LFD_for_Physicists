(sec:ModelValidation)=
# Model validation

In this lecture we will continue to explore linear regression and we will encounter several concepts that are common for machine learning methods. These concepts are:
  * Model validation
  * Overfitting and underfitting
  * Bias-variance-tradeoff
  * Regularization
  * Model hyperparameters
  
The lecture is based and inspired by material in several good textbooks: in particular chapter 4 in [Hands‑On Machine Learning with Scikit‑Learn and TensorFlow](http://shop.oreilly.com/product/0636920052289.do) {cite}`Geron2017` by Aurelien Geron, chapter 5 in the 
[Python Data Science Handbook](http://shop.oreilly.com/product/0636920034919.do) {cite}`Vanderplas2016` by Jake VanderPlas and chapters 2-4 in [The Elements of
Statistical Learning](https://link.springer.com/book/10.1007/978-0-387-84858-7) {cite}`Hastie2009`} by Trevor Hastie et al.

## Over- and underfitting

Overfitting and underfitting are common problems in data analysis and machine learning. Both extremes are illustrated in {numref}`fig-over_under_fitting`.

```{figure} ./figs/over_under_fitting.png
:name: fig-over_under_fitting

The first-order polynomial model is clearly underfitting the data, while the very high degree model is overfitting it trying to reproduce variations that are clearly noise.
```


The following quote from an unknown source provides a concise definition of overfitting and underfitting:
> A model overfits if it fits noise as much as data and underfits if it considers variability in data to be noise while it is actually not.

The question is then: How do we detect these problems and how can we reduce them.

We can detect over- and underfitting by employing holdout sets, also known as *validation* sets. This means that we only use a fraction of the data for training the model, and save the rest for validation purposes. 

I.e. we optimize the model parameters to best fit the training data, and then measure e.g. the mean-square error (MSE) of the model predictions for the validation set. The function that is used for measuring the performance of the model prediction is called an error function, and is here denoted $E(\MLoutputs, \outputs)$. We stress that this function does not necessarily have to be the same as the cost function that is used for learning. The latter can incorporate other desirable features such as regularization to avoid overfitting (see below), or some domain-specific constraints. The error function, on the other hand, should focus on measuring the property of the prediction that is most important for the application at hand. Default choices for regression and classification tasks, respectively, are

| Task             | Error function  | Measures  |
| :--------------- | :--------------------- | :--------------------- | 
|  Regression      |   $E(\MLoutput, \output) = (\MLoutput - \output)^2 $    | Squared error |
|  Classification  |    $E(\MLoutput, \output) =  1 - \delta_{\MLoutput, \output}$   | Misclassification |

where $1 - \delta_{\MLoutput, \output} = 0$ if $\MLoutput = \output$ (i.e. correct classification) and $= 1$ if $\MLoutput \neq \output$ (misclassified).

Evaluating the error function on either the training set, or the validation set, gives relevant metrics that can be used to monitor under- or overfitting

$$
E_\mathrm{train} &= \frac{1}{N} \sum_{i=1}^N E(\MLoutput(\inputs_i), \output_i), \quad\text{for } (\inputs_i, \output_i) \in \trainingdata \\
E_\mathrm{val} &= \frac{1}{N_\mathrm{val}} \sum_{i=1}^{N_\mathrm{val}} E(\MLoutput(\inputs_i), \output_i), \quad\text{for } (\inputs_i, \output_i) \in \data_\mathrm{val}. 
$$ (eq:ModelValidation:Etrain-Eval)

```{admonition} Training and validation scores
Several training and validation scores are commonly used in machine learning applications.  First we have the **Mean-Squared Error** (MSE)

$$
\mathrm{MSE} = \frac{1}{N} \sum_{i=1}^N \left( \MLoutput(\inputs_i) - \output_i) \right)^2,
$$ (eq:ModelValidation:MSE)

where we have $N$ training data and our model is a function of the parameter vector $\pars$. Note that this is the metric that we are minimizing when solving the normal equation Eq. {eq}`eq:NormalEquation`.

Furthermore, we have the **mean absolute error** (MAE) defined as.

$$
\mathrm{MAE} = \frac{1}{N} \sum_{i=1}^N \left| \MLoutput(\inputs_i) - \output_i) \right|,
$$ (eq:ModelValidation:MAE)

And the $R2$ score, also known as *coefficient of determination* is

$$
\mathrm{R2} = 1 - \frac{\sum_{i=1}^N \left( \MLoutput(\inputs_i) - \output_i) \right)^2}{\sum_{i=1}^N \left( \output_i - \bar{\output} \right)^2},
$$ (eq:ModelValidation:R2)

where $\bar{\output} = \frac{1}{N} \sum_{i=1}^N \output_i$ is the mean of the data. This metric therefore represents the proportion of variance (of $\data$) that has been explained by the independent variables in the model.
  ```

An underfit model has a *high bias*, which means that it gives a rather poor fit and the error function will be rather large in average. This will be true for both the training and the validation sets.

An overfit model will depend sensitively on the choice of training data. A different split into training and validation sets will give very different predictions. We therefore say that the model displays a *high variance*. While the overfit model usually reproduces training data very well (low bias), it does not generalize well and gives a poor reproduction of validation data. The average values for the error function are therefore very different for the training and validation sets. 

Another sign of overfitting is the appearance of very large fit parameters that are needed for the fine tunings of cancellations of different terms in the model. The fits from our example has the following root-mean-square parameters

\begin{equation}
\para_\mathrm{rms} \equiv \frac{1}{p} \sqrt{ \sum_{i=0}^{p-1} \theta_i^2 } \equiv \| \pars \|_2^2 / p.
\end{equation}


| order  | $\para_\mathrm{rms}$  |
| :----- | :--------------------- | 
|    1   |             3.0e-01    |
|    3   |             1.2e+00    |
|  	 100  |             6.3e+12    |


:::{note} 
 In some cases a learning algorithm makes good predictions despite fitting to the noise in training data. This is called "benign overfitting". See, for example, [Bartlett et al., *Benign Overfitting in Linear Regression*](https://arxiv.org/abs/1906.11300). A recent explanation of this is [Chatterji and Long, *Foolish Crowds Support Benign Overfitting*](https://arxiv.org/abs/2110.02914). From their abstract: "Our analysis exposes the benefit of an effect analogous to the 'wisdom of the crowd', except here the harm arising from fitting the *noise* is ameliorated by spreading it among many directions - the variance reduction arises from a *foolish* crowd."
:::

## Regularization: Ridge and Lasso

Assuming that overfitting is characterized by large fit parameters, we can attempt to avoid this scenario by *regularizing* the model parameters. We will introduce two kinds of regularization: Ridge and Lasso. In addition, so called elastic net regularization is also in use and basically corresponds to a linear combination of the Ridge and Lasso penalty functions.

Let us remind ourselves about the expression for the standard Mean Squared Error (MSE) which we used to define our cost function and the equations for the ordinary least squares (OLS) method. That is our optimization problem is

\begin{equation}
\boldsymbol{\theta}^* = \underset{\boldsymbol{\theta}\in {\mathbb{R}}^{p}}{\operatorname{argmin}} \frac{1}{n}\left\{\left(\boldsymbol{y}-\boldsymbol{X}\boldsymbol{	\theta}\right)^T\left(\boldsymbol{y}-\boldsymbol{X}\boldsymbol{\theta}\right)\right\}.
\end{equation}

or we can state it as

\begin{equation}
\boldsymbol{\theta}^* = \underset{\boldsymbol{\theta}\in {\mathbb{R}}^{p}}{\operatorname{argmin}}
\frac{1}{n}\sum_{i=0}^{n-1}\left(y_i-\tilde{y}_i\right)^2
= \underset{\boldsymbol{\theta}\in {\mathbb{R}}^{p}}{\operatorname{argmin}}
\frac{1}{n}\vert\vert \boldsymbol{y}-\boldsymbol{X}\boldsymbol{\theta}\vert\vert_2^2,
\end{equation}

where we have used the definition of  a norm-2 vector, that is

\begin{equation}
\vert\vert \boldsymbol{\epsilon}\vert\vert_2^2 = \sum_i \epsilon_i^2. 
\end{equation}

By minimizing the above equation with respect to the parameters
$\boldsymbol{\theta}$ we could then obtain an analytical expression for the
parameters $\boldsymbol{\theta}$.  We can add a regularization parameter $\lambda$ by
defining a new cost function to be minimized, that is

\begin{equation}
C_{\lambda,2} \left( \pars \right) \equiv
\frac{1}{n}\vert\vert \boldsymbol{y}-\boldsymbol{X}\boldsymbol{\theta}\vert\vert_2^2+\lambda\vert\vert \boldsymbol{\theta}\vert\vert_2^2 
\end{equation}

which leads to the *Ridge regression* minimization problem where we
constrain the parameters via $\vert\vert \boldsymbol{\theta}\vert\vert_2^2$ and the optimization equation becomes

\begin{equation}
\boldsymbol{\theta}^* = \underset{\boldsymbol{\theta}\in {\mathbb{R}}^{p}}{\operatorname{argmin}}
C_{\lambda,2}\left( \boldsymbol{X}, \boldsymbol{\theta} \right)
.
\end{equation}

Alternatively, *Lasso regularization* can be performed by defining

\begin{equation}
C_{\lambda,1} \left( \boldsymbol{\theta} \right) \equiv
\frac{1}{n}\vert\vert \boldsymbol{y}-\boldsymbol{X}\boldsymbol{\theta}\vert\vert_2^2+\lambda\vert\vert \boldsymbol{\theta}\vert\vert_1.
\end{equation}

Here we have defined the norm-1 as 

\begin{equation}
\vert\vert \boldsymbol{\epsilon}\vert\vert_1 = \sum_i \vert \epsilon_i\vert. 
\end{equation}

Lasso stands for least absolute shrinkage and selection operator.

```{figure} ./figs/ridge_reg.png
:name: fig-ridge_reg

Ridge regularization with different penalty parameters $\lambda$ for different polynomial models of a noisy data set. 
```


### More on Ridge Regression

Using the matrix-vector expression for Ridge regression,

\begin{equation}
C(\boldsymbol{X},\boldsymbol{\theta})=\frac{1}{n}\left\{(\boldsymbol{y}-\boldsymbol{X}\boldsymbol{\theta})^T(\boldsymbol{y}-\boldsymbol{X}\boldsymbol{\theta})\right\}+\lambda\boldsymbol{\theta}^T\boldsymbol{\theta},
\end{equation}

by taking the derivatives with respect to $\boldsymbol{\theta}$ we obtain then
a slightly modified matrix inversion problem which for finite values
of $\lambda$ does not suffer from singularity problems. We obtain

\begin{equation}
\boldsymbol{\theta}^{\mathrm{Ridge}} = \left(\boldsymbol{X}^T\boldsymbol{X}+\lambda\boldsymbol{I}\right)^{-1}\boldsymbol{X}^T\boldsymbol{y},
\end{equation}

with $\boldsymbol{I}$ being a $p\times p$ identity matrix 

We see that Ridge regression is nothing but the standard
OLS with a modified diagonal term added to $\boldsymbol{X}^T\boldsymbol{X}$. The
consequences, in particular for our discussion of the bias-variance
are rather interesting. Ridge regression imposes a constraint on the model parameters

\begin{equation}
\sum_{i=0}^{p-1} \theta_i^2 \leq t,
\end{equation}

with $t$ a finite positive number. 

For more discussions of Ridge and Lasso regression, see: [Wessel van Wieringen's](https://arxiv.org/abs/1509.09169) {cite}`Vanwieringen2015` article or [Mehta et al's](https://arxiv.org/abs/1803.08823) {cite}`Mehta2019` article.

## The bias-variance tradeoff

We will discuss the bias-variance tradeoff in the context of continuous predictions such as regression. However, many of the intuitions and ideas discussed here also carry over to classification tasks. 

Consider observations that are related to the true data-generating process $f$ via experimental noise. For a specific observation $i$ we can write

\begin{equation}
\output_i = f({\inputs_i}) + {\epsilon}_{i},
\end{equation}

where ${\epsilon}_{i}$ is an irreducible error described by a random variable. That is, even if we could find the deta-generating process $f$ we would not reproduce the data more accurately than $\epsilon$ permits. Let us assume that these errors are i.i.d. with expectation value $\expect{\epsilon} = 0$ and variance $\var{\epsilon} = \sigma^2_\epsilon$[^variance]. 
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

The expected prediction error of a machine-learning model can be expressed as a sum

$$
\expect{\left(\testoutput-\MLtestoutput\right)^2} = \left(f^\odot-\expect{\MLtestoutput}\right)^2 + \var{ \MLtestoutput} + \sigma^2_\epsilon.
$$ (eq:ModelValidation:bias-variance)

The first of the three terms represents the square of the bias of the machine-learning model, which can be thought of as the error caused by a lack of flexibility (underfitting) that inhibits our model to fully recreate $f$. The second term represents the variance of the model predictions, which can be thought of as its sensitivity to the choice of training data (overfitting). Finally, the last term comes from the irreducible error $\epsilon$ that is inherent in the observations. 
````

````{prf:proof}
To derive the {prf:ref}`bias-variance-tradeoff <theorem:ModelValidation:bias-variance>`, we start from

\begin{equation}
\testoutput = f^\odot+\epsilon^\odot
\end{equation}

and realize that the variances of $\testoutput$ and $\epsilon^\odot$ are both equal to $\sigma^2_\epsilon$, since the data-generating process $f^\odot = f(\testinputs)$ is deterministic. The mean value of $\epsilon^\odot$ is equal to zero which means that $\expect{\testoutput} = f^\odot$. The desired expectation value 

\begin{equation}
\expect{\left(\testoutput-\MLtestoutput\right)^2} = \expect{\left(f^\odot+\epsilon^\odot-\MLtestoutput\right)^2},
\end{equation}

can be rewritten by subtracting and adding $\expect{\MLtestoutput}$ 

\begin{equation}
\expect{\left(\testoutput-\MLtestoutput)^2}=\expect{(f^\odot + \epsilon^\odot - \expect{\MLtestoutput} + \expect{\MLtestoutput}-\MLtestoutput\right)^2}.
\end{equation}

Using the linearity of expectation values we can rewrite this expression as a sum of three terms:
* The first one is 

  \begin{align}
  \expect{\left(f^\odot-\expect{\MLtestoutput}+\epsilon^\odot\right)^2} &= \expect{\left(f^\odot-\expect{\MLtestoutput}\right)^2} + \expect{{\epsilon^\odot}^2} \\
  & \qquad + 2 \left(f^\odot-\expect{\MLtestoutput}\right)\expect{\epsilon} \\
  &= \left(f^\odot-\expect{\MLtestoutput}\right)^2 + \sigma_\epsilon^2
  \end{align}
  
  where we use the known expectation values, plus the fact that the model bias $f^\odot-\expect{\MLtestoutput}$ is a fixed number. Thus, this term becomes the (squared) model bias plus the irreducible data error $\sigma_\epsilon^2$

* The second term is 

  \begin{equation}
  \expect{\left(\expect{\MLtestoutput} - \MLtestoutput\right)^2} = \var{\MLtestoutput}.
  \end{equation}
  
  It corresponds to the variance of model predictions.

* The last (mixing) term is zero

  \begin{align}
  & 2\expect{\left(\testoutput-\expect{\MLtestoutput}\right) \left(\expect{\MLtestoutput}-\MLtestoutput\right)} \\
  & \quad = 2\expect{\left(\testoutput-\expect{\MLtestoutput}\right)} \left( \expect{\expect{\MLtestoutput}} -  \expect{\MLtestoutput}\right) = 0.
  \end{align}
  
In summary, we have obtained the three terms of Eq. {eq}`eq:ModelValidation:bias-variance` which concludes the proof.
````


The tradeoff between bias and variance is illustrated in {numref}`fig-bias_variance_resample` and {numref}`fig-bias_variance`.

```{figure} ./figs/bias_variance_100resamples.png
:name: fig-bias_variance_resample

The bias-variance tradeoff illustrated for different polynomial models from low- to high-complexity. For each model complexity (degree) we have trained several versions of the machine-learning model using resampled training data. For each test datum (blue dots) we show the different model predictions. Underfit models have large average errors (bias) while overfit ones have large prediction variance.
```

```{figure} ./figs/bias_variance_means.png
:name: fig-bias_variance

The bias-variance tradeoff illustrated for different polynomial models of our noisy data set. The squared errors for each degree represent the mean results of the test data.
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
and squared bias is also nonnegative. Hence, we see that the prediction error can never lie below $\var{\epsilon}) \equiv \sigma^2_\epsilon$, the irreducible error.


## Model validation

In order to make an informed choice for these hyperparameters we need to validate that our model provides a good fit to the training data while not becoming overfit. This important process is known as *model validation*. It most often involves splitting the data into two sets: the training set and the validation set. 

The model is then trained on the first set of data, while its performance is monitored on the validation set (by computing your choice of performance score/error function).

```{caution} 
Why is it important not to train and evaluate the model on the same data?
```

### Learning curves

The performance of the model will depend on the amount of data that is used for training. When using iterative optimization approaches, such as gradient descent, it will also depend on the number of training iterations. In order to monitor this dependence one usually plots a *learning curve*.

Learning curves are plots of the model performance on both the training and the validation sets, measured by some performance metric such as the mean squared error. This measure is plotted as a function of the size of the training set, or alternatively as a function of the number of training iterations. One defines an *epoch* of training as an update of the model parameters where the entire batch of training data has been used exactly once. An epoch can therefore consist of multiple updates via a random traverse of all training data one by one, or split into mini-batches.

```{figure} ./figs/learning-curve-epochs.png
:name: fig:ModelValidation:learning-curve
:width: 400px
:align: center

Learning curve for a machine-learning model. The average mean-squared error for the model evaluated on training data and on validation data are shown as a function of the number of training epochs.
```

Several features in the learning curves shown in {numref}`fig:ModelValidation:learning-curve` deserve to be mentioned:

1. The performance on both training and validation sets is very poor in the beginning of the training.
2. The error on the training set then decreases steadily as more training iterations are performed. 
3. The training error decreases quickly in th ebeginning, and much more slowly as the model parameters are becoming optimized.
4. The validation error is initially very high but decreases as the model becomes better.
5. The validation error eventually reaches a plateau. If the training proceeds much longer than this, the model can become overfit and the validation error will eventually start increasing.

For models with a high degree of complexity there will usually be a gap between the curves which implies that the model performs significantly better on the training data than on the validation set. This demonstrates the *bias-variance tradeoff*.

### Cross-validation

Cross-validation is a strategy to find model hyperparameters that yield a model with good prediction
performance. A common practice is to hold back some subset of the data from the training of the model and then use this holdout set to check the model performance. 

One of these two data sets, called the 
*training set*, plays the role of **original** data on which the model is
built. The second of these data sets, called the *validation set*, plays the
role of the **novel** data and is used to evaluate the prediction
performance (often operationalized as the log-likelihood or the
prediction error: MSE or R2 score) of the model built on the training data set. This
procedure (model building and prediction evaluation on training and
validation set, respectively) is done for a collection of possible choices for the hyperparameters. The parameter that yields the model with
the best prediction performance is to be preferred. 

The validation set approach is conceptually simple and is easy to implement. But it has two potential drawbacks:

* The validation estimate of the validation error rate can be highly variable, depending on precisely which observations are included in the training set and which observations are included in the validation set. There might be data points that are critical for training the model, and the performance metric will be very bad if those happen to be excluded from the training set.
* In the validation approach, only a subset of the observations, those that are included in the training set rather than in the validation set are used to fit the model. Since statistical methods tend to perform worse when trained on fewer observations, this suggests that the validation set error rate may tend to overestimate the validation error rate for the model fit on the entire data set.

To reduce the sensitivity on a particular data split, one can use perform several different splits. For each split the model is fit using the training data and
evaluated on the corresponding validation set. The hyperparameter that performs best on average (in some sense) is then selected.

To avoid unbalanced influence of important training samples one can use $k$-fold cross-validation to structure the data splitting. The samples are divided into $k$ more or less equally sized, exhaustive and mutually exclusive subsets. At each fold one of these subsets plays the role of the validation set while the union of the remaining subsets constitutes the training set. Such a splitting warrants a balanced representation of each sample in both training and validation set over the splits. Still the division into the $k$ subsets involves a degree of randomness. This may be fully excluded when choosing $k=n$. This particular case is referred to as leave-one-out cross-validation (LOOCV). 

```{prf:algorithm} k-fold cross-validation
:label: algorithm:ModelValidation:cross-validation

1. Define a range of interest for the  model hyperparameter(s) $\boldsymbol{\lambda}$ and create a set $\{ \boldsymbol{\lambda}_m \}_{m=1}^M$ that spans this range.
2. Divide the training data set $\data$ into $k$ exhaustive and mutually exclusive subsets $\data_{i} \subset \data$ for $i=1,\ldots,k$, and $\data_{i} \cap \data_{j} = \emptyset$ for $i \neq j$.
3. For $m \in \{1, \ldots, M\}$:
   1. For $i \in \{1, \ldots, k\}$:
      - Use $\data_{i}$ as the validation set and all other data $\data_{-i} = \left( \data \cap \data_i\right)^c$ as the training set.
      - Train the model with hyperparameter(s) $\boldsymbol{\lambda}_m$ using the training set $\data_{-i}$, which will give a best fit $\pars^*_{i}(\boldsymbol{\lambda}_m)$.
      - Evaluate the prediction performance with $\pars^*_{i}(\boldsymbol{\lambda}_m)$.
   2. Average the prediction performances on all folds. This is known as the *cross-validated error* $\mathrm{CV}_k(\boldsymbol{\lambda}_m)$. 
4. The hyperparameter(s) that minimizes the cross-validated error is the best choice. 

   $$
   \boldsymbol{\lambda}^* = \underset{\boldsymbol{\lambda}}{\operatorname{argmin}}
    \mathrm{CV}_k(\boldsymbol{\lambda}).
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

- Create one validation set and ten different training sets using different seeds in the `data_generating_process()` method call within the `measurement()` method. 
- Train linear regression models of different polynomial degrees for each training set. Evaluate both the training error and the validation error for each model.
- Plot all ten degree-0 models in a single figure (using the same color for each line, but make them slightly transparent such that they don't block the view) together with the validation data and with the true, underlying model. Plot also the ten degree-5 models in the same figure (in a different color). Now try to understand why the former family can be described as having large bias but small variance, whereas the latter has large variance.

Connect these findings to the concept of predictive power.
```

```{exercise} Implement $k$-fold cross validation
:label: exercise:ModelValidation:kfold-cross-validation

Use either the linear regression example, or the binary classification one, to implement $k$-fold cross validation. Try to use the results to determine an optimal degree of the polynomial for linear regression, or the choice of $k$ for the $k$NN classifier.
```

```{exercise} Large training error
:label: exercise:ModelValidation:large-training-error

- Explain why $E_\mathrm{train}$ is a poor metric for estimating the prediction error.
- Consider the situation when $E_\mathrm{train}$ is larger than the prediction error that you are aiming for. Explain why it then becomes a waste of time to implement cross vaiidation or other techniques to estimate the actual prediction error.
- What could help to reduce the training error?
```

## Solutions

```{solution} exercise:ModelValidation:kNN-training-error
:label: solution:ModelValidation:kNN-training-error
:class: dropdown

$E_\mathrm{train} = 0$ for $k$NN models with $k=1$.
```

```{solution} exercise:ModelValidation:kNN-model-complexity
:label: solution:ModelValidation:kNN-model-complexity
:class: dropdown

The effective number of parameters in a $k$NN model goes something like $N/k$. Think about how many effective parameters the training data corresponds to in the extreme situations with $k=1$ and $k=N$. In between, you can imagine non-overlapping regions of $k$ sized clusters.

In effect, this implies that the $k=1$ model is the one with the largest number of effective parameters and hence the most comples one (explaining the overfitting), whereas the $k=N$ model has effectively a single parameter and will underfit.
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

Note you are interested in $\mathrm{CV}_k(\lambda)$ where the hyperparameter is $\lambda=p$ for the linear regression example, or $\lambda=k$ for the $k$NN classifier.
```

```{solution} exercise:ModelValidation:large-training-error
:label: solution:ModelValidation:large-training-error
:class: dropdown

- $E_\mathrm{train}$ will always decrease with increasing model complexity as it is tuned to the data (and higher model complexity implies more model flexibility).
- $E_\mathrm{new} > E_\mathrm{train}$ in general. This is the generalization gap. So it is better to invest your time in improving the model, or collecting more data, before actually attempting to estimate the prediction error.
- See the above answer.
```

