(sec:BayesianWorkflow)=
# Bayesian research workflow

In {ref}`sec:Intro:Workflow` we presented a four-step Bayesian workflow, repeated here:


:::{admonition} Four-step Bayesian workflow in brief
1. Formulate informative priors before new data is used.
2. Define a statistical model relating the physics model and data, including all errors.
3. Compute the posterior probabilities.
4. Do model checking.
:::


In this chapter we elaborate on these steps. We start with a condensed description of a Bayesian workflow for rigorous scientific inference. It is partially based on the more extensive exposition in the Methods Primer by Van De Schoot et al. {cite}`Vandeschoot:2021`.

This formulation divides a typical Bayesian workflow into three main steps (see {numref}`fig-BayesianWorkflow-research-cycle`): (i) capturing available knowledge about given parameters in a statistical model via the prior distribution (typically performed before data collection); (ii) determining the likelihood function using the information about the data generating process; and (iii) combining the prior distribution and the likelihood function using Bayes’ theorem and so obtaining the posterior distribution. The posterior distribution is then used to conduct inferences. 
These steps correspond to the first three steps above. In order to match our previously introduced workflow we add to these three steps a fourth one: using the posterior to check the extent to which aspects of the statistical model are consistent with the data being analyzed. 

In the following subsections we expand upon each step.

```{figure} ../assets/Bayesian_workflow_diagram_v1.png
:height: 600px
:name: fig-BayesianWorkflow-research-cycle

The Bayesian research cycle. The steps needed for a research cycle using Bayesian statistics include formalizing prior distributions based on background knowledge and prior elicitation; determining the likelihood function by specifying a data-generating model and including observed data; obtaining the posterior distribution from the product of the specified prior and likelihood function; and performing checks of the statistical model using that posterior. Inferences can then be made that can then be used to start a new research cycle. Loosely based on: Stat math, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0), via Wikimedia Commons. See also {cite}`Vandeschoot:2021`.
```

## Step 1: selecting a prior

The first step in the Bayesian workflow depicted in {numref}`fig-BayesianWorkflow-research-cycle` is to determine prior distributions, shortened to priors. This is an important part of a rigorous inference process. Prior selection and the second step of likelihood determination are sometimes collectively referred to as the (statistical) experimentation phase. The suitability of the chosen priors can be ascertained using a prior predictive checking process (see {prf:ref}`remark:BayesianWorkflow:predictive-checking`). Ultimately the sensitivity of the results to details of the chosen prior should be assessed as part of the Model checking phase of the Bayesian workflow.

### Formalizing prior distributions

