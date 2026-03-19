(sec:ExploringPDFsFollowups)=
# Follow-up questions and answers to the *Exploring PDFs* section.

Make sure to look at [](./Exploring_pdfs.ipynb)  first!


::::{admonition} Confidence intervals
:class: my-checkpoint
*Bayesian confidence intervals: how are they defined?* 
:::{admonition} Answer 
:class: dropdown, my-answer
**The Bayesian confidence or credible interval for a parameter with a one-dimenional PDF is defined for a given percentage, call it $\beta\%$. The interval is such that integrating over it one gets $\beta\%$ of the toal area under the PDF. This may not be uniquely defined if the PDF is multimodal or skewed.** 
:::
::::

::::{admonition} Point estimates
:class: my-checkpoint
*Various "point estimates" were introduced (mean, mode, median); which is "best" to use?* 
:::{admonition} Answer 
:class: dropdown, my-answer
**A point estimate is a one-number summary of a distribution. Which one is best to use depends on the application. Sometimes one wants to know the most likely case: then use the mode. Sometimes one really wants the average: then use the mean. Sometimes, for an asymmetric distribution, the median is the best estimate. For a symmetric, unimodal PDF, the three point estimates are the same. Note that to a Bayesian, a point estimate is only a rough approximation to the information in the full distribution.** 
:::
::::


::::{admonition} Characteristics of PDFs
:class: my-checkpoint
*What are the characteristics (e.g., symmetry, heavy tails, ...) of different pdfs: normal, beta, student t, $\chi^2$, \ldots* 
:::{admonition} Answer 
:class: dropdown, my-answer
**Check these yourself! Note that the answers will often depend on the parameter values for the distribution. A Student t distribution may have "heavy tails" (meaning more probability in the tails than a Gaussian would have) for some parameters but for others it approaches a normal distribution (so by construction no heavy tails).** 
:::
::::


::::{admonition} Sampling
:class: my-checkpoint
*What does sampling mean?* 
:::{admonition} Answer 
:class: dropdown, my-answer
**To sample a given distribution is to draw values with probabilities given by the distribution. In Bayesian inference one is most often sampling a posterior distribution.** 
:::
::::

::::{admonition} Verifying sampling
:class: my-checkpoint
*How do you know if a distribution is correctly sampled?* 
:::{admonition} Answer 
:class: dropdown, my-answer
**One way is to look at the (normalized)histogram. If correctly sampled, this should approximate the distribution and the approximation should improve with more samples.** 
:::
::::



