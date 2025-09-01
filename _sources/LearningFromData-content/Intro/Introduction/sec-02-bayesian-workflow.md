(sec:Intro:Workflow)=
# Bayesian workflow

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

