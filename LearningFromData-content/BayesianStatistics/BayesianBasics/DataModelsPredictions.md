(sec:DataModelsPredictions)=
# Data, models, and predictions

```{epigraph}
> "All models are wrong, but models that know when and how they are wrong, are useful.."

-- revised version of George Box's quote (see {ref}`sec:OverviewModeling`)
```

## How do we make statistical predictions?

Let us consider a common scenario:
* We have a model $M$ with parameters $\pars$.
* We have some (noisy) data $\data$ that we can use to calibrate the parameters.  Generically label the input values by $x$ (a vector) and the quantities of interest by $y = y(x)$.
* Then we want to predict at other input points $x^\ast \rightarrow y^\ast$. 

How shall we proceed? Let's first say a bit more about the ingredients.

<!-- The use of probability theory to quantify uncertainty plays a central role in science and the scientific method for inferring new knowledge about the universe. Before we can elaborate on this topic of inductive inference we must briefly discuss the nature of science in terms of data, theories, and models. In the next chapter we will exemplify this using a linear model and some test data. But for now we will remain general and slightly more abstract.-->



## A statistical model for our data

<!--
Before continuing with concrete applications of Bayes' theorem, let's step back and briefly discuss the nature of science in terms of data, theories, and models in more abstract terms.
-->

From the Bayesian workflow introduced in {numref}`sec:Intro:Workflow`, a key element of our inference is to formulate a statistical model for our data.
Let us start with the *data* $\data$ already obtained through a measurement process, e.g., an experiment in a laboratory or an observation of some astronomical event. All data come with uncertainties of various origin, let us denote these as $\delta \data$. Given some data $\data$, one might immediately ask what this data can tell us about data we have not yet collected or used in the inference. We call this future data $\futuredata$. At present, we are uncertain about any future data, and we describe as a (conditional) probability $\cprob{\futuredata}{\data,I}$. All we have said so far is that _predictions are uncertain_. The obvious and interesting question is: how uncertain is the prediction? To answer that, we must go from this abstract probability to something that we can evaluate quantitatively. The first step is to develop a theoretical model to analyze the relevant data.

<!--
:::{admonition} Theories in physics
In physics, a *theory* is very often some framework that postulates, or deduces from some axioms, a master equation that governs the spacetime dependence of a system of interacting bodies, e.g., Einstein’s field equations in the general theory of relativity or Heisenberg’s equations of motion in quantum mechanics. There is no recipe for how to develop a realistic theory. All we can do is to use our imagination, try to discover patterns and/or symmetries, collaborate with other experts, and have some luck on the way! No theory is complete and we always seek improvement or sometimes face a fundamental change of interpretation, i.e., a paradigm shift. In that sense, a theory always comes with some probability for being true, and, besides for purely logical statements, this probability can never be exactly 0 or 1. In such cases, no new evidence/data will ever have any influence. In this sense, *all theories are wrong*, i.e., they are never correct with absolute certainty. This is at some level a provocative statement that is designed to draw attention to the fact that all theories can be improved or replaced, and we do this all the time using the scientific method.
:::
-->
<!-- described in the introduction section about [](intro:inference). -->

A physical *model* $M$ allows quantitative evaluation of the system under study. Any model we employ will always depend on model parameters $\pars$ with uncertain numerical values. Moreover, *all models are wrong*, in the sense that there will always be some physics that we have neglected to include or are unaware of today. If we denote mismatch between model predictions and real world observations of the system, i.e., data, as $\delta M$, we can write

$$
\data = M(\pars) + \delta \data + \delta M.
$$ (eq:DataModelsPredictions:mismatch)

The mismatch term $\delta M$ is often referred to as a model discrepancy. We are uncertain also about this term, so it must be represented as a random variable that is distributed in accordance with our beliefs about $\delta M$. It is no trivial task to incorporate model discrepancies in the analysis of scientific models and data, yet it is crucial to avoid overfitting the model parameters $\pars$ and making overly confident model predictions. 
We will touch upon $\delta M$ in two contexts in this text: in treating the truncation error in expansions such as encountered in effective field theories and with a prototypical example (the "Ball-Drop Experiment") of using Gaussian processes to model $\delta M$ (see {ref}`sec:ModelDiscrepancy` and the [](../../OtherTopics/MD_balldrop_v1.ipynb) notebook).  
<!-- Although important, we will for the most part in this course neglect $\delta M$. There is simply no time to cover also this aspect of the scientific method.--> 
Note that the model discrepancy remains present even if there is no uncertainty about $\pars$. In the following we subsume the choice of model and other decisions into the set of background knowledge $I$.

