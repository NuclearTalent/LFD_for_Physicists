---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:GPIntuition)=
# Demo: Intuition for Gaussian process

## GP sandbox widget

The widget here provides a Gaussian process (GP) visualization and some things to try to help build intuition about GPs.
A GP defines a distribution over *functions*, so in the simulation we will see draws of random functions, in analogy to drawing random variables from a normal distribution (recall that "normal" and "Gaussian" are synonymous here). 
Our principal goal is to experience how GPs look in practice and how they are used for interpolation or regression.

The defining feature of an ensemble of GP function draws is that at *any* fixed point, the histogram of the function values at that point would approximate a Gaussian distribution; while for any two points the function values would be draws from a bivariate Gaussian distribution with a proscribed covariance matrix; and so on with more points being draws from a multivariate Gaussian distribution. The covariance in each case between any two points is specified by a *kernel* evaluated at those points. 


```{raw} html
<iframe src="../../../_static/demo-gp-widget-html5.html"
    width="100%"
    height="1000"
    style="border: none;"
    scrolling="no">
</iframe>
```

## Things to try 

1. Drawing curves from a GP
    * Press the `Draw samples` button. These are draws from a GP, with each draw a function plotted from $x=-5$ to $x=+5$. 
    * Turn the `Show mean & bands` button on and off. What is the value of the mean? What are the bands?
    * Change the number of realizations (using the `# samples slider`) to 1, 5, 10, maximum allowed.  Look at any fixed $x$ value, draw a vertical line (in your mind!), and visualize the histogram; does it look like a Gaussian distribution? What is the mean and standard deviation?

2. Changing the hyperparameters
    * Try changing $\ell$ `(length scale)`, which is the *correlation length*.
     What does this (hyper)parameter control?
    * Now try different values for the noise standard deviation and the signal standare deviation. What do each control?
    * Predict how changing the covariance and length scale will affect the draws and then try out various combinations. Do the draws change as predicted?
    * Try adjusting the noise. What happens?

3. Adding points
    * Add observations by clicking in the plot.
    * What happens to the GP mean (solid red line)?  
    * What happens if you increase $\sigma_n$?
    * What if you uncheck the `Draw from posterior [prior]` box? What does it mean that you are showing the prior?
    * Takeaway: when points are added, the class of possible functions is reduced to those that pass near the points; the closeness is random scaling with the noise amplitude.     

4. Trying different kernels
    * Explore the kernels under the `Kernel` pulldown (clear any point first).
    * What changes about the GP function draws? 
    * What is the difference between the two Matern kernels?

5. Optimizing hyperparameters
    * Add at least one point. What does LML (*log marginal likelihood*) indicate?
    * If you adjust the hyperparameters by hand, what happens to the LML? Record the lowest LML and the corresponding values of the hyperparameters.
    * Now check the `Optimize hyperparameters` box. How does the LML compare to the lowest value you found by hand?



