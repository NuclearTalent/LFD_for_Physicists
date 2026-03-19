(sec:Emulators)=
# Emulators

The challenges of simulating physical phenomena are being addressed in many subfields with a wide range of accurate *high-fidelity* methods.
However, when we need to change the parameters characterizing the problem, such as Hamiltonian coupling constants, it can become computationally prohibitive to repeat high-fidelity calculations many times and challenging to reliably extrapolate.
In particular, uncertainty quantification (UQ) generally requires many samples of often expensive calculations, e.g., for Bayesian calibration, sensitivity analyses, and experimental design. 
An alternative to expensive calculations is to replace the high-fidelity model with an *emulator*, which is an approximate computer model, in the literature sometimes referred to as a ``surrogate model.''



* Reduced-basis methods are introduced in {ref}`sec:BayesFast`.
* A review of {ref}`sec:RBMEmulators`.
* For examples of multidimensional GP emulation, see [surmise](https://surmise.readthedocs.io/en/latest/).
* A new type of emulator is the Parametric Matrix Model {cite}`Cook:2024toj`.

