---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---
(sec:InformationCriteria)=
# Information criteria

Information criteria are computationally much easier than full evaluations of the evidence.
In this section we give a summary of some of the most common ICs and then give an example in some detail.

## Summary of information criteria

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


## Example: Information Criteria and Bayes factors

An example of applying Bayesian methods to perform model comparisons is ["Model comparison tests of modified gravity from the E&#246;t-Wash experiment"](https://iopscience.iop.org/article/10.1088/1475-7516/2020/07/006/pdf) by Krishak and Desai. They re-examine the claim in ["Hints of Modified Gravity in Cosmos and in the Lab?""](https://arxiv.org/abs/1904.09462) by Perivolaropoulos and Kazantzidis, made using frequentist methods, that there is evidence in the data of the E&#246;t-Wash experiment that looks for modifications of Newton's Law of Gravity on sub-millimeter scales for a residual spatially oscillating signal in the data. This could point to a modification of general relativity (in particular, of some type of nonlocal gravity theory) or it could be due to statistical or systematic uncertainties in the data.

The experiment under consideration is a modern version of the classic torsion balance experiments to measure the force due to gravity. In particular, it is sensitive to departures from Newtonian gravity at sub-millimeter scales. The data analysis from the experimenters do not indicate signs of new physics, but the re-analysis by Perivolaropoulos and Kazantzidis claims that the residual data has signatures of an oscillating signal. 

From [https://www.npl.washington.edu/eotwash/inverse-square-law](https://www.npl.washington.edu/eotwash/inverse-square-law): "Below is a cartoon of one of our initial experimental devices which illustrates the technique we employ to measure gravity at short length scales. The pendulum ring, with 10 small holes bored into it, hangs by a thin tungsten fiber (typically 20 microns thick) and acts as the detector mass. The rotating plate just below it, with 10 similar holes bored into it, acts as the drive mass providing gravitational pull on the pendulum that twists it back and forth 10 times for every revolution of the plate. The pendulum twist is measured by shining a laser beam off of a mirror mounted above the ring. The induced twist (torque) on the pendulum at varying separation distances is then compared to a detailed Newtonian calculation of the system. For many of our measurements, the rotating attractor situated just below the detector ring actually consists of 2 disks. The upper disk has holes identical to those in the detector ring. The lower, thicker attractor disk also has a similar hole pattern bored into it, but these larger holes are rotated compared to those in the upper disk, so that they lie halfway between the holes in the upper disk. If the inverse-square law is correct, the lower holes are designed such that they produce a twist on the ring that just cancels the twist induced by the upper disk. However, if gravity changes strength at short distances as the theories suggest, the twist induced by the lower disk, which is farther from the ring, will no longer cancel the twist from the upper disk and we will see a clear twist signal. The actual situation is a bit more complicated; for ordinary gravity the cancellation is exact only for one particular separation between the ring and the attractor, but the variation of the magnitude of the twist with changing separation between the ring and the disks provides a clear 'signature' for any new gravitational or other short-range phenomena."

```{image} ../assets/schematic_image_of_Eot-Wash_apparatus.jpg
:alt: Schematic image of Eot-Wash apparatus
:class: bg-primary
:width: 300px
:align: center
```

There are 87 residual torque data points ($\delta \tau$) between measured torques and expected Newtonian values. Perivolaropoulos and Kazantzidis made fits to three functions (models):

$$\begin{align}
  \delta\tau_1(\alpha',m',r) &= \alpha' \qquad \text{offset Newtonian potential} \\
  \delta\tau_2(\alpha',m',r) &= \alpha' e^{-m'r} \\
  \delta\tau_3(\alpha',m',r) &= \alpha' \cos(m'r + \phi)
\end{align}$$

Figures of the data and some fits from figures in the two papers are shown here.

```{image} ../assets/best_fit_models_for_Eot-Wash_data.png
:alt: Data and best fit models for Eot-Wash experiment
:class: bg-primary
:width: 700px
:align: center
```

```{image} ../assets/best_fit_models_for_Eot-Wash_data_better.png
:alt: Data and best fit models for Eot-Wash experiment
:class: bg-primary
:width: 600px
:align: center
```

Next we have tables from Krishak and Desai showing the best-fit results and the adopted priors.

```{image} ../assets/Tables_1_and_2_for_Eot-Wash_data.png
:alt: Tables showing parametrizations and priors
:class: bg-primary
:width: 600px
:align: center
```

Krishak and Desai applied AIC, BIC, WAIC, and calculated the Bayes factor (ratio of Bayesian evidences).

```{image} ../assets/Table_3_for_Eot-Wash_data.png
:alt: Table showing model comparisons
:class: bg-primary
:width: 600px
:align: center
```

Conclusions were based on interpretive scales found in the literature. 
For example:

<div style="text-align: center;">

|$\Delta$BIC | Evidence against Model $i$ |
| --- | --- |
| 0 − 2 | Not Worth More Than A Bare Mention |
| 2 − 6 | Positive |
| 6 − 10 | Strong | 
| $> 10$ | Very Strong |

</div>
    
For interpreting the Bayes' factor the Jeffrey's scale is used: a     value above 10 represents *strong* evidence in favor of the model     in the numerator while a value above 100 represents *decisive*     evidence.
Krishak and Desai conclude that there is decisive support that the oscillating model with fixed phase (from the Perivolaropoulos and Kazantzidis fit) and strong evidence for varying phase. However, this statistical analysis does not distinguish between a physics origin and statistical effects in the data.
Note: Krishak and Desai use nested sampling software to evaluate the evidence. 

