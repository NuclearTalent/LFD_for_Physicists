# Computing the posterior analytically

## First the likelihood

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

## Case I: uniform (flat) prior

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


## Case II: conjugate prior

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

