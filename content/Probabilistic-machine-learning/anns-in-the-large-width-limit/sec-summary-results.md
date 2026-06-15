---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:ANNFT-summary-results)=
# Summary of results

Neural network criticality offers a means to understand neural network behavior, as well as providing prescriptions for architecture and training hyperparameters. 
Here we have explored the non-empirical approach to understanding ANNs using a field-theory-based criticality analysis (ANNFT). 
We used a protoypical nuclear physics ANN as a testbed, namely a two-input/one-output feed-forward network trained from the AME2020 dataset to fit nuclear binding energies.

In pre-training, we found the expected approach to Gaussian distributions for the final layer output distributions with fixed depth but increasing width.
Within small fluctuations, normal distributions were seen by a width of 120 neurons for both ReLU and Softplus activations and for every other activation function we have tried.
The correlations between pairs of input values with a width of 120 and increasing depths showed Gaussian process (GP) correlations with the predicted kernel at depth 1 and increasing correlations with additional hidden layers.

A comparison of measured variance and excess kurtosis (difference of the fourth moment from Gaussian expectations) from many initializations for a fixed width of 240 and increasing depths validates the theoretical predictions of criticality.
In particular, for the ReLU activation function the variance grows or shrinks with depth if the initialization hyperparameters are tuned above or below the predicted critical value.
At criticality the variance is flat.
In contrast, the Softplus activation function does not have a critical fixed point for initialization.
In accordance with theory, the variance either grows or asymptotes to a constant value with depth.
Non-zero excess kurtosis (EK) indicates non-Gaussian four-point correlations.
For both activation functions, the observed behavior of the EK with depth is in good accord with theoretical expectations.

Next we considered training of the ANN.
We followed the mean absolute error (MAE) loss for a large number of epochs with several different depths, using combinations of critical and non-critical initialization and training.
The networks with critical initialization and critical training (CICT) reached the lowest loss in all cases both for ReLU and Tanh activation functions, with particular contrast to when non-critical hyperparameters were used for both initialization and training.

Most practitioners do not encounter these issues even though they rarely pay attention to details of initialization and training.
This is because the critically tuned networks are still outperformed by adaptive optimizers.
Nevertheless, the results are comparable, and differ by a much smaller factor than when untuned.

Of particular interest is the prediction by ANNFT of different training regimes, characterized by the ratio of depth to width $r$. 
The predictive analyses of ANNFT are based on the validity of a Taylor series expansion about the initialization.
By considering the mean hidden-layer rms deviation and Frobenius norms of the weight matrices
before and after training, we can see that the conditions of small deviations from initialization are achieved with sufficiently small $r$.
The different learning regimes are manifested by looking at the rms deviation of the binding energy data and ANN outputs as a function of $r$, achieved by varying the width at fixed depth, and through heatmaps of global residuals across all $N$ and $Z$ for four different $r$ values.

The results validated that ANNFT offers insight into

* why networks that are wider than they are deep are preferred, as they will have correlations in their output distribution attenuated by the larger width;
* the success of activation functions such as ReLU or Tanh compared to Softplus or sigmoid;
* the success of certain initialization schemes (He initialization is reproduced by ReLU's critical initialization).

We restricted the training protocol in this work to facilitate a clean analysis of criticality,
but the door is open to explore heuristically successful approaches to network training in the context of ANNFT.


:::{figure} ../assets/ANNFT_benign_overfitting.png
:height: 400px
:name: fig-ANNFT_benign_overfitting
:::

