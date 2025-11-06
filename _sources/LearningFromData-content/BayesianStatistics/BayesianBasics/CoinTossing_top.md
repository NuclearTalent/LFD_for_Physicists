(sec:UpdatingBayes)=
# Updating via Bayes' rule

Consider Bayes' rule (or theorem, same thing!) for the case where we seek the PDF of parameters $\thetavec$ contingent on some data.

$$
  \overbrace{\p{\thetavec|\text{data}, I}}^{\text{posterior}} =
  \frac{\overbrace{\p{\text{data}|\thetavec,I}}^{\text{likelihood}}\times \overbrace{\p{\thetavec,I}}^{\text{prior}}}{\underbrace{\p{\text{data}|I}}_{\text{evidence}}}
$$  

* $\thetavec$ is a general *vector* of parameters
* The denominator is the data probability or "fully marginalized likelihood" or evidence or maybe some other name (these are all used in the literature). We'll come back to it later. As will be clear later, it is a normalization factor.
* The *prior* PDF is what information $I$ we have (or believe) about $\thetavec$ before we observe the data.
* The *posterior* PDF is our new PDF for $\thetavec$, given that we have observed the data.
* The *likelihood* is the probability of getting the specified data *given* the parameters $\thetavec$ under consideration on the left side.

The bottom line is that Bayes' rule tells us how to *update* our
expectations. I.e., how we should modify our prior beliefs $I$ about the
parameters $\thetavec$ after we have acquired new data $D$ that has
implications for their values.
