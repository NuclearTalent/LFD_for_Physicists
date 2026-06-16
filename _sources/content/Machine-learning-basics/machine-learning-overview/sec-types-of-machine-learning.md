# Types of Machine Learning

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


