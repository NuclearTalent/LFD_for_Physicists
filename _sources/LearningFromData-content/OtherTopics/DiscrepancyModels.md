(sec:ModelDiscrepancy)=
# Bayesian approach to model discrepancy


## KOH and BOH discrepancy models

In the following we'll use the abbreviations KOH and BOH:
* KOH = Kennedy and O'Hagan, [*Bayesian calibration of computer models*](https://rss.onlinelibrary.wiley.com/doi/abs/10.1111/1467-9868.00294)
* BOH = Brynjarsdóttir and OʼHagan, [*Learning about physical parameters: the importance of model discrepancy*](https://iopscience.iop.org/article/10.1088/0266-5611/30/11/114007). This content is particularly important if you are trying to extract the value of physical parameters from modeling data.

Comparisons between theoretical models and experimental data are at the heart of scientific inquiry. Theoretical models guide our understanding of complex systems by translating hypotheses into quantitative predictions that can be tested experimentally. Traditionally, a close fit between a model's predictions and measured data is interpreted as a sign of success, often implying that the model parameters capture the underlying physical processes. However, this paradigm assumes that the model fully represents the complexity of actual systems -- an assumption that is rarely justified in practice. All models have inherent limitations beyond their domains of validity, and using them beyond these regimes without accounting for theoretical uncertainties can lead to biased parameter estimates, reducing these parameters to mere "fitting variables" rather than meaningful physical quantities,. Moreover, discrepancies between certain measurements and otherwise successful models sometimes lead researchers to assign lower weights to these data, thereby diminishing their utility and limiting the potential insights they can provide.

A model discrepancy framework employing Gaussian processes (GPs) was introduced in KOH  and variations have been explored in many studies. <!-- \cite{Higdon2004, Bayarri01052007, Arendt:etal2012:1, Arendt:etal2012:2, Brynjarsdottir_2014, GARDNER2021107381}.--> 
In these approaches, the discrepancy between experimental data and theoretical model predictions, stemming from missing physics or approximations, is modeled using a GP. However, one persistent challenge is the need to constrain the GP's covariance kernel. For example, in BOH, the authors emphasized the importance of incorporating knowledge of the theory's validity at specific points in the input space (i.e., the domain in which observables are measured) so that both the GP and its derivative could be accurately constrained. In practice, however, specifying such accurate knowledge about the theory is often difficult. In this chapter, we construct the GP covariance kernel based on only qualitative prior knowledge of the theory's domain of validity across the input space. This type of knowledge -- for example, recognizing that "*the theory is more reliable in this regime than in that one*" -- is typically easier to provide and often available. By leveraging this information, the framework prioritizes the accurate extraction of model parameters rather than simply optimizing the fit to the observables. We perform Bayesian parameter inference to simultaneously estimate both the model parameters and the GP hyperparameters, thereby quantifying uncertainties from both the experimental data and the theoretical model.

## Framework

We begin by setting up the model discrepancy framework following KOH. Let the $i$-th measurement for an observable $y$ be denoted as

$$
    y(x_i) \sim \zeta(x_i) + \epsilon_i \,,
    \qquad \epsilon_i \sim \mathcal{N}(0,\sigma_i^2) \,.
$$ (eq:stat_true)

Here, the index $i$ corresponds to the point in input space $x$ where the $i$-th observation is made (e.g., a specific time in the ball drop experiment described below). Independent observation errors $\epsilon_i$ are assumed to follow Gaussian distributions with zero mean and standard deviation $\sigma_i$. Here, $\zeta(x_i)$ represents the true value of the observable at $x_i$. (We assume that $x$ is made unitless by scaling it with a suitable reference scale $x_0$.)

We denote the prediction from a theoretical model for the observable $y$ as $\eta(x, \pars)$, where $\pars$ is the vector of true but unknown model parameters. The model for $\eta(x,\pars)$ is then defined as:

$$
    \zeta(x) = \eta(x, \pars) + \delta(x) ;
$$ (eq:md)

here $\delta(x)$ quantifies the discrepancy between the theoretical model prediction and the true system value at input setting $x$. Combining the above equations, we express the observation $y(x_i)$ as

$$
    y(x_i) \sim \eta(x_i, \pars) + \delta(x_i) + \epsilon_i .
$$ (eq:stat_MD)

Thus, each observation is modeled as the sum of the model output (evaluated at the true $\pars$), the model discrepancy $\delta$ at $x_i$, and the observational error $\epsilon_i$.
The statiscal model is summarized in {numref}`fig-statistical_model`.


:::{figure} ./figs/statistical_model.png
:height: 100px
:name: fig-statistical_model

Statistical model.
:::


Following KOH, we represent $\delta(x)$ as a zero-mean Gaussian process (GP):

$$
    \delta(\cdot \mid\boldsymbol{\phi}) \sim {\rm GP} \left(\boldsymbol{0}, K(\cdot,\cdot \mid\boldsymbol{\phi}) \right) \,,
$$

where $K(\cdot,\cdot \mid\boldsymbol{\phi})$ is the covariance kernel, which depends on a set of hyperparameters $\boldsymbol{\phi}$. A GP specifies a distribution over functions, with the covariance kernel $K$ serving as the central object that defines the properties of the functions in the distribution. In this framework, we incorporate prior knowledge about the theoretical model's uncertainties through the choice of the covariance kernel. Adopting a Bayesian approach, we assign prior probability distributions to both the model parameters $\pars$ and the GP hyperparameters $\boldsymbol{\phi}$, and update these to obtain their posterior distributions conditioned on the observations. In all examples discussed in this work, uniform priors (in appropriate ranges) are used for both the model parameters and the GP hyperparameters.

The particular $K$ we use for the test case explored here is

$$
K(x_i, x_j) = {\color{ForestGreen}{\bar{c}}}^2 (x_i x_j)^{\color{ForestGreen}{r}} \exp\left(- \frac{\lVert x_i-x_j\rVert^2}{2{\color{ForestGreen}{\ell}}^2} \right)
$$ (eq:Balldrop_Kernel)

The hyperparameters control the nature of the possible random draws, as illustrated in {numref}`fig-GP_nonstationary_comparison`. The parameter $\bar{c}$, which is fixed at $\bar{c}=1$ in the figure, controls the overall scale over which the random functions vary. The parameter $\ell$ is the correlation length between any two points; as $|x -x'|$ becomes greater than $\ell$, the points become increasingly uncorrelated. Comparing $\ell=1$ to $\ell=3$ shows that the latter curves have a longer "wavelength". Finally, $r$ is a parameter introduced to generate functions that increase with $x$ for $r>0$.



:::{figure} ./figs/GP_nonstationary_comparison.png
:height: 500px
:name: fig-GP_nonstationary_comparison

Five draws from each of four GPs of the form in Eq. {eq}`eq:Balldrop_Kernel` with hyperparameters $\ell$, $\bar c$, and $r$ as listed.
:::



:::{note}
If sampled at any one input point $x$, the prior GP will yield a Gaussian distribution with mean and variance specified by the GP definition. In many cases, the prior GP is taken to be mean zero with a constant variance for all $x$. If sampled at any two input points $x$ and $x'$, the joint distribution will be a bivariate Gaussian, with covariance given by $K(x,x'|\boldsymbol{\phi})$. 
:::

