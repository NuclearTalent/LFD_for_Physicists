(sec:Inference:PDFs)=
# Probability density functions

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



## Joint PDFs, marginal PDFs, and an example of marginalization

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

## Bayes' theorem applied to PDFs

The rules applied to probabilities in {numref}`sec:Inference:manipulation` directly extend to continuous functions, i.e., PDFs; we'll summarize the extension briefly here.
Conventionally we denote by $\thetavec$ a vector of continuous parameters we seek to determine (for now we'll use $\alphavec$ as another vector of parameters).
As before, information $I$ is kept implicit.

**Sum rule**

Probabilities integrate to one (assuming exhaustive and exclusive $\thetavec$):

$$
  \int d\thetavec\, \pdf{\thetavec}{I} = 1 .
$$

The sum rule *implies* marginalization: 

$$ 
     p(\thetavec|I) = \int d\alphavec\, p(\thetavec, \alphavec | I) .
$$

**Product rule** 

Expanding a joint probability of $\thetavec$ and $\alphavec$

$$  
   p(\thetavec, \alphavec| I) = p(\thetavec | \alphavec, I) p(\alphavec,I) = p(\alphavec| \thetavec,I) p(\thetavec,I) .
$$ (eq:pdf_joint_prob)

As with discrete probabilities, there is a symmetry between the first and second equalities.
If $\thetavec$ and $\alphavec$ are *mutually independent*, then $p(\thetavec | \alphavec,I) = p(\thetavec | I)$ and

$$
  p(\thetavec,\alphavec | I) = p(\thetavec|I) \times p(\alphavec | I) .
$$

Rearranging the 2nd equality in {eq}`eq:pdf_joint_prob` yields **Bayes' Rule** (or Theorem) just like in the discrete case:

$$
  p(\thetavec | \alphavec,I) = \frac{p(\alphavec|\thetavec,I) p(\thetavec|I)}{p(\alphavec | I)}
$$

Bayes' rule tells us how to reverse the conditional: $p(\thetavec|\alphavec) \rightarrow p(\alphavec|\thetavec)$.
A typical application is when $\alphavec$ is a vector of data $\data$. Then Bayes' rule is

$$
  \overbrace{ \pdf{\thetavec}{\data,I)} }^{\textrm{posterior}} =
  \frac{ \color{red}{ \overbrace{ \pdf{\data}{\thetavec,I} }^{\textrm{likelihood}}} 
 \color{black}{\ \times\ } 
  \color{blue}{ \overbrace{ \pdf{\thetavec}{I}}^{\textrm{prior}}}    
 } 
 { \color{darkgreen}{ \underbrace{ \pdf{\data}{I} }_{\textrm{evidence}}} }
$$

Viewing the prior as the initial information we have about $\thetavec$ (i.e., before using the data $\data$), summarized as a probability density function, then Bayes' theorem tells us how to **update** that information after observing some data: this is the posterior PDF.  In {numref}`sec:UpdatingBayes` we will give some examples of how this plays out when tossing biased coins.


## Visualizing PDFs

It is worthwhile at this stage to jump ahead and work through parts of the Jupyter notebook
[Exploring PDFs](../Exploring_pdfs.ipynb) to make a first pass at getting familiar with PDFs and how to visualize them. In the notebook you will
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

