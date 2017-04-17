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
        r'S[table-format=2.5]     % Growth rate',
        r'S[table-format=2.5]     % Frequency',
        r'}',
        r'\toprule',
        r'  &',
        r'\multicolumn{4}{c}{Present work} &',
        r'\multicolumn{2}{c}{Normal-mode analysis} \\',
        r'\cmidrule(r){2-5} \cmidrule{6-7}',
        r'{$i$} &',
        r'{$\alpha_{\text{re}}$} &',
        r'{$e_{\text{re}}$} &',
        r'{$\alpha_{\text{im}}$} &',
        r'{$e_{\text{im}}$} &',
        r'{$\alpha_{\text{re}}$} &',
        r'{$\alpha_{\text{im}}$} \\',
    ]


def build_table_footer():
    return [
        r'\bottomrule',
        r'\end{tabular}',
        r'',  # To get a trailing new line symbol in the file.
    ]


def build_table_section(e_act=None, label='', nm=None):
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
    lines.append(r'\multicolumn{7}{l}{$E_{\text{act}}=' + str(e_act) +
                 label + r'$} \\')

    for i, __ in enumerate(eigvals_computed):
        index, e_c = eigvals_computed[i]
        e_t = nm[i]
        for key in ['growth_rate', 'frequency']:
            if e_t[key] is 'nan':
                e_t[key] = NOT_AVAIL
        err = errors[i]
        lines.append(
            r'{:} & {:.5f} & {:1.0e} & {:.5f} & {:1.0e} & {} & {} \\'.format(
                index, e_c['growth_rate'], err['growth_rate'],
                e_c['frequency'], err['frequency'],
                e_t['growth_rate'], e_t['frequency']))

    return lines


Q = 50

conv_factor_sharpe = 6.8094746296699951e+00
conv_factor_toong = 9.3874939445264727e-01

e_act = 25.26
# Normal-mode results are from Sharpe1997, p. 2617.
# This conversion factor is just :math:`\bar{D}` in Erpenbeck scales.
true_eigvals_original = np.array([0.0 + 1j * 0.0779])
true_eigvals_converted = true_eigvals_original * conv_factor_sharpe
normal_modes_1 = []

for e in true_eigvals_converted:
    r = '{:.3f}'.format(e.real)
    f = '{:.3f}'.format(e.imag)

    normal_modes_1.append({'growth_rate': r, 'frequency': f})

e_act = 26.00
# Normal-mode results are from Henrick2006, p. 321.
normal_modes_2 = [{'growth_rate': '0.03710', 'frequency': '0.52215'}]

e_act = 31.05
# Normal-mode results are from Sharpe1997, p. 2617.
normal_modes_3 = []
normal_modes_3.append({'growth_rate': 'nan', 'frequency': 'nan'})
normal_modes_3.append({'growth_rate': '{:.2f}'.format(0.0*conv_factor_sharpe),
                       'frequency': '{:.2f}'.format(0.643*conv_factor_sharpe)})

e_act = 50.00
# Normal-mode results are from Lee&Stewart1990, p. 127.
rate = [1.857, 1.879, 1.888, 1.785, 1.634, 1.434, 1.214,
        0.973, 0.721, 0.459, 0.189]
freq = [0.000, 4.372, 8.333, 12.16, 15.96, 19.74, 23.53,
        27.31, 31.09, 34.87, 38.65]

# Normal modes for e_act=50 case.
# The lower branch of the fundamental mode is not specified in Lee&Stewart1990.
normal_modes_4 = [{'growth_rate': 'nan', 'frequency': 'nan'}]

for i, __ in enumerate(rate):
    r = rate[i]
    f = freq[i]
    r = r * conv_factor_toong
    r_repr = '{:.3f}'.format(r)
    f = f * conv_factor_toong
    if f > 10:
        f_repr = '{:.2f}'.format(f)
    else:
        f_repr = '{:.3f}'.format(f)

    normal_modes_4.append({'growth_rate': r_repr, 'frequency': f_repr})

lines = build_table_header() + \
        build_table_section(e_act=25.26, label='^{*}', nm=normal_modes_1) + \
        build_table_section(e_act=26.00, label='^{**}', nm=normal_modes_2) + \
        build_table_section(e_act=31.05, label='^{*}', nm=normal_modes_3) + \
        build_table_section(e_act=50.00, label='^{***}', nm=normal_modes_4) + \
        build_table_footer()

if len(sys.argv) > 1:
    outfile = os.path.join('_assets', 'comparison-with-normal-modes.tex')
    with open(outfile, 'w') as f:
        f.write('\n'.join(lines))
else:
    print('\n'.join(lines))
