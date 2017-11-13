#!/usr/bin/env python
import logging
import os
import tarfile
import tempfile
import shutil

import matplotlib.pyplot as plt

from helpers import FIGSIZE_TWO_SUBPLOTS_ONE_ROW as figsize, savefig

from lib_postprocessing import process_subsonic_supersonic


# Format for :math:`Q_2`.
FMT = '8.4f'

MAX_NUMBER_OF_MODES = 6


OUTPUT_DIR = os.path.join('_output', 'subsonic-supersonic')

logging.basicConfig(format='| %(levelname).1s | %(message)s',
                    level=logging.INFO)

# Extract stability files from .tar.gz file into a temp directory.
tempdir = tempfile.mkdtemp()
f = tarfile.open('_output/subsonic-supersonic.tar.gz')
f.extractall(tempdir)
dirname = os.path.join(tempdir, OUTPUT_DIR)

q_values, rate_0, rates, freq_0, freqs = process_subsonic_supersonic(dirname)

shutil.rmtree(tempdir)

# Plotting
fig, (ax_1, ax_2) = plt.subplots(nrows=1, ncols=2, figsize=figsize)
p = ax_1.plot(q_values, rate_0['oscil'], '-')
c = p[0].get_color()
ax_1.plot(q_values, rate_0['lower'], '-', color=c)
ax_1.plot(q_values, rate_0['upper'], '-', color=c)
ax_1.plot(q_values, rates[1, :], '-')
ax_1.plot(q_values, rates[2, :], '-')
ax_1.plot(q_values, rates[3, :], '-')
ax_1.plot(q_values, rates[4, :], '-')
ax_1.plot(q_values, rates[5, :], '-')
ax_1.set_xlim((-45, 0))
ax_1.set_ylim((-0.02, 1.22))
ax_1.set_xlabel(r'$Q_2$')
ax_1.set_ylabel(r'$\alpha_{\mathrm{re}}$')

# Annotate modes.
ax_1.text(0.96, 0.05, '0', transform=ax_1.transAxes)
ax_1.text(0.69, 0.05, '1', transform=ax_1.transAxes)
ax_1.text(0.47, 0.05, '2', transform=ax_1.transAxes)
ax_1.text(0.30, 0.05, '3', transform=ax_1.transAxes)
ax_1.text(0.16, 0.05, '4', transform=ax_1.transAxes)
ax_1.text(0.02, 0.05, '5', transform=ax_1.transAxes)

# Reset color cycle.
ax_2.set_prop_cycle(None)

# Plot frequencies.
ax_2.plot(q_values, freq_0, '-')
ax_2.plot(q_values, freqs[1, :], '-')
ax_2.plot(q_values, freqs[2, :], '-')
ax_2.plot(q_values, freqs[3, :], '-')
ax_2.plot(q_values, freqs[4, :], '-')
ax_2.plot(q_values, freqs[5, :], '-')
ax_2.set_xlabel(r'$Q_2$')
ax_2.set_ylabel(r'$\alpha_{\mathrm{im}}$')

ax_2.text(0.9, 0.05, '0', transform=ax_2.transAxes)
ax_2.text(0.77, 0.26, '1', transform=ax_2.transAxes)
ax_2.text(0.48, 0.43, '2', transform=ax_2.transAxes)
ax_2.text(0.32, 0.6, '3', transform=ax_2.transAxes)
ax_2.text(0.17, 0.75, '4', transform=ax_2.transAxes)
ax_2.text(0.04, 0.91, '5', transform=ax_2.transAxes)

fig.tight_layout(pad=0.1)

# Showing or saving
outfile_1 = 'eigval-re-alpha-vs-q_2-sub-super.pdf'
savefig(outfile_1)
