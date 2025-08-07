---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(sec:OverviewModeling)=
# Overview of modeling

```{epigraph}
> "All models are wrong, but some are useful."

-- George Box, in *Robustness in Statistics* (1979)
```

(sec:OverviewModeling:notation)=
## Notation

{{ sub_OverviewModeling_notation }}

## Models in science

In general, modeling deals with the description of **dependent** variable(s) $\outputs$ as a function of some **independent** variable(s) $\inputs$. The first variable is also often called the **response**, or the **outcome** variable while the second one can be called the **predictor** variable, or the **explanatory** variable. Both dependent and independent variables can be of various types: real-valued, integers or categorical, defined on infinite or discrete domains, etc. Note also that each of these might be a vector of variables, meaning that there could be more than one dependent variable and more than one independent variable. We therefore denoted these variables as vectors using a bold font. The general act of finding a relationship between dependent and independent variables is known as *regression analysis* and usually involves a set of collected data.

```{prf:definition} Regression analysis
:label: definition:OverviewModeling:regression-analysis

Regression analysis is the process of estimating a relationship between one or more dependent variables and one or more independent variables.

[Merriam-Webster](https://www.merriam-webster.com/dictionary/regression): 
*"A functional relationship between two or more correlated variables that is often empirically determined from data and is used especially to predict values of one variable when given values of the others.*

**History**: The earliest form of regression was the method of least squares, which was published by Legendre in 1805 and by Gauss in 1809. Legendre and Gauss both applied the method to the problem of using astronomical observations for determining the orbits of bodies (mostly comets) about the Sun.

The term "regression" was coined by Francis Galton in the 19th century to describe a biological phenomenon. The phenomenon was that the heights of descendants of tall ancestors tend to regress down towards a normal average (a phenomenon also known as regression toward the mean).
```

For simplicity in this chapter we limit ourselves to the case where both input ($\inputt$) and output ($\output$) are univariate (one input and one output) and real-valued such that

$$
\output \approx \model{\pars}{\inputt}.
$$ (eq:OverviewModeling:modeling-simple)

As indicated in this relation, a model will typically include some model parameters ($\pars$). These might already be known, or they might need to be inferred from a set of model calibration data $\data$. A large fraction of our discussions will revolve around the task of determining model parameters. We might refer to this endeavour as *model calibration* or *parameter estimation*. It is an example of a *scientific inference* problem. 

Unfortunately, model calibration is a challenging task that is often performed with a lack of scientific rigour. In future chapters we will explore both the *optimization approach*---which is very common and is absolutely dominating in the construction of machine-learning models---and the scientifically more relevant process of *statistical inference*. For the latter we will in particular use *Bayesian methods*. The Bayesian perspective is very useful as it allows a more formal definition of the process of learning that we can apply also in general machine-learning contexts.

```{prf:definition} Statistical inference
:label: definition:OverviewModeling:statistical-inference

Statistical inference is the quantitative process used for drawing conclusions about the nature of some system on the basis of data and models subject to random variation. Probability is the quantitative metric used to measure the strength of statistical inference.

[Merriam-Webster](https://www.merriam-webster.com/dictionary/inference): 
*"The act of passing from one proposition, statement, or judgment considered as true to another whose truth is believed to follow from that of the former."* (this definition is for the root term "inference")
```

Note that Eq. {eq}`eq:OverviewModeling:modeling-simple` indicates an approximate relationship. Scientific modeling usually relies on a number of approximations. The model should therefore not be expected to provide an exact representation of reality. The missing piece can be referred to as the *model discrepancy*. In addition, reality is observed via experiments that are associated with *experimental errors*. The proper way of handling these uncertainties is via random variables and associated probability distributions. We address this approach in the **Bayesian inference** part, in particular starting from {ref}`sec:DataModelsPredictions`. 

We will mainly consider *deterministic models* that uniquely maps inputs to outputs. Despite the fact that statistical inference relies on stochastic modelling of error terms, the form of the model $\model{\pars}{\inputt}$ is still a deterministic one. However, some processes are better described by *stochastic models*. We will make some acquaintance with this kind of modeling in the **Stochastic processes** part.

## Parametric versus non-parametric models

Most scientific models contain parameters and are therefore known as *parametric models*. In physics these parameters might be constrained by theoretical hypotheses and by previous observations of related systems. Moreover, the parameters values might be interesting by themselves which broadens the scope of modeling from just describing a relationship to actually extracting physics knowledge. 

