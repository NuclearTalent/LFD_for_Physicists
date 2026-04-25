(sec:InstallingPython)=
# Setting up your Python environment

**Last revised:** 22-Apr-2026

## Overview

To run the Jupyter notebooks you will need a Python installation together with a number of scientific computing libraries (NumPy, SciPy, Matplotlib, and others). We manage these using **conda**, a package and environment manager that works on Windows, macOS, and Linux.

We recommend installing conda via **Miniforge**, a minimal, community-maintained distribution that is free to use without licensing restrictions and comes pre-configured with the [conda-forge](https://conda-forge.org/) package channel. This replaces Anaconda's defaults channel, which includes licensing terms that are problematic for many users.

---

## 1. Installing Miniforge3 (fresh installation)

If you do not have conda installed, follow the instructions for your operating system below.

### macOS

Open a terminal and run one of the following commands depending on your hardware:

**Apple Silicon (M1/M2/M3 — most Macs from 2020 onwards):**
```bash
curl -L https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh -o Miniforge3.sh
bash Miniforge3.sh
```

**Intel Mac:**
```bash
curl -L https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-x86_64.sh -o Miniforge3.sh
bash Miniforge3.sh
```

Follow the prompts, accept the license, and allow the installer to initialise conda in your shell. When the installation is complete, close and reopen your terminal.

### Linux

Open a terminal and run:

```bash
curl -L https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh -o Miniforge3.sh
bash Miniforge3.sh
```

Follow the prompts as for macOS above.

### Windows

Download the Windows installer from the [Miniforge Latest Release page](https://conda-forge.org/download), selecting the Windows x86_64 options. This will download
`Miniforge3-Windows-x86_64.exe`.

Run the installer and follow the graphical prompts. We recommend:

- Installing for the current user only (does not require administrator privileges)
- Ideally you will accept the default installation path. This may not be possible if the path contains special characters (including spaces and accents). You should get a warning if this is the case, which will require setting up another installation path.
- You have the option to **"Add Miniforge to my PATH environment variable"** if you intend to use conda from a standard Command Prompt or PowerShell window. However, this has been found to cause problems for many users and the official recommendation is to not do this. Instead, you will use the **Miniforge Prompt** that is added to your Start menu.

### Verify the installation

Once installed, open the **Miniforge Prompt** (Windows) or a new terminal (macOS/Linux) and verify the installation:

```bash
conda --version
```

You should see version 24.x or later. Miniforge3 should be configured with the `conda-forge` channel by default, in which case no further channel configuration is needed. However, to be sure, continue with the next step.

---

## 2. Updating an existing conda installation (even if just installed)

Follow these steps to ensure your conda installation is compatible with current best practices.

### Step 1 — Update conda to version 23.10.0 or later

Conda 23.10.0 introduced `libmamba` as the default dependency solver, which is significantly faster than the old solver. Check your current version and update if needed:

```bash
conda --version
conda update -n base conda
```

Verify the version is 23.10.0 or higher before proceeding.

### Step 2 — Switch from the `defaults` channel to `conda-forge`

The Anaconda `defaults` channel has licensing restrictions that are problematic for many academic users. You can verify your channel configuration with:

```bash
conda config --show channels
```

The output should list only `conda-forge`.

If the `defaults` channel is used in your installation, then you should replace it with `conda-forge`:

```bash
conda config --remove channels defaults
conda config --add channels conda-forge
conda config --set channel_priority strict
```

The `strict` channel priority setting is strongly recommended when using `conda-forge` exclusively — it prevents packages from different channels from being mixed, which can cause subtle dependency conflicts.

---

## 3. Creating the course environment

The Python packages needed for this course are specified in the `environment.yml` file in the repository. Navigate to the `LFD_for_Physicists` directory you cloned from GitHub (see [cloning instructions](sec:UsingGit)) and create the environment:

```bash
conda env create -f binder/environment.yml
```

The environment creation will take a few minutes. When it completes successfully you will see a message with instructions for activating the environment.

### Activating and deactivating the environment

```bash
conda activate 2026-env-lfd       # activate
conda deactivate              # deactivate when done
```

On Windows, run these commands in the **Miniforge Prompt**.

---

## 4. Launching JupyterLab

We recommend **JupyterLab** as the interface for working with the course notebooks. Once the environment is activated, launch it with:

```bash
cd content
jupyter lab
```

This will open JupyterLab in your browser. Navigate to the notebook you want to open using the file browser on the left.

:::{note}
If you prefer the classic single-document notebook interface, Jupyter Notebook v7 is also supported. Start it with `jupyter notebook`. The old classic Notebook interface (nbclassic) is no longer maintained and should not be used.
:::

### Verifying the correct kernel

When a notebook is open, check that the kernel shown in the upper right corner of JupyterLab reads `Python [conda env:2026-env-lfd]`. If it shows a different kernel, click on it and select the correct environment from the list.

---

## 5. Updating the course environment

The `environment.yml` file is updated from time to time as new packages are added. After pulling the latest changes from the repository, update your environment with:

```bash
conda deactivate
conda env update -f binder/environment.yml --prune
conda activate 2026-env-lfd
```

The `--prune` flag removes packages that are no longer listed in the environment file, keeping the environment clean.
