# Definition of linear models

In **linear modeling** the dependence on the model parameters $\pars$ is **linear**, and this fact will make it possible to express that regression analysis as a linear algebra problem, and as we will show it will be possible to find an analytical expression for the optimal set of model parameters. Note that we will mostly operate with models depending on more than one parameter. Hence, we denote the parameters ($\pars$) using a bold symbol. In this chapter we will, however, consider models ($\modeloutput$) that relate a single dependent variable ($\output$) with a single independent one ($\inputt$).

The linear parameter dependence implies that our model separates into a sum of parameters times basis functions. Assuming $N_p$ different basis functions we have

$$
\model{\pars}{\inputt} = \sum_{j=0}^{N_p-1} \para_j f_j(\inputt).
$$ (eq_linear_model)

Note that there is no $\pars$-dependence in the basis functions $f_j(\inputt)$.

From a machine-learning perspective the different basis functions are known as **features**.

```{prf:example} Polynomial basis functions
:label: example:polynomial-linear-model

A common linear model corresponds to the use of polynomial basis functions $f_j(x) = x^j$. A polynomial model of degree $N_p-1$ would then be written

$$
M(\pars;\inputt) = \sum_{j=0}^{N_p-1} \para_j \inputt^j.
$$ (eq_polynomial_basis)

Note that the $j=0$ basis function is $f_0(x) = x^0 = 1$ such that the $\para_0$ parameter becomes the intercept.
```

```{prf:example} Liquid-drop model for nuclear binding energies
:label: example:LinearModels:liquid-drop-model

The liquid drop model is useful for a phenomenological description of nuclear binding energies (BE) as a function of the mass number $A$ and the number of protons $Z$, neutrons $N$

\begin{equation}
\text{BE}(A,N,Z) = a_0+a_1A+a_2A^{2/3}+a_3 Z^2 A^{-1/3}+a_4 (N-Z)^2 A^{-1}.
\end{equation}

We have five features: the intercept (constant term, bias), the $A$ dependent volume term, the $A^{2/3}$ surface term and the Coulomb $Z^2 A^{-1/3}$ and pairing $(N-Z)^2 A^{-1}$ terms. Although the features are somewhat complicated functions of the independent variables $A,N,Z$, we note that the $p=5$ regression parameters $\pars = (a_0, a_1, a_2, a_3, a_4)$ enter linearly. 
```

