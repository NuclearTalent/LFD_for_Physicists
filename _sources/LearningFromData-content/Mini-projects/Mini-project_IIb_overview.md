# Overview of Mini-project IIb: How many lines?

The notebook for Mini-project IIb is [](/notebooks/mini-projects/model-selection_mini-project-IIb_How_many_lines_ptemcee.ipynb).

* The problem is adapted from Sivia, section 4.2.
* Basic problem: we are given a noisy spectrum (maybe it is intensity as a function of frequency of electromagnetic signals) with some number of signal lines along with background signals.
We want to use parameter estimation and model selection (via parallel tempering) to determine what we can about the peaks.
    * Model selection addresses how many peaks;
    * parameter estimation addresses what are the positions and amplitudes of the peaks.

* The true (i.e., underlying) model is a sum of Gaussians plus a constant background.
    * The knowledge you have to analyze the data is the known width of the Gaussians but *not* how many Gaussians there are, nor what their amplitudes and positions are.
    * We add Gaussian noise with known $\sigma_{\text{exp}}$ to each data point. 
    * If there are $M$ lines, then there are $2M+1$ model parameters $\alphavec = (A_0, x_0, A_1, x_1, \ldots, B)$.
    * Formulas are in the notebook.

```{image} ./figs/miniproject_IIb_figure.png
:alt: Handdrawn schematic of the underlying model
:class: bg-primary
:width: 300px
:align: center
```
* There are 5 required subtasks, plus a bonus subtask and one to do to get a plus. Some notes:
    1. Formulate the problem in Bayesian language of how many lines and what are the model parameters.
        * This amounts to working through Sivia 4.2.
    2. Derive an approximation for the posterior probability.
        * Again, Sivia 4.2 has intermediate steps, but try doing it yourself. Be careful of the $M$!
        * Where is the Ockham factor?
        * Does this assume $B$ is known?
    3. Optional: numerical implementation.
    4. Generate data $\Lra$ just need to look at fluctuations and impact of width and noise.
    5. Parameter estimation with `emcee`.
        * Show what happens with `numpeaks = 2`.
        * Your job: explain!
    6. Main part: parallel tempering (with `ptemcee`) results for the evidence.
        * Explain the behavior (clear maximum or saturation).
        * Connect to toy model results.
    7. Repeat for another situation (different # of peaks, width, or noise).


  