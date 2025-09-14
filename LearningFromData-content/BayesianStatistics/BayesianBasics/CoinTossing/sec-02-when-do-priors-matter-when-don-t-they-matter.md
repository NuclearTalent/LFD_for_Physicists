# When do priors matter? When don't they matter?

::::{admonition} Question
:class: my-checkpoint
What happens when enough data is collected?
:::{admonition} Answer
:class: dropdown, my-answer
All posteriors, independent of prior, converge to a narrow PDF including $(p_h)_{\text{true}}$
:::
::::
Follow-ups:
* Which prior(s) get to the correct conclusion fastest for $p_h = 0.4, 0.9, 0.5$? Can you explain your observations?
* Does it matter if you update after every toss or all at once?
* Why does the "anti-prior" work well even though its dominant assumptions (most likely $p_h = 0$ or $1$) are proven wrong early on?     
    :::{admonition} Answer
    :class: dropdown, my-answer
    The "heavy tails" (which in general means the probability away from the peaks; in the middle for the "anti-prior") mean it is like uniform (renormalized!) after the ends are eliminated. An important lesson for formulating priors: allow for deviations from your expectations.
    :::


Different priors *eventually* give the same posterior with enough
data. This is called *Bayesian convergence*. How many tosses
constitute ``eventually"? Clearly it depends on $p_h$ and how close you want the posteriors to be. How about for $p_h = 0.4$ or $p_h = 0.9$?
:::{admonition} Answer
:class: dropdown, my-answer
* $p_h = 0.4$ $\Longrightarrow$ $\approx 200$ tosses will get you most of the way.
* $p_h = 0.9$ $\Longrightarrow$ much longer for the informative prior than the others.
:::

Choosing priors: a good reference is the Stan page on [Prior Choice Recommendations](https://github.com/stan-dev/stan/wiki/Prior-Choice-Recommendations).


