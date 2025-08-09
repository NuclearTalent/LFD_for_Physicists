(sec:Introduction)=
# Introduction

## Physicist's perspective

This is a book by physicists, for physicists. It is not a data science book _per se_. It is, instead, a book that we hope will help physicists learn about a set of tools and practices that will enable them to draw rigorous scientific conclusions from data. 

:::{Note}
In the spirit of Lewis Carroll's _Through the Looking Glass_ ('“When I use a word,” Humpty Dumpty said in rather a scornful tone, “it means just what I choose it to mean—neither more nor less.”') we take opportunities like this one to specify how we will use various terms throughout this book. When we say "Data" it means any information  used to form a conditional probability that is part of our inference. Data could be the quantitative output of experimental investigations--the most common understanding of the term. But, it could also be data from astronomical observations. Or it could be the results of computational simulations of theories, or even order-by-order theory predictions obtained in a perturbative expansion. Indeed, a key aspect of this book is that we will often understand our theories (or models) as providing us with data, and we may well not distinguish in our writing whether it is that kind of data we are discussing or "actual" data. The Bayesian methods we present don't care about this distinction: all data will be grist for our inference mill. 
:::

In order to draw these conclusions the act of scientific modeling is essential. But most of us are not interested in drawing a model-specific conclusion. Our goal is more ambitious: while inference will often be done in the context of a specific model, we will drive towards results and predictions whose validity is not restricted by the limitations of the model itself. 

We want these conclusions to be rigorous, but this is not synonym for certain. Conclusions from data are, by and large, contingent and revisable. But, we will argue that, if couched in the language of probability theory, the inference from data can and should be done rigorously. This can only happen if that inference is implemented within a consistent theory of probabilistic reasoning.

In order to assign a probability to some aspect of a model (a parameter being within a specified range, that the model itself is true, etc.) we need to specify the information on which we are basing this probability. Thus our understanding of models needs not only to be expressed using a probability calculus, the probabilities must always be understood as contingent upon the specified information. 

Bayes' theorem is an immediate consequence of consistent probabilistic reasoning and it expresses how the probabilities of things we care about in a model must change in the light of additional information. Bayes' theorem is therefore at the heart of this book because it is a mathematical identity regarding consistent learning from new data. It tells us how to take the probabilities that encode our knowledge regarding the model prior to acquisition of that data and update them in light of that new information. Bayes' theorem and the rules of probability calculus are introduced in Part I, {numref}`ch:Inferenceandpdfs` and applied throughout this text. 

(sec:Intro:BayesianWorkflow)=
## Bayesian workflow

We hope anyone, or at least anyone reading this book, wants to learn. As taught in this book the practice of learning from data has four steps, which we will revisit repeatedly:

1. Formulate "priors" that express our knowledge about a model before the new data is taken. Some physicists may argue that we should "let the data speak for itself", with the implication that any informative prior is biasing the result. To the contrary, not using as informative priors as possible risks biases and fails to use all the information. 
<!--This is discussed in Part II and X.-->

2. Define the probabilistic relationship between the physical model and the data. No experiment is perfect, and all models are wrong at some level, so both the "data generation process" and "theory defects" need to be accounted for as stochastic variables when we define the relationship between the physics model we want to learn and the data we are using to learn about it. We will call that relationship the "statistical model". <!-- and we discuss it in Part II and Y. -->
Without a statistical model the chain of rigorous inference is broken. But, once a statistical model is specified, that information, combined with the probability calculus we'll introduce in Part I, defines our updated knowledge of the model. 

3. Compute the updated (or "posterior") probabilities that represent our knowledge about the model, including the parameters in it. This, in general, requires a set of computational tools that sample the different possibilities for those probabilities: "samplers". These are demonstrated in detail in Part III.

4. Check the answers obtained after they have been computed to see if the statistical model we wrote down in step 2 is consistent with both what we now know (in the probabilistic sense) about the physics model and the data we are analyzing. This step is called "model checking". You will be exposed to best practices for model checking as well as specific tools to carry it out.
<!--Tools for model checking are presented in Part W.-->

These four steps are the way: the "Bayesian workflow". It is the practice by which principled learning from data can be carried out, and the results of that learning validated. The Bayesian workflow is discussed in more detail in {ref}`sec:BayesianWorkflow`.

:::{admonition} Four-step Bayesian workflow in brief
1. Formulate informative priors before new data is used.
2. Define a statistical model relating the physics model and data, including all errors.
3. Compute the posterior probabilities.
4. Do model checking.
:::

We first introduce the Bayesian tools and practices in Part I in the context of parameter estimation, i.e., we explain how they let us use data to refine our knowledge of model parameters and demonstrate with applications that the reader is encouraged to extend. But then, in Part II, we broaden our perspective and ask if we can do inference not just in the parameter space of a particular model, but in the space of all possible models. This leads us to a discussion of Model Evidence, Model Selection, Model Averaging, and Bayesian Model Combination, see {ref}`sec:MultiModelInference`. We also explore how to deal statistically with flaws in our theoretical models, see {ref}`sec:ModelDiscrepancy`.

