(sec:DimensionalityReductionEmulators)=
# Dimensionality reduction and emulators

In this chapter we consider various aspects of dimensionality reduction of data.
A key tool is SVD, which is "singular value decomposition", and its role in PCA, which is "principle component analysis".
These are described in {ref}`sec:SVDandPCA`.

The challenges of simulating physical phenomena are being addressed in many subfields with a wide range of accurate *high-fidelity* methods.
However, when we need to change the parameters characterizing the problem, such as Hamiltonian coupling constants, it can become computationally prohibitive to repeat high-fidelity calculations many times and challenging to reliably extrapolate.
In particular, uncertainty quantification (UQ) generally requires many samples of often expensive calculations, e.g., for Bayesian calibration, sensitivity analyses, and experimental design. 
An alternative to expensive calculations is to replace the high-fidelity model with an *emulator*, which is an approximate computer model, in the literature sometimes referred to as a "surrogate model."

* We start with a general discussion of emulators in {ref}`sec:BayesFast`
* Reduced basis method (RBM) emulators are reviewed in {ref}`sec:RBMEmulators`.
* A demonstration example in {ref}`demo:rbm-ho-gp-example` compares calculating observables from solving a basic eigenvalue problem with a basis expansion to using RBM and GP emulators.
* The RBM discussion is continued in {ref}`sec:Emulator_basis` with a discussion of using active learning to choose the snapshot basis.
* A new type of emulator is described in {ref}`sec:PMMs` {cite}`Cook:2024toj`.
* For examples of multidimensional GP emulation, see [surmise](https://surmise.readthedocs.io/en/latest/).

