# Iterative history matching

In these lectures we will introduce a very powerful, iterative approach known as history matching {cite}`Vernon:2010,Vernon:2014,Vernon:2018,Hu:2021trw`. The power of this method lies in the iterative confrontation of a computational model with a set of (historical) data within the Bayes linear framework. Its applicability rests on the ability to solve the model with small computational cost at low fidelities, e.g. using emulators (see {ref}`sec:BayesFast`).

Let us start with the statistical model {eq}`eq:DataModelsPredictions:mismatch`, which we repeat below, that relates data with model predictions via random quantities that describe uncertainties in data and model, respectively

$$
\data = M(\pars) + \delta \data + \delta M.
$$

This relation, and our specification of probability distributions for the random quantities, usually leads to the data likelihood $\pdf{\data}{\pars, I}$ that enters our Bayesian analysis. Here, however, we recognize the risk of arbitrariness when making such assignments. Instead, we rely on Bayes linear statistics and just specify the expectation values and covariances.

To be specific, let us consider a single observable $Z_i$ with the corresponding model prediction $M_i(\pars)$. With $\expect{\delta Z_i} = \expect{\delta M_i} = 0$ and independent data and model uncertainties---$\var{\delta Z_i} = \sigma_{Z,i}^2$ and  $\var{\delta M_i} = \sigma_{M,i}^2$, respectively---we would have

\begin{align}
\expect{Z_i} &= M_i(\pars), \\
\var{Z_i} &= \sigma_{Z,i}^2 + \sigma_{M,i}^2.
\end{align}

The aim of history matching is to identify the set $\mathcal{Q}(\mathcal{z})$ of parameterizations $\pars$, for which the evaluation of a model $M(\pars)$ yields an acceptable---or at least not implausible---match to a set of observations $\mathcal{z}$. The set $Q$ will then translate into a non-implausible volume in the multi-dimensional parameter space. Let us stress that $\mathcal{Z}$ is the set of observables while $\mathcal{z} = \{ z_1, z_2, \ldots z_M \}$ is the actual set of (numerical) observations. 

History matching has been employed in various studies involving complex computer models
ranging from effects of climate modeling to systems biology, epidemiology, and nuclear physics.

We introduce the individual implausibility measure

$$
  I_i^2(\pars) = \frac{|{M}_i(\pars) - z_i|^2}{\var{\delta Z_i + \delta M_i}},
$$ (eq:BayesLinear:IMi)

which is a function over the input parameter space and quantifies the (mis-)match between our model output ${M}_i(\pars)$ and the observation $z_i$ for an observable in the target set $\mathcal{Z}$. Note that we can employ emulation of our model as long as we quantify the expected precision of our emulator (in terms of a variance) and include that in the total variance of the denominator.

A common choice is to employ a maximum implausibility measure to make the distinction between implausible and non-implausible parameter samples. Specifically, we consider a particular value for $\pars$ as implausible if

$$
  I_M(\pars) \equiv \max_{z_i \in \mathcal{z}} I_i(\pars) > c_I.
$$ (eq:BayesLinear:IM)

We can choose $c_I \equiv 3.0$, appealing to Pukelheim's three-sigma rule {cite}`Pukelsheim:1994`, or we can use other cutoff values depending on scientific need. An alternative approach is to consider the second or third highest implausibility values, denoted $I_{2M}$ and $I_{3M}$ respectively, ensuring that errors in uncertainty variance estimates do not lead to unfairly labeling parameter samples as implausible.

In accordance with the assumptions leading to {eq}`eq:DataModelsPredictions:mismatch`, the variance in the denominator of {eq}`eq:BayesLinear:IMi` is a sum of independent squared errors. Generalizations of these assumptions are straightforward if additional information on error covariances or possible inaccuracies in our error model would become available.

An important strength of the history matching is that we can proceed iteratively, excluding regions of input space by imposing cutoffs on
implausibility measures that can include *additional* observables $Z_i$ and corresponding model outputs $M_i$ with possibly refined emulators as the parameter volume is reduced. The history matching process is designed to be independent of the order in which observables are included. This is an important feature as it allows for efficient choices regarding such orderings.

