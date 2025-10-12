# Hamiltonian Monte Carlo (HMC) overview and visualization

<!--We've seen some different strategies for sampling difficult posteriors, such as an affine-invariant sampling approach (emcee) and a thermodynamic approach (parallel tempering).-->

Here we will look at some visualizations as motivation for HMC, then consider some examples using the PyMC library.



## HMC physics



## HMC algorithm

Two steps of the HMC algorithm:

1. New values for the momentum variables are randomly drawn from their Gaussian distribution, independent of current position values.
    * This means $p_i$ will have mean zero and variance $M_{ii}$ if $M$ is diagonal.
    * $q$ isn't changed, $p$ is from the correct conditional distribution given $q$, so the canonical joint distribution is invariant.

2. Proposal from Hamiltonian dynamics for a new state. Simulate from $(q,p)$ with $L$ steps of size $\epsilon$. At the end, the momenta are flipped in sign and the new proposed step $(q^*,p^*)$ is accepted with probability (cf. $\Delta E$ with $T=1$):

$$
 \min[1,e^{-H(q^*,p^*) + H(q,p)}] = \min[1,e^{-U(q^*)+U(q)-K(p^*)+K(p)}] .
$$

    * The momentum flip makes the proposal symmetric, but not done in practice.
    * So the probability distribution for $(q,p)$ *jointly* is (almost) unchanged because energy is conserved, but in terms of $q$ we get a very different probability density.

* You can show that HMC leaves the canonical distribution invariant because detailed balance holds, which is what we need. It will also be *ergodic* $\Lra$ it doesn't get stuck in a subset of phase space but samples all of it.

* Essential features:
    * Reversability needed so that desired distribution is invariant.
    * Conservation of the Hamiltonian (which is the energy here).
    * Volume preservation - preserves volume in $(q,p)$ phase space - this is Liouville's Theorem. (If we take a cluster of points and follow their time evolution, the volume they occupy is unchanged. See [](./Liouville_theorem_visualization.ipynb) notebook.) $\Lra$ this is critical because a change in volume would mean we would have to make a nontreival adjustment to the proposal (because the normalization $Z$ would change).

