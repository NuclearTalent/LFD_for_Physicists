(sec:Inference:manipulation)=
# Manipulating probabilities: Bayesian rules of probability as principles of logic

In the school of subjective probability you can assign whatever
probability we want to the above statements. They represent, after
all, your degree of belief. But you should beware! If your probability
assignments are consistently capricious people may stop paying
attention to them.

A minimal set of rules for consistently keeping track of probabilities
is provided by two basic rules of probability arithmetic. These are the sum
and product rules. These rules can be derived from Kolmogorov's axioms of probability,
see [](introduction:definitions), which showed that probabilities can be incorporated into mathematics using the existing theory of measures. More generally, a proof that the Sum and Product rules follow in any consistent implementation of probabilistic reasoning is given by Cox {cite}`Cox:1961`. 

## Sum rule
If the set $\{x_i\}$ is *exhaustive* and *exclusive*

$$
   \sum_i \cprob{x_i}{I} = 1,
$$ (eq:discrete_sum_rule)

i.e., the sum of the probabilities of all possible outcomes is equal
to one. In quantum mechanics we are used to this as the outcome of
summing over a complete, orthonormal set of states, and indeed, in
that case the basis includes all possible values (it's complete), and
there is no overlap between its members (they are orthogonal). 

:::{note}
In {eq}`eq:discrete_sum_rule` we include $I$ (for "Information") generically as the quantities or statements that the probability of $x_i$ is contingent on. We use $I$ to avoid having to specify explicitly all the details, but we should remember that these probabilities (and probability densities introduced below) are always conditional on some information.
:::

## Product rule

The product rule tells us how to expand the joint probability of $x$
and $y$, i.e., 

$$  
\cprob{x,y}{I} = \cprob{x}{y, I} \cprob{y}{I} 
$$ (eq:joint_prob)

In words we say that the probability of both $x$ and $y$ occurring is
the probability that $x$ occurs, given that $y$ has occurred, times
the probability that $y$ occurs. 

Note, once again, that the given information $I$ is held fixed, i.e., it
if present on the left-hand side it appears in both probabilities on
the right-hand side. 

If $x$ and $y$ are *mutually independent*, then $\cprob{x}{y,I} = \cprob{x}{I}$ and {eq}`eq:joint_prob` reduces to 

$$
\cprob{x,y}{I} = \cprob{x}{I}  \cprob{y}{I}
$$ (eq:conditional_independence)

This is a rule you are probably (but we hesitate to quantify our
belief) familiar with. Crucially, {eq}`eq:joint_prob` does _not_
rely on the independence of the events $x$ and $y$.

:::{note}
When considering whether $x$ and $y$ are mutually independent, you can ask yourself: does knowing $y$ is true give me any information about whether $x$ is true? If yes, then we need to keep it on the right side of the bar in $\cprob{x}{y,I}$. If no, then it doesn't change the probability of $x$ whether it is there or not, so the probability of $x$ being true is the same if $y$ is omitted.
Hence $\cprob{x}{y,I} = \cprob{x}{I}$ follows.
:::


## Bayes' theorem

It is just a short step from the product rule to Bayes'
theorem. Although we wrote {eq}`eq:joint_prob` so that the
$\cprob{x}{y,I}$ appeared on the right-hand side there is no reason to
privilege $x$ over $y$. We could equally have written:

$$  
\cprob{x,y}{I} = \cprob{y}{x, I} \cprob{x}{I} 
$$ 

Equating this to the expression in {eq}`eq:joint_prob` yields **Bayes' Rule** (or Theorem):

\begin{equation}
\cprob{x}{y,I} = \frac{\cprob{y}{x,I} \cprob{x}{I}}{\cprob{y}{I}}
\end{equation}

Bayes' theorem tells us how to reverse the conditional: $\cprob{y}{x}
\Rightarrow \cprob{x}{y}$. The first thing to realize is that these two
probabilities are not the same thing.

::::{admonition} Checkpoint question
:class: my-checkpoint
Construct your own example of $\cprob{x}{y} \neq \cprob{y}{I}$
:::{admonition} Possible answers 
:class: dropdown, my-hint 
The probability that there is a cloud in the sky given that it is
raining is not the same as the probability that it's raining given
that there is a cloud in the sky. 
:::
::::


```{admonition} Ingredients of Bayes' theorem
A typical use of Bayes' theorem is to update information on a hypothesis $y$ according to new data $x$ that we obtain. In that case the various terms in the theorem have formal names. 
* The quantity on the far right, $\cprob{y}{I}$, is called the *prior* probability; it represents our state of knowledge (or ignorance) about the truth of the hypothesis $y$ before we have analysed the new data $x$.
* This is modified by additional information on $y$ through $\cprob{x}{y,I}$, the *likelihood* function, that tells us how likely it is that we measure $x$, given that $y$ is true (and $I$ is true as well). 
* The denominator $\cprob{x}{I}$ is called the *evidence*. It does not depend on the hypothesis and can be regarded as a normalization constant in many situations. 
* Together, these yield the *posterior* probability, $\cprob{y}{x,I}$, representing ourupdated state of knowledge about the hypothesis $y$ in light of the information we had before, $I$, and the additional data $x$.

In this sense, Bayes’ theorem is a mathematically rigorous statement of how probabilities should be updated in light of new information: the process of learning from data.
```


## The friends of Bayes' theorem

```{admonition} Normalization and marginalization

Given an exclusive and exhaustive list of hypotheses, $y_j$, we must have a normalization of the total probability

\begin{equation}
  \sum_j \cprob{y_j}{I} = 1,
\end{equation}

which also leads to the marginalization property


\begin{align}
      \cprob{x}{I} = \sum_j \cprob{y_j}{x,I} \cprob{x}{I}=\sum_j \cprob{x, y_j}{I} 
\end{align}

where we used the product rule in the second step.
  ```

This is a key tool in the Bayesian's article: the ability to obtain the  "marginal" probability for the outcome of one variable by summing the joint probability for $x$ and $y$ over all possible outcomes $\{y_j\}$ of the second variable. This second variable
is not one we are interested in when computing the pdf $\cprob{x}{I}$, so we ``marginalize over it". 

 We will use marginalization a lot! Note that the marginalization
 takes place in the presence of the conditional I, i.e., all
 probabilities involved are "given the information I". The given
 information is held fixed, while the sum of all possibilities is
 constructed.

For example, let’s imagine that there are five candidates in a presidential election; then $H_1$ could be the proposition that the first candidate will win, and so on. The probability that $A$ is true, for example that unemployment will be lower in a year’s time (given all relevant information $I$, but irrespective of whoever becomes president) is given by $\sum_i \prob(A,H_i|I)$. The president is a nuisance variable who has been marginalized out of the calculation. 

:::{warning}
Although we alluded to the analogy between inserting a complete set
of states and marginalization above this analogy breaks down in
general. It's ok to use this as a mnemonic though.
:::

:::{note}
A rule from probability says $\prob(A \cup B) = \prob(A) + \prob(B) - \prob(A \cap B)$. (That is, to calculate the probability of the union of $A$ and $B$ we need to subtract the probability of the intersection from the sum of probabilities.) This may seem to contradict our marginalization rule. However, if $A$ and $B$ are *exclusive* (as we assume) then $\prob(A \cap B) = 0$.
:::



```{exercise} Practicing the sum and product rule with population characteristics
:label: exercise:Inferenceandpdfs:sumandproductrule

In the exercise {ref}`exercise:CheckingSumProduct`
you can go through some calculations based on the sum and product
rule. You estimate the probabilities of finding an individual in a
population with a particular characteristic (tall with brown eyes for
example) based on what you're told about the population and the usual
frequentist interpretation of probability. Then the exercise will take
you through applying the sum and product rules. 
```

```{exercise} Using Bayesian rules of probability on a standard medical problem
:label: exercise:Inferenceandpdfs:medicalexample

In the exercise {ref}`exercise:MedicalExample` your goal is to find the probability that you actually have an unknown disease given some information about the test for it. This is a problem for which your intuition and personal probability reasoning logic is likely to fail. But Bayes leads the way to the correct answer! It is good practice in translating statements to probabilities (and distinguishing between joint and conditional probabilities). 
```


