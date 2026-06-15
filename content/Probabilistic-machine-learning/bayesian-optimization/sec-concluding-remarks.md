---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:concluding-remarks)=
# Concluding remarks

## From the paper [arXiv:1902.00941](https://arxiv.org/abs/1902.00941)

* **Prior knowledge/belief is everything!** Important to tailor the acquisition function and the GP kernel to the spatial structure of the objective function. Thus, the usefulness of BayesOpt hinges on the arbitrariness and uncertainty of a priori information. Complicated by the fact that we resort to BayesOpt when little is known about the objective function in the first place, since it is computationally expensive to evaluate. 
* In general, BayesOpt will never find a narrow minimum **nor be useful for extracting the exact location of any optimum**. So one might want to use it as the first stage in a hierarchical optimization scheme to identify the interesting regions of parameter space.  One may also want to switch from a more explorative acquisition function in early iterations to more exploitive in later iterations.
* We find that the **acquisition function is more important** than the form of the GP-kernel. 
* BayesOpt would probably benefit from a prior that captures the **large-scale structure of the objective function**.
* **High-dimensional parameter domains** are always challenging (subspace learning, dim reduction).


## Space-filling sampling

![sampling](https://raw.githubusercontent.com/buqeye/LearningFromData/main/LectureNotes/_images/space_filling_sampling.png)

* Sobol sequence sampling in Python, e.g. with [sobol_seq](https://github.com/naught101/sobol_seq)
* Latin Hypercube Sampling in Python, e.g. with [pyDOE](https://pythonhosted.org/pyDOE/index.html)
* Mersenne-Twister is the core random number generator in Python / numpy

