(sec:BMA)=
# Bayesian model averaging

Historically, mixing together different statistical models has been done through Bayesian model averaging (BMA).  BMA has been broadly applied in many areas of research including the physical and biological sciences, medicine, epidemiology, and  political and social sciences. For a recent survey of BMA applications, we refer to 
\cite{Fragoso2018}. BMA is a  framework where several competing (or alternative) models $\mathcal{M}_1, \dots, \mathcal{M}_K$ are available. The BMA posterior density $p(\qoi|\data)$ corresponds to the linear combination of the posterior densities of the individual models:

$$ 
    p(\qoi|\data) = \sum_{k=1}^K p(\qoi|\data,\mathcal{M}_k)\, p(\mathcal{M}_k|\data) .
$$ (eqn-posteriorBMA)

If we pull through the typical inference, we can compute the first term $p(\qoi|\data,\mathcal{M}_k)$ by 

$$
p(\qoi|\data,\mathcal{M}_k)=\int_{\Theta} p(\qoi|\data,\mathcal{M}_k,\theta) p(\theta|\data,\mathcal{M}_k) \mathrm{d} \theta.
$$ (eq:pofm1)

The second term in {eq}`eqn-posteriorBMA`, $p(\mathcal{M}_k|\data)$, represents the posterior probability that the  model $k$ is correct. It can be computed as

$$ 
p(\mathcal{M}_k|\data) = \frac{p(\data|\mathcal{M}_k)p(\mathcal{M}_k)}{\sum_{k=1}^K p(\data|\mathcal{M}_k)p(\mathcal{M}_k)}
$$ (eq:pofm)

where

$$
p(\data|\mathcal{M}_k)= \int_{\Theta} p(\data|\mathcal{M}_k,\theta) p(\theta|\mathcal{M}_k) \mathrm{d} \theta.
$$

The BMA posterior {eq}`eqn-posteriorBMA` for $\qoi$ can then be obtained by using {eq}`eq:pofm1` and {eq}`eq:pofm`.

The posterior probability of model $k$ being correct, 
$p(\mathcal{M}_k|\data)$,
accounts for the common physics assumptions or phenomenological properties being studied that may span many of these models.  But this framing works by choosing a single model that is dominant over the entire model space.    If a perfect model is explicitly considered, that is, if some $\mathcal{M}_k$ is correct, the corresponding term should dominate the sum in  (\ref{eqn:posteriorBMA}). However, generic BMA can lead to misleading results when a perfect model is not included.  One illustration is presented in  Section {ref}`sec:stat_example`.  No nuclear physics models have access to an exact representation of reality; one only hopes some are usefully close to it. It is to be noted that while  using an $\mathcal{M}-$closed approach  may be problematic in many nuclear physics applications, there are nuclear physics cases when BMA can be useful~\cite{Jay2020}. 

But, more generally, to be useful for nuclear physics, Bayesian inference methods should account for the relative performance of models among the different observables.  Some early efforts in this direction include \cite{kejzlar2019bayesian,Kejzlar2020} which consider multiple models which do not live on a common domain, resulting in some models being useful for prediction in certain physical regimes but not others. 