:::{admonition} The statistical model and underlying truth (with an alternative notation)
Let us consider the statistical model from the perspective of our (often implicit) belief as physicists that there is an underlying truth that we approach both by refining our theoretical descriptions and our experimental measurements. The spectacular agreement of theory and experiment for the anomalous magnetic dipole moment of a muon (the "muon $g-2$" measurement) is vivid testimony to the existence of this truth.

But at any given time we only approximate the truth from both theory and experiment, and statistically we seek to account for their deficiencies.
Let us denote the underlying true theory (what statisticians call "truth") as $\ytrue(x)$, where $x$ is a generic input (i.e., it could be a vector in the input space).
The truth should be our model predictions $\yth$ plus the theory error (model discrepancy):

$$
    \ytrue(x_i) = \yth(x_i;\pars) + \delta\yth(x_i) ,
    \label{eq:theory_truth}
$$

where we have explicitly noted that the model predictions depend on parameters $\pars$.
At the same time, observation $y_i$ at input $x_i$ should be the truth  plus the experimental error $\delta \yexp$:

$$
    y_i = \ytrue(x_i) + \delta\yexp(x_i) .
    \label{eq:expt_truth}
$$
Eliminating $\ytrue$ yields our statistical model for the observations:
<!-- ~\cite{kennedy2001bayesian,Brynjarsdottir:2014}, -->

$$
    y_i = \yth(x_i;\pars)  + \delta\yexp(x_i) + \delta\yth(x_i) .
    \label{eq:stat_model}
$$

These equations encode the relationship between the random variables $y_i$, $\yth(x_i;\pars)$, $\delta\yexp(x_i)$ and  $\delta\yth(x_i)$.
The underlying $\ytrue$ describing the observables used for parameter estimation and for new observations could be the same, but in general $\ytrue$ may be completely different for the predicted observable.

The correspondence to the notation for the same statistical model {eq}`eq:DataModelsPredictions:mismatch` is $y \rightarrow \data$, $\delta\yexp(x_i) \rightarrow \delta\data$, $\yth(x_i;\pars) \rightarrow M(\pars)$, and $\delta\yth(x_i) \rightarrow \delta M$.

:::


## Bayesian parameter estimation

Quantifying the posterior distribution $\pdf{\pars}{\data,I}$ for the parameters of a model is called *Bayesian parameter estimation*, and is a staple of Bayesian inference. This is a probabilistic generalization of parameter optimization and maximum likelihood estimation whereby one tries to find an extremum parameter value of some objective function or data likelihood, respectively. 
Instead of single values characterizing the distribution ("point estimates"), we seek the full distribution. 
We will see multiple examples of this in the coming chapters.
<!-- chapter on [](sec:LinearModels).-->


To evaluate the posterior for the model parameters we must employ Bayes' theorem,

```{math}
:label: eq_bayes
\pdf{\pars}{\data,I} = \frac{\pdf{\data}{\pars,I}\pdf{\pars}{I}}{\pdf{\data}{I}}.
```

Here, we must formulate a likelihood of the data $\pdf{\data}{\pars,I}$ and a prior distribution of the model parameters $\pdf{\pars}{I}$. 
<!--Unless we are able to select very particular combinations of likelihood and prior distributions (called conjugate priors) we must use numerical methods to sample the posterior for use in predictions of new data.  -->
The denominator in Eq. {eq}`eq_bayes` is sometimes referred to as the marginal likelihood or the evidence and normalizes the left-hand side such that it integrates to unity, i.e., we have

\begin{equation}
\pdf{\data}{I} = \int_{\Omega} \pdf{\data}{\pars} \pdf{\pars}{I}\, {\rm d}\pars.
\end{equation}

Often we do not need an absolutely normalized posterior distribution, so we can omit the denominator in Eq. {eq}`eq_bayes`. Indeed, the latter does not explicitly depend on $\pars$. 


Bayesian parameter estimation can sometimes be very challenging. In the chapter on [](sec:BayesianLinearRegression) we will see an example of where we can perform analytical calculations throughout. However, in most realistic applications the posterior must be evaluated numerically, and most often by sampling using [](sec:MCMC). This is no silver bullet and to quantify (or characterize) a multi-dimensional posterior, sometimes with a complicated geometry, for an intricate physical model, is by no means guaranteed to succeed. At least not in finite time. Nevertheless, obtaining posterior distributions to represent uncertainties is the gold standard in any inferential analysis.



## The posterior predictive distribution
The distribution of future data conditioned on past data and background information, i.e., $\pdf{\futuredata}{\data,I}$, is called a posterior predictive distribution (ppd). Assuming that we have a model $M(\pars)$ for the data-generating mechanism we can express this distribution by marginalizing over the uncertain model parameters $\pars \in \Omega$

```{math}
:label: eq_ppd
\pdf{\futuredata}{\data,I} = \int_{\Omega} \pdf{\futuredata}{\pars,\data, I}\pdf{\pars}{\data,I}\,{\rm d} \pars.
```

