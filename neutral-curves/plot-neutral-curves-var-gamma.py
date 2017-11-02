#!/usr/bin/env python
import os

import numpy as np
import matplotlib.pyplot as plt

from helpers import FIGSIZE_TWO_SUBPLOTS_ONE_ROW as figsize, savefig

OUTPUT_DIR = '_output'
RESULTS_FILE_1_1 = os.path.join(OUTPUT_DIR, 'results-gamma=1.1.txt')
RESULTS_FILE_1_2 = os.path.join(OUTPUT_DIR, 'results-gamma=1.2.txt')
RESULTS_FILE_1_3 = os.path.join(OUTPUT_DIR, 'results-gamma=1.3.txt')
RESULTS_FILE_1_4 = os.path.join(OUTPUT_DIR, 'results-gamma=1.4.txt')


q_list_1_1, e_list_1_1, f_list_1_1 = np.loadtxt(RESULTS_FILE_1_1, unpack=True)
q_list_1_2, e_list_1_2, f_list_1_2 = np.loadtxt(RESULTS_FILE_1_2, unpack=True)
q_list_1_3, e_list_1_3, f_list_1_3 = np.loadtxt(RESULTS_FILE_1_3, unpack=True)
q_list_1_4, e_list_1_4, f_list_1_4 = np.loadtxt(RESULTS_FILE_1_4, unpack=True)

# We need to clean data because there are incorrect results in them:
# 1. All results with e_act == 0.0 are incorrect because the algorithm
#    for finding critical e_act did not converge.
# 2. For gamma=1.1 at one point the algorithm stops at e_act=140.
# 3. For gamma 1.3 and 1.4 there is one point for each where a false mode
#    breaks continuity of frequency, but magically does not break continuity
#    for critical e_act.
cond_1 = (e_list_1_1 != 0.0) & (e_list_1_1 != 1.400000000000000000e+02)
cond_2 = (e_list_1_2 != 0.0)
cond_3 = (e_list_1_3 != 0.0) & (e_list_1_3 != 1.988012695312500000e+01)
cond_3 = cond_3 & (e_list_1_3 != 1.937580566406250071e+01)
cond_4 = (e_list_1_4 != 0.0) & (e_list_1_4 != 2.307934570312500000e+01)
q_array_1_1 = np.array(q_list_1_1[cond_1])
q_array_1_2 = np.array(q_list_1_2[cond_2])
q_array_1_3 = np.array(q_list_1_3[cond_3])
q_array_1_4 = np.array(q_list_1_4[cond_4])
e_array_1_1 = np.array(e_list_1_1[cond_1])
e_array_1_2 = np.array(e_list_1_2[cond_2])
e_array_1_3 = np.array(e_list_1_3[cond_3])
e_array_1_4 = np.array(e_list_1_4[cond_4])
f_array_1_1 = np.array(f_list_1_1[cond_1])
f_array_1_2 = np.array(f_list_1_2[cond_2])
f_array_1_3 = np.array(f_list_1_3[cond_3])
f_array_1_4 = np.array(f_list_1_4[cond_4])

# Plot figure.
styles = ['-', '--', '-.', ':']
fig, (ax_1, ax_2) = plt.subplots(nrows=1, ncols=2, figsize=figsize)
ax_1.semilogy(e_array_1_1, q_array_1_1, styles[0], label=r'$\gamma=1.1$')
ax_1.semilogy(e_array_1_2, q_array_1_2, styles[1], label=r'$\gamma=1.2$')
ax_1.semilogy(e_array_1_3, q_array_1_3, styles[2], label=r'$\gamma=1.3$')
ax_1.semilogy(e_array_1_4, q_array_1_4, styles[3], label=r'$\gamma=1.4$')
ax_1.hold(True)
ax_1.set_xlim((0, 140))
ax_1.set_ylim((10**(-0.4), 100))
ax_1.set_xlabel(r'Activation energy, $E$')
ax_1.set_ylabel(r'Heat release, $Q$')
#ax_1.legend(loc='best')
ax_1.text(0.9, 0.85, '(a)', transform=ax_1.transAxes)
ax_1.grid()

ax_2.semilogy(f_array_1_1, q_array_1_1, styles[0], label=r'$\gamma=1.1$')
ax_2.semilogy(f_array_1_2, q_array_1_2, styles[1], label=r'$\gamma=1.2$')
ax_2.semilogy(f_array_1_3, q_array_1_3, styles[2], label=r'$\gamma=1.3$')
ax_2.semilogy(f_array_1_4, q_array_1_4, styles[3], label=r'$\gamma=1.4$')
ax_2.hold(True)
ax_2.set_ylim((10**(-0.4), 100))
ax_2.set_xlabel(r'Frequency, $\alpha_\mathrm{im}$')
ax_2.set_ylabel(r'Heat release, $Q$')
ax_2.legend(loc='best')
ax_2.text(0.9, 0.85, '(b)', transform=ax_2.transAxes)
ax_2.grid()

fig.tight_layout(pad=0.1)

fn = 'neutral-stability.pdf'
savefig(fn)
