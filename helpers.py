import os

import matplotlib.pyplot as plt


# Figure size for a single-plot figure that takes 50 % of text width.
FIGSIZE_NORMAL = (3.2, 2.13)
# Figure size for a single-plot figure that takes about 75 % of text width.
FIGSIZE_LARGER = (4.8, 3.2)
# Figure size for a figure with two subplots in one row.
FIGSIZE_TWO_SUBPLOTS_ONE_ROW = (6.4, 2.13)
# Figure size for a figure with two subplots in two rows.
FIGSIZE_TWO_SUBPLOTS_TWO_ROWS = (6.4, 4.26)
# Figure size for a figure with six subplots.
FIGSIZE_SIX_SUBPLOTS = (6.4, 6.4)


TARGET_DIR = '_assets'


def savefig(filename):
    """Save figure if the environment variable SAVE_FIGURES is set."""
    cur_fig = plt.gcf()

    if 'SAVE_FIGURES' in os.environ:
        filename = os.path.join(TARGET_DIR, filename)
        cur_fig.savefig(filename)
    else:
        plt.show()
