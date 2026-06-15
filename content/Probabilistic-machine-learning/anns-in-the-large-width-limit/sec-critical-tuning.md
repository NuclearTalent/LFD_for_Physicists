---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:ANNFT-critical-tuning)=
# Critical tuning of hyperparameters

:::{figure} ../assets/ANNFT_critically_tuning_hyperparameters.png
:height: 400px
:name: fig-ANNFT_critically_tuning_hyperparameters
:::


:::{figure} ../assets/ANNFT_criticality_nuclear.png
:height: 400px
:name: fig-ANNFT_criticality_nuclear
:::


## Mean absolute error loss vs. epochs

:::{figure} ../assets/ANNFT_ReLU_MAE_loss.png
:height: 350px
:name: fig-ANNFT_ReLU_MAE_loss
The mean absolute error loss vs. epochs for ReLU activation functions. Hidden layer widths are at 100 neurons, and depths are 1,2,4, and 8 hidden layers. The CICT and CINT architectures outperform the NINT, and their performance improves with depth, whereas the NINT networks stagnate in performance after 2 hidden layers.
:::

:::{figure} ../assets/ANNFT_Tanh_MAE_loss.png
:height: 350px
:name: fig-ANNFT_Tanh_MAE_loss
Same as {numref}`fig-ANNFT_ReLU_MAE_loss` but for Tanh activation functions.
:::

