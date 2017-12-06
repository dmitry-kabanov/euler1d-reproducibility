#!/usr/bin/env python
"""
Compute ZND thermicity for models with one- and two-step chemistries
for the same max :math:`Q` and plot them together.

"""
import os
import shutil
import sys

import matplotlib.pyplot as plt
import numpy as np

from saf.action.solve import solve

from saf.euler1d.linear import ASCIIReader as SimpleASCIIReader
from saf.euler1d.linear import Config as SimpleConfig
from saf.euler1d.linear import ZNDSolver as SimpleZNDSolver

from saf.euler1d_eigval.linear import ASCIIReader as EigvalASCIIReader
from saf.euler1d_eigval.linear import Config as EigvalConfig
from saf.euler1d_eigval.linear import ZNDSolver as EigvalZNDSolver

from helpers import FIGSIZE_NORMAL as figsize, savefig

N12 = 40
FILENAME_EIGVAL_TEMPLATE = os.path.join('_output', 'eigval-q=%.0f.txt')
FILENAME_SIMPLE_TEMPLATE = os.path.join('_output', 'simple-q=%.0f.txt')


def _run_solver(q, e_act):
    # 1. Compute eigval ZND thermicity.
    q_1 = q / (1 - 0.75 + 0.75 * np.exp(1 / -0.75))
    c_eigval = _get_eigval_config(N12, q_1, e_act)
    outdir = 'eigval-q_1=%22.16e' % q_1
    outdir = os.path.join('_output', outdir)
    if os.path.isdir(outdir):
        shutil.rmtree(outdir)
    os.mkdir(outdir)
    solve('linear', c_eigval, outdir, log_to_file=False)

    r_eigval = EigvalASCIIReader(outdir)
    znd_data_eigval = r_eigval.get_znd_data()
    grid_eigval = znd_data_eigval['x']
    znd_eigval = EigvalZNDSolver(c_eigval)
    znd_eigval.compute(grid_eigval)

    ss_squared_eigval = c_eigval.gamma * znd_eigval.p * znd_eigval.v
    coeff_eigval = (c_eigval.gamma - 1) / ss_squared_eigval
    thermicity_eigval = coeff_eigval * (c_eigval.q_1 * znd_eigval.r_1 +
                                        c_eigval.q_2 * znd_eigval.r_2)
    q_eigval = znd_eigval.q_star

    # Check that computations of q_1 are correct through comparison
    # of given q_star (q) and computed q_star.
    assert np.allclose(znd_eigval.q_star, q, rtol=1e-4, atol=1e-4)

    # 2. Compute simple-depletion ZND thermicity.
    c_simple = _get_config_for_one_step_model(N12, q_eigval, e_act)
    outdir_simple = 'simple-q=%22.16e' % q_eigval
    outdir_simple = os.path.join('_output', outdir_simple)
    if os.path.isdir(outdir_simple):
        shutil.rmtree(outdir_simple)
    os.mkdir(outdir_simple)
    solve('linear', c_simple, outdir_simple, log_to_file=False)

    r_simple = SimpleASCIIReader(outdir_simple)
    znd_data_simple = r_simple.get_znd_data()
    grid_simple = znd_data_simple['x']
    znd_simple = SimpleZNDSolver(c_simple)
    znd_simple.compute(grid_simple)

    ss_squared_simple = c_simple.gamma * znd_simple.p * znd_simple.v
    coeff_simple = (c_simple.gamma - 1) / ss_squared_simple
    thermicity_simple = coeff_simple * c_simple.q * znd_simple.r

    filename_eigval = FILENAME_EIGVAL_TEMPLATE % q
    filename_simple = FILENAME_SIMPLE_TEMPLATE % q

    data_eigval = (grid_eigval, thermicity_eigval)
    data_simple = (grid_simple, thermicity_simple)

    np.savetxt(filename_eigval, np.column_stack(data_eigval))
    np.savetxt(filename_simple, np.column_stack(data_simple))


def _get_eigval_config(n12, q_1, e_act):
    c_eigval = EigvalConfig()

    c_eigval.n12 = n12
    c_eigval.final_time = 0
    c_eigval.dt = 0.005
    c_eigval.approximator = 'henrick-weno5jp-lf'
    c_eigval.weno_eps = 1e-6
    c_eigval.time_integrator = 'dopri5'
    c_eigval.plot_time_step = 0
    c_eigval.play_animation = False
    c_eigval.extend = 0

    c_eigval.lambda_tol = 1e-6
    c_eigval.gamma = 1.2
    c_eigval.q_1 = q_1
    c_eigval.q_2 = -0.75*q_1
    c_eigval.e_act = e_act
    c_eigval.f = 1
    c_eigval.rho_a = 1.0
    c_eigval.p_a = 1.0
    c_eigval.znd_solution_type = 'subsonic-supersonic'
    c_eigval.ic_amplitude = 1e-10
    c_eigval.ic_type = 'znd'
    c_eigval.truncation_coef = 0.01

    return c_eigval

def _get_config_for_one_step_model(n12, q, e_act):
    c = SimpleConfig()

    c.n12 = 40
    c.final_time = 0
    c.dt = 0.005
    c.approximator = 'henrick-upwind5-lf'
    c.time_integrator = 'dopri5'
    c.plot_time_step = 0
    c.play_animation = False
    c.extend = 0

    c.lambda_tol = 1e-6
    c.gamma = 1.2
    c.q = q
    c.e_act = e_act
    c.f = 1
    c.rho_a = 1.0
    c.p_a = 1.0
    c.ic_amplitude = 1e-10
    c.ic_type = 'znd'
    c.truncation_coef = 0.01

    return c

if __name__ == '__main__':
    data = {'eigval': None, 'simple': None}
    q = 10
    data['eigval'] = np.loadtxt(FILENAME_EIGVAL_TEMPLATE % q)
    data['simple'] = np.loadtxt(FILENAME_SIMPLE_TEMPLATE % q)

    # 3. Plot thermicity.
    plt.figure(figsize=figsize)
    ax = plt.gca()
    plt.plot(data['eigval'][:, 0], data['eigval'][:, 1], '-')
    plt.plot(data['simple'][:, 0], data['simple'][:, 1], '--')
    plt.xlim(-10, 0)
    plt.xlabel(r'$x$')
    plt.ylabel(r'Thermicity')
    plt.grid()

    plt.tight_layout(pad=0.1)

    savefig('eigval-thermicity.pdf')
