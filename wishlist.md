# Wish list for new or upgraded content in LFD Jupyter book
This list is not intended to include (at present) topics that are already explored in enough detail in one but not the other content folders. However, some content may have been missed. Please add relevant pointers below.

Please add comments or additional suggestions.

## Greater detail on formulating statistical models
* Explicit examples and start early on (the statistical model leading to $\chi^2$ fitting for sure, but include other less familiar examples.) Integrate into applications throughout.
* We have some discussion in BUQEYE LFD in [Lecture 5](https://buqeye.github.io/LearningFromData/content/Parameter_estimation/lecture_05.html), but need more substantial background and examples beyond the simplest case.
* The [Stan web pages](https://mc-stan.org/) may be a good source of guidelines and examples. However, we should convert examples to physics contexts.
* Connect to using PyMC; see the [Introductory Overview of PyMC](https://www.pymc.io/projects/docs/en/latest/learn/core_notebooks/pymc_overview.html) for some basic examples. Some of this is in the BUQEYE LFD content in [Lecture 18](https://buqeye.github.io/LearningFromData/content/MCMC_sampling_II/lecture_18.html) but not presented in detail in the language and notation of formulating statistical models that we've learned from our statistician friends.
* We need to identify good statistics references for this (what is in BDA3?).

## More explicit detail and examples on Bayesian statistics workflow
* We have little explicit discussion in BUQEYE LFD (although developing a workflow is promised).
* Include the *Checklist for statistically sound Bayesian analysis* (suitably upgraded):
    * Incorporate all sources of experimental and theoretical errors
    * Formulate statistical models for uncertainties 
    * Use as informative priors as is reasonable; test sensitivity to priors 
    * Account for correlations in inputs (type x) and observables (type y)
    * Properly propagate uncertainties through the calculation 
    * Use model checking to validate our models 
    * Interact with the experts (i.e., statisticians, applied mathematicians)
* [BDA3](http://www.stat.columbia.edu/~gelman/book/BDA3.pdf) three steps (section 1.1):
    1. "Setting up a full probability model—a joint probability distribution for all observable and
unobservable quantities in a problem. The model should be consistent with knowledge
about the underlying scientific problem and the data collection process."
    2. "Conditioning on observed data: calculating and interpreting the appropriate posterior
distribution—the conditional probability distribution of the unobserved quantities of ul-
timate interest, given the observed data."
    3. "Evaluating the fit of the model and the implications of the resulting posterior distribution:
how well does the model fit the data, are the substantive conclusions reasonable, and
how sensitive are the results to the modeling assumptions in step 1? In response, one
can alter or expand the model and repeat the three steps."
* [*Bayesian workflow*](https://arxiv.org/abs/2011.01808) by Gelman et al. (arXiv:2011.01808).

## KOH and BOH discrepancy models
* KOH = Kennedy and O'Hagan, [*Bayesian calibration of computer models*](https://rss.onlinelibrary.wiley.com/doi/abs/10.1111/1467-9868.00294)
* BOH = Brynjarsdóttir and OʼHagan, [*Learning about physical parameters: the importance of model discrepancy*](https://iopscience.iop.org/article/10.1088/0266-5611/30/11/114007). This content is particularly important for students to learn about.
* These works provide good context for statistical models to be used (including relevant examples).
* Sunil Jaiswal (BAND postdoc at OSU) has a nice Jupyter notebook illustrating with the Ball Drop Experiment how the BOH approach works for robust extraction of physical quantities from a calibration. In the example one seeks a value for $g$ using a theoretical model without air resistance fitted to data on height and speed vs. time that includes air resistance (and errors). One first sees that a discrepancy model is essential; using an RBF GP is standard and one finds good predictions for times where there is data (this is KOH). But the discrepancy model must be more informed for a robust extraction of $g$; this leads to using a nonstationary GP.  Sunil has given permission for us to adapt his notebook. This example has many extensions available to students.
* The EFT examples incorporate much of this, but need to be made more explicit.

## Gaussian processes
* Make examples more robust to changes in GP libraries both because there are many choices and the landscape shifts on a short time scale.
* Introduce and illustrate nonstationary GPs. The BOH discussion is one place they come up. Other examples are changepoint kernels to handle phase transitions (model mixing) and the BUQEYE chiral EFT model.
* Connect to ANNs in large width limit (some notebooks are in progress in collaboration with an OSU student, which can be used with minor editing).

## Sampling
* Could use Bilby ([arXiv](https://arxiv.org/abs/2106.08730), [github](https://github.com/bilby-dev/bilby)) to make common interface to many different samplers. Bilby is actively developed (e.g., there are recent commits, and 83 open vs. 720 closed issues) but the online documentation has fallen a bit behind.
* Add more examples. 

## Emulators
* Add [Parametric Matrix Models](https://arxiv.org/abs/2401.11694), aka PMMs, with examples.
* Some pointers and background (from an rjf talk) on reduced basis method (RBM) emulations are given in the BUQEYE LFD [here].(https://buqeye.github.io/LearningFromData/content/Gaussian_processes/extra_RBM_emulators.html).
* A brief introduction to emulators is given in the CF LFD [here](https://learningfromdata-cforssen-75e6959196db9d0b88353479987355fdad70a.gitlab.io/content/BayesianStatistics/ComputationalBayes/BayesFast.html).
* Some RBM (Eigenvector Continuation) examples can be adapted from BUQEYE open sources.
* We should include multidimensional GP emulation; use [surmise](https://surmise.readthedocs.io/en/latest/) for examples?

## ANNs using field theory formulation
* Much of this will probably be supplementary material.
* Can do the basics with just initializations (no training) near the beginning.
* rjf and student (Simon Sundberg) are putting together a Jupyter Book with introductory material that could be adapted.

## Model mixing
* Can build on the BAND software ([Taweret](https://taweretdocs.readthedocs.io/en/latest/) and [SAMBA](https://github.com/asemposki/SAMBA)) and basic examples.

## Using ChatGP (or other generative AI chatbot)
* I used ChatGP to introduce neural networks on PyTorch and it was extremely efficient. The example was a feed-forward network for a one-variable function; see [Neural Network for simple function_in PyTorch](https://buqeye.github.io/LearningFromData/notebooks/Machine_learning/Neural_Network_for_simple_function_in_PyTorch.html). Many generalizations are possible.

## Using PyCharm (or equivalent)
* I haven't checked whether Christian already has background material on this.
* There are multiple choices, but Jordan recommends PyCharm.
* Most likely the getting-started details are in the supplementary material.
  
