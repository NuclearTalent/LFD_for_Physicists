# Exercises

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

## Solutions to exercises

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



