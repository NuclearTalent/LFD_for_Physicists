(sec:ModelMixing)=
# Model mixing



## Bayesian inference for multiple models

This excerpt is from the BAND Manifesto.

In this section we discuss the challenge of combining the insights from a number of individual physics models to produce inference endowed with the physics models' collective wisdom. Section {ref}`subsec:theory` provides the general setup for this problem, and introduces the crucial distinction between ${\cal M}$-closed and ${\cal M}$-open settings. Section {ref}`subsec:BMA` describes the standard Bayesian solution: Bayesian Model Averaging (BMA); we then explain why BMA can only resolve the challenge in the ${\cal M}$-closed context. Section {ref}`subsec:BMMgeneralities` then articulates paths to generalize BMA to a more sophisticated Bayesian Model Mixing (BMM), wherein we combine information from different models in a more textured way than BMA accomplishes. We end with Section {ref}`subsec:stat_example`, which gives an example where BMM improves upon BMA by leveraging information on the local performance of two different models across the input domain.

(subsec:theory)=
### Bayesian inference in the multi-model setting


Recall that our generic setup is that we have observations $\data$ consisting of pairs of inputs and outputs $(x_1,y_1),\ldots,(x_n,y_n)$ and 
want to, from these, predict quantities of interest $\qoi$, which could be parameters, or interpolations or extrapolations, or even some totally new observable.
In this section we further suppose we have several  physics models $f_k$  ($k = 1,\ldots,K)$ that are purported to be a mapping from an  $x$ to a $y$.  Each physics model takes in an input setting $x \in \mathcal{X}$ and a parameter setting $\theta_k \in \Theta_k$. The $k$th physics model is represented  by $f_k(x,\theta_k)$, which should be considered a deterministic prediction of the observable at $x$ once the model $k$ and parameters $\theta_k$ are specified.  One can build a  model $\mathcal{M}_k$ for  observables by combining a physics model with an error term $\varepsilon$ that represents all uncertainties (systematic, statistical, computational):

$$
\mathcal{M}_k : y_i = f_k(x_i,\theta_k) + \varepsilon_{i,k} 
$$ (eq-stand_model)

Usually, $\varepsilon_{i,k}$---the error of the $i$th observation in the $k$th model---is decomposed into a stochastic term modeling systematic discrepancy and an independent term.  Note that the error does not always have to be an additive form, but we have displayed it as such for simplicity. Moreover, as written above, $\varepsilon_{i,k}$ depends on the physics model as well as on (hyper)parameters describing the statistical model, but this notation is suppressed as the dependence involves complex factors.

While different physics models may have different parameters, inference on multiple models involves dealing with a canonical parameter space $\Theta$ that spans all models of interest. We assume that for each $k$ in $\{1,\ldots,K\}$, the model-specific parameter space $\Theta_k$ can be mapped to $\Theta$ via some (possibly non-invertible) map $\mathcal{T}_k: {\Theta}_k \mapsto \Theta$. 
After transformation, we say the parameters are in the canonical parameter space, and simply write our canonical parameter as $\theta \in \Theta$ since $\Theta$ is common to all models after the application of $\mathcal{T}_k.$  We can think of this overall parameter space $\Theta$ as the union of the individual (transformed) model-specific parameters arising out of each model.  For notational simplicity, the $\mathcal{T}_k$ function will be suppressed throughout this article, meaning $\theta$ is understood as $\mathcal{T}_k(\theta_k)$ when appropriate. 

Our goal is to conduct inference on the values of $\theta$ as well as the error term $\varepsilon_{i,k}$ for each model using Bayesian inference. Three conceptual settings have been identified  (see, e.g., \cite{Bernardo94}) where Bayesian inference on multiple models is applied: $\mathcal{M}-$closed, $\mathcal{M}-$open, and $\mathcal{M}-$complete.  These three settings were originally motivated in the context of statistical model building.  In the $\mathcal{M}-$closed case, one has "closed off" the need to introduce new models as it is known that the *perfect model* that represents the physical reality  must be within the set of models being considered. Therefore, as data become more numerous and/or precise in the $\mathcal{M}-$closed case, that perfect model will become increasingly more likely, ultimately to the exclusion of all other models under consideration. 
In the $\mathcal{M}-$open case, one is open to introducing new  models since the perfect model is not known.  In the $\mathcal{M}-$complete case, we have decided that while we might introduce new models for the sake of accuracy, we would like to maintain inference on those in our original model set.  We will not discuss this last case further.

