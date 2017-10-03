#!/usr/bin/env python
import os
import sys

import numpy as np
import matplotlib.pyplot as plt

GAMMA = 1.2
OUTPUT_DIR = os.path.join('_output', 'gamma={}'.format(GAMMA))
RESULTS_FILE = os.path.join('_output', 'results-gamma={}.txt'.format(GAMMA))


def _collect_data():
    q_list = []
    e_list = []
    f_list = []

    dirs = os.listdir(OUTPUT_DIR)
    for d in dirs:
        chunks = d.split('=')
        q = float(chunks[1])

        q_list.append(q)

        result_file = os.path.join(OUTPUT_DIR, d, 'result.txt')
        if os.path.isfile(result_file):
            with open(result_file, 'r') as f:
                e_act_line = f.readline()
                chunks = e_act_line.split('=')
                e_act = float(chunks[1])
                e_list.append(e_act)

                f.readline()  # Skipping growth_rate line.

                freq_line = f.readline()
                chunks = freq_line.split('=')
                freq = float(chunks[1])
                f_list.append(freq)
        else:
            e_list.append(0.0)
            f_list.append(0.0)

    q_sorted = [a for (a, b, c) in sorted(zip(q_list, e_list, f_list))]
    e_sorted = [b for (a, b, c) in sorted(zip(q_list, e_list, f_list))]
    f_sorted = [c for (a, b, c) in sorted(zip(q_list, e_list, f_list))]

    header = '\n'.join([
        'Neutral stability data for gamma={}'.format(GAMMA),
        'Columns: heat release $Q$, activation energy $E_{act}$, frequency $\omega$',
    ])
    np.savetxt(RESULTS_FILE, list(zip(q_sorted, e_sorted, f_sorted)), header=header)


# Collect and read results.
if not os.path.exists(RESULTS_FILE):
    _collect_data()

q_list, e_list, f_list = np.loadtxt(RESULTS_FILE, unpack=True)

# Check for fails.
# idx = np.where(e_list == 0.0)[0]
# 
# if len(e_list[idx]) > 0:
#     print('Number of fails: {}'.format(len(e_list[idx])))
#     print('Corresponding Q:')
#     for i in idx:
#         print('{:22.16e}'.format(q_list[i]))

# Cleaning the data by removing nonconverged cases.
q_clean = q_list[np.where(e_list != 0.0)[0]]
e_clean = e_list[np.where(e_list != 0.0)[0]]
f_clean = f_list[np.where(e_list != 0.0)[0]]

ls_data = np.loadtxt(os.path.join('_output',
                                  'lee-stewart-fig7-digitized-data.txt'))

# Plot figure.
fig = plt.figure()
plt.semilogy(e_clean, q_clean, '-')
plt.semilogy(ls_data[:, 0], ls_data[:, 1], '--')
plt.xlim((0, 50))
plt.ylim((0.1, 100.0))
plt.xlabel(r'Activation energy, $E$')
plt.ylabel(r'Heat release, $Q_1$')
plt.tight_layout(pad=0.1)

if len(sys.argv) > 1:
    fn = os.path.join('_assets', 'eigval-neutral-curve-gamma=1.2.pdf')
    plt.savefig(fn)
else:
    plt.show()
