---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:Sparsity)=
# Sparsity

Roberts argues how the most generic theory in a quantum field theory framework without guiding principles would start with all combinations of interactions between the particles in the theory but that applying several guiding principles of sparsity will drastically reduce the algorithmic complexity.
He first discusses why AI is hard by considering all possible $n$-pixel images that take on two values (e.g., black or white), so that there are $2^n$ different images. 
If each of these images has one of two possible labels (e.g., cat/not-cat or spin-up/spin-down), then the images can be labeled $2^{2^n}$ ways. This is a really big number. If the labels don't correlate with image *features*, then you can't do better than memorizing images with their labels.

Roberts follows by discussing why physics is simple; these are the arguments that lead him to paraphrase Wigner.
In particular, he analyzes the degrees of freedom (dofs) within a QFT-like framework. When thinking about the associated counting of possible terms in the Hamiltonian, it is convenient to have the Ising model in mind as a concrete and familiar example (i.e., imagine a lattice of spins).
The starting point is a generic theory with all interactions between all spins; two at a time, three at a time, and so on. Generically the strength of the couplings for these interactions would all be different.
So is there are $N$ spins in the Ising model lattice, with no restriction on interactions, there will be $2^N$ possible independent interaction terms in the Hamiltonian. (I.e., a given spin is there or not in any term.) This Hamiltonian would have no predictive power because you would have to do every experiment to determine the interaction strengths, with no correlation between experiments to enable predictions.

The highest level of sparsity is to limit the number of degrees of freedom that contribute to any interaction; this is what we observe in nature. If the limit is $k$ degrees of freedom, with $k \ll N$, then the dominant term when summing interactions with $N\gg 1$ is

$$
   \binom{N}{k} \sim N^k/k! ,
$$

i.e., now the number of parameters is just polynomial in $N$. This is called *$k$-locality*. But this is too general still, because we also observe *spatial locality*: $N$ dofs interact only with neighbors (e.g., nearest or next-to-nearest). This mean in $d$ dimensions the number of parameters scales like the number of neighbors, meaning of order $Nd$.
Finally, we also observe *translational invariance*. This implies that the strength of any local interaction is the same everywhere (electric charge or the Ising model coupling). Now the number of parameters is order unity.

A summary of the sparsity counting of dofs is:

$$
 2^{\mathcal{O}(N)} \xrightarrow[\text{locality}]{k}
 \mathcal{O}(N^k) \xrightarrow[\text{locality}]{\text{spatial}}
 \mathcal{O}(N) \xrightarrow[\text{invariance}]{\text{translational}}
\mathcal{O}(1) .
$$

This is a spectacular reduction in the dofs!
A consequence is that we have structure to possible physics theories.
Sparsity enables us to learn physics and accounts for why physics can provide simple explanations for apparently complicated phenomena.

What does this imply about AI? Because machine learning *does* work, this implies that deep learning and the like will lead to sparse descriptions. We can try to use our a physics framework to organize that description.

