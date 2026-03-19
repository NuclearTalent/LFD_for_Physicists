# Information criteria

Information criteria are computationally much easier than full evaluations of the evidence.

**AIC:** *Akaiko Information Criteria*
This is essentially a frequentist approach as it relies solely on the likelihood (no priors involved). The quantity to calculate is:

$$
  \textit{AIC} = -2 \log p(D|\hat\thetavec_{\text{MLE}}) + 2k ,
$$

where $k$ is the number of free parameters and the probability distribution is the likelihood evaluated at the maximum likelihood values of the parameters.
In practice one compares the resulting quantity between the models in question.
It has the ingredients of evidence: an improved likelihood is balanced by a penalty for additional parameters. 
AIC is not well regarded by Bayesians.


**BIC:** *Bayesian Information Criteria*
This is a Gaussian approximation to the Bayesian evidence in the limit of a large amount of data.

$$
 \textit{BIC} = -2 \log p(D|\hat\thetavec_{\text{MLE}}) + k\ln N
$$

where $k$ is the number of fitted parameters and $N$ is the number of data points.
The BIC implicitly assumes that the Occam penalty is negligible.


**DIC:** *Deviance Information Criteria*
With the DIC, replace $\hat\thetavec_{\text{MLE}}$ by $\hat\thetavec_{\text{Bayes}}$, where the latter is the maximum of the posterior (as opposed to the maximum of the likelihood).
Use an effective number of parameters:

$$
  p_{DIC} = 2\log p(D|\hat\thetavec_{\text{Bayes}})
   - E[\log p(D|\thetavec)] ,
$$

where the last term averages $\thetavec$ over the posterior.
Then

$$
  \textit{DIC} = -2 \log p(D|\hat\thetavec_{\text{Bayes}}) + 2 p_{DIC} .
$$


**WAIC:** Widely Applicable Information Criteria*
This is favored by the authors of BDA-3 as being more fully Bayesian.
The implementation is: given samples $s = 1$ to $S$,

$$
  \textit{WAIC} = 2\sum_{i=1}^{n_{\text{data}}} 
    \Bigl(\log \frac{1}{S}\sum_{s=1}^S p(y_i|\thetavec^s)\Bigr)
  - \frac{1}{S}\sum_{s=1}^S \log p(D_i|\thetavec^s)
$$

The WAIC averages over the posterior distribution.
