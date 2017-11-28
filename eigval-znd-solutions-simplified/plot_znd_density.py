#!/usr/bin/env python
import os
import sys

import numpy as np
import matplotlib.pyplot as plt

types = ['subsonic-supersonic', 'subsonic-subsonic']
styles = ['-', '--', '-.']

q_2 = -3.0000000000000000e+01

plt.figure()
for i, t in enumerate(types):
    outdir = '_output/{}'.format(t)
    outdir = os.path.join(outdir, 'q_2=%+22.16e' % q_2)
    znd_fn = os.path.join(outdir, 'znd-solution.txt')
    data = np.loadtxt(znd_fn)
    x = data[:, 0]
    rho = data[:, 2]

    plt.plot(x, rho, styles[i], label=t)
    plt.xlabel(r'$x$')
    plt.ylabel(r'$\bar{\rho}$')
    plt.legend(loc='best')
    plt.xlim((-10, 0))
    plt.tight_layout(pad=0.1)

if len(sys.argv) > 1:
    fn = os.path.join('_assets', 'znd-density.pdf')
    plt.savefig(fn)
else:
    plt.show()
