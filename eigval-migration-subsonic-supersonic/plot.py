#!/usr/bin/env python
import os

import numpy as np
import matplotlib.pyplot as plt

# from matplotlib import rcParams

from saf.euler1d_eigval.linear import ASCIIReader

from helpers import savefig


# Format for :math:`Q_2`.
FMT = '8.4f'

MAX_NUMBER_OF_MODES = 6


OUTPUT_DIR = './_output'

q_values = []

dirs = os.listdir(OUTPUT_DIR)
dirs.sort()

dirs_sorted = []

for d in dirs:
    q = float(d.split('=')[1])
    q_values.append(q)

dirs_sorted = [d for (q, d) in sorted(zip(q_values, dirs))]

q_values = []
conjugate_rates = []
exponential_rates_upper = []
exponential_rates_bottom = []
freq_0 = []
other_rates = np.empty((MAX_NUMBER_OF_MODES, len(dirs_sorted)))
other_freqs = np.empty((MAX_NUMBER_OF_MODES, len(dirs_sorted)))
other_rates.fill(np.nan)
other_freqs.fill(np.nan)

for j, d in enumerate(dirs_sorted):
    d_path = os.path.join(OUTPUT_DIR, d)

    if not os.path.isfile(d_path + '/stability.txt'):
        print(d)
        continue

    q = float(d.split('=')[1])
    q_values.append(q)

    r = ASCIIReader(d_path)
    modes = r.get_stability_info()
    assert len(modes) <= MAX_NUMBER_OF_MODES
    print('For q_2={:{fmt}} number of modes {}'.format(q, len(modes), fmt=FMT))

    growth_rates = np.zeros_like(modes)
    for i, m in enumerate(modes):
        if isinstance(m, list):
            # Implicit assumption that there only two branches.
            growth_rates[i] = m[1]['growth_rate']
        else:
            growth_rates[i] = m['growth_rate']

    if np.argmax(growth_rates) != 0:
        msg = ('For q_2={:{fmt}} the fundamental mode is not dominant.'
               'Mode with number {} is.')
        print(msg.format(q, np.argmax(growth_rates), fmt=FMT))

    mode = modes[0]

    if isinstance(mode, list):
        assert len(mode) == 2
        conjugate_rates.append(None)

        exponential_rates_bottom.append(mode[0]['growth_rate'])
        exponential_rates_upper.append(mode[1]['growth_rate'])
        freq_0.append(mode[0]['frequency'])
    else:
        conjugate_rates.append(mode['growth_rate'])
        exponential_rates_upper.append(None)
        exponential_rates_bottom.append(None)
        freq_0.append(mode['frequency'])

    if len(modes) > 1:
        for i, m in enumerate(modes[1:]):
            assert isinstance(m, dict)

            other_freqs[i+1, j] = m['frequency']
            other_rates[i+1, j] = m['growth_rate']

# Analysis
for i, __ in enumerate(conjugate_rates):
    if conjugate_rates[i] is None or conjugate_rates[i+1] is None:
        continue

    if conjugate_rates[i] > 0.0 and conjugate_rates[i+1] < 0.0:
        q_crit = q_values[i+1]
        msg = 'Switch from stable to unstable at q_2={:{fmt}}'
        print(msg.format(q_crit, fmt=FMT))
        break

for i, __ in enumerate(exponential_rates_upper):
    if (exponential_rates_upper[i] is not None and
            exponential_rates_upper[i+1] is None):
        q_crit = q_values[i+1]
        msg = 'Switch to purely exponential mode at q_2={:{fmt}}'
        print(msg.format(q_crit, fmt=FMT))
        break

rates_1 = other_rates[1, :]
for i, __ in enumerate(rates_1):
    if rates_1[i] > 0.0 and rates_1[i+1] < 0.0:
        if np.abs(rates_1[i]) > np.abs(rates_1[i+1]):
            q_crit = q_values[i+1]
        else:
            q_crit = q_values[i]

        msg = 'Mode 1 becomes unstable at q_2={:{fmt}}'
        print(msg.format(q_crit, fmt=FMT))
        break

# Plotting
fig_1, ax = plt.subplots(1, 1)
ax.plot(q_values, conjugate_rates, '-', label='Mode 0')
ax.plot(q_values, exponential_rates_bottom, '-')
ax.plot(q_values, exponential_rates_upper, '-')
ax.plot(q_values, other_rates[1, :], '--', label='Mode 1')
ax.set_ylim((-0.2, 1.2))
ax.set_xlabel(r'$Q_2$')
ax.set_ylabel(r'Re $\alpha$')
ax.legend(loc='upper right')
fig_1.tight_layout(pad=0.1)

# Plot all found modes
# figsize = (2*rcParams['figure.figsize'][0], rcParams['figure.figsize'][1])
# fig_2, (ax_1, ax_2) = plt.subplots(1, 2, figsize=figsize)
# ax_1.plot(q_values, conjugate_rates, '-', label='Mode 0')
# ax_1.plot(q_values, exponential_rates_bottom, '-')
# ax_1.plot(q_values, exponential_rates_upper, '-')
# ax_1.plot(q_values, other_rates[1, :], '--', label='Mode 1')
# ax_1.plot(q_values, other_rates[2, :], '--', label='Mode 2')
# ax_1.plot(q_values, other_rates[3, :], '--', label='Mode 3')
# ax_1.plot(q_values, other_rates[4, :], '--', label='Mode 4')
# ax_1.plot(q_values, other_rates[5, :], '--', label='Mode 5')
# ax_1.set_ylim((-0.2, 1.2))
# ax_1.set_xlabel(r'$Q_2$')
# ax_1.set_ylabel(r'Re $\alpha$')
# ax_1.legend(loc='upper right')
# 
# ax_2.plot(q_values, freq_0, '-', label='Mode 0')
# ax_2.plot(q_values, other_freqs[1, :], '--', label='Mode 1')
# ax_2.plot(q_values, other_freqs[2, :], '--', label='Mode 2')
# ax_2.plot(q_values, other_freqs[3, :], '--', label='Mode 3')
# ax_2.plot(q_values, other_freqs[4, :], '--', label='Mode 4')
# ax_2.plot(q_values, other_freqs[5, :], '--', label='Mode 5')
# ax_2.set_xlabel(r'$Q_2$')
# ax_2.set_ylabel(r'Im $\alpha$')
# 
# fig_2.tight_layout(pad=0.1)

# Showing or saving
outfile_1 = 'eigval-re-alpha-vs-q_2.pdf'
savefig(outfile_1)

# outfile_2 = 'all-modes.pdf'
# outfile_2 = os.path.join('_assets', outfile_2)
# fig_2.savefig(outfile_2)
