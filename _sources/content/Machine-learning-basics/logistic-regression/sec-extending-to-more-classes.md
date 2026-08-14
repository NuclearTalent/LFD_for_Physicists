---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:ExtendingMoreClasses)=
# Extending to more classes

Until now we have focused on binary classification involving just a decision between two classes. Suppose we wish to extend to $K$ classes.  We will then introduce $K$ outputs $\boldsymbol{y}^{(i)} = \{ y_1^{(i)}, y_2^{(i)}, \ldots, y_{K}^{(i)} \}$. 

```{admonition} Question
Actually, we would only need $K-1$ outputs to create a soft classifier for $K$ classes. Why?
```

Let us for the sake of simplicity assume we have only one feature. The activations are (suppressing the index $i$)

\begin{equation}

z_1 = w_{1,0}+w_{1,1}x_1,

\end{equation}

\begin{equation}

z_2 = w_{2,0}+w_{2,1}x_1,

\end{equation}

and so on until the class $K$:th class

\begin{equation}

z_{K} = w_{K,0}+w_{K,1}x_1,

\end{equation}

and the model is specified in term of $K$ so-called log-odds or **logit** transformations $y_j^{(i)} = y(z_j^{(i)})$.


## Class probabilities: The Softmax function

The transformation of the multiple outputs, as described above, to probabilities for belonging to any of $K$ different classes can be achieved via the so-called *Softmax* function.

The Softmax function is used in various multiclass classification
methods, such as multinomial logistic regression (also known as
softmax regression), multiclass linear discriminant analysis, naive
Bayes classifiers, and artificial neural networks.  Specifically, the predicted probability for the $k$:th class given a sample
vector $\boldsymbol{x}^{(i)}$ and a weighting vector $\boldsymbol{w}$ is (with one independent variable):

\begin{equation}
\prob (t^{(i)}=k\vert \boldsymbol{x}^{(i)},  \boldsymbol{w} ) = \frac{\exp{(w_{k,0}+w_{k,1}x_1^{(i)})}} {\sum_{l=1}^{K}\exp{(w_{l,0}+w_{l,1}x_1^{(i)})}}.
\end{equation}

which means that the discrete set of probabilities is properly normalized. 

Our earlier discussions were all specialized to
the case with two classes only. It is easy to see from the above that
what we derived earlier is compatible with these equations.