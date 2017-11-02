#!/usr/bin/env python
import os
import sys

import numpy as np

from lib_helpers import (get_target_dirs_and_resolutions,
                         get_modes_list,
                         get_eigenvalues_errors,
                         enumerate_and_flatten_modes,
                         flatten_modes)


NOT_AVAIL = '{N/A}'


def build_table_header():
    return [
        r'\begin{tabular}{',
        r'S[table-format=2.0]',
        r'S[table-format=2.5]  % Growth rate',
        r'S[table-format=1.0e+2]  % Growth rate error',
        r'S[table-format=2.5]     % Frequency',
        r'S[table-format=1.0e+2]  % Frequency error',
        r'}',
        r'\toprule',
        r'{$i$} &',
        r'{$\alpha_{\text{re}}$} &',
        r'{$e_{\text{re}}$} &',
        r'{$\alpha_{\text{im}}$} &',
        r'{$e_{\text{im}}$} \\',
    ]


def build_table_footer():
    return [
        r'\bottomrule',
        r'\end{tabular}',
        r'',  # To get a trailing new line symbol in the file.
    ]


def build_table_section(e_act=None):
    target_dirs, resolutions = get_target_dirs_and_resolutions(Q=Q, Eact=e_act)
    modes_list = get_modes_list(target_dirs)

    # Checks for sanity.
    assert len(modes_list[-2]) == len(modes_list[-1])
    assert resolutions[-2] == 640
    assert resolutions[-1] == 1280

    m_640 = flatten_modes(modes_list[-2])
    m_1280 = flatten_modes(modes_list[-1])
    errors = get_eigenvalues_errors(m_640, m_1280)

    eigvals_computed = enumerate_and_flatten_modes(modes_list[-1])

    lines = []

    lines.append(r'\midrule')
    lines.append(r'\addlinespace')
    lines.append(r'\multicolumn{5}{l}{$E=' + str(e_act) +
                 r'$} \\')

    for i, __ in enumerate(eigvals_computed):
        index, e_c = eigvals_computed[i]
        err = errors[i]
        lines.append(
            r'{:} & {:.5f} & {:1.0e} & {:.5f} & {:1.0e} \\'.format(
                index, e_c['growth_rate'], err['growth_rate'],
                e_c['frequency'], err['frequency']))

    return lines


Q = 50

lines = build_table_header() + \
        build_table_section(e_act=35) + \
        build_table_section(e_act=40) + \
        build_table_footer()

if len(sys.argv) > 1:
    outfile = os.path.join('_assets', 'raw-data-modes.tex')
    with open(outfile, 'w') as f:
        f.write('\n'.join(lines))
else:
    print('\n'.join(lines))
