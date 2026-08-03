(sec:Inference:statements)=
# Statements

A Bayesian approach to the world assigns probabilities to truth
claims. It also recognizes that the probability of claim $A$ is
contingent upon statement $B$ being true. We therefore introduce
notation for conditional probability:

$$ 
   \cprob{A}{B} \equiv \text{``probability of $A$ given $B$ is true''}.
$$

For a Bayesian $A$ and $B$ could stand for anything. But, whatever
they are, statements can now be categorized as definitively true
(probability 1), or definitively false (probability 0), or anything in
between.

Examples:
* $\cprob{\text{``Betty eats grass''}}{\text{``Betty is a cow'' and
    ``All cows eat grass''}}=1$
* $\cprob{\text{``Lines A and B intersect''}}{\text{``A and B are
    parallel lines in flat space''}}=0$
* $\cprob{\text{``Particle A is negatively charged''}}{\text{``A is an electron''}}=1$

On the other hand something like $\cprob{\text{``below 0 deg,. C''}}{\text{``it is January in Ohio''}}$ should be assigned a probability
between 0 and 1. We might even estimate this probability based on our
past experience of Januarys in Ohio. But even statements for which we
cannot construct a $\text{``frequentist estimator''}$ can be assigned
probabilities, e.g. 

$$\cprob{\text{``String theory is true''}}{\text{``Data
from all high-energy colliders and cosmology''}},$$ 

or, less frivolously 

$$\cprob{\text{``I'll come to the party tonight''}}{\text{``You
invited me''}}.$$ 

This emphasizes that, for a Bayesian, the probability is interpreted
as representative of the Bayesian's current state of knowledge, and
not necessarily as the long-term average of a set of
many trials. After all, what would it mean to conduct a set of trials,
in some of which string theory was true, and in some of which it was not?

:::{warning}
It is easy to forget the meaning of the key word *given* and assume that $\cprob{A}{B}$ means that we know $B$ is actually true, which may or may not be the case. 
:::

:::{note}
In this book we employ a Bayesian interpretation of probability throughout. However, we sometimes contrast our analysis of a problem to an analysis of the same problem using a frequentist interpretation of probability. And even within a Bayesian interpretation there are several different interpretations. One of the big divisions is between the school of thought which says that probabilities should be objective, and the "subjective school of Bayesian probability". In the subjective school of probability everyone has their own state of knowledge so everyone gets to assign their own pdfs to quantities of interest. More
 discussion of these different interpretations of probability can be found in {ref}`sec:BayesianEpistemology`.
:::


(sec:ManipulatingPDFs)=
