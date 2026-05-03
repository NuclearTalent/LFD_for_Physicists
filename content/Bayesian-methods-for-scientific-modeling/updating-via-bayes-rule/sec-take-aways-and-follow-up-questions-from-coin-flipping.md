# Take-aways and follow-up questions from coin flipping

## When do priors matter? When don't they matter?

::::{admonition} Interpreting priors
:class: my-checkpoint
Give an interpretion to each of the priors in the widgetized demo    
:::{admonition} Possible answers 
:class: dropdown, my-hint 
* uniform prior: any probability is equally likely. Is this *uninformative*? (More later!)
* centered prior (informative): we have reason to believe the coin is more-or-less fair.
* anti-prior: could be anything but most likely a two-headed or two-tailed coin. 
:::
What is the minimal common information about $p_H$ (meaning it is true of *any* prior PDF)?
:::{admonition} Answer
:class: dropdown, my-answer
$$
  0 \leq p_H \leq 1 \quad \mbox{and} \quad \int_0^1 \p{p_H}\, dp_H = 1
$$
:::
::::



::::{admonition} Bayesian convergence
:class: my-checkpoint
What happens when enough data is collected?
:::{admonition} Answer
:class: dropdown, my-answer
All posteriors, independent of prior, converge to a narrow PDF including $(p_H)_{\text{true}}$. This is called *Bayesian convergence*.
:::
Different priors *eventually* give the same posterior with enough
data.  How many tosses
constitute ``eventually" for $p_H = 0.4$ or $p_H = 0.9$?
:::{admonition} Answer
:class: dropdown, my-answer
* $p_H = 0.4$ $\Longrightarrow$ $\approx 200$ tosses will get you most of the way.
* $p_H = 0.9$ $\Longrightarrow$ much longer for the informative prior than the others.
:::
Which prior(s) get to the correct conclusion fastest for $p_H = 0.4, 0.9, 0.5$? Can you explain your observations?
::::


::::{admonition} Anti-prior
:class: my-checkpoint
Why does the "anti-prior" work well even though its dominant assumptions (most likely $p_H = 0$ or $1$) are proven wrong early on?     
:::{admonition} Answer
    :class: dropdown, my-answer
    The "heavy tails" (which in general means the probability away from the peaks; in the middle for the "anti-prior") mean it is like uniform (renormalized!) after the ends are eliminated. An important lesson for formulating priors: allow for deviations from your expectations.
:::
::::


:::{note}
A good reference about selecting priors is the Stan page on [Prior Choice Recommendations](https://github.com/stan-dev/stan/wiki/Prior-Choice-Recommendations).
:::


## Updating squentially (after every toss) vs. all at once


Let's do the simplest version of the question first: two tosses.
Let the results of the first $k$ tosses be $D = \{D_k\}$ (in practice take 0's and 1's as the two choices $\Longrightarrow$ $R = \sum_k D_k$).

* First consider $k=1$ (so $D_1 = 0$ or $D_1 = 1$): 
    
    $$ p(p_H | D_1,I) \propto p(D_1|p_H,I) p(p_H|I)$$ (eq:k_eq_1)

* Now $k=2$, starting with the expression for updating all at once and then using the sum and product rules (including their corollaries, the marginalization and Bayes' Rule) to move the $D_1$ result to the right of the $|$ so it can be related to sequential updating:

    $$\begin{align}
    p(p_H|D_2, D_1) &\propto p(D_2, D_1|p_H, I)\times p(p_H|I) \\
         &\propto p(D_2|p_H,D_1,I)\times p(D_1|p_H, I)\times p(p_H|I) \\
         &\propto p(D_2|p_H,D_1,I)\times p(p_H|D_1,I) \\
         &\propto p(D_2|p_H,I)\times p(p_H|D_1,I) \\
         &\propto p(D_2|p_H,I)\times p(D_1|p_H,I) \times p(p_H,I)
    \end{align}$$ (eq:k_eq_2)

    ::::{admonition} Checkpoint question
    :class: my-checkpoint
    What is the justification for each step in {eq}`eq:k_eq_2`? 
    :::{admonition} Answer 
    :class: dropdown, my-answer 
    * 1st line: Bayes' Rule
    * 2nd line: Product Rule (applied to $D_1$)
    * 3rd line: Bayes' Rule (going backwards)
    * 4th line: tosses are independent
    * 5th line: Bayes' Rule on the last term in the 3rd line
    :::
    ::::


    The fourth line of {eq}`eq:k_eq_2` is the sequential result! (The prior for the 2nd flip is the posterior {eq}`eq:k_eq_1` from the first flip.)
* So all at once is the same as sequential as a function of $p_H$, when normalized!
* To go to $k=3$:

    $$\begin{align}
    p(p_H|D_3,D_2,D_1,I) &\propto p(D_3|p_H,I) p(p_H|D_2,D_1,I) \\
       &\propto p(D_3|p_H,I) p(D_2|p_H,I) p(D_1|p_H,I) p(p_H)
    \end{align}$$

and so on.


So they are not different, as long as the tosses are independent. 

::::{admonition} What about "bootstrapping"?
:class: my-checkpoint
Why can't we use the data to improve the prior and apply it (repeatedly) for the *same* data. I.e., use the posterior from the first set of data as the prior for the same set of data.
:::{admonition} Answer
:class: dropdown, my-answer
Let's see what this leads to (we'll label the sequence of posteriors we get $p_1,p_2,\ldots,p_N$): 

$$\begin{align}
  p_1(p_H | D_1,I) &\propto p(D_1 | p_H, I) \, p(p_H | I) \\
        \\
  \Longrightarrow p_2(p_H | D_1, I) &\propto p(D_1 | p_H, I) \,  p_1(p_H | D_1, I) \\
    &\propto [p(D_1 | p_H,I)]^2 \, p(p_H | I) 
\end{align}$$

What if we keep going $N$ times?

$$\begin{align}
  \Longrightarrow p_N(p_H | D_1, I) &\propto p(D_1|p_H, I)\, p_{N-1}(p_H | D_1, I) \\
    &\propto [p(D_1 | p_H, I)]^N \, p(p_H | I)
\end{align}$$

Suppose $D_1$ was 0, then $[p(\text{tails}|p_H,I)]^N \propto (1-p_H)^N p(p_H|I) \overset{N\rightarrow\infty}{\longrightarrow} \delta(p_H)$ (i.e., the posterior is only at $p_H=0$!). 

Similarly, if $D_1$ was 1, then $[p(\text{tails}|p_H,I)]^N \propto p_H^N p(p_H|I) \overset{N\rightarrow\infty}{\longrightarrow} \delta(1-p_H)$ (i.e., the posterior is only at $p_H=1$.)

More generally, this bootstrapping procedure would cause the posterior to get narrower and narrower with each iteration so you think you are getting more and more certain, with no new data!
```{image} ../assets/bootstrapping_cartoon.png
:alt: bootstrapping
:class: bg-primary
:width: 300px
:align: right
```

:::{warning}
Don't do that!
:::
:::
::::

## Other questions

::::{admonition} Checkpoint question
:class: my-checkpoint
How often should the 68% credible interval contain the true
answer for $p_H$?
:::{admonition} Answer 
:class: dropdown, my-answer 
68% of the time!
:::
::::

:::{admonition} Discussion question
What would your standard be for deciding the coin was so unfair that you would walk away? That you’d call the police? That you’d try and publish the fact that you found an unfair coin in a scientific journal?
:::


