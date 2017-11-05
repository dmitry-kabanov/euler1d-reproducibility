#!/usr/bin/env python
import logging
import os
import tarfile
import tempfile
import shutil

import matplotlib.pyplot as plt
import numpy as np

from helpers import FIGSIZE_LARGER as figsize, savefig

from lib_postprocessing import (process_subsonic_supersonic as p_super,
                                process_subsonic_subsonic as p_sub)


# We don't any output from `lib_postprocessing` module, so log to abyss.
logging.basicConfig(handlers=[logging.NullHandler()])

tempdir = tempfile.mkdtemp()
f_sub = tarfile.open('_output/subsonic-subsonic.tar.gz')
f_sub.extractall(tempdir)
f_super = tarfile.open('_output/subsonic-supersonic.tar.gz')
f_super.extractall(tempdir)
dir_sub = os.path.join(tempdir, '_output/subsonic-subsonic')
dir_super = os.path.join(tempdir, '_output/subsonic-supersonic')

q_sub, rate_0_sub, rates_sub = p_sub(dir_sub)
q_super, rate_0_super, rates_super = p_super(dir_super)

shutil.rmtree(tempdir)

rate_0_oscil_sub = rate_0_sub['oscil']
rate_0_lower_sub = rate_0_sub['lower']
rate_0_upper_sub = rate_0_sub['upper']

# Cleaning subsonic-subsonic data.
idx_0_oscil = np.isfinite(rate_0_oscil_sub)
rate_0_lower_sub[q_sub > -25] = np.nan
idx_1 = np.isfinite(rates_sub[1, :])
idx_4 = np.isfinite(rates_sub[4, :])

rate_0_oscil_super = rate_0_super['oscil']
rate_0_lower_super = rate_0_super['lower']
rate_0_upper_super = rate_0_super['upper']

plt.figure(figsize=figsize)

# Plot subsonic-supersonic case.
p_super = plt.plot(q_super, rate_0_oscil_super, '-')
color_super = p_super[0].get_color()
plt.plot(q_super, rate_0_lower_super, '-', color=color_super)
plt.plot(q_super, rate_0_upper_super, '-', color=color_super)
plt.plot(q_super, rates_super[1, :], '-')
plt.plot(q_super, rates_super[2, :], '-')
plt.plot(q_super, rates_super[3, :], '-')
plt.plot(q_super, rates_super[4, :], '-')
plt.plot(q_super, rates_super[5, :], '-')

# Reset color cycle to make colors matching each other.
plt.gca().set_prop_cycle(None)

# Plot subsonic-subsonic case.
p_sub = plt.plot(q_sub[idx_0_oscil], rate_0_oscil_sub[idx_0_oscil], '--')
color_sub = p_sub[0].get_color()

plt.plot(q_sub, rate_0_lower_sub, '--', color=color_sub)
plt.plot(q_sub, rate_0_upper_sub, '--', color=color_sub)

plt.plot(q_sub[idx_1], rates_sub[1, idx_1], '--')
plt.plot(q_sub, rates_sub[2, :], '--')
plt.plot(q_sub, rates_sub[3, :], '--')
plt.plot(q_sub[idx_4], rates_sub[4, idx_4], '--')

# Annotate modes.
ax = plt.gca()
ax.text(0.96, 0.05, '0', transform=ax.transAxes)
ax.text(0.69, 0.05, '1', transform=ax.transAxes)
ax.text(0.47, 0.05, '2', transform=ax.transAxes)
ax.text(0.30, 0.05, '3', transform=ax.transAxes)
ax.text(0.16, 0.05, '4', transform=ax.transAxes)
ax.text(0.02, 0.05, '5', transform=ax.transAxes)

plt.xlabel(r'$Q_2$')
plt.ylabel(r'$\alpha_{\mathrm{re}}$')
plt.xlim((-45, 0))
plt.ylim((-0.02, 1.22))
plt.tight_layout(pad=0.1)

savefig('eigval-re-alpha-vs-q_2-together.pdf')
