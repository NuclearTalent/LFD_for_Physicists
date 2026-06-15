---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:ANNFT)=
# ANNs in the large-width limit

Machine learning methods such as artificial neural networks (ANNs) are offering physicists new ways to explore and understand a wide range of physics systems, as well as improving existing solution methods {cite}`Mehta2019`.
ANNs are commonly treated as black boxes that are empirically optimized. Given their growing prominence as a tool for physics research, it is desirable to have a framework that allows for a more structured analysis based on an understanding of how they work. 
Several authors have proposed a field theory approach to analyze and optimize neural networks using a combination of methods from quantum field theory (QFT) and Bayesian statistics {cite}`Roberts:2021lll,Roberts:2021fes,Halverson:2020trp,Halverson:2021aot`. It is based on expanding about the large-width limit of ANNs and is known as ANNFT.


Dan Roberts, in an essay entitled "Why is AI hard and Physics simple?" {cite}`Roberts:2021lll`, claims that the principle of *sparsity* means that methods of theoretical physics and associated physical intuition can be powerful in understanding machine learning.
Roberts interprets Wigner’s observations about "The Unreasonable Effectiveness of Mathematics in the Natural Sciences" as "the laws
of physics have an (unreasonable?) lack of algorithmic complexity".
The key idea is that many neural network architectures (including the common ones) have a well-defined limit when the network width (which is the number of neurons in each layer) is taken to infinity. In particular, they reduce to Gaussian processes (GPs), and with gradient-based training they evolve in a clear way as linear models according to the so-called neural tangent kernel (or NTK). 

This infinite width limit by itself is not an accurate model for actual deep-learning networks, because it is too limited in what it can learn from the data.
But there is a way to describe *finite-width* effects systematically using the correspondence with field theories (statistical or quantum). In this correspondence, the infinite-width limit is associated with free (non-interacting) theories that can be corrected *perturbatively* for finite width as weakly interacting theories. The concepts of effective (field) theories carry over as well, as the information propagation through the layers of a deep neural network can be understood in terms of a renormalization group (RG) flow. A fixed point analysis motivates strategies for tuning the network to criticality, which deals with gradient problems (blowing up and going to zero).




