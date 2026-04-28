---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:GPIntuition)=
# Intuition for Gaussian process from simulations

## Websites with visualizations 

Here are four websites with Gaussian process (GP) visualizations and some things to try with each to help build intuition about GPs.
A GP defines a distribution over *functions*, so in each simulation we will see draws of random functions, in analogy to drawing random variables from a normal distribution (recall that "normal" and "Gaussian" are synonymous here). 
Our principal goal is to experience how GPs look in practice.

The defining feature of an ensemble of GP function draws is that at *any* fixed point, the histogram of the function values at that point would approximate a Gaussian distribution; while for any two points the function values would be draws from a bivariate Gaussian distribution with a proscribed covariance matrix; and so on with more points being draws from a multivariate Gaussian distribution. The covariance in each case between any two points is specified by a *kernel* evaluated at those points. 

1. The  [*Sample Size Calculations for Computer Experiments*](https://harario.shinyapps.io/Sample_Size_Shiny/) app provides a sandbox for playing with Gaussian processes. Read the "About" tab first; it includes definitions of parameters used in the GP "correlation family" (which define the covariance). The "Sample Path Plots" tab has an app that lets you draw samples of functions that depend on user selected parameters (actually "hyperparameters") that specify the details of the correlation family.

    * Start with *Sample Path Plots*. These are draws from a GP, with each draw a function plotted from $x=0$ to $x=1$. Change the number (No.) of realizations to 1, 5, 10, 100, 1000. Look at any fixed $x$ value, draw a vertical line, and visualize the histogram; does it look like a Gaussian distribution?
    * Try changing *Correlation length* (switch "No. of realizations" to get new draws). What does this (hyper)parameter control?
    * Change "Select correlation family" (kernel).
        * What changes about the GP function draws? 
        * Note the extra parameter with Matern.
    * See the "About" tab for the formulas of the kernels (scroll down).

2. The [*Gaussian process regression: a function space perspective*](http://rpradeep.me/gpr/) app by Pradeep Ranganathan "demonstrates how a GP prior is a distribution over functions, and how observing data conditions the prior to obtain the GP posterior." 

    * You should see (animated) successive draws from a GP.
    * Predict how changing the covariance and length scale will affect the draws and then try out various combinations. Do the draws change as predicted?
    * Now try adding points. What happens? (Note: the darkest black line is the *mean function* of the GP.)
    * Try adjusting the noise. What happens?
    * Takeaway: when points are added, the class of possible functions is reduced to those that pass near the points; the closeness is random scaling with the noise amplitude. 

3. The [*Gaussian process regression demo*](http://www.tmpl.fi/gp/ ) app "demonstrates Gaussian process regression with one covariate and a set of different covariance kernels." 

    * Check "Show mean and credible intervals" and "sample independently".
    * Add observations.
    * Add a new process.  

4. [*A visual exploration of Gaussian processes*](https://distill.pub/2019/visual-exploration-gaussian-processes/) is a complete run-through of Gaussian processes.

    * Try changing the covariance matrix under *Multivariate Gaussian distributions*.
    * Try the different kernels under *Gaussian Processes / Kernels*.
    * Under *Gaussian Processes*, try *Prior distribution* and *Posterior distribution*.
    * Try *Gaussian Processes / Combining different kernels*.



