#!/usr/bin/env python
import os

from helpers import savefig
from lib_eigval_znd_solutions import znd_read_data, znd_plot_data


OUTPUT_DIR = os.path.join('_output', 'subsonic-supersonic')

Q_VALUES = [-1.0, -10.0, -20.0, -30.0]


x, rho, u, p, lamda_1, lamda_2 = znd_read_data(Q_VALUES, OUTPUT_DIR)
znd_plot_data(x, rho, u, p, lamda_1, lamda_2)

savefig('eigval-znd-solutions-subsonic-supersonic.pdf')