One of the chief virtues of the Bayesian approach is that it should force the practitioner to be explicit and clear about what the ingredients that go into the inference. Step 1 requires that they specify the prior. Step 2 mandates that a statistical model relates the data to the model. And Step 4 asks them to check that their process is at least self-consistent. 

## Machine learning

The Bayesian workflow sets us up to talk about Machine Learning (ML) from a Bayesian perspective. 
Indeed there are corresponding steps in the typical ML workflow, although they might not be immediately recognized as such (e.g., regularization in ML is a type of prior that imposes the knowledge that weights should not be overly large when trained).
The use of ML methods such as Gaussian processes are already naturally formulated in a Bayesian statistical setting, with priors, posteriors, and probability distributions. 
But we can also cast neural networks in a probabilistic framework.
Furthermore, there are special features about ML for physics, summarized below, which argue for a less "black box" approach to ML than is common.
All of these aspects motivate an integrated discussion of ML within this text, which we carry out in Part IV.

```{admonition} What is special about machine learning in physics?
Physics research takes place within a special context:
  * Physics data and models are connected with physical processes and are often fundamentally different from those encountered in typical computer science contexts. 
  * Physicists ask different types of questions about their data, sometimes requiring new methods.
  * Physicists have different priorities for judging the quality of a model: interpretability, error estimates, predictive power, etc.

Providing slightly more detail:
  * Physicists are data **producers**, not (only) data consumers:
    * Experiments can (sometimes) be designed according to needs.
    * Statistical errors on experimental data can be quantified.
    * Much effort is spent to understand systematic errors.

  * Physics data represents measurements of physical processes:
    * Dimensions and units are important.
    * Measurements often reduce to counting photons, etc, with known a-priori random errors.
    * In some experiments and scientific domains, the data sets are *huge* ("Big Data")

  * Physics models are usually traceable to an underlying physical theory:
    * Models might be constrained by theory and previous observations.
    * There might exist prior knowledge about underlying physics that should be taken into account.
    * Parameter values are often intrinsically interesting.
    * The error estimate of a prediction is just as important as its value.
  ```

## Virtues 

In carrying out a principled Bayesian approach to learning from data, there are virtues that we wish to uphold. A good list of these is reproduced here from the [paper by Gelman and Hennig](https://sites.stat.columbia.edu/gelman/research/published/gelman_hennig_full_discussion.pdf).
These are broadly relevant for the practice of science and not only Bayesian inference. 

:::{Admonition} Aspirational virtues for Bayesian inference and beyond

1. Transparency
    - Clear and unambiguous definitions of concepts
    - Open planning and following agreed protocols
    - Full communication of reasoning, procedures, spelling out of (potentially
unverifiable) assumptions and potential limitations
2. Consensus
    - Accounting for relevant knowledge and existing related work
    - Following generally accepted rules where possible and reasonable
    - Provision of rationales for consensus and unification
3. Impartiality
    - Thorough consideration of relevant and potentially competing theories and
points of view
    - Thorough consideration and if possible removal of potential biases: factors
that may jeopardize consensus and the intended interpretation of results
    - Openness to criticism and exchange
4. Correspondence to observable reality
    - Clear connection of concepts and models to observables
    - Clear conditions for reproduction, testing and falsification
5. Awareness of multiple perspectives
6. Awareness of context dependence
    - Recognition of dependence on specific contexts and aims
    - Honest acknowledgement of the researcher’s position, goals, experiences
and subjective point of view
7. Investigation of stability
    - Consequences of alternative decisions and assumptions that could have
been made in the analysis
    - Variability and reproducibility of conclusions on new data

:::

George Pólya was a Hungarian-American mathematician who, in addition to many contributions to pure mathematics, developed a framework for problem solving that incorporated many principles of plausible inference that we build into our Bayesian methods. He also articulated three moral qualities essential for the robust practice of scientific discovery in general, which we have adapted here with the hope they are shared by all of our readers. 

:::{Admonition} Moral qualities of the scientist

Adapted from G. Polya, Induction and Analogy in Mathematics, chapter 1, section 4, which is entitled "The Inductive Attitude".

Intellectual courage
: One should be ready to revise any one of our beliefs.

Intellectual honesty
: One should change a belief when there is a compelling reason to do so. To stick to a conjecture clearly contradicted by experience is dishonest. It is also dishonest to ignore information or not to state and criticize all assumptions.

Wise restraint
: One should not change a belief wantonly, without some good reason. Don't just follow fashion. Do not believe anything, but question only what is worth questioning.
:::