We should not underestimate the power of physics insights when creating a model. Such insights help in making informed decisions on relevant modeling approximations, which in turn helps in quantifying the size of model discrepancies. In fact, one could claim that true predictive power rests in the ability to make reliable statements on the precision (uncertainty) of a prediction.

It is also possible to learn a relationship without having detailed modeling insights. For this purpose one can consider very general models characterized by large flexibility (allowing to model different relationships) and set up a learning algorithm that adjusts the model to fit a specific purpose. This approach could in general be labeled as machine learning and has proven to be very powerful in many different contexts. Very often, the learning process is performed with a large amount of labeled training data but it might also be possible to achieve without such "supervision". The machine-learning models and learning algorithms usually involve various kinds of parameters, but since these are not meaningful in themselves we can refer to the models as *non-parametric*. We will encounter this approach in the **Machine learning** part of these lecture notes.

## Linear versus non-linear models

In **linear modeling** the dependence on the model parameters $\pars$ is **linear**. As we will see in {numref}`sec:LinearModels`: {ref}`sec:LinearModels` this implies that we can utilize rather straightforward linear algebra methods to perform linear regression analysis.

Linear models are not always applicable. When the parameter dependence is more complicated we will have to use the much broader family of **non-linear modeling**. In general it will be more computationally demanding to deal with non-linear regression analysis.

```{prf:example} Linear models
:label: example:OverviewModeling:linear-models

This is an example of a linear model 

$$
\model{\pars}{\inputt} = \para_0 + \para_1 \inputt + \para_2 \inputt^2.
$$

Note that the parameters $\pars$ enter linearly although the dependence on $\inputt$ (which is the independent variable) is quadratic.

Here is a second example that corresponds to a truncated trigonometric series

$$
\model{\pars}{\inputt} = A_0 + \sum_{n=1}^N A_n \sin(n\inputt) + B_n \cos(n\inputt),
$$ 

where the model parameters $\pars = \{ A_0, A_1, \ldots, A_N, B_1, \ldots, B_N\}$ again enter linearly.
```

```{prf:example} Non-linear models
:label: example:OverviewModeling:nonlinear-models

This is an example of a non-linear model

$$
\model{\pars}{\inputt} = \para_0 + \para_1 \exp( - \para_2 \inputt),
$$

with three parameters.
```


## Regression analysis: optimization versus inference

Assuming that we have access to $N_d$ instances of data corresponding to measured responses $\{ \output_1, \output_2, \ldots \output_{N_d} \}$ and the corresponding values for the independent variable $\{ \inputt_1, \inputt_2, \ldots \inputt_{N_d} \}$. Let us define a *cost function* $C(\pars)$ that quantifies how well our model $\model{\pars}{\inputt}$ reproduces the training data,

\begin{equation}
C(\pars) = \sum_{i=1}^{N_d} \frac{(\output_i - \model{\pars}{\inputt_i})^2}{\sigma_i^2},
\end{equation}

where we have introduced some scaling parameters $\{ \sigma_i \}_{i=1}^{N_d}$ to produce 
a dimensionless value. Let us stress that the choice of cost function is by no means unique and we will offer both pragmatic and statistical perspectives on this later on.

The most common approach to regression analysis is to *optimize* the model parameters. The goal is then to find

$$
\pars^* = \mathop{\mathrm{arg} \min}_{\pars\in \mathbb{R}^p} \, C(\pars).
$$ (eq:OverviewModeling:Optimization)

We note that this task is an optimization problem that can become challenging when the model is non-linear and the parameter dimension $p$ is large. We will discuss gradient-descent-based optimization methods in {numref}`sec:MathematicalOptimization`: {ref}`sec:MathematicalOptimization`.

The optimization approach to regression will provide limited information on the model precision. It is also prone to overfitting and other issues of high-dimensional parameter volumes. In the **Bayesian inference** part we will therefore formulate regression as an inductive inference problem, with rigorous handling of uncertainties. See in particular {numref}`sec:BayesianLinearRegression`: {ref}`sec:BayesianLinearRegression`.

## Exercises

```{exercise} Independent and dependent
:label: exercise:OverviewModeling:independent-dependent

Consider a free-falling body with mass $m$. Neglecting a drag force it is straight-forward to use Newton's equation to derive an expression for the distance $d$ that the body has fallen during a time $t$ when starting from rest at $t=0$. Identify the dependent and the independent variable in this relation. What is the model parameter(s)?
```

