{.tight-h1}
# Learning from data for physicists

<span style="font-size: 1.8em; font-weight: bold; font-style:italic; display:inline-block; margin-bottom:0.5em;">
&nbsp;&nbsp; Bayesian and machine learning methods</span>

<!--## Bayesian and machine learning methods-->

by [Christian Forssén](https://www.chalmers.se/en/persons/f2bcf/), [Dick Furnstahl](https://physics.osu.edu/people/furnstahl.1), and [Daniel Phillips](https://www.ohio.edu/cas/phillid1). 

```{epigraph}
> "We demand rigidly defined areas of doubt and uncertainty!"

-- Douglas Adams, *The Hitchhiker's Guide to the Galaxy*
```


(sec:AboutJB)=
## About this book

This text is aimed at physicists seeking to learn from data using Bayesian methods. It is particularly designed for use in an advanced-level course but should be broadly accessible to those with a physics background.


<!--## About these lecture notes-->

The content of this book has emerged from previous work and courses taught by the authors.
The materials are released under a [Creative Commons BY-NC license](https://creativecommons.org/licenses/by-nc/4.0/).

The book format is powered by [Jupyter Book](https://jupyterbook.org/).
You can also download the [complete book as a pdf file](https://nucleartalent.github.io/LFD_for_Physicists/LFD_for_Physicists.pdf). 

```{admonition} This book is work in progress
:class: note
New content is added and existing  sections are revised on an ongoing basis. We welcome feedback, suggestions, and bug reports. Please feel free to open an issue on our [GitHub repository](https://github.com/NuclearTalent/LFD_for_Physicists/issues) (see also the *Open an issue* box further down) or contact us by email. 
```

## Materials to help you get started

Appendix C has various materials to set you up for Learning from Data (see {ref}`sec:RootGettingStarted`). You may have the option to run the Jupyter notebooks on a cloud server, but eventually you will likely want to set up an environment on your own machine. 
* See {ref}`sec:SettingUpJB` for instructions how to use git for cloning the repository with all the book material ({ref}`sec:UsingGit`) and for guides to setting up a Python environment on your computer ({ref}`sec:InstallingPython`).
* If Python and/or Jupyter notebooks are new to you (or if you need a refresher), you can find a notebook: {ref}`exercise:jupyter-notebooks-and-python` that will take you from zero to just what you need to know about Python and running the Jupyter notebooks in this Jupyter Book.
* For more advanced Python summaries, see the other Python notebooks linked in Appendix C.


## Brief guide to online Jupyter Book features


```{admonition} Icons and menus
  The Jupyter Book has many useful features:
* A clickable high-level table of contents (TOC) is available in the panel at the left of each page. (You can toggle this panel open or close with the contents icon at the upper left of the middle panel.) At the top of this TOC is a search box for the book.
* The icons at the top-right in the middle panel can be used to take you to the source repository for the book; download the source code for the page (in different formats); view the page in full-screen mode; or switch between light and dark mode.
* For each section that has subsections, a clickable table of contents appears in the rightmost panel.
* There are hyperlinks throughout the text to other sections, equations, references, and more.
```


```{admonition} Open an issue

If you find a problem or have a suggestion--whether related to physics, statistics, Python, or formatting--we encourage you to let us know via a GitHub issue. You will need a [GitHub account](https://github.com/signup) to do this (free to create).

From any page in the book, click the GitHub icon <img src="_assets/GitHub-Mark-32px.png" alt="github icon" width="20px"> in the top right toolbar and select Open issue. This will take you to the Issues section of the book's GitHub repository, where you can give your issue a title and describe the problem or suggestion in the text box below.
  ```

## Acknowledgments

The material in this book has evolved over several years. The genesis was an intensive three-week summer school course taught at the [University of York](https://www.york.ac.uk/) in 2019 by the authors as part of the [TALENT](https://fribtheoryalliance.org/TALENT/) initiative. 
New material was subsequently added by [Christian Forssén](https://www.chalmers.se/en/persons/f2bcf/) for course developments at Chalmers and for lecture series at other universities. Contributions from Andreas Ekström are particulaly acknowledged. 
In parallel, [Dick Furnstahl](https://physics.osu.edu/people/furnstahl.1) adapted the TALENT material (plus much of Forssén's new material) for a graduate course at The Ohio State University, which was then revised by [Daniel Phillips](https://www.ohio.edu/cas/phillid1) for a course at Ohio University.
This book is a merger and update of all these developments. It includes significant additions of new material. A previous version of this book is archived at a [legacy site](https://nucleartalent.github.io/LFD_for_Physicists/legacy/).

Both the original notes and subsequent revisions have been informed by interactions with many colleagues, who have taught us different aspects of Bayesian inference. 
This includes many statistician colleagues who have taken the time to carefully and patiently address our misconceptions regarding statistics, probability, or even basic mathematics. Many of the important interactions have occurred at meetings in the [ISNET](https://isnet-series.github.io/meetings/) series.
Among our physics and statistics colleagues we are particularly grateful to:
* Andreas Ekström, Chalmers University of Technology
* Morten Hjorth-Jensen, Oslo University and Michigan State University
* Jordan Melendez, Ohio State University and Root Insurance
* Matt Plumlee, Northwestern University and Amazon
* Matt Pratola, Indiana University
* Ian Vernon, Durham University
* Sarah Wesolowski, York, UK
* Frederi Viens, Michigan State University


Many of the advanced Bayesian methods that might be included in these notes have been used in scientific studies with different collaborators. In particular, several postdocs, PhD students and master students have had leading roles in the development and application of these methods to address various scientific questions. Christian Forssén would like to highlight the contributions (in alphabetical order) of: Boris Carlsson, Tor Djärv, Weiguang Jiang, Eleanor May, Isak Svensson, and Oliver Thim.

The full list of people that have contributed with ideas, discussions, or by generously sharing their knowledge is very long. Rather than inadvertently omitting someone, we simply say thank you to all. More generally, we are truly thankful for being part of an academic environment in which ideas and efforts are shared rather than kept isolated.
The last statement extends to the open-source communities through which great computing tools are made publicly available. In this course we take great advantage of open-source python libraries.

The development of this course would not have been possible without the knowledge gained through the study of several excellent textbooks, most of which are listed as recommended course literature. Here is a short list of those references that we have found particularly useful as physicists learning Bayesian statistics and the fundamentals of machine learning:

{cite}`gelman2013bayesian` Andrew Gelman et al., *"Bayesian Data Analysis, Third Edition"*, Chapman & Hall/CRC Texts in Statistical Science (2013). <br/>
{cite}`Gregory2005` Phil Gregory, *"Bayesian Logical Data Analysis for the Physical Sciences"*, Cambridge University Press (2005). <br/>
{cite}`Jaynes2003` E. T. Jaynes, *"Probability Theory: The Logic of Science"*, Cambridge University Press (2003). <br/>
{cite}`Mackay2003` David J.C. MacKay, *"Information Theory, Inference, and Learning Algorithms"*, Cambridge University Press (2005). <br/>
{cite}`Sivia2006` D.S. Sivia with J. Skilling, *"Data Analysis : A Bayesian Tutorial"*, Oxford University Press (2006).



Needless to say, although we have benefited tremendously from all this input, any errors that remain in this book are solely our responsibility.

Lastly we thank our families for their support and for putting up with us occasionally lapsing into Bayes speak in everyday life. 






<!--
* For each section that has subsections, a clickable table of contents appears in the rightmost panel.
* The "Search this book..." icon is the magnifying glass icon to the far right in the top-middle.   Try it! 
* On pages that are not generated from Jupyter notebooks, the other four icons at the top-middle-right will take you to the github repository for the book or let you open an issue (see the top of this page); show you the markdown source (.md) of the page or generate a pdf version of the page; put you into full-screen mode; or toggle light/dark mode.
* On pages generated from Jupyter notebooks, there is an additional icon at the top-middle-right (leftmost), which enables you to run the notebook on a cloud server using [Binder](https://mybinder.org). When running on Binder, be patient; it may take a while to generate the page if the environment needs to be created from scratch (in general it is cached, so it will be much faster if others have been recently using notebooks from the repository).  
-->
