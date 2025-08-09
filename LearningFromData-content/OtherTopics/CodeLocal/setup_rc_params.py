
def setup_rc_params(presentation=False, constrained_layout=True, usetex=True, dpi=400):
    import matplotlib.pyplot as plt

    if presentation:
        fontsize = 12
    else:
        fontsize = 9
    black = "k"

    plt.rcdefaults()  # Set to defaults
    x_minor_tick_size = y_minor_tick_size = 2.4
    x_major_tick_size = y_major_tick_size = 3.9

    # plt.rc("text", usetex=True)
    plt.rcParams["font.size"] = fontsize
    plt.rcParams["text.usetex"] = usetex
    # plt.rcParams["text.latex.preview"] = True
    plt.rcParams["font.family"] = "serif"

    plt.rcParams["axes.labelsize"] = fontsize
    plt.rcParams["axes.edgecolor"] = black
    # plt.rcParams['axes.xmargin'] = 0
    plt.rcParams["axes.labelcolor"] = black
    plt.rcParams["axes.titlesize"] = fontsize

    plt.rcParams["ytick.direction"] = "in"
    plt.rcParams["xtick.direction"] = "in"
    plt.rcParams["xtick.labelsize"] = fontsize
    plt.rcParams["ytick.labelsize"] = fontsize
    plt.rcParams["xtick.color"] = black
    plt.rcParams["ytick.color"] = black
    # Make the ticks thin enough to not be visible at the limits of the plot (over the axes border)
    plt.rcParams["xtick.major.width"] = plt.rcParams["axes.linewidth"] * 0.95
    plt.rcParams["ytick.major.width"] = plt.rcParams["axes.linewidth"] * 0.95
    # The minor ticks are little too small, make them both bigger.
    plt.rcParams["xtick.minor.size"] = x_minor_tick_size  # Default 2.0
    plt.rcParams["ytick.minor.size"] = y_minor_tick_size
    plt.rcParams["xtick.major.size"] = x_major_tick_size  # Default 3.5
    plt.rcParams["ytick.major.size"] = y_major_tick_size
    plt.rcParams["xtick.minor.visible"] =  True
    plt.rcParams["ytick.minor.visible"] =  True

    ppi = 72  # points per inch
    plt.rcParams["figure.titlesize"] = fontsize
    plt.rcParams["figure.dpi"] = 150  # To show up reasonably in notebooks
    plt.rcParams["figure.constrained_layout.use"] = constrained_layout
    # 0.02 and 3 points are the defaults:
    # can be changed on a plot-by-plot basis using fig.set_constrained_layout_pads()
    plt.rcParams["figure.constrained_layout.wspace"] = 0.0
    plt.rcParams["figure.constrained_layout.hspace"] = 0.0
    plt.rcParams["figure.constrained_layout.h_pad"] = 0#3.0 / ppi
    plt.rcParams["figure.constrained_layout.w_pad"] = 0#3.0 / ppi

    plt.rcParams["text.latex.preamble"] = r"\usepackage{amsfonts}"

    plt.rcParams["legend.title_fontsize"] = fontsize
    plt.rcParams["legend.fontsize"] = fontsize
    plt.rcParams[
        "legend.edgecolor"
    ] = "inherit"  # inherits from axes.edgecolor, to match
    plt.rcParams["legend.facecolor"] = (
        1,
        1,
        1,
        0.6,
    )  # Set facecolor with its own alpha, so edgecolor is unaffected
    plt.rcParams["legend.fancybox"] = True
    plt.rcParams["legend.borderaxespad"] = 0.8
    plt.rcParams[
        "legend.framealpha"
    ] = None  # Do not set overall alpha (affects edgecolor). Handled by facecolor above
    plt.rcParams[
        "patch.linewidth"
    ] = 0.8  # This is for legend edgewidth, since it does not have its own option

    plt.rcParams["hatch.linewidth"] = 0.5

    return None
