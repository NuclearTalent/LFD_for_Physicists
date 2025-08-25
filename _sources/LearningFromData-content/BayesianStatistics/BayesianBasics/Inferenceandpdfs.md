(ch:Inferenceandpdfs)=
#  Inference and PDFs

## Statements

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
Further discussion on the interpretation of probability can be found in {ref}`sec:BayesianEpistemology`.
:::


(sec:ManipulatingPDFs)=
## Manipulating probabilities: Bayesian rules of probability as principles of logic

In the school of subjective probability you can assign whatever
probability we want to the above statements. They represent, after
all, your degree of belief. But you should beware! If your probability
assignments are consistently capricious people may stop paying
attention to them.

A minimal set of rules for consistently keeping track of probabilities
is provided by two basic rules of probability arithmetic. These are the sum
and product rules. A proof that the Sum and Product rules follow in any consistent implementation of probabilistic reasoning is given by Cox {cite}`Cox:1961`.


### Sum rule
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

The sum rule implies a key tool in the Bayesian's arsenal,
_marginalization_ 

\begin{align}
      \cprob{x}{I} = \sum_j \cprob{x, y_j}{I} 
\end{align}

with the second equality being the generalization of marginalization
to the context of variables $x$ and $y$ that can take on a
continuous set of values, rather
than just a discrete set of outcomes $\{x_i\}$ and $\{y_j\}$. 

 We will use marginalization a lot! Note that the marginalization
 takes place in the presence of the conditional I, i.e., all
 probabilities involved are ``given the information I''. The given
 information is held fixed, while the sum of all possibilities is
 constructed. 

:::{warning}
Although we alluded to the analogy between inserting a complete set
of states and marginalization above this analogy breaks down in
general. It's ok to use this as a mnemonic though.
:::

:::{note}
A rule from probability says $\prob(A \cup B) = \prob(A) + \prob(B) - \prob(A \cap B)$. (That is, to calculate the probability of the union of $A$ and $B$ we need to subtract the probability of the intersection from the sum of probabilities.) This may seem to contradict our marginalization rule. The difference is that if $A$ and $B$ are *exclusive*, as we assume, then $\prob(A \cap B) = 0$.
:::

### Product rule

The product rule tells us how to expand the joint probability of $x$
and $y$, i.e., 

$$  
\cprob{x,y}{I} = \cprob{x}{y, I} \cprob{y}{I} 
$$ (eq:joint_prob)

In words we say that the probability of both $x$ and $y$ occurring is
the probability that $x$ occurs, given that $y$ has occurred, times
the probability that $y$ occurs. 

Note, once again, that the given information I is held fixed, i.e., it
if present on the left-hand side it appears in both probabilities on
the right-hand side. 

If $x$ and $y$ are *mutually independent*, then $\cprob{x}{y,I} = \cprob{x}{I}$ and {eq}`eq:joint_prob` reduces to 

$$
\cprob{x,y}{I} = \cprob{x}{I} \times \cprob{y}{I}
$$ (eq:conditional_independence)

This is a rule you are probably (but we hesitate to quantify our
belief) familiar with. Crucially, {eq}`eq:joint_prob` does _not_
rely on the independence of the events $x$ and $y$.

:::{note}
When considering whether $x$ and $y$ are mutually independent, you can ask yourself: does knowing $y$ is true give me any information about whether $x$ is true? If yes, then we need to keep it on the right side of the bar in $\cprob{x}{y,I}$. If no, then it doesn't change the probability of $x$ whether it is there or not, so the probability of $x$ being true is the same if $y$ is omitted.
Hence $\cprob{x}{y,I} = \cprob{x}{I}$ follows.
:::


### Bayes' theorem

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

Bayes' theorem tells us how to reverse the conditional: $\cprob{x}{y}
\Rightarrow \cprob{y}{x}$. The first thing to realize is that these two
probabilities are not the same thing.

::::{admonition} Checkpoint question
:class: my-checkpoint
Construct your own example of $\cprob{x}{y} \neq \cprob{y}{x}$
:::{admonition} Possible answers 
:class: dropdown, my-hint 
The probability that there is a cloud in the sky given that it is
raining is not the same as the probability that it's raining given
that there is a cloud in the sky. 
:::
::::


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


## Probability density functions

The key mathematical entity used over and over again throughout this book will be the "probability density function", PDF for short. PDFs for continuous quantities are integrated to obtain probabilities. An example familiar to every physicist will be the probability density of a quantum-mechanical particle. Max Born somewhat belatedly decided to put a square on Schrodinger's wave function when interpreting the integral from $x=a$ to $x=b$ as the probability of measuring the particle to be between $a$ and $b$:

$$
   \prob(a \leq x \leq b) = \int_a^b |\psi(x)|^2\, dx
$$

We note that the unit of $|\psi(x)|^2$ is inverse length, and it is generally true that PDFs, unlike probabilities, have units. If we divorce the previous equation from the quantum-mechanical context we would write:

$$
   \prob(a \leq x \leq b) = \int_a^b \p{x}\, dx
$$

where $\p{x}$ is the PDF for the continuous variable $x$. 

