---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:BayesFast)=
# Bayes goes fast: Emulator overview

```{epigraph}
> "Emulation is not rivalry. Emulation is the child of ambition; rivalry is the unlovable daughter of envy."

-- Honore de Balzac
```


## Emulators

Being able to efficiently vary the parameters in high-fidelity models to enable design, control, optimization, inference, and uncertainty quantification is a general need across engineering and science fields.
A common theme in these endeavors is that much of the information in high-fidelity models is superfluous. This can be exploited when tracing parametric dependencies by reducing the complexity through a so-called reduced order model, i.e., an emulator.
The universe of model order reduction (MOR) methods is relatively mature but continues to expand, along with their applications.
There remain tremendous opportunities for physicists to adapt and extend methods from the MOR literature.


:::{figure} ../assets/MOR_Venn_diagram_6.png
:height: 300px
:name: fig-MOR_Venn_diagram

Schematic classification of model order reduction emulators into data-driven methods, including Gaussian processes,  artificial neural networks, and dynamic mode decomposition; model-driven methods, including reduced-basis methods (RBMs); and hybrid methods. Eigenvector continuation (EC) approaches are a subset of RBM.

:::



## Reduced-Basis Methods

Computational Bayesian methods, in particular, have a need for models that can be solved at different fidelities. High fidelity implies high precision, but also high computational cost. Low fidelity versions of the model are much faster to evaluate, but associated with a smaller precision. They are still very useful for model calibration and statistical studies. 

There is a vast theory of model-order reduction for scientific applications. See, e.g., Ref. {cite}`Melendez:2022kid` for an overview and many useful references. Let us broadly categorize them into two types (see {numref}`fig-MOR_Venn_diagram`):

```{admonition} Model-order reduction
:class: note

**Date driven**: Non-intrusive approaches where the outputs of a high-fidelity model are interpolated (or even dangerously extrapolated) without the need for detailed access to the model or an understanding of the underlying model structure. Examples include:
- Gaussian process regression models
- Artificial neural networks
- Dynamic mode decomposition


**Model driven**: Intrusive approaches where reduced-order equations are derived from the full high-fidelity equations (often using projection), so they are physics-based. These methods require a deeper understanding of the model and respect the underlying structure, which often means they can extrapolate reliably. 
Examples include the broad class of reduced-basis methods or RBMs. 

**Hybrid**: Increasingly, there are hybrid approaches drawing from knowledge about the underlying physics problem and thereby combining both data- and model-driven aspects. An example are Parametric Matrix Models (see {numref}`sec:PMMs`).


```

:::{admonition} Physics-informed data-driven method
:class: note
An example of a physics-informed data-driven method is to constrain the kernel for a Gaussian process emulator by where we know a priori that it will be more reliable.
:::



In general, we will use model-order reduction to emulate our model, that is we will replace the high-fidelity version $M(\pars)$ with a low-fidelity emulator $\tilde M(\pars)$ which is much faster to evaluate but hopefully acceptably accurate. We will need to keep track of the emulator uncertainty via quantification of $\var{M(\pars) - \tilde M(\pars)} \equiv \var{\delta \tilde M (\pars)}$. We will often neglect the parameter dependence such that 

$$
M(\pars) = \tilde M(\pars) + \delta \tilde M,
$$ (eq:BayesFast:emulator-error)

where $\var{\delta \tilde M} = \sigma_\mathrm{em}^2$.

A large subset of model-driven approaches are known as **Reduced-Basis Methods (RBMs)** {cite}`Quarteroni2015`. We will mainly be concerned with the application of RBMs to quantum models, which was introduced to physics as **eigenvector continuation (EC)** {cite}`Frame:2017fah`.
The introduction of emulators derived from EC was a game-changing development for Bayesian UQ in low-energy nuclear physics. 