If $\futuredata$ is conditionally independent of $\data$, we can replace $\pdf{\futuredata}{\pars,\data, I}$ by $\pdf{\futuredata}{\pars, I}$, but there are cases of ppds where this is not true and we must be more careful (e.g., sometimes when we include $\delta M$). 
By performing this integral we account for the uncertainty in the model parameters $\pars$ when making predictions. In fact, one can marginalize (average) predictions over anything and everything that we are uncertain about as long as we have access to the necessary probability distributions. 

::::{admonition} Checkpoint question
:class: my-checkpoint
How would you notate the statement that $\futuredata$ is *conditionally independent* of $\data$ in {eq}`eq_ppd`?
:::{admonition} Answer
:class: dropdown, my-answer 
If we know $\pars$, then *if* $\data$ gives no additional information, we are able to replace $\pdf{\futuredata}{\pars,\data,I} \longrightarrow \pdf{\futuredata}{\pars,I}$.
:::
::::





## Exercises

```{exercise}
:label: exercise:ppd_definition
Derive Eq. {eq}`eq_ppd` using the rules of probability calculus and inference.
```

```{exercise}
:label: exercise:pdf_normalization
Can you think of a situation where you would have to compute the denominator in Eq. {eq}`eq_bayes` 
```

```{exercise}
:label: exercise:rain

In Gothenburg it rains on 60\% of the days. The weather forecaster at SMHI attempts to predict whether or not it will rain tomorrow. 75\% of rainy days and 55\% of dry days are correctly predicted thusfar. Given that forecast for tomorrow predicts rain, what is the probability that it will actually rain tomorrow?
```

```{exercise}
:label: exercise:monty_hall

Suppose you're on a game show, and you're given the choice of three doors: Behind one door is a car; behind the others, there are goats. You pick a door, say No. 1. This door remains closed. Instead, the game-show host, who knows what's behind all three doors, opens another door where he knows there will be a goat, say No. 3, which indeed has a goat. He then says to you, "Do you want to pick door No. 2?" Is it to your advantage to switch your initial choice of door? Motivate your answer using Bayes' theorem. (This is a famous problem known as *the Monty Hall problem*)
```

```{exercise}
:label: exercise:coin_ppd

Assume we have three coins in a bag. All three coins feel and look the same, but we are told that: the first coin is biased with a 0.75 probability of obtaining heads when flipped -- the second coin is fair, i.e., 0.5 probability of obtaining heads -- the third coin is biased towards tails with a 0.25 probability of coming up heads.

Assume that you reach your hand into the bag and pick a coin randomly, then flip it and obtain heads. What is the probability for obtaining heads if you flip it once more?
```

## Solutions

Here are answers and solutions to selected exercises.

````{solution} exercise:ppd_definition
:label: solution:ppd_definition
:class: dropdown

*Hint:* see part of the solution to {ref}`exercise:coin_ppd`.

````

````{solution} exercise:pdf_normalization
:label: solution:pdf_normalization
:class: dropdown

For instance when making comparisons of quantities averaged over two or more posterior distributions. 

````

````{solution} exercise:rain
:label: solution:rain
:class: dropdown

Let $r$ be rain, $\bar{r}$ be not rain, and $p$ be rain predicted. We seek $\prob(r|p,I)$, where $I$ is the background information we were given in the problem definition. Let us use Bayes' theorem

$$
\prob(r|p,I) = \frac{ \prob(p|r,I)\prob(r|I)}{\prob(p|I) } = \frac{\prob(p|r,I)\prob(r|I)}{\prob(p|r,I)\prob(r|I) + \prob(p|\bar{r},I)\prob(\bar{r}|I) }
$$

With $\prob(r|I) = 0.6$, $\prob(\bar{r}|I) = 0.4$, $\prob(p|r,I) = 0.75$, $\prob(p|\bar{r},I) = 0.45$, we have $\prob(r|p,I) \approx 0.71$

````

````{solution} exercise:monty_hall
:label: solution:monty_hall
:class: dropdown

You should switch to door No. 2 to increase your chance of winning the car. This, somewhat counter-intuitive, result can be obtained using Bayesian reasoning.

Let us introduce some notation for different events: $p_i = $ (the player initially picks door $i$), $h_j = $ (Monty opens door $j$), $c_k = $(car is behind door $k$). In the problem definition we had the series of events $p_1$ and $h_3$, and now we would like to know which probability is the greatest: $\prob(c_1|p_1,h_3)$ or $\prob(c_2|p_1,h_3)$? Let's compute them:

This is the probability that the car is behind door 1:

