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


## Coin tossing: Frequentists and Bayesaians


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

The notebook is [](./demo-BayesianBasics) (non-widget) and/or [](./Bayesian_updating_coinflip_interactive.ipynb) (with widget). Try both!

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

## When do priors matter? When don't they matter?

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


## Computing the posterior analytically

### First the likelihood

Suppose we had a fair coin $\Longrightarrow$ $p_h = 0.5$

$$
  p(\mbox{$R$ heads of out $N$ tosses | fair coin}) = p(R,N|p_h = 0.5)
   = {N \choose R} (0.5)^R (0.5)^{N-R}
$$

Is the sum rule obeyed?

$$
 \sum_{R=0}^{N} p(R,N| p_h = 1/2) = \sum_{R=0}^N {N \choose R} \left(\frac{1}{2}\right)^N
   = \left(\frac{1}{2}\right)^N \times 2^N = 1 
$$

:::{admonition} Proof of penultimate equality
:class: dropdown, my-answer
$(x+y)^N = \sum_{R=0}^N {N \choose R} x^R y^{N-R} \overset{x=y=1}{\longrightarrow} \sum_{R=0}^N {N \choose R} = 2^N$.  More generally, $x = p_h$ and $y = 1 - p_h$ shows that the sum rule works in general. 
:::

The likelihood for a more general $p_h$ is the binomial distribution:

$$
   p(R,N|p_h) = {N \choose R} (p_h)^R (1 - p_h)^{N-R}
   $$ (eq:binomial_likelihood)

Maximum-likelihood means: what value of $p_h$ maximizes the likelihood (notation: $\mathcal{L}$ is often used for the likelihood)?

$$
  p(R,N|p_h) \equiv \mathcal{L}(R,N|p_h) = \mathcal{N}p_h^R (1-p_h)^{N-R} \,?
$$  

Exercise: Carry out the maximization

But, as a Bayesian, we want to know about the PDF for $p_h$, so we actually want the PDF the other way around: $p(p_h|R,N)$. Bayes says

$$
  p(p_h | R,N) \propto p(R,N|p_h) \cdot p(p_h)
$$

* Note that the denominator doesn't depend on $p_h$ (it is just a normalization).


So how are we doing the calculation of the updated posterior?
* In this case we can do analytic calculations.

### Case I: uniform (flat) prior

$$
 \Longrightarrow\quad p(p_h| R, N, I) = \mathcal{N} p(R,N|p_h) p(p_h)
$$ (eq:coinflip_posterior)

where we will suppress the "$I$" going forward. 
But

$$
\begin{align}
 \int_0^1 dp_h \, p(p_h|R,N) &= 1 \quad \Longrightarrow \quad 
         \mathcal{N}\frac{\Gamma(1+N-R)\Gamma(1+R)}{\Gamma(2+N)} = 1
\end{align}
$$ (eq:coinflip_posterior_norm)

:::{admonition} Recall Beta function
$$
  B(x,y) = \int_0^1 t^{x-1} (1-t)^{y-1} \, dt = \frac{\Gamma(x)\Gamma(y)}{\Gamma(x+y)}
  \ \  \mbox{for } \text{Re}(x,y) > 0
$$  (eq:beta_function)

and $\Gamma(x) = (x-1)!$ for integers.
:::

$$
  \Longrightarrow\quad \mathcal{N} = \frac{\Gamma(2+N)}{\Gamma(1+N-R)\Gamma(1+R)}
$$ (eq:beta_normalization)

and so evaluating the posterior for $p_h$ for new values of $R$ and $N$ is direct: substitute {eq}`eq:beta_normalization` into {eq}`eq:coinflip_posterior`.
If we want the unnormalized result with a uniform prior (meaning we ignore the normalization constant $\mathcal{N}$ that simply gives an overall scaling of the distribution), then we just use the likelihood {eq}`eq:binomial_likelihood` since $p(p_h) = 1$ for this case.


### Case II: conjugate prior

Choosing a conjugate prior (if possible) means that the posterior will have the same form as the prior. Here if we pick a beta distribution as prior, it is conjugate with the coin-flipping likelihood. From the [scipy.stats.beta documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.beta.html) the beta distribution (function of $x$ with parameters $a$ and $b$):

$$
  f(x, a, b) = \frac{\Gamma(a+b) x^{a-1} (1-x)^{b-1}}{\Gamma(a)\Gamma(b)}
$$ (eq:scipy_beta_distribution)

where $0 \leq x \leq 1$ and $a>0$, $b>0$. 
So $p(x|a,b) = f(x,a,b)$ and our likelihood is a beta distribution $p(R,N|p_h) = f(p_h,1+R,1+N-R)$ to agree with {eq}`eq:binomial_likelihood`.

If the prior is $p(p_h|I) = f(p_h,\alpha,\beta)$ with $\alpha$ and $\beta$ to reproduce our prior expectations (or knowledge), then by Bayes' theorem the *normalized* posterior is

