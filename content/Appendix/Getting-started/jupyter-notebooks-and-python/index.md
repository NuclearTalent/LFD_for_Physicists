(sec:JupyterNotebooksPython)=
# Jupyter notebooks and Python

The exercises and demos in this book correspond to Jupyter notebooks that you can run yourself (rather than just looking at the static version shown in the book). You are highly encouraged to download the source files, as described in {ref}`sec:UsingGit`, such that you can perform the exercises interactively.

A Jupyter notebook is a powerful tool for interactively developing and presenting data and computational science projects. Jupyter notebooks integrate markdown text notes, mathematical equations, interactive code cells and their output into a single document. They can be displayed on a web browser running on a computer, on a tablet (e.g., IPad), or even on your smartphone.  

This integrated interface promotes fast, iterative development since each output of your code will be displayed right away. That’s why notebooks have become very popular in data science and for explorative computational projects.

For serious code development projects, however, the Jupyter notebook format does have some serious drawbacks, such as lack of version control, and should be avoided.

## What you should know about Python and using Jupyter notebooks

1. Know how to switch between `Code` and `Markdown` cells and how to run them (`shift-Return` or `Run` button)

1. Basics of Python evaluation and printing
    * string concatenation
    * exponentiation with `**`
    * use of fstrings

1. Importing numpy and basic functions (sqrt, exp, sin, $\ldots$)
    * numpy arrays using `arange(min, max, step)`

1. Getting help via Google (or alternative): StackOverflow and manuals

1. Defining functions in Python
    * `def my_function(x):` $\longleftarrow$ semicolon and then indented lines
    * position vs. keyword argument and defaults
    * `shift + tab + tab` to reveal definitions

1. Plotting with Matplotlib
    * Standard sequence for plot: data $\longrightarrow$ make figure $\longrightarrow$ add subplots $\longrightarrow$ make plot
    * dressing up and saving a plot
    * names for the figure and axis objects are our choice

    <!---
    * `%matplotlib inline` to generate inline plots in Jupyter notebooks
    -->

1. Numpy linear algebra
    * defining a matrix and finding its shape or particular elements
    * matrix (or vector) operations: multiplying them with @, transpose, trace, inverse, eigensolution  

## Good online cheat-sheets:
* [Python Crash Course](https://ehmatthes.github.io/pcc_3e/cheat_sheets/)
* [datacamp cheat-sheets](https://www.datacamp.com/cheat-sheet)
* [Python debugging flowchart](https://imgur.com/gallery/3fwBFTn)

