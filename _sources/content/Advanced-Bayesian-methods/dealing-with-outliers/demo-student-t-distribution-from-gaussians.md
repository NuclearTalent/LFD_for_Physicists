---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(demo:student-t-distribution-from-gaussians)=
# Demo: Student's t-distribution from Gaussians

## Overview: not a Gaussian distribution

Physicists often assume that most distributions are Gaussian. But sometimes they are Student's t-distributions.

David C. Bailey, in the paper *[Not Normal: the uncertainties of scientific measurements](https://royalsocietypublishing.org/doi/epdf/10.1098/rsos.160600)*, 
analyses 41000 measurements of 3200 quantities from medicine, nuclear and   particle physics, and many interlaboratory comparisons.  He finds "Uncertainty-normalized   differences between  multiple  measurements  of  the  same  quantity  are consistent with heavy-tailed Student’s t-distributions that are often almost Cauchy, far from a Gaussian Normal bell curve".

Appendix A of *Rigorous constraints on three-nucleon forces in chiral effective field theory from fast and accurate calculations of few-body observables* by Wesolowski et al. ([arXiv:2104.0441](https://arxiv.org/abs/2104.04441)) explains why, in linear parameter estimation problems with variance estimation, one finds that the parameters are typically t distributed after one marginalizes over the variance. 

In short, if you are uncertain of your uncertainty (variance), and being a good Bayesian you integrate over the distribution of variances, you will get a t distribution.
So imagine a mixture of normal distributions with a common mean but with the precision (the inverse of the variance) distributed according to a gamma distribution (or the variance is distributed with an inverse gamma distribution).

## Emergence of a Student's t-distribution

As a visualization, Rasmus Bååth in this [blog entry](https://www.sumsar.net/blog/2013/12/t-as-a-mixture-of-normals/) created an animation by making draws from a normal distribution whose width (standard deviation) "jumps around".
Here we have created a version of this animation that also includes the sampling of the variance. (Note: instead of variance sampling we could have alternatively used conjugate priors.)


A t distribution with mean $\mu$, scale $s$, and degrees of freedom $\nu$ 

$$
  y \sim \text{t}(\nu, \text{loc}=\mu, \text{scale}=s)
$$

can be created from

$$
  y \sim \text{Normal}(\mu, \sigma)
$$

where $\sigma$ comes from 

$$
  \frac{1}{\sigma^2} \sim \text{Gamma}(a=\nu/2, \text{scale}=1/(s^2 \nu/2))
$$


```{code-cell} python3
:label: code-t-distribution-from-gaussians
:tags: [hide-input]

%matplotlib inline

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
from matplotlib import animation 

import ipywidgets as widgets
from IPython.display import display, HTML

from scipy.stats import norm, t, gamma

# set up graphics defaults
def setup_rc_params(presentation=False, uselatex=False):
    if presentation:
        fontsize = 11
    else:
        fontsize = 9
    black = 'k'

    mpl.rcdefaults()  # Set to defaults

    if uselatex:
       #mpl.rc('text', usetex=True)
       mpl.rcParams['text.usetex'] = True
       mpl.rc("text.latex", preamble=r"\usepackage{amsmath}")

    mpl.rcParams['font.size'] = fontsize
    mpl.rcParams['font.family'] = 'serif'

    mpl.rcParams['axes.labelsize'] = fontsize
    mpl.rcParams['axes.edgecolor'] = black
    # mpl.rcParams['axes.xmargin'] = 0
    mpl.rcParams['axes.labelcolor'] = black
    mpl.rcParams['axes.titlesize'] = fontsize

    mpl.rcParams['ytick.direction'] = 'in'
    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['xtick.labelsize'] = fontsize
    mpl.rcParams['ytick.labelsize'] = fontsize
    mpl.rcParams['xtick.color'] = black
    mpl.rcParams['ytick.color'] = black
    # Make the ticks thin enough to not be visible at the limits of the plot (over the axes border)
    mpl.rcParams['xtick.major.width'] = mpl.rcParams['axes.linewidth'] * 0.95
    mpl.rcParams['ytick.major.width'] = mpl.rcParams['axes.linewidth'] * 0.95
    # The minor ticks are little too small, make them both bigger.
    mpl.rcParams['xtick.minor.size'] = 2.4  # Default 2.0
    mpl.rcParams['ytick.minor.size'] = 2.4
    mpl.rcParams['xtick.major.size'] = 3.9  # Default 3.5
    mpl.rcParams['ytick.major.size'] = 3.9

    ppi = 72  # points per inch
    # dpi = 150
    mpl.rcParams['figure.titlesize'] = fontsize
    mpl.rcParams['figure.dpi'] = 150  # To show up reasonably in notebooks
    mpl.rcParams['figure.constrained_layout.use'] = True
    # 0.02 and 3 points are the defaults:
    # can be changed on a plot-by-plot basis using fig.set_constrained_layout_pads()
    mpl.rcParams['figure.constrained_layout.wspace'] = 0.0
    mpl.rcParams['figure.constrained_layout.hspace'] = 0.0
    mpl.rcParams['figure.constrained_layout.h_pad'] = 3. / ppi  # 3 points
    mpl.rcParams['figure.constrained_layout.w_pad'] = 3. / ppi

    mpl.rcParams['legend.title_fontsize'] = fontsize
    mpl.rcParams['legend.fontsize'] = fontsize
    mpl.rcParams['legend.edgecolor'] = 'inherit'  # inherits from axes.edgecolor, to match
    mpl.rcParams['legend.facecolor'] = (1, 1, 1, 0.6)  # Set facecolor with its own alpha, so edgecolor is unaffected
    mpl.rcParams['legend.fancybox'] = True
    mpl.rcParams['legend.borderaxespad'] = 0.8
    mpl.rcParams['legend.framealpha'] = None  # Do not set overall alpha (affects edgecolor). Handled by facecolor above
    mpl.rcParams['patch.linewidth'] = 0.8  # This is for legend edgewidth, since it does not have its own option

    mpl.rcParams['hatch.linewidth'] = 0.5

    # bbox = 'tight' can distort the figure size when saved (that's its purpose).
    # mpl.rc('savefig', transparent=False, bbox='tight', pad_inches=0.04, dpi=350, format='png')
    mpl.rc('savefig', transparent=False, bbox=None, dpi=400, format='png')


#from graphs_rjf import setup_rc_params
setup_rc_params(presentation=False, uselatex=False)  # Switch to True for larger fonts
                           # Switch to True for LaTeX but SLOW

mpl.rcParams['figure.constrained_layout.use'] = False
plt.rcParams['animation.html'] = 'jshtml'  # auto-inline via JS (no ffmpeg needed)



# For normal distribution
mu = 0      # mean
sigma = 3   # standard deviation

# For gamma distribution
a1 = 1
b1 = 1/9

# For t distribution
t_df = 2  # degrees of freedom
t_loc = 0 # mean
t_scale = 3  # standard deviation


# Student's t-distribution with particular parameters
t_loc = 0
t_scale = 3
t_df = 2  # 20 # degrees of freedom, using written with nu

t_dist = t(df=t_df, loc=t_loc, scale=t_scale)


# Now the gamma distribution, converted to a sigma distribution
N_gamma = 6000 #  500000 # 6000
gamma_a = t_df / 2
gamma_scale = 1 / (t_scale**2 * t_df / 2)
sigma_vals = 1 / np.sqrt(gamma.rvs(gamma_a, scale=gamma_scale, size=N_gamma))

# Gaussian (normal) distribution
norm_loc = t_loc
norm_scaled_vals = np.array([norm.rvs(norm_loc, sigma, size=1) for sigma in sigma_vals]).flatten()


# Plot the t distribution as a bar chart, as we'll use in the movie
x_max = 20
x_t = np.linspace(-x_max, x_max, 500) 

t_label = 't dist.'
t_color = 'red'
n_color = 'green'
t_dist_pts = t_dist.pdf(x_t)
t_dist_max = max(t_dist_pts)



def animate(nframe, empty=False):
    """
    Draw a new frame every time with the sampled value and the Gaussian pdf
    
    Many global variables here, so this should be refactored! 
    """
    t_label = "Student's t pdf"
    norm_label = 'gaussian pdf'
    samp_label = 'sampled pts'
    num_bins = 50
    
    point_alpha = 0.2
    
    # prepare a clean and image-filling canvas for each frame
    fig = plt.gcf()
    fig.clf()

    ax1 = fig.add_subplot(1,1,1)
    ax1.yaxis.set_visible(False)
    ax1.set_xlim(-20, 20)
    ax1.set_ylim(-0.1, 1.1)
    ax1.set_xlabel(' ')
    ax1.axhline(0., color="gray", alpha=0.5)
    ax1.set_title("Student's t-distribution from Gaussians")

    # These are in unitless percentages of the figure size. (0,0 is bottom left)
    max_sigma_vals = max(sigma_vals)
    left, bottom, width, height = [0.15, 0.6, 0.2, 0.2]
    ax2 = fig.add_axes([left, bottom, width, height])
    ax2.set_title(r'$\sigma$ samples')
    sigma_max = 15
    ax2.set_xlim(0, sigma_max)
    ax2.xaxis.set_visible(False)
    ax2.yaxis.set_visible(False)
    ax2.axhline(0., color="gray", alpha=0.5)
    ax2.hist(sigma_vals, bins=num_bins, range=(0,sigma_max), density=True, color=n_color, alpha=0.8)
    ax2.axvline(sigma_vals[nframe], color='red')
    ax2.set_ylim(bottom=-0.02)
    

    if nframe < frame_switch:
        sigma_now = sigma_vals[nframe]    
        norm_pts = norm.pdf(x_t, loc=norm_loc, scale=sigma_now)
        max_norm_pts = max(norm_pts)
        scale = 1 / max_norm_pts  # t_dist_max / max_norm_pts
        
        ax1.plot(x_t, scale * norm_pts, color=n_color, label=norm_label)    
        ax1.plot(norm_scaled_vals[:nframe], np.zeros(nframe), '.', color='blue', alpha=point_alpha, label=samp_label)
        ax1.plot(norm_scaled_vals[nframe], 0, '.', color='red')
    else:
        sigma_now = sigma_vals[nframe]    
        norm_pts = norm.pdf(x_t, loc=norm_loc, scale=sigma_now)
        max_norm_pts = max(norm_pts)
        scale = 1 / max_norm_pts  # t_dist_max / max_norm_pts

        index = int(frame_switch + (nframe - frame_switch) * frame_skip)

        #ax1.plot(norm_scaled_vals[:index], np.zeros(index), '.', color='blue', alpha=point_alpha, label=samp_label)
        
#         count, bins, ignored = ax1.hist(norm_scaled_vals[:index], range=(-20,20), bins=num_bins, density=False,
#                                      color='blue', alpha=0.4)
        hist_pts, bin_edges = np.histogram(norm_scaled_vals[:index], bins=num_bins, range=(-x_max, x_max))
        ax1.bar(bin_edges[:-1], hist_pts * hist_norm / t_dist_max, align = "edge", width = np.diff(bin_edges), 
                color='blue', ec='black', label=samp_label)
        if (nframe < nframes - 2):
            ax1.plot(x_t, scale * norm_pts, color=n_color, label=norm_label)    
            ax1.plot(norm_scaled_vals[nframe], 0, '.', color='red')

    # Plot the expected t distribution at the end of the animation
    if (nframe > nframes - 2):
        ax1.plot(x_t, t_dist.pdf(x_t) / t_dist_max, label=t_label, color=t_color)
      
    ax1.legend(loc='upper right')
    #fig.tight_layout()



    # Settings
# from datetime import date
# today = date.today()
# date_formatted = today.strftime("%d%b%Y")

# gif_filename = 'Student_t_animation_' + date_formatted  # filename for gif
width, height = 640, 224  # dimensions of each frame
nframes = 120  #  80  # number of frames
fps = 3  # frames per second
interval = 100

num_bins = 50
delta_bin = 2 * x_max / (num_bins)
frame_switch = 40
frame_skip = N_gamma / 100
index_max = int(frame_switch + (nframes - frame_switch) * frame_skip)
#print(f'max index: {index_max}')
hist_pts_all, bin_edges = np.histogram(norm_scaled_vals[:index_max], bins=num_bins, range=(-x_max, x_max))
hist_norm = 1 / (np.sum(hist_pts_all) * delta_bin)  #  1 / max(hist_pts)


fig = plt.figure(figsize=(4.5,3))
anim = animation.FuncAnimation(fig, animate, frames=nframes, repeat=False, blit=False)

html_anim = HTML(anim.to_jshtml())
plt.close(fig)
html_anim


# Save as an animated gif
# print('Saving animated gif: ', gif_filename + '.gif')
# anim.save(gif_filename + '.gif', writer='imagemagick', fps=fps)

# saving to mp4 using ffmpeg writer
# print('Saving mp4 video: ', gif_filename + '.mp4')
# writervideo = animation.FFMpegWriter(fps=fps)
# anim.save(gif_filename + '.mp4', writer=writervideo)






```
