(sec:stat_example)=
# A tale of two models: contrasting BMA with BMM

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
