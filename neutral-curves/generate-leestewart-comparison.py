#!/usr/bin/env python
import os
import sys

import numpy as np
import matplotlib.pyplot as plt

from helpers import savefig

OUTPUT_DIR = '_output'
RESULTS_FILE_0 = os.path.join(OUTPUT_DIR, 'results-gamma=1.2.txt')
LEESTEWART_FILE = 'lee-stewart-fig7-digitized-data.txt'
LEESTEWART_FILE = os.path.join(OUTPUT_DIR, LEESTEWART_FILE)


q_list_0, e_list_0, __ = np.loadtxt(RESULTS_FILE_0, unpack=True)
ls_e_0, ls_q_0 = np.loadtxt(LEESTEWART_FILE, unpack=True)

# Cleaning my data.
idx = np.where(e_list_0 != 0.0)[0]
q_clean_0 = q_list_0[idx]
e_clean_0 = e_list_0[idx]

plt.figure()
plt.hold(True)
plt.semilogy(e_clean_0, q_clean_0, '-', label='Present work')
plt.semilogy(ls_e_0[::2], ls_q_0[::2], 's', label='Normal modes')
plt.xlim((0, 50))
plt.ylim((0.1, 105))
plt.xlabel(r'Activation energy, $E$')
plt.ylabel(r'Heat release, $Q$')
plt.legend(loc='best')
plt.grid()
plt.tight_layout(pad=0.1)

if len(sys.argv) > 1:
    fn = 'LeeStewart-comparison.pdf'
    savefig(fn)
else:
    plt.show()