## The ball-drop model

Sunil Jaiswal has developed a nice Jupyter notebook illustrating with the Ball Drop Experiment how the BOH approach works for robust extraction of physical quantities from a calibration. In the example one seeks a value for the acceleration due to gravity $g$ using a theoretical model without air resistance fitted to data on height vs. time that includes air resistance and measurement errors. (A more general version with results shown below also has measurements of velocity and acceleration.) One first sees that a discrepancy model is essential; using a radial basis function (RBF) GP is standard (see [Wikipedia RBF article](https://en.wikipedia.org/wiki/Radial_basis_function_kernel)) and one finds good predictions for times where there is data (this is KOH). But the discrepancy model must be more informed for a robust extraction of $g$; this leads to using a nonstationary GP.  Sunil has given permission for us to adapt his notebook. This example has many extensions available to students.

We test the model discrepancy framework on a simple system (popularized by statistician Dave Higdon) in which a ball is dropped from a tower of height $h_0=60\,$m at time $t=0\,$s. Measurements of the ball's height above the ground, velocity, and acceleration are recorded at discrete time points until $t=1$\,s. (In this example $x=t$/(1\,s) serves as the unitless input parameter, $0\leq x \leq 1$.)
The true theory, used to generate mock experimental data, incorporates a gravitational force $\mathbf{f}_G=-Mg\,\hat{\bf z}$ and a drag force given by $\mathbf{f}_D = -0.4 v^2\, \hat{\bf{v}}$. 
Here, $M=1\,$kg is the mass of the ball, $g=9.8\,{\rm m/s}^2$ the acceleration due to gravity, and we set the initial velocity $v_0$ to $v_0=0\,$m/s.


We assume that the observational errors for height, velocity, and acceleration are independent and identically distributed Gaussian random variables.
<!-- with standard deviations of $\sigma = 0.1$, $0.2$, and $0.3$, respectively.--> Mock experimental data are generated by sampling from Gaussian distributions with specified standard deviations and with means given by the predictions of the true theory, which are determined by the equations of motion:

$$
    a = \frac{d v}{dt} = g - 0.4 v |v| \,, \qquad 
\frac{dh}{dt} = -v .
$$ (eq:BD_evol)

:::{figure} ./figs/ball_drop_data.png
:height: 200px
:name: fig-ball_drop_data

Data for the ball drop experiment, including measurement errors.

:::


We compare these mock data with a theoretical model that neglects the drag force and is governed by the simpler equations of motion:

$$
    v = v_0 + g t \,, \qquad h = h_0 - v_0 t - \frac{1}{2} g t^2 .
$$

Here $h_0=60\,$m is fixed to the value used in generating the mock experimental data. The parameters $g$ and $v_0$ are model parameters, which we infer using Bayesian parameter inference (in the notebook, for simplicity, only $g$ is inferred). We incorporate our prior knowledge about the theory's domain using the two distinct GP kernels discussed earlier. Since our model neglects drag forces, we are more confident in its predictions at earlier times (small $x$), when the velocity is lower, than at later times (larger $x$).


:::{figure} ./figs/balldrop_height_only.png
:height: 400px
:name: fig-balldrop_height_only

Balldrop analysis with only the height measurements.

:::


{numref}`fig-balldrop_height_only` shows both the inferred posteriors for the model parameters and the corresponding model predictions when only the height data is used. We perform Bayesian parameter inference under three scenarios: (i) without the model discrepancy (MD) term (red), (ii) with MD using GP-kernel $\texttt{I}$ (blue), and (iii) with MD using GP-kernel $\texttt{II}$ (green). The kernels are defined in {numref}`kernels_for_balldrop2`; their hyperparameters are learned at the same time as the model parameters. Parameter inference is carried out by sequentially incorporating additional observables to examine their influence on the inferred posteriors. The posteriors and predictions for when height and velocity are included are shown in {numref}`fig-balldrop_height_velocity` and when height, velocity, and acceleration included are shown in {numref}`fig-balldrop_all_three`.
<!--In the top row of Fig.~\ref{fig:balldrop}, the left panel shows the corner plot when only height measurements are considered, the middle panel adds measurements of the velocity, and the right panel includes all observables. The vertical dashed gray lines in the diagonal panels mark the true parameter values used to generate the mock data, and the shaded purple regions denote the priors.-->


:::{figure} ./figs/kernels_for_balldrop2.png
:height: 180px
:name: kernels_for_balldrop2

GP kernels $\texttt{I}$ and $\texttt{II}$ for the balldrop analysis.
:::



:::{figure} ./figs/balldrop_height_velocity.png
:height: 400px
:name: fig-balldrop_height_velocity

Balldrop analysis with both the height and velocity measurements.

:::


:::{figure} ./figs/balldrop_all_three.png
:height: 400px
:name: fig-balldrop_all_three

Balldrop analysis with  height, velocity, and acceleration measurements.

:::



The posteriors incorporating MD (blue and green) consistently cover the true values and become narrower as more observables are included. In particular, the posteriors with MD using Kernel $\texttt{II}$ (green), which encodes strong prior information about the theory's domain of validity, are consistently tighter, reflecting greater constraining power, yet remain consistent with those obtained using the more conservative Kernel $\texttt{I}$ (blue). Remarkably, when acceleration data are included ({numref}`fig-balldrop_all_three`), the posterior with Kernel $\texttt{II}$ nearly recovers the true parameter values, even though the model predicts a constant acceleration that does not capture the observed decreasing trend in the data. In contrast, the posteriors from the inference without the MD term (red) deviate significantly from the truth and become increasingly narrow as more observables are added, resulting in model parameter estimates that are both incorrect *and* overconfident.



In the right panels of the figures, the mock experimental data are compared with the model predictions generated using the inferred parameter posteriors from the left panels. Notably, predictions with MD (blue, green) match the data at early times and deviate at later times, a behavior that directly results from incorporating prior knowledge about the theory's domain of applicability into the covariance kernel. In contrast, predictions without MD (red) prioritize achieving the best fit to the data, leading to inaccurate and overconfident parameter estimates.