```{exercise} Linear or non-linear
:label: exercise:OverviewModeling:linear-nonlinear

Consider the relation between fall time $t$ and velocity $v$ for a free-falling body of mass $m$ (starting from rest) that experiences a drag force that is modeled as $bv$

$$
v = v_T \left( 1 - e^{-\frac{b}{m}t}\right),
$$

where $v_T$ is the terminal velocity. 

- What are the model parameters?
- Is this a linear or a non-linear model?
- How would the relation look like if the drag force was neglected? Would that be a linear or a non-linear model? 
```

```{exercise} Linear or non-linear; more examples
:label: exercise:OverviewModeling:linear-nonlinear-examples

Are these models linear or non-linear?

1. $\model{\pars}{\inputt} = \para_0 + (\para_1 \inputt)^2$
2. $\model{\pars}{\inputt} = e^{\para_0 - \para_1\inputt/2}$
3. $\model{\pars}{\inputt} = \para_0 e^{-\inputt/2}$
4. $\model{\pars}{\inputt} = \para_0 e^{-\inputt/2} + \para_1 \sin(\inputt^2\pi)$
5. $\model{\pars}{\inputt} = (\para_0 + \para_1 \inputt)^2$
6. $\model{\pars}{\inputt} = (\para_0 + \para_1 \inputt)^2 + \para_2\inputt$
```

```{exercise} Model discrepancy
:label: exercise:OverviewModeling:model-discrepancy

Consider again the relation between fall time $t$ and velocity $v$ for a free-falling body of mass $m$ (starting from rest) that experiences a drag force that is modeled as $bv$

$$
v = v_T \left( 1 - e^{-\frac{b}{m}t}\right),
$$

where $v_T$ is the terminal velocity. Discuss possible model discrepancies. Are they expected to be large or small effects?
```

## Solutions

```{solution} exercise:OverviewModeling:independent-dependent
:label: solution:OverviewModeling:independent-dependent
:class: dropdown

The relation is $d = g t^2/2$. Here we are describing how the distance traveled depends on the time of the free fall. Therefore $d$ is the dependent variable and $t$ is the independent one. There is a single model parameter $g$ that we could infer from observational data.
```

```{solution} exercise:OverviewModeling:linear-nonlinear
:label: solution:OverviewModeling:linear-nonlinear
:class: dropdown

- The model parameters are $v_T$ and $b/m$. Alternatively, since $v_T = mg/b$, we could conisder $g$ and $b/m$ as the model parameters. It would not be correct to claim that we have three model parameters since $b$ and $m$ only appear in a ratio.
- This is a non-linear model since $b/m$ appears in an exponential.
- The corresponding relation without drag force is $v = gt$. That is a linear model.
```

```{solution} exercise:OverviewModeling:linear-nonlinear-examples
:label: solution:OverviewModeling:linear-nonlinear-examples
:class: dropdown

1. Linear (we can consider $\para_1^2$ as a parameter).
2. Non-linear.
3. Linear (there is no parameter-dependence in the exponential function).
4. Linear.
5. Non-linear. It would be tempting to consider $\para_0^2$, $\para_1^2$, and $2\para_0 \para_1$ as three independent parameters in which case it would be a linear model. But these are not independent and we would need to keep the quadratic parameter dependence.
6. Linear if we consider $\para_0^2$, $\para_1^2$, and $2\para_0 \para_1 + \para_2$ as parameters. 
```

```{solution} exercise:OverviewModeling:model-discrepancy
:label: solution:OverviewModeling:model-discrepancy
:class: dropdown

First, we are assuming that the gravitational force is constant for the duration of the fall. This approximation corresponds to setting $GM/(R+h)^2 \approx GM / R^2 = g$ where $G$ is the gravitational constant, $M$($R$) is the earth mass(radius), and we neglect the small and varying height $h$. The error that is made here will be of order $(h/R)^2$ which is really small.

More importantly, the linear drag force is a simplification. We could add a term that is quadratic in the velocity. The error made by not including this term will grow with velocity.

Finally, Newton's equations of motion has turned out to be an approximation of the general theory of relativity. Again, the modeling error will be negligible for "normal" masses and velocities.
```


