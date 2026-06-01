---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:BayesianCredibleIntervals)=
# Bayesian credible intervals

## Defining credible intervals

For a one-dimensional posterior that is *symmetric*, it is clear how to define the $d\%$ confidence interval. 
The algorithm is: start from the center, step outward on both sides, stop when $d\%$ is enclosed.
For a two-dimensional posterior, we need a way to integrate from the top. (One approach is to lower a plane, as described below for HPD.)

What if the distribution is asymmetic or multimodal? Here are two possible choices.
* Equal-tailed interval (or central interval): define the boundaries of the interval so that the area above and below the interval are equal.
* Highest posterior density (HPD) region: the posterior density for
every point is higher than the posterior density for any point
outside the
interval. E.g., lower a horizontal line over the distribution until the desired interval percentage is covered by regions where the distribution is above the line.


## Bayesian credible intervals and frequentist confidence intervals

There are important differences between the Bayesian
68% credible (DoB) interval for the most likely value  and a frequentist $1 \sigma$ confidence
interval. 

The first point is that $1 \sigma=68$% assumes a Gaussian distribution
around the maximum of the posterior. While this will
often work out to be roughly correct, it may not. And, as we seek to translate 
$n \sigma$ intervals into DoB statements, assuming a Gaussian
becomes more and more questionable the higher $n$ is. (*Why?*)

But the second point is more philosophical (meta-statistical?). One
  interval is a statement about $p(x|D,I)$, while the other is a
  statement about $p(D|x,I)$.
(Note that because the conversion between the two PDFs requires the
 use of Bayes' theorem, the Bayesian interval may be affected by the
 choice of the prior.)

The Bayesian version of a confidence interval is easy; a 68% credible interval or degree-of-belief (DoB) interval is: given
  some data and some information $I$, there is a 68% chance (probability) that the interval contains the true parameter. 

On the other hand, the frequentist 68% confidence interval is trickier:
assuming the model (contained in $I$) and the value of the
parameter $x$, then if we do the experiment a large number of
times then 68% of them will produce data in that interval.
So the *parameter* is fixed (no PDF) and the confidence
interval is a statement about *data*.
Frequentists will try to make statements about parameters, but
they end up a bit tangled, e.g., "There is a 68% probability
that when I compute a confidence interval from data of this sort
that the true value of $\theta$ will fall within the
(hypothetical) space of observations."





