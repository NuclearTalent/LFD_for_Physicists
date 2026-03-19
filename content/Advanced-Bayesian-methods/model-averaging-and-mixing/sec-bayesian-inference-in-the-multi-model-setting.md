(sec:theory)=
# Bayesian inference in the multi-model setting


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

