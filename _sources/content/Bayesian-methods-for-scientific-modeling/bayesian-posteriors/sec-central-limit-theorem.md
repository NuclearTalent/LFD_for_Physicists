---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:CLT)=
# The Central Limit Theorem


Another reason a Gaussian PDF emerges in many situations is because
the Central Limit Theorem (CLT) states that the sum of random variables drawn
from all (or almost all) probability
distributions will eventually produce Gaussians if the number of samples in
each sum is large enough. 

:::{admonition} Central Limit Theorem
The sum of $n$ random values drawn from any
PDF of finite variance $\sigma^2$ tends as $n \rightarrow \infty$ to
be Gaussian distributed about the expectation value of the sum, with
variance $n \sigma^2$.
:::

## Consequences of the CLT:

* The mean of a large number of values becomes normally distributed
  _regardless_ of the probability distribution the values are drawn
  from.

* The binomial, Poisson, chi-squared, and Student's t- distributions all approach 
  Gaussian distributions in the limit of a large number
  of degrees of freedom (e.q., for large $n$ for binomial). This consequence is probably not immediately obvious to you from the statement of the CLT! (See below for further details on the Poisson distribution.)


::::{admonition} Checkpoint Question
:class: my-checkpoint
Why would we expect the CLT to work for a binomial distribution?
:::{admonition} Hint
:class: dropdown, my-hint 
If we denote Bin($n,p$) as the binomial distribution for $n$ trials with probability $p$ of success, how is Bin($1,p$) related to Bin($n,p$)?
:::
:::{admonition} Answer
:class: dropdown, my-answer
If we add up $n$ random variables from Bin($1,p$), each with value 0 or 1, this is equivalent to a Bin($n,p$) random variable with the same number of successes. So we already have a sum of random variables built in and the CLT will apply. (In more detail: getting $k$ ones and $n-k$ zeros from the $n$ Bin($1,p$) draws will have probability $p^k$ times $(1-p)^{n-k}$ times the number of combinations $n\choose k$. This is the same as the binomial probability for $k$ successes.)
::::

## Moments of a PDF from a sum of random variables

A Gaussian distribution is completely determined by its first and second moments (that is, its mean $\mu$ and variance $\sigma^2$). This is obvious if we know the distribution is a Gaussian, because its parametrization is fully specified given $\mu$ and $\sigma^2$. But this implies that all of the higher moments of a Gaussian distribution are fully determined by $\mu$ and $\sigma$. 
And if we find a distribution with the same pattern of higher moments, it must be a Gaussian.
In this subsection we see how this observation leads us toward the CLT by returning to the analyses in {ref}`sec:Inference:moments`.


It will be sufficient here (and much cleaner) to work with mean-zero distributions.
The moments $\{m_k\}_{\mathcal{N}(0,\sigma^2)}$ of a mean-zero Gaussian distribution, which will be our target, can be found directly from the moment-generating function in {eq}`eq:expectation:moments_gaussian`:

$$
   \{M_X(t)\}_{\mathcal{N}(0,\sigma^2)} = \exp(\frac{1}{2}\sigma^2 t^2)
   = \sum_{j=0}^{\infty} \frac{1}{j!}\left(\frac{\sigma^2 t^2}{2} \right)^j ,
$$

which means for $X \sim \mathcal{N}(0,\sigma^2)$ we find

$$
  \{m_k\}_{\mathcal{N}(0,\sigma^2)} = \mathbb{E}_{\mathcal{N}(0,\sigma^2)}[X^k]
  = \begin{cases}
      0, & \text{if } k \text{ odd} \\
      (2j-1)!! \sigma^{2j} & \text{if } k=2j \text{ even}
    \end{cases}
  = \begin{cases}
      0, & \text{if } k \text{ odd} \\
      \frac{k!}{2^{k/2} (k/2)!} \sigma^{k} & \text{if } k \text{ even}
    \end{cases} \ ,
$$ (eq:gaussian_momdents)

