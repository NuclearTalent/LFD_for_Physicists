# Linear versus non-linear models

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


