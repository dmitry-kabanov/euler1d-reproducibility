#!/usr/bin/env python
import os

import matplotlib.pyplot as plt

from saf.euler1d.linear.asciireader import ASCIIReader
from matplotlib.ticker import FormatStrFormatter

from helpers import FIGSIZE_TWO_SUBPLOTS_TWO_ROWS as figsize


r_35 = ASCIIReader('_output/q=050.00-e_act=035.00/n12=0640')
r_40 = ASCIIReader('_output/q=050.00-e_act=040.00/n12=0640')


t_35, d_35 = r_35.get_time_and_detonation_velocity()
t_40, d_40 = r_40.get_time_and_detonation_velocity()

fig, ax = plt.subplots(nrows=2, ncols=1, figsize=figsize)
ax[0].plot(t_35, d_35, '-')
ax[0].set_xlim((0, 50))
ax[0].set_ylim((-0.1, 0.85))
#ax[0].set_ylim((-1e-4, 1e-4))
ax[0].set_xlabel(r'$t$')
ax[0].set_ylabel(r"$\psi '$")
f_1_x = FormatStrFormatter('%6.1f')
ax[0].yaxis.set_major_formatter(f_1_x)

ax[1].plot(t_40, d_40, '-')
ax[1].set_ylim((-100, 2000))
ax[1].set_ylabel(r"$\psi '$")
ax[1].set_xlabel(r'$t$')

fig.tight_layout(pad=0.1)

first_stage_time = 35
inset_1 = fig.add_axes([0.29, .79, .45, .2])
f_1 = FormatStrFormatter('%1.0e')
inset_1.plot(t_35[t_35<=first_stage_time], d_35[t_35<=first_stage_time], '-')
inset_1.yaxis.set_major_formatter(f_1)
inset_1.set_xlabel(r'$t$')
inset_1.set_ylabel(r"$\psi '$")
inset_1.set_xticks([5, 15, 25, 35])
inset_1.set_yticks([-2e-4, 2e-4, 6e-4])

# Second inset.
first_stage_time_2 = 10
inset_2 = fig.add_axes([0.29, .27, .45, .2])
f_2 = FormatStrFormatter('%1.0e')
inset_2.plot(t_40[t_40<=first_stage_time_2], d_40[t_40<=first_stage_time_2], '-')
inset_2.yaxis.set_major_formatter(f_2)
inset_2.set_ylim((-5e-7, 4e-6))
inset_2.set_xlabel(r'$t$')
inset_2.set_ylabel(r"$\psi '$")
inset_2.set_xticks([0, 5, 10])
inset_2.set_yticks([0, 2e-6, 4e-6])

outfile = os.path.join('_assets', 'raw-data-examples.pdf')
plt.savefig(outfile)
