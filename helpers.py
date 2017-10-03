import os

import matplotlib.pyplot as plt


TARGET_DIR = '_assets'


def savefig(filename):
    """Save figure if the environment variable SAVE_FIGURES is set."""
    cur_fig = plt.gcf()

    if 'SAVE_FIGURES' in os.environ:
        filename = os.path.join(TARGET_DIR, filename)
        cur_fig.savefig(filename)
    else:
        plt.show()
