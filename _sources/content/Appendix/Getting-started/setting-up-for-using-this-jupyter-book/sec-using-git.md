(sec:UsingGit)=
# Using git for cloning the book repository 

## Prerequisites: Install git

If you do not have git installed, download and install it from the official site before proceeding:

- **All platforms:** [https://git-scm.com/downloads](https://git-scm.com/downloads)
- **macOS (alternative):** git is included with the Xcode Command Line Tools. Run `xcode-select --install` in a terminal to install.
- **Linux:** Install via your package manager, e.g. `sudo apt install git` (Debian/Ubuntu) or `sudo dnf install git` (Fedora).

Open a terminal and verify that git is available by running:

```bash
git --version
```

## Cloning the repository

Open a terminal, navigate to the directory where you want to store the book material, and run:

```bash
git clone https://github.com/NuclearTalent/LFD_for_Physicists.git
```

This will create a folder called `LFD_for_Physicists` in your current directory containing the repository with all files.

Move into the repository folder:

```bash
cd LFD_for_Physicists
```

The book material, including demo and exercise notebooks, is in the `content` subdirectory organized by parts and chapters in the book. You will need a working python environment to run the notebooks interactively on your local computer. See {ref}`sec:InstallingPython`.

## Keeping your local copy up to date

As the book material is updated, you can pull the latest changes by running the following command from inside the repository folder:

```bash
git pull
```

## Recommended git guides

There are plenty of tutorials and guides how to use git. Two recommended ones are:

- [The Git Handbook](https://guides.github.com/introduction/git-handbook/) (a GitHub Guide),
- [Pro Git](https://git-scm.com/book/en/v2) (an extensive online book).