where $(2j-1)!! = (2j-1)\cdot(2j-3)\cdots 3 \cdot 1$.
Then all the odd moments are zero and 
$\{m_2\}_{\mathcal{N}(0,\sigma^2)}= \sigma^2$, $\{m_4\}_{\mathcal{N}(0,\sigma^2)} = 3\sigma^4$, $\{m_6\}_{\mathcal{N}(0,\sigma^2)} = 15\sigma^6$, and so on.


With those results in hand, we consider any distribution with mean zero and a finite variance $\sigma^2$.
We consider a sum of $n$ random variables, all drawn independently from that same mean-zero (but not necessarily symmetric) distribution (hence they are iid), scaled by an overall $1/\sqrt{n}$ factor:

$$
  X = \frac{1}{\sqrt{n}}(x_1 + x_2 + \cdots + x_n)
   = \sum_{j=1}^n \frac{x_j}{\sqrt{n}} .   
$$ (eq:sum_of_iid)
 
Let's consider moments $m_k = \mathbb{E}[X^k]$ of $X$ as $n$ gets large. $m_0 = 1$ and $m_1 = 0$, since the distribution is normalized and mean zero. By using the linearity of expectation values, the independence of the $x_i$, and $\mathbb{E}[x_i]=0$, we find $m_2$ directly:

$$
 m_2 = \mathbb{E}[X^2] = \frac{1}{n} \left( n\cdot\mathbb{E}[x_1^2] + n (n-1)\cdot \mathbb{E}[x_1]\mathbb{E}[x_2]\right)
                 = \sigma^2 .
$$

We see that the scaling $1/\sqrt{n}$ in the definition of $X$ ensures an $n$-independent variance equal to the variance of the distribution.
For $m_3$, 

$$
  \mathbb{E}[X^3] = \frac{1}{n^{3/2}} \left( n\cdot\mathbb{E}[x_1^3] + 0 \right) = \frac{1}{n^{1/2}}\mathbb{E}[x_1^3],
$$

where the terms set equal to zero have at least one $\mathbb{E}[x_1] = 0$. Note that while the distribution can have a non-zero skewness (third moment), it will be suppressed as $n$ gets large.
For $m_4$,

$$
 \mathbb{E}[X^4] = \frac{1}{n^2}\left( n\cdot\mathbb{E}[x_1^4] + 3n(n-1)\cdot\mathbb{E}[x_1^2]\cdot\mathbb{E}[x_2^2] + 0  \right) = \frac{1}{n}\cdot\mathbb{E}[x_1^4] + 3(1-\frac{1}{n})\sigma^4 .
$$

Now as $n$ gets large, $m_4$ reduces to the Gaussian kurtosis result of $3\sigma^4$.
Note that as long as $n$ is finite, however, there will be non-Gaussian contributions (called excess kurtosis).

More generally, we see that the $\mathbb{E}[x_i^k]$ term in $m_k$ for $k\geq 2$ comes with a single factor of $n$, so it will always be suppressed by increasing powers of $\frac{1}{n}$.
The only $n$-independent terms will be $k/2$ products of $\mathbb{E}[x_i^2] = \sigma^2$, with a coefficient that exactly matches $\{m_k\}_{\mathcal{N}(0,\sigma^2)}$.

Thus, the moments of the $X$ distribution will tend toward those of a Gaussian, meaning that the distribution itself tends towards a Gaussian distribution.
That is the central limit theorem. Now let's make a different construction towards the same end.


## Proof of the CLT

Start with *independent* random variables $x_1,\cdots,x_n$ drawn from a distribution with mean $\langle x \rangle = 0$ and variance $\langle x^2\rangle = \sigma^2$, where

$$
  \langle x^n \rangle \equiv \int x^n p(x)\, dx .
$$

(Assuming mean zero is general, because we can always work with the distribution of $x - \mu$.)
As in the last section, let 

$$
  X = \frac{1}{\sqrt{n}}(x_1 + x_2 + \cdots + x_n)
   = \sum_{j=1}^n \frac{x_j}{\sqrt{n}} ,   
