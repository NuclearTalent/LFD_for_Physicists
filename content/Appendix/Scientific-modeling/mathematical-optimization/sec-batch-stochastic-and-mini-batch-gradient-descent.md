# Batch, stochastic and mini-batch gradient descent

{{ sub_extra_tif385_admonition }}

The use of the full data set in the cost function for every parameter update would correspond to *batch gradient descent* (BGD). The gradient of the cost function then has the following generic form

\begin{equation}
\boldsymbol{\nabla} C_n \equiv \left. \boldsymbol{\nabla}_{\pars} C(\pars) \right|_{\pars=\pars_n}
= \sum_{i=1}^{N_d} \left. \boldsymbol{\nabla}_{\pars} C^{(i)}(\pars) \right|_{\pars=\pars_n},
\end{equation}

where the sum runs over the data set (of length $N_d$) and $C^{(i)}(\pars)$ is the cost function evaluated for a single data instance $\data_i = (\inputs_i, \outputs_i)$.

A typical Python implementation of batch gradient descent would look something like the following:

```python
# Pseudo-code for batch gradient descent
for i in range(N_epochs):
  params_gradient = evaluate_gradient(cost_function, data, params)
  params = params - learning_rate * params_gradient
```
for a fixed numer of epochs `N_epochs` and a function `evaluate_gradient` that returns the gradient vector of the cost function (that depends on the data `data` and the model parameters `params`) with respect to the parameters. The update step depends on the `learning_rate` hyperparameter.

Depending on the size of the data set, batch gradient descent can be rather inefficient since all data must be processed to perform a single parameter update. Instead, one often employs *stochastic gradient descent* (SGD) for which parameter updates are performed for every data instance $\data_i = (\inputs_i, \outputs_i)$ one at a time. Note that the total number of iterations for SGD is $N_\mathrm{epochs} \times N_d$.

SGD performs frequent and fast updates of the paranmeters. The updates are often characterized by a high variance that can cause the cost function to fluctuate heavily during the iterations. This ultimately complicates convergence to the exact minimum, as SGD will keep overshooting. However, employing a learning rate that slowly decreases with iterations can make SGD more efficient. A typical Python implementation would look something like the following:

```python
# Pseudo-code for stochastic gradient descent
for i in range(N_epochs):
  np.random.shuffle(data)
  learning_rate = decreasing_learning_rate(i)
  for data_instance in data:
    params_gradient = evaluate_gradient(cost_function, data_instance, params)
    params = params - learning_rate * params_gradient
```

where you should note the loop over all data instances for each epoch. To improve convergence and generalization to other data it is important that we shuffle the training data at every epoch.

Finally, *mini-batch gradient descent* (MBGD) combines the best of the previous algorithms and performs an update for every mini-batch of data

\begin{equation}
\pars \mapsto \pars - \eta \boldsymbol{\nabla} C_{i N_\mathrm{mb}:(i+1) N_\mathrm{mb}}(\pars),
\end{equation}

where $N_\mathrm{mb}$ is the mini-batch size. This way one can make use of highly optimized matrix optimizations for the reasonably sized mini-batch evaluations, and one usually finds much reduced variance of the parameter updates which can lead to more stable convergence. Mini-batch gradient descent is typically the algorithm of choice when training a neural network. The total number of parameter updates for MBGD is $N_\mathrm{epochs} \times N_d / N_{mb}$.

```python
# Pseudo-code for mini-batch gradient descent
for i in range(N_epochs):
  np.random.shuffle(data)
  learning_rate = decreasing_learning_rate(i)
  for data_batch in get_batches(data, batch_size=50):
    params_gradient = evaluate_gradient(cost_function, data_batch, params)
    params = params - learning_rate * params_gradient
```

Be aware that the terms stochastic or batch gradient descent can both be used to denote mini-batch gradient descent. 