$$
\prob(c_1|p_1,h_3) = \frac{\prob(h_3|c_1,p_1)\prob(c_1,p_1)}{\prob(p_1,h_3)} = \frac{\prob(h_3|c_1,p_1)\prob(c_1)\prob(p_1)}{\prob(h_3|p_1)\prob(p_1)} = \frac{\prob(h_3|c_1,p_1)\prob(c_1)}{\prob(h_3|p_1)}
$$

We have $\prob(h_3|c_1,p_1)=1/2$ (since Monty can open doors 2 or 3), $\prob(c_1) = 1/3$ (car can be placed initially behind any of the three doors), $\prob(h_3|p_1) = 1/2$ (this probability is independent of car location!). Combined, this gives us that $\prob(c_1|p_1,h_3) = 1/3$

Now we compute the probability that the car is behind door 2:

$$
\prob(c_2|p_1,h_3) = \frac{\prob(h_3|c_2,p_1)\prob(c_2,p_1)}{\prob(p_1,h_3)} = \frac{\prob(h_3|c_2,p_1)\prob(c_2)\prob(p_1)}{\prob(h_3|p_1)\prob(p_1)} = \frac{\prob(h_3|c_2,p_1)\prob(c_2)}{\prob(h_3|p_1)}
$$

We have $\prob(h_3|c_2,p_1)=1$ (since Monty can only open door 3), $\prob(c_2) = 1/3$ (car can be placed initially behind any of the three doors), $\prob(h_3|p_1) = 1/2$ (this probability is independent of car location!). Combined, this gives us that $\prob(c_2|p_1,h_3) = 2/3$

So, you have a higher probability of getting the car if you change your initial pick from door number 1 to door number 2.

You can convince yourself that this is true by considering an extreme version of the game show where there are 100 doors, 99 goats, and 1 car. You first pick one door. After this, Monty opens 98 doors where he knows there are goats. There's only one door left closed at this point. Would you switch?

````

````{solution} exercise:coin_ppd
:label: solution:coin_ppd
:class: dropdown

Let $H/T$ denote the result of a coin flip coming up heads/tails. We seek the posterior predictive probability

$$
\prob(\mathcal{F}=H|\mathcal{D}=H,I)
$$

where $I$ is the information given in the problem definition. We do not know which one out of the three coins we are flipping, so the appropriate thing to do is to marginalize with respect to the coin type. Let us number the coins using the discrete random variable $C=1,2,3$. This gives us the following expression for the posterior predictive probability

$$
\prob(\mathcal{F}=H|\mathcal{D}=H,I) = \sum_{C=1}^{3} \prob(\mathcal{F}=H,C|\mathcal{D}=H,I) = \sum_{C=1}^{3} \prob(\mathcal{F}=H|C,I)\prob(C|\mathcal{D}=H,I),
$$

where we used the product rule of probabilities in the last step and that once we have knowledge of $C$ then the probability $\prob(\mathcal{F}=H|C,I)$ is conditionally independent of previous coin flips.

The left-hand factor in the last step is a likelihood, and we know that $\prob(\mathcal{F}=H|C=1,I) = 0.75$, $\prob(\mathcal{F}=H|C=2,I) = 0.5$, and $\prob(\mathcal{F}=H|C=3,I) = 0.25$. The right hand factor is a posterior probability for having coin $C$ if observing heads (in the first flip). To compute this, we must use Bayes' theorem

$$
\prob(C|\mathcal{D}=H,I) = \frac{\prob(\mathcal{D}=H|C,I)\prob(C|I)}{\prob(\mathcal{D}=H|I)}.
$$

Evaluating the denominator

$$
\prob(\mathcal{D}=H|I) = \sum_{C=1}^3 \prob(\mathcal{D}=H|C,I)\prob(C|I) = \frac{3}{4}\frac{1}{3} + \frac{1}{2}\frac{1}{3} + \frac{1}{4}\frac{1}{3} = \frac{1}{2}.
$$

With this, we have for the three coin posteriors

$$
\prob(C=1|\mathcal{D}=H,I) = 2\cdot \frac{3}{4}\cdot\frac{1}{3} = \frac{1}{2}.
$$

$$
\prob(C=2|\mathcal{D}=H,I) = 2\cdot \frac{1}{2}\cdot\frac{1}{3} = \frac{1}{3}.
$$

$$
\prob(C=3|\mathcal{D}=H,I) = 2\cdot \frac{1}{4}\cdot\frac{1}{3} = \frac{1}{6}.
$$

We can now evaluate the posterior predictive probability that we set out to obtain in the first place

$$
\prob(\mathcal{F}=H|\mathcal{D}=H,I) = \sum_{C=1}^{3} \prob(\mathcal{F}=H|C,I)\prob(C|\mathcal{D}=H,I) = \frac{3}{4}\frac{1}{2} + \frac{1}{2}\frac{1}{3} + \frac{1}{4}\frac{1}{6} = \frac{7}{12} \approx 0.58.
$$



````