The iterative history matching proceeds in waves according to a straightforward
strategy that can be summarized as follows:

```{prf:algorithm} The history-matching algorithm
:label: algorithm:BayesLinear:History-Matching

1. At wave $j$: Evaluate a set of model runs over the current NI volume $\mathcal{Q}_j$ using a space-filling design of sample values for the parameter inputs $\pars$. Choose a rejection strategy based on implausibility measures for a set $\mathcal{Z}_j$ of informative observables.
2. Construct or refine emulators for the model predictions across $\mathcal{Q}_j$.
3. The implausibility measures are then calculated over $\mathcal{Q}_j$ using the emulators, and implausibility cutoffs are imposed. This defines a new, smaller non-implausible volume $\mathcal{Q}_{j+1}$ which should satisfy $\mathcal{Q}_{j+1} \subset \mathcal{Q}_{j}$.
4. Unless (a) computational resources are exhausted, or (b) all considered points in the parameter space are deemed implausible, we may include additional informative observables in the considered set $\mathcal{Z}_{j+1}$, and return to step 1.
5. If 4(a) is true we generate a number of acceptable runs from the final non-implausible volume $\mathcal{Q}_\mathrm{final}$, sampled according to scientific need.
```

The strength of the history-matching scheme lies within its ability to achieve an iterative volume reduction. It is the removal of implausible regions that is the main goal. There are several ways in which that non-implausible volume may continue to shrink in subsequent waves:

- The emulator is often refined as we reduce the parameter volume. Thereby, the variance in the denominator of {eq}`eq:BayesLinear:IMi` will decrease and the resolving power of the implausibility metric will increase.
- The density of samples will increase as we reduce the parameter volume which allows to better identify the non-implausible volume. Furthermore, a larger density of samples allows to employ additional confirmation of non-implausible volumes from optical depths (which indicate the density of non-implausible samples; see Eqs. (25) and (26) in
{cite}`Vernon:2018`). 
- Additional observables may be introduced in later waves. The parameter space is then further constrained by model predictions for these new observables.
- One or more parameters can be set as *inactive* during early waves and then become activated as new observables are being introduced. There might be situations where the modeling output is independent of certain parameters, or it could be that the output is just not very sensitive to certain parameter variations. The modeling or emulation can then be performed without these parameters with an additional uncertainty that reflects the missing sensitivity. This is a well known emulation procedure called inactive parameter identification {cite}`Vernon:2010`. 
- The mapping of non-implausible samples to a non-implausible volume might be more sophisticated in later waves. The easiest mapping is from the non-implausible range found for each individual parameter to a hyperrectangle. This mapping allows a very strainghtforward space-filling design in the next wave. However, we would completely ignore possible correlation structures. A better approach is then to identify rotated hyperrectangles, or ellipsoids, that encompass the non-implausible samples. See for example Ref. {cite}`May:2022`.

## What next?

The non-implausible samples do not offer a straightforward probabilistic interpretation. The author would just be comfortable with the following weak statement

$$
\cprob{\pars \notin Q(\mathcal{z})}{\mathcal{Z}, M, I} \leq \text{implausible},
$$

where $I$ contains all definitions of implausibility that have been employed through the analysis. What then are they good for?

The following is a (possible incomplete) list of possible uses of a history-matching analysis

1. The non-implausible samples summarise the parameter region of interest, and can directly aid insight regarding interdependencies between parameters induced by the match to observed data. This region is also where we would expect the bulk of the posterior distribution to reside. 
1. Consequently, the non-implausible samples offer good starting points for a subsequent Bayesian analysis (assuming that we dare to make fully probabilistic statements concerning unknown quantities). The convergence of MCMC sampling will be much faster if it is initialized in the region of highest probability mass.
1. Furthermore, the efficient search of large, high-dimensional volumes can aid in identifying multiple regions of interest. The non-implausible samples do not necessarily reside in a single, connected domain but might represent multiple modes of a probability distribution.
1. Implausible regions will correspond to small likelihood densities. The history-matching procedure is therefore well suited to be combined with [Sampling/Importance Resampling](sec:AdvancedMCMC:SIR), see also Ref. {cite}`Jiang:2022off`.
