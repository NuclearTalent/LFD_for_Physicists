(sec:UpdatingBayes)=
# Updating via Bayes' rule

Bayes' rule (or theorem, same thing!) plays a central role in Bayesian statistics. It is the heart of how we update our knowledge given new information:

$$
        \text{\large prior} \quad \overset{\text{\Large likelihood}}{\Large\longrightarrow} 
        \ \ \ \text{\large posterior}
$$

Let us recall the specifics and nomenclature of Bayes' rule  for the case where we seek the PDF of parameters $\thetavec$ contingent on some data:

$$
  \overbrace{\p{\thetavec|\text{data}, I}}^{\text{posterior}} =
  \frac{\overbrace{\p{\text{data}|\thetavec,I}}^{\text{likelihood}}\times \overbrace{\p{\thetavec|I}}^{\text{prior}}}{\underbrace{\p{\text{data}|I}}_{\text{evidence}}}
  ,
$$  

where
* $\thetavec$ is a general *vector* of parameters
* The *prior* PDF is based on information $I$ we have (or believe) about $\thetavec$ before we observe the data.
* The *posterior* PDF is our new PDF for $\thetavec$, given that we have observed the data.
* The *likelihood* is the probability of getting the specified data *given* the parameters $\thetavec$ under consideration on the left side.
* The denominator is the data probability or "fully marginalized likelihood" or evidence or maybe some other name (these are all used in the literature).  It is a normalization factor that scales the posterior *independent of $\thetavec$* and so often does not need to be calculated.

The bottom line is that Bayes' rule tells us how to *update* our
expectations. I.e., how we should modify our prior beliefs $I$ about the
parameters $\thetavec$ after we have acquired new data that has
implications for their values. (Note this says "new" data; we can build upon previous data.)

There are many types of parameter estimation based on Bayes' rule; each of the {ref}`ch:PartIExercises` provides an example. 
But we will apply Bayes' rule for updating in other contexts in this book. These include
<!-- * {ref}`sec:ThePPD` -->
* {ref}`sec:BayesianModelSelection`
* Model discrepancy ({ref}`sec:ModelDiscrepancy`)
* {ref}`sec:ModelMixing`
* {ref}`sec:bayesian-optimization`
* {ref}`sec:BNN`

In this chapter we return to the prototypical coin-tossing experiment introduced in {ref}`sec:CoinExample` and look at the updating process in more detail.