The key distinction for inference in nuclear physics is between $\mathcal{M}-$closed, when the set of models is expected to include the perfect one, and $\mathcal{M}-$open, when we know that the set of models does not include the perfect one.  We briefly outline the standard statistical solution for the $\mathcal{M}-$closed setting in the next section before moving on to describing some potential approaches for the $\mathcal{M}-$open setting that is more  interesting in the context of the BAND framework.

(subsec:BMA)=
### Bayesian model averaging and the $\mathcal{M}$-closed assumption


Historically, mixing together different statistical models has been done through Bayesian model averaging (BMA).  BMA has been broadly applied in many areas of research including the physical and biological sciences, medicine, epidemiology, and  political and social sciences. For a recent survey of BMA applications, we refer to 
\cite{Fragoso2018}.    BMA is a  framework where several competing (or alternative) models $\mathcal{M}_1, \dots, \mathcal{M}_K$ are available. The BMA posterior density $p(\qoi|\data)$ corresponds to the linear combination of the posterior densities of the individual models:

$$ 
    p(\qoi|\data) = \sum_{k=1}^K p(\qoi|\data,\mathcal{M}_k)\, p(\mathcal{M}_k|\data) .
$$ (eqn-posteriorBMA)

If we pull through the typical inference, we can compute the first term $p(\qoi|\data,\mathcal{M}_k)$ by 

$$
p(\qoi|\data,\mathcal{M}_k)=\int_{\Theta} p(\qoi|\data,\mathcal{M}_k,\theta) p(\theta|\data,\mathcal{M}_k) \mathrm{d} \theta.
$$ (pofm1)

The second term in {ref}`eqn-posteriorBMA`, $p(\mathcal{M}_k|\data)$, represents the posterior probability that the  model $k$ is correct. It can be computed as

$$ 
p(\mathcal{M}_k|\data) = \frac{p(\data|\mathcal{M}_k)p(\mathcal{M}_k)}{\sum_{k=1}^K p(\data|\mathcal{M}_k)p(\mathcal{M}_k)}
$$ (pofm)

where

$$
p(\data|\mathcal{M}_k)= \int_{\Theta} p(\data|\mathcal{M}_k,\theta) p(\theta|\mathcal{M}_k) \mathrm{d} \theta.
$$

The BMA posterior ({ref}`eqn-posteriorBMA`) for $\qoi$ can then be obtained by using (\ref{pofm1}) and (\ref{pofm}).

The posterior probability of model $k$ being correct, 
$p(\mathcal{M}_k|\data)$,
accounts for the common physics assumptions or phenomenological properties being studied that may span many of these models.  But this framing works by choosing a single model that is dominant over the entire model space.    If a perfect model is explicitly considered, that is, if some $\mathcal{M}_k$ is correct, the corresponding term should dominate the sum in  (\ref{eqn:posteriorBMA}). However, generic BMA can lead to misleading results when a perfect model is not included.  One illustration is presented in  Section {ref}`subsec:stat_example`.  No nuclear physics models have access to an exact representation of reality; one only hopes some are usefully close to it. It is to be noted that while  using an $\mathcal{M}-$closed approach  may be problematic in many nuclear physics applications, there are nuclear physics cases when BMA can be useful~\cite{Jay2020}. 

But, more generally, to be useful for nuclear physics, Bayesian inference methods should account for the relative performance of models among the different observables.  Some early efforts in this direction include \cite{kejzlar2019bayesian,Kejzlar2020} which consider multiple models which do not live on a common domain, resulting in some models being useful for prediction in certain physical regimes but not others. 



(subsec:BMMgeneralities)=
### Using Bayesian model mixing to open the model space


Suppose then, that no models are exactly correct through the domain of interest. To conceptualize this situation we introduce 
 notation for the physical process $f_\star(\cdot, \theta)$, which gives the perfect (or oracle) model. 
That model's predictions are related to the experimental observations by:

$$
 y_i = f_\star(x_i,\theta) + \varepsilon_{i,\star}, 
$$ (eq-true_model)

