(sec:cointossing)=
# Coin tossing: Frequentists and Bayesians


**Storyline:** 
We are observing successive flips of a coin. There is a definite true
probability of getting heads $(p_H)_{\text{true}}$, but we don't know
what the value is, although we do know that it is between 0 and 1.

So, is the coin fair? By fair, we mean that we would be prepared to lay an even 1 : 1 bet on the outcome of a flip being a head or a tail. The frequentist approach to this problem is to set up a null hypothesis, i.e., the hypothesis that the coin is fair (meaning $p_H=0.5$), and then determine the probability that the observed data is generated given that that hypothesis holds. If the probability is a low number $p_H \ll 1$ then the null hypothesis can be rejected at a confidence of $1 - p_H$.

Thus, if the data is that the coin produces $H$ heads after $N$ tosses
the frequentist wants to compute 

$$\p{N~\text{tosses}, H~\text{heads}|p_H=0.5},$$ 

and only is allowed to get excited if this probability is a low number. 

The Bayesian, however, gets to ask a more general question. What is:

$$
  \p{p_H | N~\text{tosses}, H~\text{heads}, I} \, ?
$$

Note that the *outcome* of any one coin toss is discrete (either heads or tails) but
$p_H$ can take any value between 0 and 1, therefore this PDF is a function
of the continuous variable $p_H$.   Best estimates for $p_H$,
intervals that encompass the true value with a certain probability,
etc. can then all be computed from the probability density
function $\p{p_H | N~\text{tosses}, H~\text{heads}, I}$. Determining
this probability distribution function for $p_H$ given the data on the
coin's behavior is an example of Bayesian parameter estimation.


One of the key points of this exercise, is that with each flip of the
coin we acquire more information on the value of $p_H$. The logical
thing to do is to update the state of our belief, our PDF for $\p{p_H|\rm{How~many~heads~in~as~many~tosses~as~we've~made},I}$ each time the number of coin tosses is incremented by 1. The PDF will tend to get narrower, i.e., our state of knowledge of $p_H$ more definite, as we acquire more data. 

Note that we exploit the fungibility of mathematical symbols to let $I$ stand for different things at different stages of the coin tossing experiment. If we are going to "update" after every coin toss then $D$ is just the result of the $N$th coin toss and $I$ is what we know about the coin after $N-1$ coin tosses.

There are two demo notebooks you can use to explore this problem:
{ref}`demo:bayesian-coin-tossing` (non-widget) and/or {ref}`demo:WidgetCoinTossing`. Try both!

Play a bit with the simulation and then we'll consider some of the details.
Here are some things to try with the widgetized version:
* Look at each of the priors under the *Priors* tab and interpret them.
* First do one flip at a time. How do you understand the changes intuitively?
* What happens with more and more tosses? Can you explain the differences with different priors?
* Hit `New Data` multiple times to see the fluctuations (this changes the random seed). 
* Try different values of the true $p_H$.

