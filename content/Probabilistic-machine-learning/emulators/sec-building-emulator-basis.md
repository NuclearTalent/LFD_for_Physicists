---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:Emulator_basis)=
# Building an emulator basis

In this section we consider two alternatives to selecting an RBM basis (i.e., the snapshots) at random.
They are the Proper Orthogonal Decomposition (POD) methods and the greedy algorithm.
We use figures from [Maldonado et al.](https://arxiv.org/abs/2504.06092) to provide a short overview and refer the reader to the literature for more details.

## Overview

{numref}`fig-emulator_basic_construction` gives an overview of how the two alternative methods of making an informed choice of basis work.

:::{figure} ../assets/emulator_basic_construction.png
:height: 480px
:name: fig-emulator_basic_construction 

Figures from [Maldonado et al.](https://arxiv.org/abs/2504.06092) illustrating on the left the basic problem of where to place snapshots and describing the two options. On the right is a comparison of how the two methods arrive at a basis of size six. The POD requires an evaluation of a large number of full-order model (FOM) calculations, that are processed to arrive at six basis elements while the greedy algorithm simply chooses successively the next snapshot according to which has the greatest error (based on a proxy calculation of the error). 
:::

## POD approach

{numref}`fig-Proper_Orthogonal_Decomposition` gives a schematic illustration of how POD is implemented using a singular value decomposition (SVD). See {numref}`sec:DimensionalityReduction` for details on SVDs and also the related Principle Component Analysis (PCA) approach to dimensional reduction.

:::{figure} ../assets/Proper_Orthogonal_Decomposition.png
:height: 480px
:name: fig-Proper_Orthogonal_Decomposition

Figure from [Maldonado et al.](https://arxiv.org/abs/2504.06092) indicating how the POD is carried out. Matrix $M$ is the original matrix of $m$ snapshops each of length $n$. The matrix $U_r$ is the $r$-dimensional basis that is to be applied in the RBM emulator.

:::


## Greedy algorithm

{numref}`fig-Greedy_algorithm_in_action` shows the sequence of steps in implementing the greedy algorithm to select a snapshot basis.

:::{figure} ../assets/Greedy_algorithm_in_action.png
:height: 480px
:name: fig-Greedy_algorithm_in_action


Figure from [Maldonado et al.](https://arxiv.org/abs/2504.06092) showing how the greedy algorithm is implemented.
:::


## Comparison

{numref}`fig-POD_vs_greedy_algorithm` summarizes the comparison between POD and greedy algorithm approaches to selecting snapshots for an emulator that calculates observables for a quantum scattering problem (from [Maldonado et al.](https://arxiv.org/abs/2504.06092)).

:::{figure} ../assets/POD_vs_greedy_algorithm.png
:height: 480px
:name: fig-POD_vs_greedy_algorithm

Figures from [Maldonado et al.](https://arxiv.org/abs/2504.06092) showing that while the POD provides slightly more accuracy, the greedy algorithm is close and requires many fewer high fidelity snapshots.
:::



