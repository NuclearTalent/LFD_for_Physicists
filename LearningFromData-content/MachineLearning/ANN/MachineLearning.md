---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---
(sec:MachineLearning)=
# Machine learning: Overview and notation

(sec:MachineLearning:notation)=
## Notation

{{ sub_MachineLearning_notation }}

See also the notation table in [](sec:OverviewModeling).

## Machine learning in science and society

Machine learning is about learning from data using computer programs. The algorithms in these programs are constructed to process data to find patterns or to make predictions or recommend actions. The automatic aspect of this process opens a wide range of application areas for machine learning techniques and algorithms. In particular, machine learning is used in computer technology but there has also been a swift and amazing development in the last decades that impact domains in the natural sciences, humanities, social sciences, medicine, law, etc. Indeed, almost all possible disciplines are affected. The applications are incredibly many, from self-driving cars to solving high-dimensional differential equations or complicated quantum mechanical many-body problems. Machine learning is perceived by many as a *disruptive technology*, i.e., implying that it will change our society.  

Statistics, data science and machine learning form important fields of research in modern science.  They describe how to learn and make predictions from data, as well as allowing us to find correlations between features in (large) data sets. Such big data sets now appear frequently in essentially all disciplines, from the traditional Science, Technology, Engineering and Mathematics (STEM) fields to Life Science, Law, Education research, the Humanities and the Social Sciences. Having a solid understanding of data analysis and machine learning is thus becoming central to scientific computing in many fields, and competences and skills within the fields of machine learning and scientific computing are nowadays strongly requested by many potential employers. 

Machine learning is a subfield of computer science, and is closely related to computational statistics.  It evolved from the study of pattern recognition in artificial intelligence (AI) research, and has made contributions to AI tasks like computer vision, natural language processing and speech recognition. Many of the methods we will study are also  strongly rooted in basic mathematics and physics research. 

Ideally, machine learning represents the science of giving computers the ability to learn without being explicitly programmed.  The idea is that there exist generic algorithms which can be used to find patterns in a broad class of data sets without having to write code specifically for each problem. The algorithm will build its own logic based on the data.  You should however always keep in mind that machines and algorithms are to a large extent developed by humans. The insights and knowledge we have about a specific system, play a central role when we develop a specific machine learning algorithm. 

```{admonition} Three main ingredients of machine learning
A machine learning model learns from available training data. Thus, one can usually identify three ingredients of basically any machine learning application:

The data
: The first, and often most important, ingredient is the data set. The data is usually split into *training, validation, and test sets*.

The mathematical model 
: The second ingredient is a model, which can be a function of some parameters. The complexity of the model can often be varied.

The learning algorithm  
: The final ingredient is the algorithm that is used for learning. A specific component of the *learning algorithm* is often a so-called *cost function*, which allows us to present an estimate on how good our model is in reproducing the data.

We will encounter several examples (and variations) of these building blocks in the next few chapters.
```  


Machine learning is an extremely rich field, in spite of its young age. Increases in computational capabilities have been followed by developments of methods and techniques for analyzing and handling large date sets---relying heavily on statistics, computer science and mathematics, but also importing ideas from other disciplines such as physics. The field is rather new and developing rapidly. Popular software packages (many of them written in Python) are freely available at their respective GitHub sites and involve developer communities measured in the thousands or more. And the number of code developers and contributors keeps increasing.

```{admonition} Python for machine learning
Some very popular Python libraries for machine learning and probabilistic programming are

- [Scikit-learn](http://scikit-learn.org/stable/),
- [Tensorflow](https://www.tensorflow.org/), 
- [Keras](https://keras.io/)
- [PyMC](https://github.com/pymc-devs/pymc),
- [PyTorch](http://pytorch.org/), 
- [Edward](http://edwardlib.org/) 

In addition, Python is an excellent programming language for prototype construction and for data visualization (with extensive galleries of existing examples).

Still, it should be noted that Python is notoriously slow. Therefore, analysis codes tend to utilize compiled languages (C++,C,  Fortran) and possibly hardware acceleration for the heavy computations.
```  

Not all machine learning algorithms and methods can be given a rigorous mathematical justification, thereby opening up opportunities for experimenting, trial and error, and exciting new developments.  However, a solid command of linear algebra, multivariate analysis, probability theory, statistical data analysis, Bayesian inference, understanding errors and Monte Carlo methods are central elements in a proper understanding of machine learning applications.

## Types of Machine Learning

