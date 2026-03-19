# Models in science

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

