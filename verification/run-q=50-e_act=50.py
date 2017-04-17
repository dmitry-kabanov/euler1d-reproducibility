#!/usr/bin/env python
import os
import multiprocessing as mp
import sys

import numpy as np

from scipy import linalg

from saf.action.solve import solve
from saf.euler1d.linear.config import Config
from saf.euler1d.linear.asciireader import ASCIIReader


E_ACT = 50.0
T_FINAL = 20


def _run_solver(args):
    q, n12 = args
    c = Config()

    c.n12 = n12
    c.final_time = T_FINAL
    c.dt = 0.01
    c.approximator = 'henrick-upwind5-lf'
    c.weno_eps = 1e-40
    c.time_integrator = 'dopri5'
    c.plot_time_step = 0
    c.play_animation = False

    c.lambda_tol = 1e-12
    c.gamma = 1.2
    c.q = q
    c.e_act = E_ACT
    c.f = 1
    c.rho_a = 1.0
    c.p_a = 1.0
    c.ic_amplitude = 1e-10
    c.ic_type = 'znd'
    c.truncation_coef = 1e6

    outdir = 'q={:06.2f}-e_act={:06.2f}-n12={:04d}'.format(q, E_ACT, n12)
    outdir = os.path.join('_output', outdir)
    solve('linear', c, outdir, log_to_file=True)

    return outdir


if __name__ == '__main__':
    q = 50.0
    n12_list = [20, 40, 80, 160, 320, 640, 1280, 2560]
    tasks = [(q, n12) for n12 in n12_list]

    with mp.Pool(processes=12) as pool:
        results = pool.map(_run_solver, tasks)

    assert results == sorted(results)

    sim_results = []
    for r in results:
        reader = ASCIIReader(r)
        __, d = reader.get_time_and_detonation_velocity()

        sim_results.append(d)

    for i, n12 in enumerate(n12_list[:-1]):
        print('*** Difference between N12={} and N12={}'.format(
            n12_list[i], n12_list[i+1]))

        d_1 = sim_results[i]
        d_2 = sim_results[i+1]

        print('    L2-norm of difference: {}'.format(linalg.norm(d_1 - d_2, 2)))
        print('    LInf-norm of difference: {}'.format(linalg.norm(d_1 - d_2, np.Inf)))
