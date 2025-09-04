(sec:AdvancedMethods)=
# Overview of Part II: Advanced Bayesian methods

In this part we extend our introduction to Bayesian methods to include more advanced techniques and examples.

The chapters in this part are
* {ref}`sec:ModelDiscrepancy` addresses an important topic: accounting for the errors in our model (we often call this the "theoretical error"). All models are approximate to some degree and failing to account for the discrepancy can lead to erroneous and often over-confident results.
* {ref}`sec:AssigningProbabilities` looks at a variety of methods to specify prior PDFs, including symmetry invariance and maximum entropy.
* {doc}`./BayesianParameterEstimation/dealing_with_outliers` explores several ways to extend linear regression to treat outlier data.
* {ref}`sec:BayesLinear` describes a powerful technique that starts with the statistical model. 
* {ref}`sec:MultiModelInference` is a large topic with multiple facets. One approach to dealing with multiple models for the same data is {ref}`sec:ModelSelection`, which gives a probabilistic ranking among candidate models. Another set of approaches, {ref}`sec:MultiModelInference`, combine ("mix") results from the models rather than seeking the best, with the goal of more informed inference.
