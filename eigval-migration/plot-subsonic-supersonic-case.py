#!/usr/bin/env python
import logging
import os
import tarfile
import tempfile
import shutil

import matplotlib.pyplot as plt

from helpers import FIGSIZE_LARGER as figsize, savefig

from lib_postprocessing import process_subsonic_supersonic


# Format for :math:`Q_2`.
FMT = '8.4f'

MAX_NUMBER_OF_MODES = 6


OUTPUT_DIR = os.path.join('_output', 'subsonic-supersonic')

logging.basicConfig(format='%(levelname)8s | %(message)s', level=logging.INFO)

# Extract stability files from .tar.gz file into a temp directory.
tempdir = tempfile.mkdtemp()
f = tarfile.open('_output/subsonic-supersonic.tar.gz')
f.extractall(tempdir)
dirname = os.path.join(tempdir, OUTPUT_DIR)

q_values, rate_0, rates = process_subsonic_supersonic(dirname)

shutil.rmtree(tempdir)

# Plotting
plt.figure(figsize=figsize)
p = plt.plot(q_values, rate_0['oscil'], '-')
c = p[0].get_color()
plt.plot(q_values, rate_0['lower'], '-', color=c)
plt.plot(q_values, rate_0['upper'], '-', color=c)
plt.plot(q_values, rates[1, :], '-')
plt.plot(q_values, rates[2, :], '-')
plt.plot(q_values, rates[3, :], '-')
plt.plot(q_values, rates[4, :], '-')
plt.plot(q_values, rates[5, :], '-')
plt.xlim((-45, 0))
plt.ylim((-0.02, 1.22))
plt.xlabel(r'$Q_2$')
plt.ylabel(r'$\alpha_{\mathrm{re}}$')

# Annotate modes.
ax = plt.gca()
ax.text(0.96, 0.05, '0', transform=ax.transAxes)
ax.text(0.69, 0.05, '1', transform=ax.transAxes)
ax.text(0.47, 0.05, '2', transform=ax.transAxes)
ax.text(0.30, 0.05, '3', transform=ax.transAxes)
ax.text(0.16, 0.05, '4', transform=ax.transAxes)
ax.text(0.02, 0.05, '5', transform=ax.transAxes)

plt.tight_layout(pad=0.1)

# Showing or saving
outfile_1 = 'eigval-re-alpha-vs-q_2-sub-super.pdf'
savefig(outfile_1)
