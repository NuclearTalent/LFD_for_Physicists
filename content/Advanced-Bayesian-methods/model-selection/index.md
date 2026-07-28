---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---
(sec:ModelSelection)=
# Model Selection
<!-- !split -->
So far, we have been concerned with the problem of parameter estimation. In studying the linear relationship between two quantities, for example, we discussed how to infer the slope and the offset of the associated straight-line model. Often, however, there is a question as to whether another functional form (such as quadratic or cubic) might be a more appropriate model. In this lecture, we will consider the broad class of scientific problems when there is uncertainty as to which one of a set of alternative models is most suitable. In the Bayesian terminology these can be labeled as **Model Selection** problems and we will discuss them in some depth.


:::{note}
Good references for model selection are Sivia, chapter 4 {cite}`Sivia2006`, [*Bayesian Model Selection and Model Averaging*](https://www.sciencedirect.com/science/article/pii/S0022249699912786) by Wasserman, and chapter 7 of BDA3 {cite}`gelman2013bayesian`.
:::

<!-- !split -->
One of the main objectives in science is that of inferring the truth of one or more hypotheses about how some aspect of nature works. Because we are always in a state of incomplete information, we can never prove any hypothesis (theory) is true.


<!-- !split -->
We will start, however, in {numref}`sec:FrequentistHypothesisTesting` with a brief discussion on sampling theory and the frequentist approach to **hypothesis testing**. This will involve the introduction of the $P$-value or significance measure&mdash;quantities that are often misinterpreted even by scientists themselves. See, for example, the following comment published in Nature (March 20, 2019): [Scientists rise up against statistical significance](https://www.nature.com/articles/d41586-019-00857-9).

In {ref}`sec:BayesianModelSelection` we provide a gentle introduction through the story of Dr. A and Prof. B and then in {ref}`sec:evidence-ratios-expansion` we step through the prototypical problem of different orders of an expansion, for which model selection can be analyzed analytically. Methods for {ref}`sec:EvidenceCalculations` are next and we finish by surveying {ref}`sec:InformationCriteria`, which are computationally light approximations to the evidence.

There are also several problems in {ref}`ch:PartIIProblems` that apply and supplement the presentation in this chapter. See [](../problems-advanced-bayesian-methods/problem-model-selection-basics.ipynb), [](../problems-advanced-bayesian-methods/problem-evidence-calculation-for-eft-expansions.ipynb), and [](../problems-advanced-bayesian-methods/problem-model-selection-how-many-lines-ptemcee.ipynb).

