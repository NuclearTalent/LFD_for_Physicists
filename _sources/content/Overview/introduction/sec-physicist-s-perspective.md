(sec:Intro:Perspective)=
# Physicist's perspective

This is a book by physicists, for physicists. It is not a data science book _per se_. It is, instead, a book that we hope will help physicists learn about a set of tools and practices that will enable them to draw rigorous scientific conclusions from data. 

:::{Note}
In the spirit of Lewis Carroll's _Through the Looking Glass_ ('“When I use a word,” Humpty Dumpty said in rather a scornful tone, “it means just what I choose it to mean—neither more nor less.”') we take opportunities like this one to specify how we will use various terms throughout this book. When we say "Data" it means any information  used to form a conditional probability that is part of our inference. Data could be the quantitative output of experimental investigations--the most common understanding of the term. But, it could also be data from astronomical observations. Or it could be the results of computational simulations of theories, or even order-by-order theory predictions obtained in a perturbative expansion. Indeed, a key aspect of this book is that we will often understand our theories (or models) as providing us with data, and we may well not distinguish in our writing whether it is that kind of data we are discussing or "actual" data. The Bayesian methods we present don't care about this distinction: all data will be grist for our inference mill. 
:::

In order to draw these conclusions the act of scientific modeling is essential. But most of us are not interested in drawing a model-specific conclusion. Our goal is more ambitious: while inference will often be done in the context of a specific model, we will drive towards results and predictions whose validity is not restricted by the limitations of the model itself. 

We want these conclusions to be rigorous, but this is not synonym for certain. Conclusions from data are, by and large, contingent and revisable. But, we will argue that, if couched in the language of probability theory, the inference from data can and should be done rigorously. This can only happen if that inference is implemented within a consistent theory of probabilistic reasoning.

In order to assign a probability to some aspect of a model (a parameter being within a specified range, that the model itself is true, etc.) we need to specify the information on which we are basing this probability. Thus our understanding of models needs not only to be expressed using a probability calculus, the probabilities must always be understood as contingent upon the specified information. 

Bayes' theorem is an immediate consequence of consistent probabilistic reasoning and it expresses how the probabilities of things we care about in a model must change in the light of additional information. Bayes' theorem is therefore at the heart of this book because it is a mathematical identity regarding consistent learning from new data. It tells us how to take the probabilities that encode our knowledge regarding the model prior to acquisition of that data and update them in light of that new information. Bayes' theorem and the rules of probability calculus are introduced in Part I, {numref}`ch:Inferenceandpdfs` and applied throughout this text. 

(sec:Intro:BayesianWorkflow)=
