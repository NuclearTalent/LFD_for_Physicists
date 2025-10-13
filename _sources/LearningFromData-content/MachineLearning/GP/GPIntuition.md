---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(sec:GPIntuition)=
# Intuition from Gaussian process websites

Here are four websites with Gaussian process visualizations and some things to try with each to help build intuition about GPs.

1. The  [*Sample Size Calculations for Computer Experiments*](https://harario.shinyapps.io/Sample_Size_Shiny/) app provides a sandbox for playing with Gaussian processes. Read the "About" tab first; it includes definitions of parameters used in the GP "correlation family" (which define the covariance). The "Sample Path Plots" tab has an app that lets you draw samples of functions that depend on user selected parameters (actually "hyperparameters") that specify the details of the correlation family.

    * Start with *Sample Path Plots*.
    * Try changing *Correlation length* (switch "No. of realizations" to get new draws).
    * Change "Select correlation family".
        * Note the extra parameter with Matern.
    * See the "About" tab for formulas.

2. The [*Gaussian process regression: a function space perspective*](http://rpradeep.me/gpr/) app by Pradeep Ranganathan "demonstrates how a GP prior is a distribution over functions, and how observing data conditions the prior to obtain the GP posterior." 

    * You should see successive draws from a GP.
    * Try changing the covariance and length scale; does it change as predicted?
    * Now try adding points. What happens?
    * Try adjusting the noise. What happens?

3. The [*Gaussian process regression demo*](http://www.tmpl.fi/gp/ ) app "demonstrates Gaussian process regression with one covariate and a set of different covariance kernels." 

    * Check "Show mean and credible intervals" and "sample independently".
    * Add observations.
    * Add a new process.  

4. [*A visual exploration of Gaussian processes*](https://distill.pub/2019/visual-exploration-gaussian-processes/) is a complete run-through of Gaussian processes.

    * Try changing the covariance matrix under *Multivariate Gaussian distributions*.
    * Try the different kernels under *Gaussian Processes / Kernels*.
    * Under *Gaussian Processes*, try *Prior distribution* and *Posterior distribution*.
    * Try *Gaussian Processes / Combining different kernels*.


