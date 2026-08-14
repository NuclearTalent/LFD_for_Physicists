---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:probabilistic-model)=
<!-- !split -->
# Probabilistic model

A Bayesian neural network can be viewed as probabilistic model in which we want to infer $p(y \lvert \boldsymbol{x},\mathcal{D})$ where $\mathcal{D} = \left\{\boldsymbol{x}^{(i)}, y^{(i)}\right\}$ is a given training dataset. 

We construct the likelihood function $p(\mathcal{D} \lvert \boldsymbol{w}) = \prod_i p(y^{(i)} \lvert \boldsymbol{x}^{(i)}, \boldsymbol{w})$ which is a function of parameters $\boldsymbol{w}$. Maximizing the likelihood function gives the maximimum likelihood estimate (MLE) of $\boldsymbol{w}$. The usual optimization objective during training is the negative log likelihood. For a categorical distribution this is the *cross entropy* error function, for a Gaussian distribution this is proportional to the *sum of squares* error function. MLE can lead to severe overfitting though.

Multiplying the likelihood with a prior distribution $p(\boldsymbol{w})$ is, by Bayes theorem, proportional to the posterior distribution $p(\boldsymbol{w} \lvert \mathcal{D}) \propto p(\mathcal{D} \lvert \boldsymbol{w}) p(\boldsymbol{w})$. Maximizing $p(\mathcal{D} \lvert \boldsymbol{w}) p(\boldsymbol{w})$ gives the maximum a posteriori (MAP) estimate of $\boldsymbol{w}$. Computing the MAP estimate has a regularizing effect and can prevent overfitting. The optimization objectives here are the same as for MLE plus a regularization term coming from the log prior.

Both MLE and MAP give point estimates of parameters. If we instead had a full posterior distribution over parameters we could make predictions that take weight uncertainty into account. This is covered by the posterior predictive distribution $p(y \lvert \boldsymbol{x},\mathcal{D}) = \int p(y \lvert \boldsymbol{x}, \boldsymbol{w}) p(\boldsymbol{w} \lvert \mathcal{D}) d\boldsymbol{w}$ in which the parameters have been marginalized out. This is equivalent to averaging predictions from an ensemble of neural networks weighted by the posterior probabilities of their parameters $\boldsymbol{w}$.

Returning to the binary classification problem, $y^{(n+1)}$ corresponds to the probability $p_{t^{(n+1)}=1}$ and a Bayesian prediction of a new datum $y^{(n+1)}$ will correspond to a pdf and involves *marginalizing* over the weight and bias parameters

$$
 p(y^{(n+1)} | x^{(n+1)}, D, \alpha) = \int d \boldsymbol{w} p( y^{(n+1)} | x^{(n+1)}, w, \alpha) p(w|D,\alpha), 
$$ (eq:binaryinference)

where we have also included the weight decay hyperparameter $\alpha$ from the prior (regularizer). Marginalization could, of course, also be performed over this parameter.

We show an example of such inference, comparing the point estimate $y(x; w^*, \alpha)$ and the Bayesian approach, in {numref}`fig-bnn_binary_classifier_mean`.

<!-- ![<p><em>The predictions for a Bayesian (left panel) and regular (right panel) binary classifier that has been learning from ten training data (circles) with a weight decay $\alpha = 1.0$. The decision boundary ($y=0.5$, i.e. the activation $a=0$) is shown together with the levels 0.12,0.27,0.73,0.88 (corresponding to the activation $a=\pm1,\pm2$). Test data is shown as plus symbols.</em></p>](../assets/bnn_binary_classifier_mean.png) -->

```{figure} ../assets/bnn_binary_classifier_mean.png
:name: fig-bnn_binary_classifier_mean

The predictions for a Bayesian (left panel) and regular (right panel) binary classifier that has been learning from ten training data (circles) with a weight decay $\alpha = 1.0$. The decision boundary ($y=0.5$, i.e. the activation $a=0$) is shown together with the levels 0.12,0.27,0.73,0.88 (corresponding to the activation $a=\pm1,\pm2$). Test data is shown as plus symbols.
```

The Bayesian classifier is based on sampling a very large ensamble of single neurons with different parameters. The distribution of these samples will be proportional to the posterior pdf for the parameters. The decision boundary shown in the figure is obtained as the mean of the predictions of the sampled neurons evaluated on a grid. It is clear that the Bayesian classifier is more uncertain about its predictions in the lower left and upper right corners, where there is little training data. 

This becomes even more clear when we plot the standard deviation of the predictions of the Bayesian classifier in {numref}`fig-bnn_binary_classifier_stddev`.

<!-- ![<p><em>The standard deviation of the class label predictions for a Bayesian binary classifier.</em></p>](../assets/bnn_binary_classifier_stddev.png) -->

```{figure} ../assets/bnn_binary_classifier_stddev.png
:name: fig-bnn_binary_classifier_stddev

The standard deviation of the class label predictions for a Bayesian binary classifier.
```

The predictions are rather certain along a diagonal line (close to the training data). Note that the interpretation of the prediction in the center of {numref}`fig-bnn_binary_classifier_stddev` (near $x_1,x_2 = 0,0$) is the following: The Bayesian binary classifier predicts a probability of $\sim 0.5$ for this point in the input parameter space to belong to class 1 (i.e. the decision is very uncertain). The Baysian classifier is also very certain about this uncertainty (the standard deviation is small).

In contrast, predictions for points in the upper left or lower right corners are very certain about the class label (and there is little uncertainty about this certainty).


