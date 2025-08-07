(sec:OtherTopics)=
# Overview of other topics

In this part we collect additional material that does not fit directly into previous categories and may be considered unessential in an introductory treatment of Bayesian statistics and machine learning.
The chapters are:

* {ref}`sec:Emulators`, which are fast & accurate computer models of expensive theoretical simulations.  Bayesian inference often requires a large number of samples of the simulations, e.g., for parameter estimation, which could be prohibitive unless we can use emulators to generate the samples.
* [Student t distributions](./Student_t_distribution_from_Gaussians.ipynb) arise in the context of multiple measurements of experimental quantity but also in theory when we have an unknown variance (e.g., in parameter estimation). This notebook shows how in the latter context marginalizing over the variance turns Gaussian distributions into Student t distributions. 
* {ref}`sec:PCAandSVD` gives an overview of singular value decompositions (SVD), which is a key component of dimensional reduction methods such as principal component analysis (PCA).
* {ref}`sec:QBism` is an interpretation of quantum mechanics based on the Bayesian principle that probabilities are contingent on the state of knowledge of observers.
