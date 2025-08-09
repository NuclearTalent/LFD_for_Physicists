# Overlap between BUQEYE LFD version, Forssén version, and previously existing materials #

This file collects overlap between the two versions of the course (labeled 'BUQEYE' and 'Forssén' here). It also identifies significant overlap with other published material.

- BUQEYE version: https://buqeye.github.io/LearningFromData/
- Forssén version: https://cforssen.gitlab.io/learningfromdata/

## Bayes-ics ##

Lecture 1 BUQEYE is quite similar to Lecture 15 Forssén. It introduces probability calculus, and Bayes' theorem. This draws on, but does not parrot, Sivia.

Lectures 2 and 3 BUQEYE parallel Lectures 16 and 17 Forssén. Here we discuss coin tossing, and use it as an example of Bayesian updating. Similar comments about Sivia. The medical testing example, or other examples of Bayesian calculation, can also be discussed here.

Lecture 4 BUQEYE discusses Gaussians, the Central Limit Theorem, and the lighthouse problem as an example of CLT failure. This could be a good place to first introduce the concept of a statistical model. (This is done in Christian's Lecture 18.) 

## Parameter estimation ##

Lectures 5 and 13 BUQEYE and Forssén Lectures 20 and 7 discuss Bayesian linear regression and standard linear regression. Here I would argue in favour of Christian's ordering. He provides a Bayesian statistical model and displays the result in Lecture 20. This could then be used to flow smoothly into a discussion of multi-dimensional posteriors, i.e., how correlation coefficients etc. emerge in the Bayesian framework. That is Lecture 6 in the BUQEYE materials. Some care, though, may be required here, as the presentation adopted is quite close to that in Sivia. 

Lecture 10 BUQEYE and Lecture 19 Forssén discuss "Why Bayes is better" in the context of linear regression specifically. This could probably be folded into the previous discussion on linear regression. Lecture 10 BUQEYE also defines statistical models for the linear regression, which is a win IMO. 

There is a (draft) chapter on the Bayesian Workflow in Chapter 21 of https://cforssen.gitlab.io/tif285-book/ (another version of the notes)

I like the Bayesian billiard (BUQEYE Lecture 9) example but did not find it in Christian's course.

Lecture 11 BUQEYE and Lecture 19 Forssén discuss error propagation in the Bayesian approach. 


## Sampling

BUQEYE Lectures 7 and 8 introduce MCMC sampling based heavily on the discussion in Gregory (this is in a section on "MCMC Sampling I"). There is little or no background on Markov chains. Simple examples demonstrating Metropolis-Hastings are presented (e.g., Poisson distribution sampling) and autocorrelation is introduced. An overview of MCMC diagnostics for assessing convergence is covered in a notebook adapted from TALENT and there is an assignment to extend the radioactive lighthouse location problem using MCMC. Lecture 12 is an interlude on sampling with intuition on marginalization. 
The Forssén LFD section on "Stochastic processes and Markov Chains" has four lectures (11 though 14) that give a more coherent development of random walks (and a first look at Gaussian processes) and then MCMC, with overlap in the last two lectures with the BUQEYE presentation.

BUQEYE Lectures 17 and 18 (in "MCMC sampling II") plus some associated notebooks address sampling beyond MH, such as parallel tempering, HMC, using PyMC, and slice sampling. The advanced MCMC sampling in the Forssén LFD is under "Computational Bayes" in Lecture 26.


## Model selection

There is a separate BUQEYE section on Model selection (section 5) with Lectures 14, 15, 16 covering the story of Dr. A and Prof. B, Laplace's method, evidence in the model EFT prolem, computational possibilities for calculating the evidence, a survey of various information criteria, and evidence calculation using parallel tempering. 
The Forssén LFD has Lecture 25 on Model Selection, which starts with frequentist hypothesis testing, then Dr. A and Prof. B, then evidence calculations with Laplace's method in detail. 

## Assigning probabilities 

This is covered in Section 8/Lecture 21 of the BUQEYE version of the course. In Christian's version it is Sections 21 and 22. Christian covers conjugate priors in Section 23, and uses this to move into Baysian linear regression. For myself (Daniel) I would rather bring conjugate priors up earlier, as an example of the priors that can be chosen for paraameter estimation. This may mean that some of the material in Section 23, gets covered earlier, when we are talking about linear regression.

## Gaussian processes

BUQEYE section 7 is on Gaussian processes and includes Lectures 19 and 20 and some demonstration notebooks from Christian. An intro to GPs in Lecture 19 is adapted from Melendez et al. (2019) and there is also a guide to some online widgets demonstrating GPs. 
Christians Lectures 28 and 29 introduce GPs and have some similar material as the BUQEYE notebooks (not surprising, since he wrote them).

## (Bayesian) Neural networks

BUQEYE section 9 is on Machine Learning: Bayesian Methods and includes an intro to neural networks in 9.4 and a pyTorch example (with help from chatGPT) in 9.5. Section 9.6 is similar to Chapters 33, 36 in https://cforssen.gitlab.io/tif285-book/.

Bayesian Neural Networks are introduced in BUQEYE section 9.4 / Forssén chapter 36. The brute-force sampling example is from MacKay's book on Information theory. Variational inference is introduced in BUQEYE Lecture 24 and section 9.10.

## Non-overlapping topics

- Maximum entropy for function reconstruction (BUQEYE lecture 22)
- PCA, SVD, and all that (BUQEYE lecture 25)
- Emulators (Forssén Section 27)
- History matching (Forssén Section 28)
- Bayesian Optimization (BUQEYE Section 9.2)

