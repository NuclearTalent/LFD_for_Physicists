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
We will start, however, with a brief discussion on sampling theory and the frequentist approach to **hypothesis testing**. This will involve the introduction of the $P$-value or significance measure&mdash;quantities that are often misinterpreted even by scientists themselves. See, for example, the following comment published in Nature (March 20, 2019): [Scientists rise up against statistical significance](https://www.nature.com/articles/d41586-019-00857-9).
