(sec:ModelDiscrepancy)=
# Discrepancy models with GPs

In {numref}`sec:DataModelsPredictions` we introduced the mismatch term $\delta M$, typically referred to as a model discrepancy, in the statistical model

$$
\data = M(\pars) + \delta \data + \delta M.
$$ (eq:DiscrepancyModels:mismatch)

In this chapter, we describe and illustrate an approach to model discrepancy that uses Gaussian processes (see {numref}`sec:RootGP`) to model $\delta M$.

Most of our discussion of discrepancy models is based on the seminal papers of Kennedy and O'Hagan and of Brynjarsdóttir and OʼHagan.
In this chapter we'll refer to these works using the abbreviations KOH and BOH:
* KOH = Kennedy and O'Hagan, [*Bayesian calibration of computer models*](https://rss.onlinelibrary.wiley.com/doi/abs/10.1111/1467-9868.00294)
* BOH = Brynjarsdóttir and OʼHagan, [*Learning about physical parameters: the importance of model discrepancy*](https://iopscience.iop.org/article/10.1088/0266-5611/30/11/114007). This content is particularly important if you are trying to extract the value of physical parameters from modeling data.

