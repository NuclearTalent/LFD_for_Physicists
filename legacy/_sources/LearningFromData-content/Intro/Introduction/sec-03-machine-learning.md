(sec:Intro:ML)=
# Machine learning

The Bayesian workflow sets us up to talk about Machine Learning (ML) from a Bayesian perspective. 
Indeed there are corresponding steps in the typical ML workflow, although they might not be immediately recognized as such (e.g., regularization in ML is a type of prior that imposes the knowledge that weights should not be overly large when trained).
The use of ML methods such as Gaussian processes are already naturally formulated in a Bayesian statistical setting, with priors, posteriors, and probability distributions. 
But we can also cast neural networks in a probabilistic framework.
Furthermore, there are special features about ML for physics, summarized below, which argue for a less "black box" approach to ML than is common.
All of these aspects motivate an integrated discussion of ML within this text, which we carry out in Part IV.

```{admonition} What is special about machine learning in physics?
Physics research takes place within a special context:
  * Physics data and models are connected with physical processes and are often fundamentally different from those encountered in typical computer science contexts. 
  * Physicists ask different types of questions about their data, sometimes requiring new methods.
  * Physicists have different priorities for judging the quality of a model: interpretability, error estimates, predictive power, etc.

Providing slightly more detail:
  * Physicists are data **producers**, not (only) data consumers:
    * Experiments can (sometimes) be designed according to needs.
    * Statistical errors on experimental data can be quantified.
    * Much effort is spent to understand systematic errors.

  * Physics data represents measurements of physical processes:
    * Dimensions and units are important.
    * Measurements often reduce to counting photons, etc, with known a-priori random errors.
    * In some experiments and scientific domains, the data sets are *huge* ("Big Data")

  * Physics models are usually traceable to an underlying physical theory:
    * Models might be constrained by theory and previous observations.
    * There might exist prior knowledge about underlying physics that should be taken into account.
    * Parameter values are often intrinsically interesting.
    * The error estimate of a prediction is just as important as its value.
  ```