$$

scaling by $1/\sqrt{n}$ so that the variance of $X$ is constant in the $n\rightarrow\infty$ limit.

What is the distribution of $X$?
$\Longrightarrow$ call it $p(X|I)$, where $I$ is the information about the probability distribution for $x_j$. 

**Plan:** Use the sum and product rules and their consequences to relate $p(X)$ to what we know of $p(x_j)$. (Note: we'll suppress $I$ to keep the formulas from getting too cluttered.)

$$\begin{align}
  p(X) &= \int_{-\infty}^{\infty} dx_1 \cdots dx_n\,
            p(X,x_1,\cdots,x_n) \\
       &= \int_{-\infty}^{\infty} dx_1 \cdots dx_n\,
            p(X|x_1,\cdots,x_n)\,p(x_1,\cdots,x_n) \\
       &= \int_{-\infty}^{\infty} dx_1 \cdots dx_n\,
            p(X|x_1,\cdots,x_n)\,p(x_1)\cdots p(x_n) .     
\end{align}$$

::::{admonition} Checkpoint question
:class: my-checkpoint
State the rule used to justify each step.
:::{admonition} Answer
:class: dropdown, my-answer 
1. marginalization
1. product rule
1. independence
:::
::::

We might proceed by using a direct, normalized expression for $p(X|x_1,\cdots,x_n)$,
::::{admonition} Checkpoint question
:class: my-checkpoint
What is $p(X|x_1,\cdots,x_n)$?
:::{admonition} Hint
:class: dropdown, my-hint 
If we know each of the $x_i$ values, we know $X$ *exactly*!
:::
:::{admonition} Answer
:class: dropdown, my-answer 
$p(X|x_1,\cdots,x_n) = \delta\Bigl(X - \frac{1}{\sqrt{n}}(x_1 + \cdots + x_n)\Bigr)
  = \frac{1}{2\pi} \int_{-\infty}^{\infty} d\omega
    \, e^{i\omega\Bigl(X - \frac{1}{\sqrt{n}}\sum_{j=1}^n x_j\Bigr)}$
:::
::::

and perform one of the integrations.
Instead we will use a Fourier representation (see the answer to the Checkpoint question):

$$
p(X|x_1,\cdots,x_n) 
 % = \delta\Bigl(X - \frac{1}{\sqrt{n}}(x_1 + \cdots + x_n)\Bigr) 
  = \frac{1}{2\pi} \int_{-\infty}^{\infty} d\omega
    \, e^{i\omega\Bigl(X - \frac{1}{\sqrt{n}}\sum_{j=1}^n x_j\Bigr)} .
$$  

Substituting into $p(X)$ and gathering together all pieces with $x_j$ dependence while exchanging the order of integrations:

$$ 
 p(X) = \frac{1}{2\pi} \int_{-\infty}^{\infty} d\omega
    \, e^{i\omega X} \prod_{j=1}^n \left[\int_{-\infty}^{\infty} dx_j\, e^{-i\omega x_j / \sqrt{n}} p(x_j) \right] . 
$$ 

Observe that the terms in []s have factorized into a product of independent integrals and they are all the same (just different labels for the integration variables).
Now we Taylor expand $e^{-i\omega x_j/\sqrt{n}}$, arguing that the Fourier integral is dominated by small $x$ as $n\rightarrow\infty$. (*When does this fail?*) We find:

$$
  e^{i\omega x/\sqrt{n}} = 1 - \frac{i\omega x}{\sqrt{n}}
    + \frac{(i\omega)^2 x^2}{2 n} - \mathcal{O}\left(\frac{\omega^3 x^3}{n^{3/2}}\right) .
$$

Then, using that $p(x)$ is normalized (i.e., $\int_{-\infty}^{\infty} dx\, p(x) = 1$) and with the notation $\langle f(x) \rangle$ for the expectation value of $f(x)$, 

$$
\begin{align}
\int_{-\infty}^{\infty} dx\, e^{-i\omega x / \sqrt{n}}
p(x)&=
\int_{-\infty}^\infty dx\, p(x)
\left[1 -\frac{ i \omega x}{\sqrt{n}} + \frac{(i \omega)^2 x^2}{2 n} + \ldots\right]\\
&=1  - \frac{i \omega}{\sqrt{n}} \langle x \rangle  - \frac{\omega^2}{2
n} \langle x^2 \rangle + i \langle x^3 \rangle
\frac{\omega^3}{n^{3/2}}\\
&=1 - \frac{\omega^2 \sigma^2}{2 n} +
\mathcal{O}\left(\frac{\omega^3}{n^{3/2}}\right) .
\end{align}
$$

Now we can substitute into the posterior for $X$ and take the large
$n$ limit:

$$
\begin{align}
p(X)&=\frac{1}{2 \pi} \int_{-\infty}^\infty d\omega\, e^{i \omega X}
\left[1 - \frac{\omega^2 \sigma^2}{2 n} + \mathcal{O} \left(\frac{\omega^3}{n^{3/2}}\right)\right]^n\\
&\stackrel{n\rightarrow \infty}{\longrightarrow} \frac{1}{2 \pi} \int
d\omega\, e^{i \omega X} e^{- \omega^2 \sigma^2/2}=\frac{1}{\sqrt{2
\pi}} e^{-X^2/(2 \sigma^2)}.
\end{align}
$$

::::{admonition} Checkpoint question
:class: my-checkpoint
How did we use the large $n$ limit to get the first equality on the last line?
:::{admonition} Answer
:class: dropdown, my-answer 
We used

$$
  \lim_{n\rightarrow\infty} (1 + \frac{z}{n})^n = e^z \quad \text{for any $z$, here applied to }
  z = -\frac{\omega^2 \sigma^2}{2}.
$$

We can understand this intuitively by multiplying out 

$$ \begin{align}
    \underbrace{(1 + \frac{z}{n})(1 + \frac{z}{n})\cdots(1 + \frac{z}{n})}_{n\ \text{terms}}
    &= 1 + n\cdot\frac{z}{n} + \binom{n}{2}\frac{z^2}{n^2} + \binom{n}{3}\frac{z^3}{n^3} + \ldots
    \\
    &\overset{n\rightarrow\infty}{\longrightarrow} 1 + z + \frac{z^2}{2!} + \frac{z^3}{3!} + \ldots 
\end{align} $$

In getting this result we have dropped terms that are of order $1/n$ and $1/n^2$.
All terms that we dropped in truncating the Taylor expansions for each Fourier integral will also be suppressed by inverse powers (or half powers) of $n$.

:::
::::


## Visualizing the CLT

The general statement of the central limit theory (CLT) is that the sum of $n$ random variables drawn from *any* PDF (or multiple PDFs) of finite variance $\sigma^2$ tends as $n\rightarrow\infty$ to be Gaussian distributed about the expectation value of the sum, with variance $n\sigma^2$.  (So we would scale the sum by $1/\sqrt{n}$ to keep the variance fixed.) In this section we look visually at several consequences of the CLT.

::::
:::{admonition} Things to think about:
:class: my-checkpoint
1. *What does "large" number of degrees of freedom actually mean? Does
it matter where we look?*
1. *If we have a large number of draws from a uniform distribution, does the CLT imply that the histogrammed distribution should look like a Gaussian?*
1. *Can you identify a case (that we have seen) where the CLT will fail?*
:::{admonition} Answers
:class: dropdown, my-answer 
1. "Large" *will* depend on detail, but it is often surprising how few the number is before the CLT kicks in (e.g., often of order 30).
1. Yes! This is illustrated below.
1. The Cauchy distribution will fail because its variance is not finite.
:::
::::

### Limit of Poisson distribution is Gaussian

One consequence of the CLT is that distributions such as the Binomial and Poisson distributions all tend to look like Gaussian distributions in the limit of a large number of drawings.
Here we visualize how the Poisson distribution in the limit $D \rightarrow \infty$ approaches a Gaussian distribution:

$$
 p(N \mid D) = \frac{D^N e^{-D}}{N!} 
 \stackrel{D\rightarrow\infty}{\longrightarrow} \frac{1}{\sqrt{2\pi D}}e^{-(N-D)^2/(2D)}
$$

with $N$ an integer. *You will be asked to prove this limit in a later notebook.*

**Note: this limiting functional form is not obviously connected to the general statement of the CLT up above. What is the connection of the Gaussian limit to a sum of random variables as prescribed by the CLT? Answered below with a test.** 

Make successive histogram plots of the Poisson distribution, increasing the value of $D$ from 0.5 to 50, and superposing the normal distribution it is supposed to approach.

<!--
Note that the arguments of stats.norm.pdf are the # of points, the mean, and the standard deviation (not the variance) of the distribution. -->

```{code-cell} python3
:label: CLT-visualization-1
:tags: [hide-input]

%matplotlib inline   

import scipy.stats as stats  # We'll use stats as our source of PDFs
from scipy.special import factorial
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # nicer plots!

def poisson(N, D):
    """
    Returns a Poisson distribution value with mean D for integer N.
    We require N to be an integer greater than equal to zero.
    """
    assert (isinstance(N, int) and N >= 0), \
            "N must be a non-negative integer!"

    return D**N * np.exp(-D) / factorial(N) 

def poisson_plot(ax, D, max_N):
    """
    Make a bar plot on the axis ax of the Poisson distribution for mu = D
     and out to a maximum integer max_N.
    UPDATE: we eplaced our own poisson function with poisson.pmf from 
     scipy.stats so that we can go to larger N. 
    """
    N_pts = np.arange(0, max_N, 1, dtype=int)
    poisson_pts = [stats.poisson.pmf(N, D) for N in N_pts] # poisson_pts = [poisson(int(N), D) for N in N_pts]
    
    ax.bar(N_pts, poisson_pts, width=0.8, bottom=None, align='center')
    ax.set_xlabel(r'Number of counts $N$', fontsize=18)
    ax.set_ylabel(fr'$\mathrm{{p}}(N \mid D={D:.1f})$', fontsize=18)
    ax.set_title(rf'$D = {D:.1f}$', fontsize=20)
    ax.tick_params(labelsize=16)
    return N_pts

D_list = np.array([0.5, 1.2, 1.7, 12.5, 20., 50., 100., 150.])
num_rows = int(D_list.size / 2)

fig, axes = plt.subplots(num_rows, 2, figsize=(15, 5 * num_rows))

for D, ax in zip(D_list, axes.flatten()):
    max_N = int(D + 6.*np.sqrt(D))  # mean + multiple of standard deviation
    N_pts = np.arange(0, max_N, 0.01)
    y_pts = stats.norm.pdf(N_pts, D, np.sqrt(D))
    poisson_plot(ax, D, max_N)
    ax.plot(N_pts, y_pts, color='red')

fig.tight_layout()

```


### Compare a sum of D Poisson draws with mean 1 to a single Poisson distribution with mean D

Now we answer the question asked above: **What is the connection of the Gaussian limit to a sum of random variables as prescribed by the CLT?**

The answer is that a sum of Poisson distributed random variables is itself Poisson distributed. For example, if $X_1,\ldots,X_D$  are independent Poisson random variables with mean 1 ($D$ is an integer here), then $Y = \sum_{i=1}^D X_i$ is a Poisson random variable with mean $D$. So the sum is built in by directly considering $Y$. Note the analogy to the situation with the binomial distribution and the CLT.

Here we test this answer by plotting the histogram of num_draws samples, each the sum of $D$ mean-1 Poisson samples, to the probability mass function (pmf) of a Poisson with mean-D (and also plot the Gaussian limit).

```{code-cell} python3
:label: CLT-visualization-2
:tags: [hide-input]

D = 5
num_draws = 1000

# set upper range of N
max_N = int(D + 6.*np.sqrt(D))  # mean + multiple of standard deviation

# make an array of the Poisson pmf with mean D
N_pts = np.arange(0, max_N, 1, dtype=int)
poisson_pts = [stats.poisson.pmf(N, D) for N in N_pts]

# (num_draws) samples of the sum of D mean-1 poisson draws
test_poisson_pts = np.array([np.sum([stats.poisson.rvs(1) for index in range(D)]) \
                             for draws in range(num_draws)])
my_bins = np.arange(0, test_poisson_pts.max() + 1.5) - 0.5

# Gaussian limit (mean D and standard deviation D)
norm_x_pts = np.arange(0, max_N, 0.01)
norm_y_pts = stats.norm.pdf(norm_x_pts, D, np.sqrt(D))

# Make the plot
fig, ax = plt.subplots(1, 1, figsize=(12, 5))

# normalized histogram of draws from summed Poissons with mean 1
ax.hist(test_poisson_pts, my_bins, density=True, color='green', alpha=0.5, 
        label='sum of Poisson')

# plot the Poisson pmf with mean D
ax.bar(N_pts, poisson_pts, width=0.8, bottom=None, align='center', 
       color='blue', alpha=.5, label=fr'$\mathrm{{p}}(N \mid D={D})$')

# plot normal distribution
ax.plot(norm_x_pts, norm_y_pts, color='red', label='normal')
    
ax.set_xlabel(r'Number of counts $N$', fontsize=18)
ax.set_ylabel(fr'$\mathrm{{p}}(N)$', fontsize=18)
ax.set_title(rf'Comparing sum of {D} mean 1 Poissons vs. mean $D = {D}$ Poisson', fontsize=20)
ax.tick_params(labelsize=16)

ax.legend(fontsize=18)

fig.tight_layout()



```

**Things to try:**
* Change the number of draws
* Change the value of D

### Behavior of the mean of a fixed-size sample 

Here we take the mean of a fixed-size sample drawn from any PDF, and then repeat a number of times and look at the distribution of the means.  According to the CLT, this distribution should approach a Gaussian PDF.  For our test PDF we'll use a uniform distribution, although this is easy to switch to another distribution.


#### First example: each sample is only one point

Since the sample size is one, the mean is just the point, so the distributions here will look like the original distribution (no approach to Gaussian). Note that we bin the trivial means (the individual draws) into 20 bins.


```{code-cell} python3
:label: CLT-visualization-3
:tags: [hide-input]

import numpy as np
import matplotlib.pyplot as plt
 
# Sample the distribution we will use (by default a uniform distribution)   
total_draws = 100000
uni_min, uni_max = 0., 1.
ran_uniform_array = np.random.uniform(uni_min, uni_max, total_draws)

bins = 15  # bins for the historam

# Find the mean and standard deviation of our distribution, to use for 
#  plotting a comparison Gaussian distribution.
mu = ran_uniform_array.mean()
sigma = ran_uniform_array.std()

print(f' mean of uniform array = {mu:.3f}')
print(f' standard deviation of uniform array = {sigma:.3f}')

def histogram_ax(ax, means_array, N_means, sample_size, bins, CLT_pdf=False):
    """
    Plot a histogram on axis ax that shows the means.  Add the expected
     limiting normal distribution if CLT_pdf is True.
    """
    sigma_tilde = sigma / np.sqrt(sample_size)
    x_min = mu - 4.*sigma_tilde
    x_max = mu + 4.*sigma_tilde
    
    (_, bin_array, _) = ax.hist(means_array[:N_means], bins = bins, 
                                    align='mid')
    bin_width = bin_array[1] - bin_array[0]
    title_string = fr'Sampling size n={sample_size} of uniform PDF ' + \
                   fr'drawn {N_means:d} times'
    ax.set_title(title_string)
    ax.set_xlabel('Value of Mean')
    ax.set_ylabel('Count in bin')
    ax.set_xlim(x_min, x_max)

    if (CLT_pdf):  # if true, plot a normal PDF with the same mu and sigma
                   #  divided by the sqrt of the sample size.
        x_pts = np.linspace(x_min, x_max, 200)
        y_pts = stats.norm.pdf(x_pts, mu, sigma_tilde)
        ax.plot(x_pts, y_pts * (bin_width*N_means), color='red')


def plot_sample_result(sample_size, bins):
    """Plot a series of histograms to show the approach to a Gaussian."""
    sample_means_fixed_sample_size = []
    for i in range(10000):
        samples = ran_uniform_array[np.random.randint(ran_uniform_array.size, 
                                                      size = sample_size)]
        sample_means_fixed_sample_size.append(np.mean(samples))
    
    N_means_array = np.array([1, 5, 10, 20, 50, 100, 500, 1000, 10000])
    
    fig3 = plt.figure(figsize=(15,10))
    
    axes = fig3.subplots(nrows=3, ncols=3)
    fig3.suptitle(f'Sample size n={sample_size:d} sampled by various times', 
                  fontsize=16, va='baseline')
     
    for index, ax in enumerate(axes.flatten()):
        histogram_ax(ax, sample_means_fixed_sample_size, N_means_array[index], 
                     sample_size, bins, CLT_pdf=True)
         
    fig3.tight_layout(w_pad=1.8)
    fig3.subplots_adjust(top = 0.92)        

plot_sample_result(1, 20)   # n=1 so just the original distribution
```

As expected, we just get a better and better reproduction of the original distribution, which is uniform in this case. We don't expect any connection to a Gaussian from the CLT in this case. That is, just taking a lot of samples from a distribution doesn't mean in general that we will get a normal distribution.

#### Second example: each sample is two points

So the mean is the average of the two points. We divide the means into 20 bins.

```{code-cell} python3
:label: CLT-visualization-3
:tags: [hide-input]

plot_sample_result(2, 20)
```

As the number of means gets larger, we see that a peak develops at 1/2 and the shape becomes triangular. If we think of the average of two uniformly drawn points from \[0,1\], it is most likely that their average will be close to 1/2 and unlikely to be at the ends (e.g., to get near 0, one would need both numbers to be close to 0).

#### Third example: each sample is 10 points

Now we see the trends from $n=2$ being accentuated. By the time we have 10000 means to histogram, it looks like a pretty good Gaussian. **Note that the width of the Gaussian is set by the sample size $n=10$, not by how many draws are made.** The width decreases as $1/\sqrt{n}$, so from $n=2$ above to $n=10$ here it is roughly a factor of 2.2 smaller (0.25 vs. 0.1).

```{code-cell} python3
:label: CLT-visualization-3
:tags: [hide-input]

plot_sample_result(10, 20)
```

#### Fourth example: each sample is 50 points

By now we are taking the mean of 50 points with each sample. This will increasingly be close to 1/2 and very rarely far from 1/2. The width decreases as $1/\sqrt{n}$, so from $n=10$ to $n=50$ it is roughly a factor of 2.2 smaller (0.1 vs. 0.04).

```{code-cell} python3
:label: CLT-visualization-4
:tags: [hide-input]

plot_sample_result(50, 20)
```

### Adding $n$ variables drawn from a distribution

We'll use the results derived for combining $n$ variables drawn from the same zero-mean probability distribution with an overall $1/\sqrt{n}$.  The generalization to different PDFs (and to non-zero means) is straightforward.

$$ \begin{aligned}
  p(z)  &= \int_{-\infty}^{+\infty} \frac{d\omega}{2\pi}\, e^{-i\omega z}
    \left[ \int_{-\infty}^{+\infty}\! dx_1\, e^{i\omega x_1/\sqrt{n}} p(x_1) \right]
    \left[ \int_{-\infty}^{+\infty}\! dx_2\, e^{i\omega x_2/\sqrt{n}} p(x_2) \right]
    \cdots
    \\
    & \qquad\times
    \left[ \int_{-\infty}^{+\infty}\! dx_{n-1}\, e^{i\omega x_{n-1}/\sqrt{n}} p(x_{n-1}) \right]
    \left[ \int_{-\infty}^{+\infty}\! dx_n\, e^{i\omega x_n/\sqrt{n}} p(x_n) \right]
\end{aligned} $$

So the idea will be to take a distribution, do an FT with the frequency divided by $\sqrt{n}$, raise it to the $n^{\rm th}$ power, then do an inverse FT.  This should approach a Gaussian as $n$ gets large based on the proof we worked through.


In the widget below
we'll start with a uniform distribution again.
(For better viewing, toggle the left table of contents with the three-line icon at the top left of the page.)
The plot below on the right are the $n$ products of the Fourier-transformed distributions
(so this is in the Fourier space) with the frequency divided by $\sqrt{n}$. 
The plots on the left are the inverse Fourier transforms of the plots on the right.
You can adjust $n$ with the slider.

<!--
```{code-cell} python3
:label: CLT-visualization-5
:tags: [hide-input]

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

try:
    trapezoid = np.trapezoid
except AttributeError:
    trapezoid = np.trapz

def invCFT(t, omega_pts, FT_pts):
    """Inverse Fourier transform for an even transform sampled on omega_pts."""
    integrand_pts = np.cos(omega_pts * t) * FT_pts
    return trapezoid(integrand_pts, omega_pts) / (2. * np.pi)

def gaussian(x, sigma=1.):
    """One-dimensional normalized Gaussian."""
    return (1. / np.sqrt(2. * np.pi * sigma**2)
            * np.exp(-x**2 / (2. * sigma**2)))

def FT_uniform_scaled_sum(omega_pts, n):
    """
    Characteristic function of (X1+...+Xn)/sqrt(n),
    where Xi ~ Uniform[-1, 1].
    """
    z = omega_pts / (np.pi * np.sqrt(n))
    return np.sinc(z)**n

# x range
x_pts = np.linspace(-4., 4., 401)

# uniform distribution from -1 to +1
uni_dist = stats.uniform(loc=-1., scale=2.)
uni_dist_pts = uni_dist.pdf(x_pts)

# CLT Gaussian has the same variance as Uniform[-1,1], namely 1/3
uni_gauss_pts = gaussian(x_pts, sigma=uni_dist.std())

# omega range
omega_pts = np.linspace(-40., 40., 401)

n_vals = np.array([1, 2, 3, 4, 5, 8])

FT_uniform_pts = np.array([
    FT_uniform_scaled_sum(omega_pts, n) for n in n_vals
])

invFT_uniform_pts = np.array([
    [invCFT(x, omega_pts, FT_uniform_pts[i]) for x in x_pts]
    for i in range(n_vals.size)
])

with plt.rc_context({
    "font.size": 18,
    "axes.titlesize": 18,
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,
    "legend.fontsize": 16,
}):
    fig, ax = plt.subplots(n_vals.size, 2, figsize=(15, 5 * n_vals.size))
    
    for index, n in enumerate(n_vals):
        ax[index, 0].plot(
            x_pts, invFT_uniform_pts[index],
            color='blue', label=rf'invFT[uniform] $n={n}$'
        )
        ax[index, 0].plot(
            x_pts, uni_gauss_pts,
            color='red', label='CLT gaussian'
        )
        ax[index, 0].legend()
        ax[index, 0].set_title(rf'$n = {n}$')
    
        ax[index, 1].plot(
            omega_pts, FT_uniform_pts[index],
            color='blue', label=rf'FT[uniform] $n={n}$'
        )
        ax[index, 1].legend()
        ax[index, 1].set_title(rf'$n = {n}$')
    
    fig.tight_layout()
```
-->


```{raw} html
<iframe src="../../../_static/clt_characteristic_function_widget.html"
    width="100%"
    height="920"
    style="border: none;"
    scrolling="no">
</iframe>
```

So we see that multiplying the original Fourier transform will rapidly kill off the tails and highlight the central part. The $n$ scalings enforce that the Gaussians in both the original and Fourier space have constant variances.

Try some of the other distributions from the pull-down menu.