where the set of $\varepsilon_{i,\star}$'s represent the error between the perfect model and  imperfect observations. Equation (\ref{eq:true_model}) is introduced purely for conceptual purposes. It is not practical because only an oracle has access to $f_\star(\cdot, \theta)$.  Someone who knows $f_\star$ because they have direct access to the underlying reality of the universe would likely not be bothered with statistical inference---or with the scientific process at all.  By presuming the $\mathcal{M}-$open scenario we invite the possibility that there is no $k$ for which $f_\star(\cdot, \theta)$ is equivalent to $f_k(\cdot,\theta)$.   The challenge is if that is true it breaks the statistical modeling principles that undergird the effectiveness of BMA as an inferential strategy. 

The generalized alternative framework we now present does not attempt to weight models based on their performance across the entire input space.  We say that such a generalized framework is an example of Bayesian model mixing (BMM).  Our approach has connections to existing statistical literature such as \cite{goldstein2009reified} in addition to the single-model frameworks of \cite{KoH} and \cite{higdon2004combining}.  Our objective is to establish different distributional assumptions beyond the assumption that any one model is perfect throughout the input space.    We do this by constructing a model $\mathcal{M}_\dagger$ that combines the physics models to inform on the observations:
\begin{equation}
\mathcal{M}_\dagger: y_i = f_\dagger(x_i,\theta) + \varepsilon_{\dagger,i},  \text{ where }  f_\dagger(\cdot, \theta) \text{ is formed by combining }f_1(\cdot,\theta),\ldots,f_K(\cdot,\theta). 
\label{eq:completeModel}
\end{equation}
The \emph{supermodel}  $f_\dagger$ is built to contain the collective wisdom of all existing models (this model was also termed reified in  Ref.~\cite{goldstein2009reified}).
One possible way to combine the models is BMA, where $f_\dagger(\cdot, \theta)$ has a prior distribution that is a point mass at each of $\{f_k(\cdot, \theta):k=1,\ldots,K\}$ that holds universally throughout the domain of interest. In BMM, we open up the possibility to combine the $K$ models in more sophisticated ways.   By mixing, one can form many potential inferences about $f_\dagger$, and---we hope---produce inferences using $f_\dagger$ that more closely resemble inferences produced by the oracle using $f_\star$.

The mixing approach would then give $p(\qoi|\data) = p(\qoi|\data,\mathcal{M}_\dagger).$  BMA is thus a particular special case of the BMM approach.  The key to the BAND BMM framework is that $\mathcal{M}_\dagger$ accounts for underlying information present in the individual models. In the next subsection we present an example where such an $\mathcal{M}_\dagger$ is constructed in a way that takes into account the different places in the input domain $\mathcal{X}$ in which each of them is more accurate.  


(subsec:stat_example)=
### A tale of two models: contrasting BMA with BMM} 

Let us discuss a brief statistical example to unpack the sometimes subtle difference between BMA and BMM.  This should not be considered a general assessment of the approaches, but instead an example to ground the concepts. For simplicity of presentation, we assume that we have two physics models: $f_1(\cdot,\theta)$ and $f_2(\cdot,\theta)$. We want to combine these two models to produce a model $f_\dagger$ that is as close to the perfect model $f_\star$ as possible. Since perfection is not attainable we distinguish between $f_\star$, which we continue to use as a {\it gedankenmodel}, and $f_\dagger$ and try only to build the latter. 

The first of the two models being mixed, $f_1$, is an imperfect model everywhere. Conceptually we imagine that, for all values of $x\in \lbrace x_1,\ldots,x_n\rbrace$, $f_1$ differs from $f_\star$ by a stochastic discrepancy a priori normally distributed with mean zero and some moderate variance. In contrast the second model, $f_2$, is such that there is a single observation, say the one at the first point $x_1$, for which $f_2(x_1,\theta) - f_\star(x_1,\theta)$ is potentially very large, i.e., here we think that the stochastic discrepancy is normally distributed with mean zero and an extremely large variance. But everywhere else the model is essentially perfect.
We convert this information into Bayesian inference for $f_\dagger$ by saying that $f_1(x_i,\theta)$ given $f_\dagger(x_i,\theta)$ is normally distributed with mean $f_\dagger(x_i,\theta)$ and variance $v_1$.   And that $f_2(x_1,\theta)$ given $f_\dagger(x_1,\theta)$ is normally distributed with mean $f_\dagger(x_1,\theta)$ and variance $v_2 \gg v_1$, while, for $j = 2,\ldots,n$, we have $f_2(x_j,\theta) = f_\dagger(x_j,\theta)$.  

