---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:OptimizationDeepLearning)=
# Optimization and Deep learning

Logistic regression will also serve as our stepping stone towards
neural network algorithms and supervised deep learning. For logistic
learning, the minimization of the cost function leads to an 
optimization problem that is non-linear in the parameters $\boldsymbol{w}$. This optimization (how to find reliable minima of a multi-variable function) is a key challenge for all machine learning algorithms. This leads us back to the
family of gradient descent methods encountered in the chapter on {ref}`sec:MathematicalOptimization`. These methods are the working horses
of basically all modern machine learning algorithms.

We note also that many of the topics discussed here on logistic 
regression are also commonly used in modern supervised deep learning
models, as we will see later.

## Basics and notation

We consider the case where the dependent variables (also called the
responses, targets, or outcomes) are discrete and only take values
from $k=1, \dots, K$ (i.e. $K$ classes).

The goal is to predict the
output classes from the design matrix $\boldsymbol{X}\in\mathbb{R}^{n\times p}$
made of $n$ samples, each of which carries $p$ features or predictors. The
primary goal is to identify the classes to which new unseen samples
belong.

```{admonition} Notation
We will use the following notation:
* $\boldsymbol{x}$: independent (input) variables, typically a vector of length $p$. A matrix of $N$ instances of input vectors is denoted $\boldsymbol{X}$, and is also known as the *design matrix*. The input for machine-learning applications are often referred to as *features*.
* $t$: dependent, response variable, also known as the target. For binary classification the target $t^{(i)} \in \{0,1\}$. For $K$ different classes we would have $t^{(i)} \in \{1, 2, \ldots, K\}$. A vector of $N$ targets from $N$ instances of data is denoted $\boldsymbol{t}$.
* $\mathcal{D}$: is the data, where $\mathcal{D}^{(i)} = \{ (\boldsymbol{x}^{(i)}, t^{(i)} ) \}$.
* $\boldsymbol{y}$: is the output of our classifier that will be used to quantify probabilities $p_{t=C}$ that the target belongs to class $C$.
* $\boldsymbol{w}$: will be the parameters (weights) of our classification model.
```

