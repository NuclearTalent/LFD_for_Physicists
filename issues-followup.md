## Issues to follow-up on following the directory restructure:

- [x] **1. How to name chapter and section overview md files in the file structure?**

We could either use descriptive file names (option 1) or the more recommended use of index.md for the landing page of each part/chapter (option 2).

I made an executive decision to go for **option 2**.

Option 1:
│   ├── MCMC-sampling
│   │   └── Overview_MCMC-sampling.md
│   │   ├── Intuition-for-MCMC
│   │   │   ├── Intuition-for-MCMC.md
│   │   │   ├── sec-basic-structure-and-intuition-for-mh.md

Option 2:
│   ├── MCMC-sampling
│   │   └── index.md
│   │   ├── Intuition-for-MCMC
│   │   │   ├── index.md
│   │   │   ├── sec-basic-structure-and-intuition-for-mh.md

- [ ] **2. Should we specify(possibly shorter) titles in the toc?**

**Decisions and Action items**:
- We will shorten some titles in the md files, specifically aiming for all chapter titles to fit on one line. 
- We will keep the title  specification in the toc for clarity, but should make sure that navigation and markdown titles are consistent (a validation scripts exists and can be used).
- We might need to revisit these choices depending on toc format changes in jb 2.0.
*End Action Items*

E.g., the following code appears in the toc:

```
  - title: "Details of MCMC"
    file: content/MCMC-sampling/Details-of-MCMC/Details-of-MCMC.md
    sections:
    - title: "Stochastic processes"
      file: content/MCMC-sampling/Details-of-MCMC/sec-stochastic-processes.md

```

The explicit specification of section/chapter title is not always done. E.g.

```
  - title: "Multi-model inference with Bayes"
    file: content/Advanced-Bayesian-methods/Multi-model-inference-with-Bayes/Multi-model-inference-with-Bayes.md
    sections:
    - file: content/Advanced-Bayesian-methods/Multi-model-inference-with-Bayes/sec-model-selection/sec-model-selection.md
      sections:
      - file: content/Advanced-Bayesian-methods/Multi-model-inference-with-Bayes/sec-model-selection/BUQ/Evidence_for_model_EFT_coefficients.ipynb

```
Note that in example 1 the md file has its own title definition

```
(sec:StochasticProcesses)=
# Stochastic processes
```

and it is this one that sets the title of the section and that is used when {ref}`sec:StochasticProcesses` is used.
The title: "Stochastic processes" in the toc is used in the navigation menu (meaning that it can be different than the title in the section itself)

Should we use (possibly shorter) navigation menu titles in the toc, or just file names?
- (+) the mapping between toc and files becomes even more clear
- (+) one can use shortened title names in the navigation menu
- (+) having the title in the toc might allow us to shorten the file names but keep the clear mapping
- (-) the toc becomes even longer
- (-) there is a risk that sections are named inconsistently in the navigation menu and in the text itself
- (-) risk for confusion with short and long titles

The validate_toc_advanced.sh script can be run to check for heading mismatches.

- [ ] **3. Nested sections in the toc should be removed.**

**Decisions and Action items**:
- CF will make selected, obvious updates: 
   - Model selection and Model averaging should be promoted to chapters.
   - Demo notebooks that are currently sub subsections should be promoted to sections
- Other instances of nested sections will be left intact since they indicate material that must be iterated. => Will be copied to a new issue after the restructuring.
*End Action Items*

See for example

```
  - title: "Multi-model inference with Bayes"
    file: content/Advanced-Bayesian-methods/multi-model-inference-with-bayes/index.md
    sections:
    - file: content/Advanced-Bayesian-methods/multi-model-inference-with-bayes/sec-model-selection/sec-model-selection.md
      sections:
      - file: content/Advanced-Bayesian-methods/multi-model-inference-with-bayes/sec-model-selection/BUQ/Evidence_for_model_EFT_coefficients.ipynb
      - title: "Follow-up to EFT evidence"
        file: content/Advanced-Bayesian-methods/multi-model-inference-with-bayes/sec-model-selection/BUQ/two_model_evidence.md
      - title: "Computing the evidence"
        file: content/Advanced-Bayesian-methods/multi-model-inference-with-bayes/sec-model-selection/BUQ/computing_evidence.md
      - file: content/Advanced-Bayesian-methods/multi-model-inference-with-bayes/sec-model-selection/BUQ/MCMC-parallel-tempering_ptemcee_vs_zeus.ipynb
```

