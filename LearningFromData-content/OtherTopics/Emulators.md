(sec:Emulators)=
# Emulators

The challenges of simulating physical phenomena are being addressed in many subfields with a wide range of accurate \emph{high-fidelity} methods.
%but often computationally expensive 
However, when we need to change the parameters characterizing the problem, such as Hamiltonian coupling constants, it can become computationally prohibitive to repeat high-fidelity calculations many times and challenging to reliably extrapolate.
In particular, uncertainty quantification (UQ) generally requires many samples of often expensive calculations, e.g., for Bayesian calibration, sensitivity analyses, and experimental design. 
An alternative to expensive calculations is to replace the high-fidelity model with an \emph{emulator}, which is an approximate computer model, in the literature sometimes referred to as a ``surrogate model.''



* Add [Parametric Matrix Models](https://arxiv.org/abs/2401.11694), aka PMMs, with examples.
* Some pointers and background (from an rjf talk) on reduced basis method (RBM) emulations are given in the BUQEYE LFD [here].(https://buqeye.github.io/LearningFromData/content/Gaussian_processes/extra_RBM_emulators.html).
* A brief introduction to emulators is given in the CF LFD [here](https://learningfromdata-cforssen-75e6959196db9d0b88353479987355fdad70a.gitlab.io/content/BayesianStatistics/ComputationalBayes/BayesFast.html).
* Some RBM (Eigenvector Continuation) examples can be adapted from BUQEYE open sources.
* We should include multidimensional GP emulation; use [surmise](https://surmise.readthedocs.io/en/latest/) for examples?
