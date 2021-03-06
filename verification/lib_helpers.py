import os

import numpy as np

from scipy import linalg

from saf.euler1d.linear.asciireader import ASCIIReader


def get_target_dirs_and_resolutions(Q=None, Eact=None):
    """Find directories with results corresponding to `Q` and `Eact`."""
    if Q is None or Eact is None:
        raise Exception('Specify Q and Eact')

    dirs = os.listdir('_output')

    target_dirs = []
    for d in dirs:
        if d.startswith('q={:06.2f}-e_act={:06.2f}'.format(Q, Eact)):
            target_dirs.append(d)

    target_dirs.sort()

    resolutions = []
    for d in target_dirs:
        chunks = d.split('=')
        resolutions.append(int(chunks[-1]))

    return target_dirs, resolutions


def get_rel_LInf_errors(target_dirs):
    d_list = []

    for outdir in target_dirs:
        full_outdir = os.path.join('_output', outdir)
        r = ASCIIReader(full_outdir)
        __, d = r.get_time_and_detonation_velocity()

        d_list.append(d)

    errors_LInf = [float('NaN')]
    for i, d in enumerate(d_list):
        if i == 0:
            continue

        d_1 = d_list[i-1]
        d_2 = d_list[i]

        error = linalg.norm(d_1 - d_2, np.Inf) / linalg.norm(d_2, np.Inf)
        errors_LInf.append(error)

    assert len(target_dirs) == len(errors_LInf)

    errors_LInf_array = np.asarray(errors_LInf)

    return errors_LInf_array


def print_convergence_table_latex(resolutions, errors_LInf_rel, filename=None):
    """Print table resolution versus error in :math:`L_\infty`-norm."""
    NAN_REPR = '{N/A}'

    err_list = []
    r_list = []
    for i, r in enumerate(resolutions):
        err_rel = errors_LInf_rel[i]

        if i >= 2:
            err_rel_repr = '\\num{{{:8.0e}}}'.format(err_rel)
            err_rel_prev = errors_LInf_rel[i-1]
            r_rel = np.log(err_rel_prev / err_rel) / np.log(2)
            r_rel_repr = '{:4.2f}'.format(r_rel)
        elif i == 1:
            err_rel_repr = '\\num{{{:8.0e}}}'.format(err_rel)
            r_rel_repr = '{:4s}'.format(NAN_REPR)
        else:
            err_rel_repr = '{:8s}'.format(NAN_REPR)
            r_rel_repr = '{:4s}'.format(NAN_REPR)

        err_list.append(err_rel_repr)
        r_list.append(r_rel_repr)

    line_res = (
        r'$N_{1/2}$ & ' + 
        ' & '.join([str(r) for r in resolutions]) +
        r' \\')
    line_err = r'$E$ & ' + ' & '.join(err_list) + r' \\'
    line_r = r'$r_{\text{acc}}$ & ' + ' & '.join(r_list) + r' \\'

    lines = []
    line_header = r'\begin{tabular}{l' + len(resolutions)*'c' + r'} \\'

    lines.append(line_header)
    lines.append(r'\toprule')
    lines.append(line_res)
    lines.append(line_err)
    lines.append(line_r)
    lines.append(r'\bottomrule')
    lines.append(r'\end{tabular}')
    lines.append('')  # To have final newline symbol.

    if filename is None:
        return lines
    else:
        with open(os.path.join('_assets', filename), 'w') as f:
            f.write('\n'.join(lines))