::::{admonition} Checkpoint question
:class: my-checkpoint
What is the unit of $p(\xvec)$ (or $|\psi(\xvec)|^2$) in three dimensions (assuming $\xvec$ is a vector of length)?
:::{admonition} Answer 
:class: dropdown, my-answer 
We can use the normalization equation (which is the sum rule):

$$
  \int d^3x\, p(\xvec) = 1 ,
$$ 

which is dimensionless on the right side, so the unit of $p(\xvec)$ (or $|\psi(\xvec)|^2$) is the inverse unit of $d^3x$, or $1/\text{length}^3$. Note that if $\xvec$ represented a different quantity, the unit of $p(\xvec)$ would differ accordingly.
:::
::::



We note that the case of a discrete random variable, e.g., the numbers
that can be rolled on a die, mean that the PDF only is non-zero at a
discrete set of numbers. In that case $\p{x}$ can be represented as
a sum of Dirac delta functions, and the resulting object is sometimes
called a probability mass function. Thus the cases discussed above,
in which $\prob$ represented probability measured over a discrete set
of outcomes, can be understood as special cases of pdfs.

In fact, working this from the other end,  the sum and product rules
to pdfs in just the same way as they do to probabilities. Therefore Bayes' theorem (or
rule) can also be applied to relate the pdf of x given y, $\pdf{x}{y}$
to the pdf of $y$ given $x$, $\pdf{y}{x}$.

In Bayesian statistics there are PDFs (or PMFs if discrete) for
everything. Here are a few examples:
* fit parameters --- like the slope and intercept of a line in a
  straight-line fit
* experimental *and* theoretical imperfections that lead to
  uncertainties in the final result
* events ("Will it rain tomorrow?")

We will stick to the $\p{\cdot}$ notation here, but it's worth pointing out that many different variants of the letter $p$ are used to represent probabilities and PDFs in the literature. If we are interested in the PDF in a higher-dimensional space (say the probability of finding a particle in 3D space) you might see $p(\vec x) = p(\mathbf{x}) = P(\vec x) = \text{pr}(\vec x) = \text{prob}(\vec x) = \ldots$.


::::{admonition} Checkpoint question
:class: my-checkpoint
What is the PDF $\p{x}$ if we know **definitely** that $x = x_0$ (i.e., fixed)?
:::{admonition} Answer 
:class: dropdown, my-answer 
$\p{x} = \delta(x-x_0)\quad$  [Note that $p(x)$ is normalized.]
:::
::::



### Joint PDFs, marginal PDFs, and an example of marginalization

$\p{x_1, x_2}$ is the *joint* probability density of $x_1$ and $x_2$. In quantum mechanics the probability density $|\Psi(x_1, x_2)|^2$ to find particle 1 at $x_1$ and particle 2 at $x_2$ is a joint probability density.

::::{admonition} Checkpoint question
:class: my-checkpoint
What is the probability to find particle 1 at $x_1$ while particle 2 is *anywhere*?
:::{admonition} Answer 
:class: dropdown, my-answer 
$\int_{-\infty}^{+\infty} |\psi(x_1, x_2)|^2\, dx_2\ \ $ or, more generally, integrated over the domain of $x_2$.
:::
::::

This is a specific example of the marginalization rule, now in the pdf
context, that we
discussed the general form for probabilities above. The *marginal
probability density* of $x_1$ is the result when we marginalize the
*joint probability distribution* over $x_2$: 

$$
 \p{x_1} = \int \p{x_1, x_2} \,dx_2 .
$$

So, in our quantum mechanical example, it's the probability
density we get when we just focus on particle 1, and don't care about
particle 2. *Marginalizing* in the Bayesian context means
``integrating out'' a parameter one is--at least temporarily--not
interested in, to leave the focus on the PDF of other parameters. This
can be particularly useful if there are "nuisance" parameters in the
statistical model that account for the impact of defects in the
measuring apparatus, but ultimately one is interested in the physics
extracted with the imperfect apparatus. 

:::{note}
You may have noticed that we wrote $\p{x_1}$ and $\p{x_1, x_2}$ rather than $\pdf{x_1}{I}$ and $\pdf{x1,x2}{I}$, where "$I$" is information we know but do not specify explicitly. Our PDFs will always be contingent on *some* information, so we were really being sloppy by trying to be compact. (See {ref}`sec:continuum_limit` for more careful versions of these equations.)
:::


### Visualizing PDFs

It is worthwhile at this stage to jump ahead and work through parts of the Jupyter notebook
[Exploring PDFs](Exploring_pdfs.ipynb) to make a first pass at getting familiar with PDFs and how to visualize them. In the notebook you will
work with the python package `scipy.stats`, which has many
distributions built in. You can learn more about those distributions by
reading the manual page (which you can find by googling).

:::{note}
See {ref}`sec:Statistics` in Appendix A for further details on PDFs.
:::

The diversity of distributions available there should make it clear
that the "default" choice of a Gaussian distribution is just that: a
default choice. In {ref}`sec:Gaussians` we will explore why this default
choice is often the correct one. But often is not the same as all the
time, and it is frequently the case that other distributions, such as
the Student t, gives a better description of the way data is
distributed.