Priors can come in many different distributional forms, such as a normal, uniform or Poisson distribution, etc. Most importantly, priors can have different levels of informativeness. The information reflected in a prior distribution can be anywhere on a continuum from complete uncertainty to relative certainty. Although priors can fall anywhere along this continuum, there are three main classifications of priors that are used in the literature to categorize the degree of (un)certainty they encode: informative, weakly informative and diffuse. One way to assess the informativeness of a normal prior is to compare its standard deviation to its mean value. The informativeness of the prior must also be assessed in the context of how well the likelihood constrains the parameter on which the prior is being placed.
A good practical guide to choosing priors is the [Stan Prior Choice Recommendations](https://github.com/stan-dev/stan/wiki/Prior-Choice-Recommendations) on github. 

### Prior elicitation 

Prior elicitation is the process by which a suitable prior distribution is constructed. Strategies for prior elicitation include asking an expert or a panel of experts to provide values for the hyperparameters of the prior distribution.

Prior elicitation can also involve implementing data-based priors. Then, the hyperparameters for the prior are derived from sample data using methods such as maximum likelihood. Such approaches, however, must avoid "double-dipping": the data used to form the prior must be distinct from the data included in the likelihood.

The subjectivity of priors is highlighted by critics as a potential drawback of Bayesian methods. Two distinct points should be mentioned in this context. First, many elements of the estimation process are subjective in the sense that they may differ from modeler to modeler. Different reasonable people may make different reasonable choices not only for priors, but also for the likelihood, and certainly for the model itself. To lay blame for the "sin" of subjectivity solely at the feet of the priors is a misleading distraction from the other elements in the process that are inherently modeler dependent. Second, there can be circumstances in which informative priors are a sensible choice, for example if a parameter is known to be positive, or previous data already constrains it well. 

This illustrates that priors should encode knowledge that the practitioner possesses that is independent of the data whose generation is modeled through the likelihood. To the extent that knowledge is justified, true belief, the level at which it is justified can then be incorproated in the informativeness of the prior. 

Sometimes, diffuse priors are assigned to reflect an indifference to the location or scale of some parameter. Symmetry arguments can then be used to assign a prior that reflects this indifference via a  symmetry or invariance principle. See {numref}`sec:Ignorance` for more on this topic and specific examples.

Even with quantified prior information, the choice of distributional form for the prior (as needed for a full Bayesian analysis) typically involves extra assumptions. Say that you wish to assign a prior with a specific mean value and standard deviation for a model parameter. In this scenario you are still left with the choice between many different distributional forms that fulfill those constraints. Fortunately,  arguments based on the maximum entropy principle can help translating a finite set of prior knowledge into a probability distribution with the least restrictive extra assumptions. These ideas are presented in {numref}`sec:MaxEnt` {ref}`sec:MaxEnt`.

### Checking the prior

Finally, there is the question of how to formulate a prior in a multi-dimensional parameter space. Typically practitioners will formulate priors for each parameter separately and then combine them assuming independence, i.e., take the prior $\pdf{\para}{I}$ to be the product of the one-dimensional prior pdfs for each individual parameter. However, if previous data or a theoretical argument indicates that two parameters should be correlated then that correlation should be incorporated into the prior. Note that correlations derived from the data set being analyzed should _not_ be incorporated into the prior. These will emerge from the posterior when it is formed from the prior and the likelihood. Building them into the prior right from the start of the analysis would be an example of the "double dipping" warned about above. 

Because inference based on a Bayesian analysis will only be valid if the prior is not incorrect, it is of importance to carefully check whether the specified prior is in conflict with the data being analyzed. One way to check that a prior is not manifestly incorrect in this sense is via the process known as prior predictive checking (see box below). 

The prior predictive distribution is the distribution of all possible data that could be generated given the prior, the statistical model for the data generating process, and the physics model that relates the parameters of the model to the outputs. A prior will be in conflict with the combination of data-generating process and physics model if the three, when combined, yield a data distribution that is disjoint with the actual measured data. Prior predictive checking thus compares the observed data, or statistics of the observed data, with the prior predictive distribution, or statistics of the predictive distribution, and checks that they are not incompatible. It is to be expected that the prior predictive distribution will be broader than the distribution of actual data---otherwise the new data is not adding any information to the analysis. But there is conflict inherent in our analysis if the prior predictive distribution and data distribution do not overlap at least somewhat. There should be minimal statistical tension between the two if the analysis that is envisioned is going to be useful. Significant tension signals that our prior knowledge is in conflict with one or more of: the measured data, our physics model of the output(s) corresponding to those data, or the statistical relaion we have assumed between the data and the output(s). 

### Step 2: determining the likelihood function

The likelihood is used in both Bayesian and frequentist inference. In both inference paradigms, its role is to quantify the strength of support the observed data lends to possible value(s) for the unknown parameter(s). In the likelihood the unknown parameters are considered to be fixed; the likelihood is the conditional probability distribution $\pdf{\output}{\para}$ of the data ($\output$), given fixed parameters ($\para$). A particular likelihood function therefore collects the following elements of a Bayesian analysis: a statistical model that stochastically generates all of the data from particular model outputs, and a physics model that relates the parameter(s) of interest to those model outputs. For further discussion of ways to think about the likelihood see the discussion "Two views of the likelihood" in {ref}`sec:blr-workflow`.

The statistical model should also account for possible correlations in the outputs (type-y correlations). Such correlations result in a multivariate statistical distribution for the random variable $\output$ that does not simply factor into a product of independent, univariate ones for each datum. 

In some cases, specifying a likelihood function can be very straightforward. A product of normal distributions, one for each output, is a standard choice. However, this assumes that the data generating process for a particular output is conditionally independent from the data generating process for any other output. In practice there may be correlations between them, e.g., shared analysis tools, electrical noise that is correlated between detectors, etc.  Researchers often naively choose the standard data-generating model out of habit or because they cannot easily change it in the software. The statistical data-generating model is itself a modeling choice--just as much as the prior or the physics model themselves are modeling choices. It therefore needs to be justified and clearly documented, so that the choice made, and the reasons for that choice, are available to the reader. Robustness checks should be performed on the selected likelihood function to verify its influence on the posterior estimates.

The sensitivity of the posterior to the inclusion of different output in the likelihood is reflective of the *information content* of that observable. Sensitivity studies of the posterior based on simulated outputs for different future data is a branch of statistical inference known as *experimental design*. It can help determine which observable(s) to spend resources on measuring to improve the accuracy and precision of a desired inference.

## Step 3: Results for the posterior--and other things of interest

In the Bayesian Research Workflow, once the statistical model has been defined and the associated likelihood function derived, the next step is to combine the likelihood with the prior and use the resulting posterior to estimate the unknown parameters of the model. 

In contrast, the frequentist framework for model fitting focuses on the expected long-term outcomes of an experiment with the intent of producing a single point estimate for model parameters such as the maximum likelihood estimate and associated confidence interval. Within the Bayesian Research Workflow, probability distributions are assigned to the model parameters, describing the associated uncertainties. In Bayesian statistics, the focus is on estimating the entire posterior distribution of the model parameters. This posterior distribution is often summarized with associated point estimates, such as the posterior mean or median, and a credible interval.

In these lecture notes, we frequently use Markov Chain Monte Carlo (MCMC) for posterior inference, see  {ref}`sec:RootMCMC`. MCMC combines two concepts: obtaining a set of parameter values from the posterior distribution using the Markov chain; and obtaining a distributional estimate of the posterior and associated statistics with sampled parameters using Monte Carlo integration. MCMC is able to indirectly compute inferences on the posterior distribution by simulating different sets of parameters according to the product of the prior probability and the likelihood.
This results in sets of values for the parameters $\para$ (vectors in the multi-dimensional setting) that are obtained from the posterior distribution with frequencies that will correspond to the posterior distribution if the MCMC has converged. This can be achieved despite the fact that a Bayesian posterior obtained from a likelihood and a prior will typically be high-dimensional, not have a closed anlaytic form, and only be known up to a constant of proportionality. The samples of values of the parameters are then used to obtain empirical estimates of the posterior distribution of interest. It is often more difficult to obtain converged estimates of multivariate distributions, or of the form of low-probability tails. It is therefore often useful to focus on the marginal posterior distribution of each parameter, or pairs of parameters, defined by integrating out all but one or two of the parameters from the multi-dimensional posterior.

One important payoff of MCMC sampling is that any quantity of interest that is a function of the model parameters can also be obtained by computing the function over the set of MCMC samples. This then generates a set of samples for that quantity which can be analyzed via summary statisticis, histograms, etc. If we are interested in multiple quantities that are functions of the parameters we can represent their multi-dimensional distribution as samples in this sense, and so determine not just summary statistics for each one, but also the correlations between these derived quantities.

## Step 4: Model checking

Since the data analyzed in the Bayesian Workflow is itself a function of the model parameters this technology can be directly applied to generate the predictive posterior distribution (PPD). The PPD is the distribution that the model predicts for the model outputs that were measured, given the posterior inferred from those data. The PPD is our first example of Step 4 in the Bayesian Research Workflow. 

Another important check is to assess prior sensitivity. In general a Bayesian analysis should be re-run several times, with different, reasonable, prior choices in order to assess how, and if so, where, the posterior is affected by those choices. 

```{prf:remark} Prior and posterior predictive checking
:label: remark:BayesianWorkflow:predictive-checking
Prior and posterior predictive checks are two cases of the general concept of predictive checks, just conditioning on different things (no data and the observed data, respectively). 

Posterior predictive checking works by simulating new replicated data sets based on the fitted model parameters and then comparing statistics applied to the replicated data set with the same statistic applied to the original data set. The prior predictive distribution is just like the posterior predictive distribution with no observed data, so that a prior predictive check is nothing more than the limiting case of a posterior predictive check with no data. 

A standard posterior predictive check would plot a histogram of each replicated data set along with the original data set and compare them by eye. If a model captures the data well, summary statistics such as sample mean and standard deviation should have similar values in the original and replicated data sets. 

Prior predictive checks evaluate the prior the same way. Specifically, they evaluate what data sets would be consistent with the prior. They will not be calibrated with actual data, but extreme values help diagnose priors that are either too strong, too weak, poorly shaped, or poorly located.

This is easy to carry out mechanically by simulating parameters according to the priors, then simulating data according to the data model given the simulated parameters. This allows a check of how the probability mass of prior predictions is distributed. The posterior predictive distribution can be strongly affected by the prior when there is not much observed data and substantial prior mass is concentrated around infeasible values. 
```

## Reproducibility

Not reporting the choice of priors is problematic for any Bayesian paper. There are many dangers in naively using priors and practitioners should record what was done and justify it as part of the research output. Specifying priors is a way of declaring to future readers of your work what information you considered known before you began your data analysis.

For the same reason, likelihood specification should be clear, as already discussed above. 

More generally, proper reporting on statistics, including sharing of data and scripts, is a crucial element in the verification and reproducibility of research. A workflow incorporating good research practices should encourage reproducibility. Allowing others to assess the statistical methods and underlying data used in a study through transparent reporting and code and data sharing helps with interpreting the study results, generalizations to other cases, assessment of the suitability of modeling choices, and the detection and correction of errors. Reporting practices are not yet consistent in this regard across fields or even journals in individual fields.

To enable reproducibility and allow others to run Bayesian statistics on the same data with different parameters, priors, models or likelihood functions, it is important that the underlying data and code used are properly documented and shared following the FAIR principles: findability, accessibility, interoperability and reusability. Preferably, data and code should be shared in a trusted repository (Registry of Research Data Repositories) with their own persistent identifier (such as a DOI), and tagged with metadata describing the data set or codebase. This also allows the data set and the code to be recognized as separate research outputs and allows others to cite them accordingly. Repositories can be general, such as Zenodo or github; language-specific, such as PyPI for Python code; or domain-specific. Many scientific journals adhere to transparency and openness promotion guidelines, which specify requirements for code and data sharing.

Open-source software should be used as much as possible, as open sources reduce the monetary and accessibility threshold to replicating scientific results. Moreover, it can be argued that closed-source software keeps part of the academic process hidden, including from the researchers who use the software themselves. It is worth emphasizing that open-source software is only truly accessible with proper documentation, which includes listing dependencies and configuration instructions in Readme files, commenting on code to explain functionality and including comprehensive documentation for any packages released as part of the research process.

## Checklists

We end this chapter with two different recommended checklists for statistically sound Bayesian inference that incorporate many of the points made in this chapter. The first one (see {prf:ref}`remark:BayesianWorkflow:buqeye-checklist`) has mainly natural science applications in mind. 

```{prf:remark} Checklist for statistically sound Bayesian inference
:label: remark:BayesianWorkflow:buqeye-checklist

1. Interact with the experts (i.e., statisticians, applied mathematicians).
2. Identify all sources of experimental and theoretical uncertainties that are identified in this process.
3. Formulate statistical models for those uncertainties.
4. Choose priors that are as informative as you consider reasonable; but test sensitivity to those choices.
5. Account for correlations in observables (type y) when formulating the likelihood.
7. Use model checking to validate the analysis.
```

Note that this first checklist matches up quite well with the Bayesian workflow given at the start of this section. 

The second checklist, labeled WAMBS (when to Worry and how to Avoid the Misuse of Bayesian Statistics), originates in work by statistics experts from a wide range of application areas {cite}`Vandeschoot:2021`. This checklist also includes a number of recommendations for monitoring the MCMC convergence (more details in Part III).

```{prf:remark} An adapted version of the WAMBS checklist
:label: remark:BayesianWorkflow:wambs-checklist

Here we have adapted the WAMBS-v2 checklist, an updated version of the WAMBS (when to Worry and how to Avoid the
Misuse of Bayesian Statistics) checklist. Reproduced from {cite}`Vandeschoot:2021`.

1. Ensure the prior distributions and the model or likelihood are well understood (see checklist above).
2. Describe them thoroughly in your research output (article, analysis notebook, etc.).
3. Use prior-predictive checking to help identify any prior–data conflict.
4. Check convergence of your MCMC chain. (See MCMC Workflow section.)
5. To assess the impact of informative priors, compare the posterior results with an analysis using diffuse priors. This comparison can facilitate a deeper understanding of the impact the informative priors have on findings.
6. Examine the sensitivity of your results to priors, especially multivariate priors. These priors can be particularly influential on the posterior, even with slight modifications to the hyperparameters. 
7. It may also be worth testing different forms for the likelihood, in order to see what impact they have on the final results. 
8. Report findings, including Bayesian interpretations. Take advantage of explaining and capturing the entire posterior rather than simply using point estimates. It may be helpful to examine the density at different quantiles to fully capture and understand the posterior distribution.

```

Ticking all the boxes of checklists such as these can be considered an aspirational goal for performing a truly rigorous statistical inference in science.

