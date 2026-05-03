# Analytic coin-flipping posterior

In practical applications, we will very often find posteriors by *sampling*, which means we acquire a (generally multi-dimensional) set of outcomes, whose histogram approximates the exact posterior.
In some cases we are able to derive an analytic expression for the posterior. This includes the case of *conjugate priors*, which we exploit below. 
In the process we see the flexibility of the [beta distribution](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.beta.html), which we use to parametrize a rather general prior distribution.

Here we derive analytic expressions for the coin-flipping posterior that are used in the demo notebooks {ref}`demo:bayesian-coin-tossing` and {ref}`demo:WidgetCoinTossing`.

## First the likelihood

Suppose we had a fair coin $\Longrightarrow$ $p_H = 0.5$

$$
  p(\mbox{$H$ heads of out $N$ tosses | fair coin}) = p(H,N|p_H = 0.5)
   = {N \choose H} (0.5)^H (0.5)^{N-H}
$$

Is the sum rule obeyed?

$$
 \sum_{H=0}^{N} p(H,N| p_H = 1/2) = \sum_{H=0}^N {N \choose H} \left(\frac{1}{2}\right)^N
   = \left(\frac{1}{2}\right)^N \times 2^N = 1 
$$

:::{admonition} Proof of penultimate equality
:class: dropdown, my-answer
$(x+y)^N = \sum_{H=0}^N {N \choose H} x^H y^{N-H} \overset{x=y=1}{\longrightarrow} \sum_{H=0}^N {N \choose H} = 2^N$.  More generally, $x = p_H$ and $y = 1 - p_H$ shows that the sum rule works in general. 
:::

The likelihood for a more general $p_H$ is the binomial distribution:

$$
   p(H,N|p_H) = {N \choose H} (p_H)^H (1 - p_H)^{N-H}
   $$ (eq:binomial_likelihood)

Maximum-likelihood means: what value of $p_H$ maximizes the likelihood (notation: $\mathcal{L}$ is often used for the likelihood)?

$$
  p(H,N|p_H) \equiv \mathcal{L}(H,N|p_H) = \mathcal{N}p_H^H (1-p_H)^{N-H} \,?
$$  

Exercise: Carry out the maximization

But, as a Bayesian, we want to know about the PDF for $p_H$, so we actually want the PDF the other way around: $p(p_H|H,N)$. Bayes says

$$
  p(p_H | H,N) \propto p(H,N|p_H) \cdot p(p_H)
$$

* Note that the denominator doesn't depend on $p_H$ (it is just a normalization).


So how are we doing the calculation of the updated posterior?
* In this case we can do analytic calculations.

## Case I: uniform (flat) prior

$$
 \Longrightarrow\quad p(p_H| H, N, I) = \mathcal{N} p(H,N|p_H) p(p_H)
$$ (eq:coinflip_posterior)

where we will suppress the "$I$" going forward. 
But

$$
\begin{align}
 \int_0^1 dp_H \, p(p_H|H,N) &= 1 \quad \Longrightarrow \quad 
         \mathcal{N}\frac{\Gamma(1+N-H)\Gamma(1+H)}{\Gamma(2+N)} = 1
\end{align}
$$ (eq:coinflip_posterior_norm)

:::{admonition} Recall Beta function
$$
  B(x,y) = \int_0^1 t^{x-1} (1-t)^{y-1} \, dt = \frac{\Gamma(x)\Gamma(y)}{\Gamma(x+y)}
  \ \  \mbox{for } \text{He}(x,y) > 0
$$  (eq:beta_function)

and $\Gamma(x) = (x-1)!$ for integers.
:::

$$
  \Longrightarrow\quad \mathcal{N} = \frac{\Gamma(2+N)}{\Gamma(1+N-H)\Gamma(1+H)}
$$ (eq:beta_normalization)

and so evaluating the posterior for $p_H$ for new values of $H$ and $N$ is direct: substitute {eq}`eq:beta_normalization` into {eq}`eq:coinflip_posterior`.
If we want the unnormalized result with a uniform prior (meaning we ignore the normalization constant $\mathcal{N}$ that simply gives an overall scaling of the distribution), then we just use the likelihood {eq}`eq:binomial_likelihood` since $p(p_H) = 1$ for this case.


## Case II: conjugate prior

Choosing a conjugate prior (if possible) means that the posterior will have the same form as the prior. Here if we pick a beta distribution as prior, it is conjugate with the coin-flipping likelihood. From the [scipy.stats.beta documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.beta.html) the beta distribution (function of $x$ with parameters $a$ and $b$):

$$
  f(x, a, b) = \frac{\Gamma(a+b) x^{a-1} (1-x)^{b-1}}{\Gamma(a)\Gamma(b)}
$$ (eq:scipy_beta_distribution)

where $0 \leq x \leq 1$ and $a>0$, $b>0$. 
So $p(x|a,b) = f(x,a,b)$ and our likelihood is a beta distribution $p(H,N|p_H) = f(p_H,1+H,1+N-H)$ to agree with {eq}`eq:binomial_likelihood`.

If the prior is $p(p_H|I) = f(p_H,\alpha,\beta)$ with $\alpha$ and $\beta$ to reproduce our prior expectations (or knowledge), then by Bayes' theorem the *normalized* posterior is

$$
\begin{align}
  p(p_H | H,N) &\propto p(H,N | p_H) p(p_H) \\
  & \propto f(p_H,1+H,1+N-H) \times f(p_H,\alpha,\beta) \\
  & \longrightarrow f(p_H, \alpha+H, \beta+N-H)
\end{align}  
$$ (eq:coinflip_updated)

so we *update the prior* simply by changing the arguments of the beta distribution: $\alpha \rightarrow \alpha + H$, $\beta \rightarrow \beta + N-H$ because the (normalized) product of two beta distributions is another beta distribution. Heally easy!

:::{warning} Check this against the code! 
Look in the code where the posterior is calculated and see how the beta distribution is used. Verify that {eq}`eq:coinflip_updated` is evaluated. Try changing the values of $\alpha$ and $\beta$ used in defining the prior to see the shapes.
:::

