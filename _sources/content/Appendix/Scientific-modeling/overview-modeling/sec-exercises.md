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

