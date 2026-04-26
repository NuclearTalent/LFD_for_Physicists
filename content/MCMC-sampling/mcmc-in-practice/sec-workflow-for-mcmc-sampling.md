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

(sec:workflow-for-mcmc)=
# Workflow for MCMC sampling

Topics to cover:

- *Warm-up phase* (state-space region)
  Intended to move the simulations from a possibly unrepresentative region of state space to something closer to the region where the log posterior density is close to its expected value. Note, the alternative view on this in the Handbook of MCMC.
- *Tuning phase* (algorithm tuning)
  Optimize parameters of the sampling algorithm to the target distribution, represented by the samples found during warm-up.
- *Sampling phase* 
  Accompanied by diagnostics.
  
We should also mention:

- Different views on warm-up plus the alternative terminology of burn-in.
- Pseudo-convergence (and multimodality).
- Many short runs versus (at least) one long run.
- Forward reference to the next section on diagnostics.
- Forward reference to best practices section, and to the advanced MCMC implementations.