A BMA approach that acknowledges these model discrepancies expands the observed variance by the model error variance.  We will assume each model has the same prior probability of being correct and the prior $p(\theta)$ on $\theta$ is given such that $p(\mathcal{M}_1,\theta) = p(\mathcal{M}_2,\theta) = \frac{1}{2}p(\theta)$.  In terms of a posterior on the parameters, this implies that


$$\begin{align}
p_{\rm BMA}(\theta | \data) \propto &\ p(\theta)\left[\prod_{i=1}^n\frac{1}{\sqrt{\sigma_i^2 + v_1}}  \exp \left(- \frac{1}{2} \frac{(y_i - f_1(x_i,\theta))^2}{\sigma_i^2 + v_1} \right)\right. \\\nonumber
+&\left.\frac{1}{\sqrt{\sigma_1^2 + v_2}}  \exp \left(- \frac{1}{2}  \frac{(y_1 - f_2(x_1,\theta))^2}{\sigma_1^2 + v_2}  \right) \prod_{i=2}^n\frac{1}{\sigma_i}  \exp\left(- \frac{1}{2}  \frac{(y_i - f_2(x_i,\theta))^2}{\sigma_i^2}   \right) \right] 
.
\end{align}$$ (simplemodel)

As mentioned previously, the BMA approach presumes that one model is correct throughout the entire domain of interest. If $v_2$ is truly extremely large, the BMA formalism will implement this presumption in the most extreme way possible. The spectacular failure of the second model at the first data point causes it to lose badly to the first model which just manages to be mediocre everywhere.  That is, the expression for the posterior when $v_2 \rightarrow \infty$ becomes

$$
p_{\text{BMA}}(\theta|\data) \propto \exp \left(- \frac{1}{2} \sum_{i=1}^n \frac{(y_i - f_1(x_i,\theta))^2}{\sigma_i^2 + v_1} \right) p(\theta).
$$

The model  $f_2$ has no role in the BMA posterior because the BMA weights consider only the overall performance of the model over the entire  domain of interest! But it seems unduly wasteful to discard the entirety of $f_2$ because it performs poorly in one small subset of the  domain of interest.

Now we consider a BMM approach where we do not presume a single model is correct throughout the entire input space. 
One potential BMM approach obtains the distribution of $f_\dagger(x,\theta)$ by using standard Bayesian updating formulae to combine the probability distributions
of $f_1(x,\theta)$ and $f_2(x,\theta)$ given $f_\dagger(x,\theta)$
with a Normally distributed prior on $f_\dagger$ having variance $v_\dagger$. Taking $v_{\dagger} \rightarrow \infty$, we have

$$
f_\dagger (x_i, \theta) \text{ is distributed as} \begin{cases}
\mathcal{N} \left(  \frac{v_2 f_1(x_i,\theta) + v_1 f_2 (x_i,\theta)}{ v_1  + v_2}, \frac{v_1v_2}{ v_1  + v_2} \right)& \text{ if }  i = 1 \\
f_2(x_i, \theta) & \text{ if } i = 2,\ldots,n.
 \end{cases}
$$ (eqn-fstarexample34)

This seems to use our inference on both $f_1$ and $f_2$ in an effective way.  Pulling this into a posterior, we get that at $v_2 \rightarrow \infty$ 

$$
p_{\text{BMM}}(\theta|\data) \propto \exp \left(- \frac{1}{2}  \frac{(y_1 - f_1(x_1,\theta))^2}{\sigma_1^2 + v_1} -\frac{1}{2}   \sum_{i=2}^n \frac{(y_i - f_2(x_i,\theta))^2}{\sigma_i^2} \right)  p(\theta).
$$

Now both models are being used in their respective strong areas: the model $f_2$ is ignored only at a single point $x_1$ where it is very wrong and $f_1$ is  ignored everywhere that $f_2$ provides a perfect result. 

This example illustrates nicely that BMM can be a more effective tool for combining models than BMA. Although the example is simple we believe the concept it represents has wide applicability  in NP applications  where the models we want to mix perform well in different regions of the domain of interest.


## 

