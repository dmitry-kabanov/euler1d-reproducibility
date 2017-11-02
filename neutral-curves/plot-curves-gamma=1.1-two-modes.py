#!/usr/bin/env python
import os

import numpy as np
import matplotlib.pyplot as plt

from helpers import FIGSIZE_NORMAL, savefig

GAMMA = 1.1
RESULTS_FILE_MODE_0 = 'results-gamma={}.txt'.format(GAMMA)
RESULTS_FILE_MODE_1 = 'results-gamma={}-mode=1.txt'.format(GAMMA)
RESULTS_FILE_MODE_0 = os.path.join('_output', RESULTS_FILE_MODE_0)
RESULTS_FILE_MODE_1 = os.path.join('_output', RESULTS_FILE_MODE_1)

q_list_0, e_list_0, f_list_0 = np.loadtxt(RESULTS_FILE_MODE_0, unpack=True)
q_list_1, e_list_1, f_list_1 = np.loadtxt(RESULTS_FILE_MODE_1, unpack=True)

# Cleaning data
idx_0 = np.where((e_list_0 != 0.0) & (e_list_0 != 140.0))[0]
cond_1_1 = (e_list_1 != 0.0000000000000000e+00)
cond_1_2 = (e_list_1 != 1.2517321777343751e+01)
cond_1_3 = (e_list_1 != 1.2555725097656250e+01)
cond_1_4 = (e_list_1 != 1.2666015625000000e+01)
idx_1 = np.where(cond_1_1 & cond_1_2 & cond_1_3 & cond_1_4)[0]
q_clean_0 = q_list_0[idx_0]
e_clean_0 = e_list_0[idx_0]
q_clean_1 = q_list_1[idx_1]
e_clean_1 = e_list_1[idx_1]

# Plot figure.
fig = plt.figure(figsize=FIGSIZE_NORMAL)
plt.semilogy(e_clean_0, q_clean_0, '-', label='Mode 0')
plt.semilogy(e_clean_1, q_clean_1, '--', label='Mode 1')
plt.hold(True)
plt.xlim((10, 35))
plt.ylim((2, 80))
plt.xlabel(r'Activation energy, $E$')
plt.ylabel(r'Heat release, $Q$')
plt.grid()
plt.tight_layout(pad=0.1)

fn = 'neutral-stability-gamma={}-two-modes.pdf'.format(GAMMA)
savefig(fn)
