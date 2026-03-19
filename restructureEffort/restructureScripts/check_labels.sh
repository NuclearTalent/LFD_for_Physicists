#!/usr/bin/env bash

# Original label list (duplicates allowed here)
labels_raw=(
"demo:exploring-pdfs"
"demo:visualization-of-the-central-limit-theorem"
"demo:sum-of-normal-variables-squared"
"demo:exploring-pdfs"
"exercise:gaussian-noise-and-averages-ii"
"demo:visualization-of-the-central-limit-theorem"
"demo:visualization-of-the-central-limit-theorem"
"demo:bayesian-coin-tossing-interactive"
"demo:bayesian-coin-tossing-interactive"
"exercise:fitting-a-straight-line-i"
"exercise:gaussian-noise-and-averages-ii"
"exercise:radioactive-lighthouse-problem"
"exercise:gaussian-noise-and-averages-ii"
"exercise:fitting-a-straight-line-i"
"exercise:fitting-a-straight-line-i"
"demo:ball-drop-experiment"
"sec:RootMCMC"
"demo:exploring-pdfs"
"demo:bayesian-coin-tossing"
"demo:bayesian-coin-tossing-interactive"
"demo:pymc-introduction"
"demo:pymc-introduction"
"demo:comparing-samplers-for-a-simple-problem"
"project:zeus-multimodal"
"sec:mcmc-parallel-tempering-ptemcee-vs-zeus"
"demo:random-walk-and-sampling"
"demo:random-walk-and-sampling"
"exercise:fitting-a-straight-line-i"
"exercise:fitting-a-straight-line-ii"
"demo:one-dimension-regression-example"
"demo:prior-and-posterior-with-different-kernels"
"demo:gaussian-processes"
"exercise:gaussian-processes"
"exercise:gaussian-processes"
)

# Deduplicate labels while preserving order
unique_labels=()
seen=""
for label in "${labels_raw[@]}"; do
    if [[ ! " $seen " =~ " $label " ]]; then
        unique_labels+=("$label")
        seen="$seen $label"
    fi
done

echo ""
echo "Checking label definitions in content/ …"
echo "------------------------------------------------"

for label in "${unique_labels[@]}"; do
    if grep -R "(${label})=" content >/dev/null 2>&1; then
        echo "[OK]       $label"
    else
        echo "[MISSING]  $label"
    fi
done

echo "------------------------------------------------"
echo "Done."
echo ""