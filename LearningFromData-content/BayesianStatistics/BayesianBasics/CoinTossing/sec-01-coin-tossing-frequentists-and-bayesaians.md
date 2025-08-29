# Coin tossing: Frequentists and Bayesaians


**Storyline:** 
We are observing successive flips of a coin. There is a definite true
probability of getting heads $(p_h)_{\text{true}}$, but we don't know
what the value is, although we do know that it is between 0 and 1.

So, is the coin fair? The frequentist approach to this problem is to set up a null hypothesis, i.e., the hypothesis that the coin is fair, and then determine the probability that the observed data is generated given that that hypothesis holds. If the probability is a low number $p_h \ll 1$ then the null hypothesis can be rejected at a confidence of $1 - p_h$.

Thus, if the data is that the coin produces $R$ heads after $N$ tosses
the frequentist wants to compute 

$$\p{N~\text{tosses}, R~\text{heads}|p_h=0.5}$$ 

and only is allowed to get excited if this probability is a low number. 

The Bayesian, however, gets to ask a more general question:

What is:

$$
  \p{p_h | N~\text{tosses}, R~\text{heads}, I} \, ?
$$

Note that the *outcome* of any one coin toss is discrete (either heads or tails) but
$p_h$ can take any value between 0 and 1, and this PDF is a function
of the continuous variable $p_h$.   Best estimates for $p_h$,
intervals that encompass the true value with a certain probability,
etc. can then all be computed from the probability density
function $\p{p_h | N~\text{tosses}, R~\text{heads}, I}$. Determining
the probability distribution function for $p_h$ given the data on the
coin's behavior is an example of Bayesian parameter estimation.


One of the key points of this exercise, is that with each flip of the
coin we acquire more information on the value of $p_h$. The logical
thing to do is to update the state of our belief, our PDF for $\p{p_h|\rm{How~many~heads~in~as~many~tosses~as~we've~made},I}$ each time the number of coin tosses is incremented by 1. The PDF will tend to get narrower, i.e., our state of knowledge of $p_h$ more definite, as we acquire more data. 

Note that in what follows we exploit the fungibility of mathematical symbols to let $I$ stand for different things at different stages of the coin tossing experiment. If we are going to "update" after every coin toss then $D$ is just the result of the $N$th coin toss and $I$ is what we know about the coin after $N-1$ coin tosses.

The notebook is [](../demo-BayesianBasics) (non-widget) and/or [](../Bayesian_updating_coinflip_interactive.ipynb). Try both!

Let's first play a bit with the simulation and then come back and think of the details.

* Note a few of the Python features:
    * there is a class for data called Data. Python classes are easy compared to C++!
    * a function is defined to make a type of plot that is used repeatedly
    * elaborate widget $\Longrightarrow$ use it as a guide for making your own! (Optional!) Read from the bottom up in the widget definition to understand its structure.

* Widget user interface features:
    * tabs to control parameters or look at documentation
    * set the true $p_h$ by the slider
    * press "Next" to flip "jump" # of times
    * plot shows updating from three different initial prior PDFs


::::{admonition} Class exercises
:class: my-checkpoint
Tell your neighbor how to interpret each of the priors    
:::{admonition} Possible answers 
:class: dropdown, my-hint 
* uniform prior: any probability is equally likely. Is this *uninformative*? (More later!)
* centered prior (informative): we have reason to believe the coin is more-or-less fair.
* anti-prior: could be anything but most likely a two-headed or two-tailed coin. 
:::
What is the minimal common information about $p_h$ (meaning it is true of *any* prior PDF)?
:::{admonition} Answer
:class: dropdown, my-answer
$$
  0 \leq p_h \leq 1 \quad \mbox{and} \quad \int_0^1 \p{p_h}\, dp_h = 1
$$
:::
::::

* Things to try:
    * First one flip at a time. How do you understand the changes intuitively?
    * What happens with more and more tosses?
    * Try different values of the true $p_h$.
	* Hit `New Data` multiple times to see the fluctuations. 

