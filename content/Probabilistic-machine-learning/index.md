(sec:ProbML)=
# Probabilistic machine learning and emulation

In this part we focus on machine learning that 
we define from a Bayesian perspective as methods that provide probability distributions over functions trained on data (defined broadly). 
We can think conceptually of the discussion of machine learning in {ref}`sec:RootML` as applying to *point estimates* while now we will consider *distributions*.

The chapters are:
* {ref}`sec:BNN` (or BNNs) build on a probabilistic interpretation of ANNs.
* {ref}`sec:RootGP` (or GPs) are distributions over functions.
* {ref}`sec:ANNFT` illustrates how a controlled expansion around neural networks in the large-width limit can be formalized (the infinite-width limit of an ANN is a GP!).
* {ref}`sec:Bayesian-optimization` is a strategy to optimize computationally expensive functions using a surrogate (often a GP) for the function of interest.
* {ref}`sec:DimensionalityReductionEmulators` gives an overview of singular value decompositions (SVD), which is a key component of dimensional reduction methods such as principal component analysis (PCA).
It also covers emulators, which are fast & accurate computer models of expensive theoretical simulations.  Bayesian inference often requires a large number of samples of the simulations, e.g., for parameter estimation, which could be prohibitive unless we can use emulators to generate the samples. The particular focus is on reduced basis model (RBM) emulators.
* {ref}`ch:PartVProblems`.
