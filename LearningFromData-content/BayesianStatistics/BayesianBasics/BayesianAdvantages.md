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

(sec:BayesianAdvantages)=
# Advantages of the Bayesian approach

```{epigraph}
> “Bayesian inference probabilities are a measure of our state of knowledge about nature, not a measure of nature itself."

-- Devinderjit Sivia 
```

The Bayesian approach offers a number of distinct advantages in scientific applications. Some of them are listed below. In this chapter we introduce in particular the important tasks of inference with parametric models and the propagation of errors. 

```{admonition} How the Bayesian approach helps in science
1. Provides an elegantly simple and rational approach for answering any scientific question for a given state of information. The procedure is well-defined:
   * Clearly state your question and prior information.
   * Apply the sum and product rules. The starting point is always Bayes’ theorem.
2. Provides a way of eliminating nuisance parameters through marginalization. 
   * For some problems, the marginalization can be performed analytically, permitting certain calculations to become computationally tractable.
3. Provides a well-defined procedure for propagating errors,
   * E.g., incorporating the effects of systematic errors arising from both the measurement operation and theoretical model predictions.
4. Incorporates relevant prior (e.g., known signal model or known theory model expansion) information through Bayes’ theorem. 
   * This is one of the great strengths of Bayesian analysis.
   * Enforces explicit assumptions.
   * For data with a small signal-to-noise ratio, a Bayesian analysis can frequently yield many orders of magnitude improvement in model parameter estimation, through the incorporation of relevant prior information about the signal model.
5. For some problems, a Bayesian analysis may simply lead to a familiar statistic. Even in this situation it often provides a powerful new insight concerning the interpretation of the statistic.
6. Provides a more powerful way of assessing competing theories at the forefront of science by automatically quantifying Occam’s razor. 
   * The evidence for two hypotheses or models, $M_i$ and $M_j$, can be compared in light of data $\data$ by evaluating the ratio $p(M_i|\data, I) / (M_j|\data, I)$.
   * The Bayesian quantitative Occam’s razor can also save a lot of time that might otherwise be spent chasing noise artifacts that masquerade as possible detections of real phenomena.
```


````{admonition} Occam's razor
:class: tip
Occam’s razor is a principle attributed to the medieval philosopher William of Occam (or Ockham). The principle states that one should not make more assumptions than the minimum needed. It underlies all scientific modeling and theory building. It cautions us to choose from a set of otherwise equivalent models of a given phenomenon the simplest one. In any given model, Occam’s razor helps us to "shave off" those variables that are not really needed to explain the phenomenon. It was previously thought to be only a qualitative principle.

```{figure} ./figs/Leprechaun_or_Clurichaun.png
:height: 250px
:name: fig-Leprechaun

Did the Leprechaun drink your wine, or is there a simpler explanation?
```
````

## Inference with parametric models

Inductive inference with parametric models is a very important tool in the natural sciences.
* Consider $N$ different models $M_i$ ($i = 1, \ldots, N$), each with a parameter vector $\pars_i$. The number of parameters (length of $\pars_i$) might be different for different models. Each of them implies a sampling distribution for possible data

\begin{equation}
p(\data|{\pars}_i, M_i)
\end{equation}

* The likelihood function is the pdf of the actual, observed data ($\data_\mathrm{obs}$) given a set of parameters $\boldsymbol{\theta}_i$:

\begin{equation}
{\mathcal{L}}_i (\pars_i) \equiv p(\data_\mathrm{obs}|\pars_i, M_i)
\end{equation}
* We may be uncertain about $M_i$ (model uncertainty),
* or uncertain about $\pars_i$ (parameter uncertainty).


```{Admonition} Parameter Estimation:
  :class: tip
  Premise: We have chosen a model (say $M_1$)
  
  $\Rightarrow$ What can we say about its parameters $\boldsymbol{\theta}_1$?
  ```
```{Admonition} Model comparison:
  :class: tip
  Premise: We have a set of different models $\{M_i\}$
  
  $\Rightarrow$ How do they compare with each other? Do we have evidence to say that, e.g. $M_1$, is better than $M_2$?
  ```
```{Admonition} Model checking:
  :class: tip
  Premise: We have a model $M_1$
  
  $\Rightarrow$ Is $M_1$ adequate?
  ```
```{Admonition} Hybrid Uncertainty:
  :class: tip
  Premise: Models share some common parameters: $\pars_i = \{ \boldsymbol{\varphi}, {\boldsymbol{\eta}}_i\}$
  
  $\Rightarrow$ What can we say about $\boldsymbol{\varphi}$? (Systematic error is an example)
```
  
Further discussion on parameter estimation and scientific model predictions will appear in subsequent chapters. 

```{figure} ./figs/m1m2.png
:name: fig-m1m2
:width: 400px
:align: center

Joint pdf for the masses of two black holes merging obtained from the data analysis of a gravitational wave signal. This representation of a joint pdf is known as a corner plot. 
```