:::{note}
Trivia: "Student" was the pen name of the Head Brewer at Guinness --- a pioneer of small-sample experimental design (hence not necessarily Gaussian). His real name was William Sealy Gossett. 
:::

Because we can draw an arbitrary number of samples from the
distributions defined in scipy.stats we can see how the distributions
build up as the number of samples increases, and how there are
fluctuations around the asymptotic distribution that are larger for a
small number of samples. 

## Summary

We have put on the table the axioms of probability theory and some of their consequences, in particular Bayes' theorem. 
Before looking further at concrete applications of Bayesian inference, we provide further insight into Bayes' theorem in {ref}`sec:MoreBayesTheorem` and introduce some additional ingredients for Bayesian inference in {ref}`sec:DataModelsPredictions`. The latter include the idea of a statistical model, how to predict future data conditioned on (i.e., given) past data and background information (the posterior predictive distribution), and Bayesian parameter estimation.

In Appendix A there is a summary and further details on {ref}`sec:Statistics`. Particularly important are {ref}`sec:ExpectationValuesAndMoments` and {ref}`sec:CentralMoments`; we summarize the key discrete and continuous definitions here.

:::{admonition} Brief summary of expectation values and moments
The *expectation value* of a function $h$ of the random variable $X$ with respect to its distribution $p(x_i)$ (a PMF) or $p(x)$ (a PDF) is

$$
\mathbb{E}_{p}[h] =  \sum_{i}\! h(x_i)p(x_i) \quad\Longrightarrow\quad
  \mathbb{E}_p[h] = \int_{-\infty}^\infty \! h(x)p(x)\,dx .
$$

The $p$ subscript is usually omitted. *Moments* correspond to $h(x) = x^n$, with $n=0$ giving 1 (this is the normalization condition) and the mean $\mu$ by $n=1$:

$$
\mathbb{E}[X] \equiv \mu =  \sum_{i}\! x_ip(x_i) \quad\Longrightarrow\quad
  \mathbb{E}[X] \equiv \mu = \int_{-\infty}^\infty \! xp(x)\,dx .
$$

The variance and covariance are moments with respect to the mean for one and two random variables (we give only the continuous version here):

$$\begin{align}
\text{Var}(X) &\equiv \sigma^2  \equiv \mathbb{E}\left[ \left( X - \mathbb{E}[X] \right)^2 \right] \\
\text{Cov}(X,Y) &\equiv \sigma_{XY}^2 \equiv \mathbb{E}\left[ \left( X - \mathbb{E}[X] \right) \left( Y - \mathbb{E}[Y] \right)  \right].
\end{align}$$

The standard deviation $\sigma$ is simply the square root of the variance $\sigma^2$. 
The **correlation coefficient** of $X$ and $Y$ (for non-zero variances) is 

$$
\rho_{XY} \equiv \frac{\text{Cov}(X,Y)}{\sqrt{\text{Var}(X)\text{Var}(Y)}},
$$
:::


::::{admonition} Checkpoint question
:class: my-checkpoint
Show that we can also write

$$
\sigma^2 = \mathbb{E}[X^2]  - \mathbb{E}[X]^2
$$
:::{admonition} Answer 
:class: dropdown, my-answer 
$$\begin{align}
\sigma^2 &= \int_{-\infty}^\infty (x-\mathbb{E}[X] )^2 p(x)dx\\
&=  \int_{-\infty}^\infty \left(x^2 - 2 x \mathbb{E}[X] +\mathbb{E}[X]^2\right)p(x)dx \\
& =  \mathbb{E}[X^2]  - 2 \mathbb{E}[X] \mathbb{E}[X]  + \mathbb{E}[X]^2 \\
&=  \mathbb{E}[X^2]  - \mathbb{E}[X]^2
\end{align}$$

Make sure you can justify each step.
:::
::::

::::{admonition} Checkpoint question
:class: my-checkpoint
Show that the mean and variance of the normalized Gaussian distribution

$$
p \longrightarrow \mathcal{N}(x | \mu,\sigma^2) = \frac{1}{\sigma\sqrt{2\pi}} \exp{\Bigl(-\frac{(x-\mu)^2}{2\sigma^2}\Bigr)},
$$

are $\mu$ and $\sigma^2$, respectively.
:::{admonition} Answer 
:class: dropdown, my-answer 
Just do the integrals!

$$\begin{align}
  \mu &= \int_{-\infty}^\infty \! x \frac{1}{\sigma\sqrt{2\pi}} \exp{\Bigl(-\frac{(x-\mu)^2}{2\sigma^2}\Bigr)}\,dx = \mu \quad\checkmark \\
  \sigma^2 &= \int_{-\infty}^\infty (x-\mu )^2 
  \frac{1}{\sigma\sqrt{2\pi}} \exp{\Bigl(-\frac{(x-\mu)^2}{2\sigma^2}\Bigr)} \,dx
  = \sigma^2 \quad\checkmark
\end{align}$$

In doing these integrals, simplify by changing the integration variable to $x' = x-\mu$ and use that the distribution is normalized (integrates to one) and that integrals of odd integrands are zero.
:::
::::