The approaches to machine learning are many, but are often split into two main categories.  In *supervised learning* we claim to know the system under investigation and we use the computer to deduce the strengths of relationships and dependencies. On the other hand, *unsupervised learning* is used for finding patterns and relationship in data sets without any prior knowledge of the system. Some authours also operate with a third category, namely *reinforcement learning*. This is a paradigm of learning inspired by behavioral psychology, where learning is achieved by trial-and-error using a system of rewards and punishments. Here we will focus mainly on algorithms for supervised learning.

Another way to categorize machine learning is to consider the desired output. What kind of inference are you performing with your data? Is the aim to classify a result into categories, to predict a continuous response variable, or to simply observe patterns within the data? Let’s briefly introduce different types of tasks:

```{admonition} Regression algorithms
  aims to find a functional relationship between input and output (predictor and response). The goal is often to construct a function that maps input data to continuous output values. These algorithms also require labeled output.
  ```

```{admonition} Classification algorithms
  are used to predict splitting of a data set into separate classes; binary or multiple. The outputs are discrete and represent target classes. Classification algorithms often undergo supervised training, which means they require labeled true output data. 
  ```  
  
```{admonition} Clustering algorithms
  can also be used for classification or simply to observe data patterns. By observing structures of data within the feature space, clustering algorithms aim to identify clusters. Some algorithms of this type don’t require output labels, making them unsupervised algorithms.
  ```

```{admonition} Dimensionality reduction algorithms
  focuses on decreasing the number of features from your data set, identifying the most important predictor variables and preventing your models from overfitting. They are usually unsupervised.
  ```

```{admonition} Generative models
  aims to find patterns and structures within a data set and turn these into a generative model that that can be used to create new data.
  ```

Sometimes, the data collection process automatically provides the labels used in supervised learning, but in some cases the labeling is in itself a painstaking task that involves manual labor.

In the natural sciences, where we often confront scientific models with observations, there is certainly a large interest in regression algorithms. However, there are also many examples where other classes of machine-learning algorithms are being used. 


## Data handling, machine learning  and ethical aspects

The data collection (or selection) process in a machine learning pipeline has important ethical aspects. Undetected biases in the data set will propagate via the learning algorithm to the final model predictions. In physics, the model might be rather well understood, and we might have good control over the data generation process, but we should still develop a sound ethical attitude to the use, processing and analysis of data.

Another pressing ethical aspects deals with our approach to the scientific process. In particular, it is of utmost importance that scientific results are reproducible. In fact, reproducibility should be imprinted as part of the dialectics of science.  Nowadays, with version control software like [Git](https://git-scm.com/) and various online repositories like [Github](https://github.com/), [Gitlab](https://about.gitlab.com/) etc, we can easily make our codes and data sets openly and easily accessible to a wide community. This service helps almost automagically to make our science reproducible. The large open-source development communities involved in [Scikit-Learn](http://scikit-learn.org/stable/), [Tensorflow](https://www.tensorflow.org/), [Keras](https://keras.io/), etc, are all excellent examples of this. The codes can be tested and improved continuosly, helping thereby our scientific community at large in developing data analysis and machine learning tools.  It is much easier today to gain traction and acceptance for making your science reproducible. From a societal stand, this is an important element since many of the developers are employees of large public institutions like universities and research labs.

Let us also add a disclaimer concerning the fantastic progress of machine learning technology. Even though we may dream of computers developing some kind of higher learning capabilities, at the end it is we (yes you reading these lines) who end up constructing and instructing, via various algorithms, the machine learning approaches. 

For self-driving vehicles, where the standard machine learning algorithms discussed here enter into the software, there are stages where the human programmer must make choices. As an example, all carmakers have the safety of the driver and the accompanying passengers as their utmost priority. Consider the scenario where the programmer has to construct an *if* statement that decides in an accident scenario between crashing into a truck or steering into a group of bicyclists.  

This leads to serious ethical aspects. Who is entitled to make such choices? Keep in mind that many of the algorithms you will encounter in this series of lectures, or that you will hear about later, are indeed based on simple programming instructions. And you are very likely to be one of the people who end up writing such a code. Thus, developing a sound ethical attitude is much needed. The example of the self-driving cars is just one of infinitely many cases where we have to make choices. Other domains where applications might have serious ethical aspects include the financial sector, law, and medicine.

We do not have the answers here, nor will we venture into a deeper discussions of these aspects, but you should think over these topics in a more overarching way.  A statistical data analysis with its dry numbers and graphs meant to guide the eye, does not necessarily reflect the truth, whatever that is.  As a scientist, and after a university education, you are supposedly a highly qualified citizen, with an improved critical view and understanding of the scientific method, and perhaps some deeper understanding of the ethics of science at large. Use these insights. You owe it to our society.