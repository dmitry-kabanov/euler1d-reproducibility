#!/usr/bin/env python
import os
import sys

import numpy as np
import matplotlib.pyplot as plt

from saf.euler1d_eigval.linear import ASCIIReader

FMT_UNSIGNED = '22.16e'
FMT_SIGNED = '+22.16e'


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

    q_star = np.zeros_like(q_sorted)

    for i, q_1 in enumerate(q_sorted):
        q_2 = -0.75 * q_1
        e_act = e_sorted[i]
        if e_act == 0.0:
            continue
        outdir = '_output/gamma=1.2/q_1={:{fmt_s}}/e_act={:{fmt_u}}'
        outdir = os.path.join(outdir.format(q_1, e_act,
                                            fmt_s=FMT_SIGNED,
                                            fmt_u=FMT_UNSIGNED))

        r = ASCIIReader(outdir)
        vals = r.get_computed_values()
        lamda_1_star = vals['lamda_1_star']
        lamda_2_star = vals['lamda_2_star']

        q_max = q_1 * lamda_1_star + q_2 * lamda_2_star
        q_star[i] = q_max

    header = '\n'.join([
        'Neutral stability data for gamma={}'.format(GAMMA),
        ('Columns: heat release $Q_1$, activation energy $E_{act}$, '
         'frequency $\omega$, max heat release $Q^*$'),
    ])
    data = list(zip(q_sorted, e_sorted, f_sorted, q_star))
    np.savetxt(RESULTS_FILE, data, header=header)


# Collect and read results.
if not os.path.exists(RESULTS_FILE):
    _collect_data()

q_list, e_list, f_list, q_star = np.loadtxt(RESULTS_FILE, unpack=True)

# Check for fails.
# idx = np.where(e_list == 0.0)[0]
# 
# if len(e_list[idx]) > 0:
#     print('Number of fails: {}'.format(len(e_list[idx])))
#     print('Corresponding Q:')
#     for i in idx:
#         print('{:22.16e}'.format(q_list[i]))

# Cleaning the data by removing nonconverged cases.
idx = np.where(e_list != 0.0)[0]
q_clean = np.array(q_list[idx])
e_clean = np.array(e_list[idx])
f_clean = np.array(f_list[idx])
q_star_clean = np.array(q_star[idx])

ls_data = np.loadtxt('_output/lee-stewart-fig7-digitized-data.txt')

# Plot figure.
fig = plt.figure()
plt.semilogy(e_clean, q_star_clean, '-', label='Two-step chemistry')
plt.semilogy(ls_data[:, 0], ls_data[:, 1], '--', label='One-step chemistry')
plt.xlim((0, 50))
plt.ylim((0.1, 100.0))
plt.xlabel(r'Activation energy, $E$')
plt.ylabel(r'Max heat release, $Q$')
plt.legend(loc='best')
plt.grid()
plt.tight_layout(pad=0.1)

if len(sys.argv) > 1:
    fn = os.path.join('_assets', 'eigval-neutral-curve-gamma=1.2.pdf')
    plt.savefig(fn)
else:
    plt.show()
