---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:acquisition-functions)=
# Acquisition functions

We will consider two different acquisition functions:
* Expected Improvement (EI)
* Lower Confidence Bound (LCB)


Note that we abbreviate the notation below and write $\mathcal{A}(\mathbf{\theta}) \equiv \mathcal{A}(\mathbf{\theta}| D)$.

## Expected Improvement
The expected improvement acquisition function is defined by the
expectation value of the rectifier ${\rm max}(0,f_{\rm min} -
f(\mathbf{\theta}))$, i.e. we reward any expected reduction of $f$ in
proportion to the reduction $f_{\rm min} - f(\mathbf{\theta})$. This can be evaluated analytically

$$
\begin{align}
  \begin{split}
    \mathcal{A}_{\rm EI}({\mathbf{\theta}})=  \langle {\rm max}(0,f_{\rm min} - f(\mathbf{\theta})) \rangle &= \int_{-\infty}^{\infty} {\rm max}(0,f_{\rm min}-f)\mathcal{N}(f(\mathbf{\theta})|\mu(\mathbf{\theta}),\sigma(\mathbf{\theta})^2)\,\, df(\mathbf{\theta}) \\
           &= \int_{-\infty}^{f_{\rm min}} (f_{\rm min} - f) \frac{1}{\sqrt{2\pi \sigma^2}}\exp\left[{-\frac{(f-\mu)^2}{2\sigma^2}}\right] \,\,df  \\
            &= (f_{\rm min} - \mu)\Phi\left(\frac{f_{\rm min} - \mu}{\sigma}\right) + \sigma \phi\left(\frac{f_{\rm min} - \mu}{\sigma}\right) \\
            &= \sigma \left( z \Phi(z) + \phi(z) \right),
  \end{split}  
\end{align}
$$


where

$$
\mathcal{N}(f(\mathbf{\theta})|\mu(\mathbf{\theta}),\sigma(\mathbf{\theta})^2)
$$

indicates the density function of the normal distribution, whereas the standard normal distribution and the cumulative
distribution function are denoted
$\phi$ and $\Phi$, respectively, and we dropped the explicit
dependence on $\mathbf{\theta}$ in the third step. 

In the last step we
write the result in the standard normal variable $z=\frac{f_{\rm
    min}-\mu}{\sigma}$. BayesOpt will exploit regions of expected
improvement when the term $z \Phi(z)$ dominates, while new, unknown
regions will be explored when the second term $\phi(z)$ dominates. For
the expected improvement acquisition function, the
exploration-exploitation balance is entirely determined by the set of
observed data $\mathcal{D}_n$ and the $\mathcal{GP}$ kernel.

Note 1: Density function of the normal distribution:
  $\mathcal{N}(\theta|\mu,\sigma^2) =
  \frac{1}{\sqrt{2\pi}\sigma}\exp\left(
  -\frac{1}{2\sigma^2}(\theta-\mu)^2\right)$ 
  
 Note 2: Density function of the *standard* normal distribution: $\phi(z) \equiv \mathcal{N}(z|\mu=0,\sigma^2=1) = \frac{1}{\sqrt{2 \pi}}\exp\left( -\frac{1}{2}z^2\right)$
 
 Note 3: Cumulative distribution function of the standard normal: $\Phi(z) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{z}\exp\left(-\frac{t^2}{2}\right)\, dt$

## Lower Confidence Bound
The lower confidence-bound acquisition function introduces an additional
parameter $\beta$ that explicitly sets the level of exploration

$$
  \mathcal{A}(\mathbf{\theta})_{\rm LCB} = \beta \sigma(\mathbf{\theta}) - \mu(\mathbf{\theta}).
$$

The maximum of this acquisition function will occur for the maximum of
the $\beta$-enlarged confidence envelope of the $\mathcal{GP}$. We
use $\beta=2$, which is a very common setting. Larger values of
$\beta$ leads to even more explorative BayesOpt algorithms. 
