#!/usr/bin/env python
import os
import matplotlib.pyplot as plt

from saf.euler1d.linear import ASCIIReader

from helpers import FIGSIZE_NORMAL, savefig

dirname = 'time-series-gamma=1.1'
dirname = os.path.join('_output', dirname)

r = ASCIIReader(dirname)
t, d = r.get_time_and_detonation_velocity()

plt.figure(figsize=FIGSIZE_NORMAL)
plt.plot(t, d, '-')
plt.xlabel(r'$t$')
plt.ylabel(r'$\psi\prime$')
plt.xlim((0, 50))
plt.ylim((-3e-10, 3e-10))
plt.tight_layout(pad=0.1)

savefig('time-series-gamma=1.1.pdf')
