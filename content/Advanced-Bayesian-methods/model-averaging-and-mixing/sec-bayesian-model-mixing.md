(sec:BMMgeneralities)=
# Using Bayesian model mixing to open the model space


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
