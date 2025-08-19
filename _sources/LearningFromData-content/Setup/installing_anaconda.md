(sec:InstallingAnaconda)=
# Using Anaconda

## Installing Anaconda

**Last revised:** 26-Jul-2025 by Dick Furnstahl (furnstahl.1@osu.edu)

**Overview of what you need: Anaconda Python**

You may already have Python on your computer, but it may not be the version we need (Python changes rapidly) and there are many additional software libraries we will need for scientific computing: Numpy, Scipy, Matplotlib are examples. Fortunately, there is a one-stop-shopping solution: download and install Anaconda Python. It comes with all of the packages we need, plus a great mechanism (a package manager called conda) for updating or installing new packages. Anaconda is available for Windows, macOS, and Linux. One caveat is that the package is not small: the size is over 3GB. If that is a problem, ask about other options to installing the full package (see the documentation on Miniconda).

**How to get Anaconda Python** **[Also see the Anaconda Distribution Starter Guide]**

Step-by-step instructions for downloading and installing Anaconda are available for Windows, Mac OSX (Intel or Apple silicon), or Linux. Here we&#39;ll step through the relevant options for us (based on following the graphical installer, which is what you will get by default for Windows and Macs; for Linux it is assumed you can follow the instructions for Linux (note: there is now a graphical installer option).

1. Go to [https://www.anaconda.com/products/individual - Downloads](https://www.anaconda.com/download/success) and select the **Download** button for your type of computer (use the 64-bit installer).
2. An installation program will be downloaded. Start it up (e.g., by double clicking).
3. Accept the license agreement.
4. Install for All Users (this assumes you have admin privileges; it avoids potential later problems if you can do this). Allow the installation if your virus protection software asks you.
5. It is suggested you accept the suggestion for the installation location (e.g., C:\ProgramData\Anaconda3 on Windows). [Note: steps 4 and 5 may be reversed for a Mac install.]
6. For Windows, accept the checked Advanced Options as &quot;Register Anaconda as my default Python x.x&quot; and click **Install**.
7. While it is installing, you might want to click **Show Details** to see progress. It will take a while, depending on your hardware. Be patient!
8. If it works, you&#39;ll get to a &quot;Thanks for installing Anaconda Individual Edition!&quot; page. There will be two already-checked boxes. You _ **do not** _ need to sign up for Anaconda Cloud, so uncheck that one. But you might want to read the &quot;Getting started with Anaconda&quot; information. Click **Finish** you are done.

## Anaconda and github

**Installation of the LearningFromData notes and Jupyter notebooks from GitHub by command line**

Go to the location where you want the notebook files. 

Download the LFD_for_Physicists repository from GitHub with the following:

```
git clone https://github.com/NuclearTalent/LFD_for_Physicists.git
```

The notebooks that we will be using depend on several scientific python modules (see the list in environment.yml) and require a python3.x installation based on Anaconda. This is best done within a conda environment, as described in the next section.


## Anaconda environments

### Creating a conda environment

The python modules needed for Learning from Data and their dependencies are best installed using ``conda`` by creating
a virtual environment:

	conda env create

which reads the `environment.yml` file in your current directory (in this case, however, the file is in the `binder` subdirectory). [Note: if you are using Windows, you should do this in an Anaconda Prompt window.]

To use a different file name such as `environment_JB.yml`: `conda env create -f environment_JB.yml`. This is the environment to use if you want to build the Jupyter Book locally (this is not necessary; you can get all the libraries you need using `binder/environment.yml`)

It will take a while to generate the new environment; be patient!  You will see a listing being generated like:
        
       Downloading and Extracting Packages
       scikit-learn-0.21.3  | 5.9 MB    | ##################################### | 100% 
       glib-2.58.3          | 3.1 MB    | ##################################### | 100% 
       libcxx-8.0.1         | 1000 KB   | ##################################### | 100% 
       scipy-1.3.1          | 18.1 MB   | ##################################### | 100% 
etc. (it will be a pretty long list with more up-to-date version numbers and not necessarily in this order).  Then you'll see

       Preparing transaction: done
       Verifying transaction: done
       Executing transaction: done 
where "done" appears when it has finished.  If all is well at the end, you'll get a success message.  If it fails, email the message you get to furnstahl.1@osu.edu and we'll figure out the problem.

Some packages might not be found in the default conda channels. One
can either specify relevant package channel(s) in the environment.yml
file (as done here), or add them to the default conda channel configuration via, e.g,

	conda config --append channels conda-forge

You shouldn't need to do this for the initial setup.

Once the virtual environment has been created it can be activated (the name "2025-env" was specified in the `environment.yml` file and "2025-book-env" in the `environment_JB.yml` file):

    conda activate 2025-env

To deactivate the virtual environment:

    conda deactivate

Note that earlier versions of conda used 'source' instead of 'conda'
to activate environments. If you have an earlier version of conda you
might have to do

    conda update conda

Note that there are also other options ('venv', 'pipenv') for creating virtual
environments that includes the python version and packages that we will be using.

Once the environment is set up and activated, you are encouraged to run some of the Jupyter notebooks by doing this:

    cd LearningFromData-content
    jupyter notebook

and looking for notebooks in the subdirectories.

### Updating your conda environment for Learning from Data

Go to the `LFD_for_Physicists` directory you created by cloning the class repository from GitHub.  This is where the relevant `environment_JB.yml` file (or `binder/environment.yml`) is stored.  This file defines the environment and will be occasionally updated to add additional modules.  
You can update to the new environment with:

    conda deactivate
    conda env update 
    
Now if you activate the environment again:

    conda activate 2025-book-env

you will have access to the new packages.

### Changing to the `2025-book-env` env kernel when running a Jupyter notebook

If you are running the `2025-book-env` kernel, you should see

    Python [conda env:2025-book-env] *

in the upper right-hand corner of the Jupyter notebook you are running.  If it just says something like `Python 3` then you are not running the `2025-book-env` kernel.  In that case, look under the `Kernel` menu to `Change kernel` and select `Python [conda env:2025-book-env]`.  The kernel should restart and indicate the new kernel in the upper corner.