$$
\begin{align}
  p(p_h | R,N) &\propto p(R,N | p_h) p(p_h) \\
  & \propto f(p_h,1+R,1+N-R) \times f(p_h,\alpha,\beta) \\
  & \longrightarrow f(p_h, \alpha+R, \beta+N-R)
\end{align}  
$$ (eq:coinflip_updated)

so we *update the prior* simply by changing the arguments of the beta distribution: $\alpha \rightarrow \alpha + R$, $\beta \rightarrow \beta + N-R$ because the (normalized) product of two beta distributions is another beta distribution. Really easy!

:::{warning} Check this against the code! 
Look in the code where the posterior is calculated and see how the beta distribution is used. Verify that {eq}`eq:coinflip_updated` is evaluated. Try changing the values of $\alpha$ and $\beta$ used in defining the prior to see the shapes.
:::

## Degree of belief/credibility intervals vs frequentist 1-sigma intervals

Work through the section of the notebook the compares the Bayesian 68%
credibility interval against the 1-sigma interval obtained with the
frequentist estimator.


## Take-aways and follow-up questions from coin flipping:

1. How often should the 68% degree of belief interval contain the true
answer for $p_H$?

2. What would your standard be for deciding the coin was so unfair that you would walk away? That you’d call the police? That you’d try and publish the fact that you found an unfair coin in a scientific journal?

3. Is there a difference between updating sequentially or all at once? Do the simplest problem first: two tosses.
Let results be $D = \{D_k\}$ (in practice take 0's and 1's as the two choices $\Longrightarrow$ $R = \sum_k D_k$).

    * First $k=1$ (so $D_1 = 0$ or $D_1 = 1$): 
        
        $$ p(p_h | D_1,I) \propto p(D_1|p_h,I) p(p_h|I)$$ (eq:k_eq_1)
    
    * Now $k=2$, starting with the expression for updating all at once and then using the sum and product rules (including their corollaries marginalization and Bayes' Rule) to move the $D_1$ result to the right of the $|$ so it can be related to sequential updating:
    
        $$\begin{align}
        p(p_h|D_2, D_1) &\propto p(D_2, D_1|p_h, I)\times p(p_h|I) \\
             &\propto p(D_2|p_h,D_1,I)\times p(D_1|p_h, I)\times p(p_h|I) \\
             &\propto p(D_2|p_h,D_1,I)\times p(p_h|D_1,I) \\
             &\propto p(D_2|p_h,I)\times p(p_h|D_1,I) \\
             &\propto p(D_2|p_h,I)\times p(D_1|p_h,I) \times p(p_h,I)
        \end{align}$$ (eq:k_eq_2)
    
        ::::{admonition} Checkpoint question
        :class: my-checkpoint
        What is the justification for each step? 
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
    * So all at once is the same as sequential as a function of $p_h$, when normalized!
    * To go to $k=3$:

        $$\begin{align}
        p(p_h|D_3,D_2,D_1,I) &\propto p(D_3|p_h,I) p(p_h|D_2,D_1,I) \\
           &\propto p(D_3|p_h,I) p(D_2|p_h,I) p(D_1|p_h,I) p(p_h)
        \end{align}$$

and so on.


So they are not different, as long as the tosses are independent. 

4. What about "bootstrapping"? Why can't we use the data to improve the prior and apply it (repeatedly) for the *same* data. I.e., use the posterior from the first set of data as the prior for the same set of data. Let's see what this leads to (we'll label the sequence of posteriors we get $p_1,p_2,\ldots,p_N$): 

    $$\begin{align}
      p_1(p_h | D_1,I) &\propto p(D_1 | p_h, I) \, p(p_h | I) \\
            \\
      \Longrightarrow p_2(p_h, D_1, I) &\propto p(D_1 | p_h, I) \,  p_1(p_h | D_1, I) \\
        &\propto [p(D_1 | p_h,I)]^2 \, p(p_h | I) \\
      \mbox{keep going?}\quad & \\
      p_N(p_h | D_1, I) &\propto p(D_1|p_h, I)\, p_{N-1}(p_h | D_1, I) \\
        &\propto [p(D_1 | p_h, I)]^N \, p(p_h | I)
    \end{align}$$

    Suppose $D_1$ was 0, then $[p(\text{tails}|p_h,I)]^N \propto (1-p_h)^N p(p_h|I) \overset{N\rightarrow\infty}{\longrightarrow} \delta(p_h)$ (i.e., the posterior is only at $p_h=0$!). Similarly, if $D_1$ was 1, then $[p(\text{tails}|p_h,I)]^N \propto p_h^N p(p_h|I) \overset{N\rightarrow\infty}{\longrightarrow} \delta(1-p_h)$ (i.e., the posterior is only at $p_h=1$.)

    More generally, this bootstrapping procedure would cause the posterior to get narrower and narrower with each iteration so you think you are getting more and more certain, with no new data!
    ```{image} ./figs/bootstrapping_cartoon.png
    :alt: bootstrapping
    :class: bg-primary
    :width: 300px
    :align: right
    ```

    :::{warning}
    Don't do that!
    :::



