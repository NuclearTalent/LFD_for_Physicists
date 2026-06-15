---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---


# Criticality analysis


## Variance

:::{figure} ../assets/ANNFT_variance_ReLU_notes.png
:height: 150px
:name: fig-ANNFT-variance_ReLU_notes
:::

:::{figure} ../assets/ANNFT_variance_Softplus_notes.png
:height: 180px
:name: fig-ANNFT-variance_Softplus_notes
:::



:::{figure} ../assets/ANNFT_variance_plots2.png
:height: 750px
:name: fig-ANNFT_variance_plots
The final layer pre-training output variance as a function of neural network depth with a fixed width of 240. 
    Results are given for a ReLU activation function tuned  (a) below ($C_W = 1.0$, $C_b = 0.0$), \(c\) at the critical point ($C_W = 2.0$, $C_b = 0.0$), and (e) above ($C_W = 3.0$, $C_b = 0.0$) and for a Softplus activation function with  (b) lowest, (d) intermediate, and (f) highest initialization widths for the weights by using the same initialization hyperparameters as the ReLU.
    The measured variance is plotted in blue, a recursive calculation using empirical values of the variance is plotted as a dashed red line, and a recursive calculation using only theoretically calculated variances is plotted as a dashed pink line.
    When above/below the critical values of the initialization width, the variance explodes/vanishes with depth. When the ReLU network is tuned to critical initialization, the variance is fixed with depth. The Softplus activations do not have a critical point for initialization. As such, the Softplus variance either grows or asymptotes towards a constant value with depth, and does not have initialization hyperparameters that give a fixed variance with depth.
:::

## Excess kurtosis


:::{figure} ../assets/ANNFT_excess_kurtosis_I.png
:height: 400px
:name: fig-ANNFT-excess-kurtosis_I
:::


:::{figure} ../assets/ANNFT_excess_kurtosis_II.png
:height: 400px
:name: fig-ANNFT-excess-kurtosis_II
:::


:::{figure} ../assets/ANNFT_excess_kurtosis_ReLU_notes.png
:height: 180px
:name: fig-ANNFT-excess-kurtosis_ReLU_notes
:::

:::{figure} ../assets/ANNFT_excess_kurtosis_Softplus_notes.png
:height: 180px
:name: fig-ANNFT-excess-kurtosis_Softplus_notes
:::


:::{figure} ../assets/ANNFT_kurtosis_plots2.png
:height: 750px
:name: fig-ANNFT_kurtosis_plots
The final-layer pre-training-output (unstandardized) excess kurtosis (abbreviated here as EK, and also known as the non-Gaussian 4-point correlations) as a function of neural network depth with a fixed width of 240. 
    Results are given for a ReLU activation function tuned  (a) below ($C_W=1.0$, $C_b=0.0$), \(c\) at the critical point ($C_W=2.0$, $C_b=0.0$) and (e) above ($C_W=3.0$, $C_b=0.0$), and for a Softplus activation function with (b) lowest, (d) intermediate, and (f) highest initialization widths for the weights by using the same initialization hyperparameters as ReLU.
    The measured EK is plotted as a green line, a recursive calculation of EK using empirical values of the variance and initial EK is plotted as a dashed red line, and a recursive calculation using only theoretical values is plotted as a dashed pink line.
    An additional blue line is present in (e), representing an exact calculation of the critical EK without treating $1/n$ terms as subleading.
    When critically tuned, ReLU networks' EK behaves linearly with depth as predicted by ANNFT, demonstrating that the higher-order moments of the distribution are controlled by an expansion in $r$.
    Non-critical distributions are seen to grow non-linearly with depth, reflecting that criticality allows for a perturbative ANNFT that lets deeper network network behavior to be analyzed.
:::


## The story so far

:::{figure} ../assets/ANNFT_story_so_far.png
:height: 350px
:name: fig-ANNFT-story-so-far
:::