- [x] **4. Decide on directory structure for figures and data.**

I made an executive decision to use **option 2** (see below).

- Given that we might have both figures and data I suggets using the name "assets".
- The number of data files will be much smaller, so I suggest just putting both figures and data directly under assets without additional substructure.
- Concerning the location of assets there are two options:
  - Option 1: A root level assets directory with the different parts as subdirectories. I.e., assets/PARTNAME/
  - Option 2: An assets directory inside each part: content/PARTNAME/assets/

The advantage of option 1 is having a single, central location.
The advantage of option 2 is easier (relative path) markdown referencing, and avoiding two PARTNAME directories (one in content and one in assets).

- [x] **5. Validate that all figure references are working as expected.**

This work is ongoing, but we might want to decide on the nested section structure before proceeding.

See scripts:
- find_figure_references.sh might be useful
- but create a new script for this task

- [ ] **6. Consistent use of apostrophe fencing.**

**Decisions and Action items**
- Dick will consult the jb 2 manual to figure out how to proceed.
*End Action Items*

There are several instances of colon fencing in figure environments, e.g.,

```
:::{figure} ../figs/statistical_model.png
```

using three (or more) colons. We should consider converting all colon‑fenced figures to fenced code blocks (Jupyter Book’s canonical form!?):

````
```{figure} ../figs/statistical_model.png
:name: fig-statistical-model
:width: 70%
Caption here.
```
````

- [ ] **7. Replace all external url references to other versions of the LfD book with internal references.**

**Decisions and Action items**
- Should be relatively easy.
- Check format for references in jb 2.0.
*End Action Items*

MyST format for, e.g., section references, or what?

- [ ] **8. Demo notebooks.**

**Decisions and Action items**
- We will label all demonstrations as demo-[demo title].ipynb
- All chapters will then contain: landing page (index.md), sections (sec-[section title].md) and demonstrations (demo-[demo title].ipynb)
- All demonstrations should have the same title format: Demonstration: NAME OF DEMO
- Revisiting consistent titles might be a follow-up issue after the restructuring.
*End Action Items*

We have used the convention that these are named sec-demo-NAME.ipynb
(but not consistently)

## Issues to follow up after the restructuring

- [ ] Nested sections need cleanup.
- [ ] Chapter and section titles might need cleanup.
- [ ] Making sure that demonstration notebooks have relevant names. E.g. *Demonstration: descriptive title*
- [ ] Execution times of certain notebooks. Exclude from execution or increase time limit? 
- [ ] Special modules used in certain notebooks. Several demo files are now excluded from execution due to the book environment not containing all modules that are used.
- [ ] Replaced execute block in config.yml with mystnb block to avoid conflicts and to prepare for jb 2.0. However, the mystnb block was still ignored. Probably because there was a sphinx config block. I moved the instructions there.
- [ ] Make sure that path-based references are completely gone. Cross-referencing should be done with labels and {ref}`sec:title`.
- [ ] My previous convention for labels is not good but still used.
      I.e., I used labels such as `example:BayesFast:eigenvector-continuation` where the first word is fig, eq, example, etc, and the last one is a descriptive name. The middle one, however, refers to the old structure of directories.
- [ ] All ipynb files now start with a markdown cell with the label. This appears right before the title cell. 
```
{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "93fae5e8f11e45998bc6c2495d39addb",
   "metadata": {},
   "source": [
    "(demo:exploring-pdfs)="
   ]
  },
  {
   "cell_type": "markdown",
   "id": "c8668eca06114065894475e82f78ee54",
   "metadata": {
    "slideshow": {
     "slide_type": "slide"
    }
   },
   "source": [
    "# 📥 Demo: Exploring PDFs\n",
 ```
- [ ] Images in ipynb files: For book builds: prefer Markdown/MyST. For JupyterLab and JupyterBook portability: use attachments in json file.
- [ ] Replace all hyperlinks to pages on https://nucleartalent.github.io
- [ ] Use {eq}`label` rather than {ref}`label` for equation references.