#!/usr/bin/env python
import os
import multiprocessing as mp


from lib_helpers import run_solver


Q = 50.0
E_ACT = 31.05
T_FINAL = 10.0


if __name__ == '__main__':
    n12_list = [20, 40, 80, 160, 320, 640, 1280]
    top_outdir = 'q={:06.2f}-e_act={:06.2f}'.format(Q, E_ACT)
    top_outdir = os.path.join('_output', top_outdir)

    if not os.path.isdir(top_outdir):
        os.mkdir(top_outdir)

    tasks = [(Q, E_ACT, T_FINAL, top_outdir, n12) for n12 in n12_list]

    with mp.Pool(processes=2) as pool:
        pool.map(run_solver, tasks)
