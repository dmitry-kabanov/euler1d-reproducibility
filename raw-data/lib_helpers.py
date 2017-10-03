import os

import matplotlib.pyplot as plt
import numpy as np

from functools import lru_cache

from scipy import linalg

from saf.action.solve import solve
from saf.euler1d.linear.config import Config
from saf.euler1d.linear.asciireader import ASCIIReader


def run_solver(args):
    q, e_act, t_final, top_outdir, n12 = args
    c = Config()

    c.n12 = n12
    c.final_time = t_final
    c.dt = 0.005
    c.approximator = 'henrick-upwind5-lf'
    c.weno_eps = 1e-40
    c.time_integrator = 'dopri5'
    c.plot_time_step = 0
    c.play_animation = False

    c.lambda_tol = 1e-12
    c.gamma = 1.2
    c.q = q
    c.e_act = e_act
    c.f = 1
    c.rho_a = 1.0
    c.p_a = 1.0
    c.ic_amplitude = 1e-10
    c.ic_type = 'znd'
    c.truncation_coef = 1e6

    sub_outdir = 'n12={:04d}'.format(n12)
    outdir = os.path.join(top_outdir, sub_outdir)
    solve('linear', c, outdir, log_to_file=True)

    return outdir


@lru_cache()
def get_target_dirs_and_resolutions(Q=None, Eact=None):
    """Find directories with results corresponding to `Q` and `Eact`."""
    if Q is None or Eact is None:
        raise Exception('Specify Q and Eact')

    outdir = 'q={:06.2f}-e_act={:06.2f}'.format(Q, Eact)
    outdir = os.path.join('_output', outdir)
    dirs = os.listdir(outdir)
    dirs.sort()

    target_dirs = [os.path.join(outdir, d) for d in dirs]

    resolutions = []
    for d in dirs:
        chunks = d.split('=')
        resolutions.append(int(chunks[-1]))

    return target_dirs, resolutions


def get_abs_LInf_errors(target_dirs):
    d_list = []

    for outdir in target_dirs:
        r = ASCIIReader(outdir)
        __, d = r.get_time_and_detonation_velocity()

        d_list.append(d)

    errors_LInf = [float('NaN')]
    for i, d in enumerate(d_list):
        if i == 0:
            continue

        d_1 = d_list[i-1]
        d_2 = d_list[i]

        error = linalg.norm(d_1 - d_2, np.Inf)
        errors_LInf.append(error)

    assert len(target_dirs) == len(errors_LInf)

    errors_LInf_array = np.asarray(errors_LInf)

    return errors_LInf_array


def get_rel_LInf_errors(target_dirs):
    d_list = []

    for outdir in target_dirs:
        r = ASCIIReader(outdir)
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


def get_modes_list(target_dirs):
    modes_list = []

    for outdir in target_dirs:
        r = ASCIIReader(outdir)
        modes = r.get_stability_info()
        modes_list.append(modes)

    return modes_list


def print_convergence_table(resolutions, errors_LInf_abs, errors_LInf_rel):
    """Print table resolution versus error in :math:`L_\infty`-norm."""
    print('Resolution   Abs. LInf-error   Rel. LInf-error   Abs. r      Rel. r')
    for i, r in enumerate(resolutions):
        err_abs = errors_LInf_abs[i]
        err_rel = errors_LInf_rel[i]

        if i >= 2:
            err_abs_prev = errors_LInf_abs[i-1]
            err_rel_prev = errors_LInf_rel[i-1]
            r_abs = np.log(err_abs_prev / err_abs) / np.log(2)
            r_rel = np.log(err_rel_prev / err_rel) / np.log(2)
            print('{:10d} {:14.2e} {:14.2e} {:12.2f} {:12.2f}'.format(r, err_abs, err_rel, r_abs, r_rel))
        else:
            print('{:10d} {:14.2e} {:14.2e}          N/A          N/A'.format(r, err_abs, err_rel))


def print_table_resolution_modes(resolutions, modes_list):
    for i, modes in enumerate(modes_list):
        for j, mode in enumerate(modes):
            if type(mode) is list:
                for k, m in enumerate(mode):
                    rate = m['growth_rate']
                    freq = m['frequency']
                    print('{}    {}.{}   {:.3f}    {:.3f}'.format(resolutions[i], j, k, rate, freq))
            else:
                rate = mode['growth_rate']
                freq = mode['frequency']
                print('{}    {}   {:.3f}    {:.3f}'.format(resolutions[i], j, rate, freq))


def print_resolutions_and_number_of_modes(resolutions, modes_list):
    """Print table resolution vs number of modes (eigenvalues)."""
    print('Resolution   No of modes')
    for i, modes in enumerate(modes_list):
        print('{:6d} {:12d}'.format(resolutions[i], len(modes)))


def print_convergence_table_latex(resolutions, errors_LInf_rel, filename=None):
    """Print table resolution versus error in :math:`L_\infty`-norm."""
    NAN_REPR = '{N/A}'
    lines = [
        r'\begin{tabular}{',
        r'  r',
        r'  S[table-format=1.2,',
        r'    table-figures-exponent=2,',
        r'    table-sign-mantissa,',
        r'    table-sign-exponent]',
        r'  S[table-format=1.2]}',
        r'\toprule',
        r'\multicolumn{1}{c}{$N_{1/2}$} & ',
        r'\multicolumn{1}{c}{$E_{\infty}$} & ',
        r'\multicolumn{1}{c}{$r_{\text{c}}$} \\',
        r'\midrule',
    ]
    for i, r in enumerate(resolutions):
        err_rel = errors_LInf_rel[i]

        if i >= 2:
            err_rel_repr = '{:8.2e}'.format(err_rel)
            err_rel_prev = errors_LInf_rel[i-1]
            r_rel = np.log(err_rel_prev / err_rel) / np.log(2)
            r_rel_repr = '{:4.2f}'.format(r_rel)
        elif i == 1:
            err_rel_repr = '{:8.2e}'.format(err_rel)
            r_rel_repr = '{:4s}'.format(NAN_REPR)
        else:
            err_rel_repr = '{:8s}'.format(NAN_REPR)
            r_rel_repr = '{:4s}'.format(NAN_REPR)

        lines.append(r'{:10d} & {:s} & {:s} \\'.format(r, err_rel_repr, r_rel_repr))

    lines.append(r'\bottomrule')
    lines.append(r'\end{tabular}')
    lines.append('')  # To have final newline symbol.

    if filename is None:
        return lines
    else:
        with open(os.path.join('_assets', filename), 'w') as f:
            f.write('\n'.join(lines))


def plot_time_series(E_act):
    r = ASCIIReader('_output/q=050.00-e_act=0{:4.2f}/n12=0160/'.format(E_act))
    t, d = r.get_time_and_detonation_velocity()

    plt.figure()
    plt.plot(t, d, '-')
    plt.xlabel('time')
    plt.ylabel(r"$\psi '$")
    plt.tight_layout(pad=0.1)
    savefig('time-series-e_act={:4.2f}.pdf'.format(E_act))


def plot_eigenvalue(resolutions, modes_list, start_with, what):
    assert what == 'growth_rate' or what == 'frequency'
    styles = ['o', 's', '^', 'v', '*', '.']
    modes_list = modes_list.copy()
    if len(modes_list[start_with:]) > len(styles):
        print('WARNING: not enough styles, will plot only several first ones.')

    max_indices_len = 0
    plt.figure()
    for i, modes in enumerate(modes_list[start_with:start_with + len(styles)]):
        modes_flatten = []
        indices = []
        for j, mode in enumerate(modes):
            if type(mode) is list:
                for m in mode:
                    indices.append(j)
                    modes_flatten.append(m[what])
            else:
                indices.append(j)
                modes_flatten.append(mode[what])
        
        if len(indices) > max_indices_len:
            max_indices_len = len(indices)
        plt.plot(indices, modes_flatten, styles[i], label='N={}'.format(resolutions[start_with+i]))
                
    #plt.legend(['N={}'.format(N) for N in resolutions[start_with:]])
    plt.legend(loc='lower center')
    plt.xlim((-0.2, max_indices_len-1 + 0.2))
    plt.xlabel('Index')
    if what == 'growth_rate':
        plt.ylabel('Growth rate')
    else:
        plt.ylabel('Frequency')
    plt.tight_layout(pad=0.1)


def flatten_modes(modes_list):
    result = []

    for i, mode in enumerate(modes_list):
        if type(mode) is list:
            for j, m in enumerate(mode):
                result.append(m)
        else:
            result.append(mode)

    return result


def enumerate_and_flatten_modes(modes_list):
    result = []

    for i, mode in enumerate(modes_list):
        if type(mode) is list:
            for j, m in enumerate(mode):
                result.append(('{}.{}'.format(i, j), m))
        else:
            result.append(('{}'.format(i), mode))

    return result


def print_eigenvalues_convergence_table(resolutions, modes, start_value):
    modes = modes.copy()
    modes = modes[start_value:]
    modes_list = []
    res = resolutions.copy()
    res = res[start_value:]
    
    for k in range(len(modes)):
        modes_list.append(enumerate_and_flatten_modes(modes[k]))
        
    for k in range(1, len(modes_list)):
        assert len(modes_list[k]) == len(modes_list[k-1])
    
    string = '{:6s} ' + ' '.join(['{:12d}']*len(res)) + '   Relative errors for last two columns'
    print(string.format('Index', *res))
    for k in range(len(modes_list[0])):
        index = modes_list[0][k][0]
        growth_rates = []
        frequencies = []
        for i, __ in enumerate(res):
            m = modes_list[i][k][1]
            growth_rate = m['growth_rate']
            frequency = m['frequency']
            growth_rates.append(growth_rate)
            frequencies.append(frequency)
            
        growth_rates_errors = []
        growth_rates_errors.append(compute_rel_error(growth_rates[-3], growth_rates[-2]))
        growth_rates_errors.append(compute_rel_error(growth_rates[-2], growth_rates[-1]))
        
        frequencies_errors = []
        frequencies_errors.append(compute_rel_error(frequencies[-3], frequencies[-2]))
        frequencies_errors.append(compute_rel_error(frequencies[-2], frequencies[-1]))
        
        string = '{:4s} | ' + ' '.join(['{:12.8f}']*len(growth_rates)) + ' | ' + ' '.join(['{:7.0e}']*2)
        print(string.format(index, *growth_rates, *growth_rates_errors))
        print(string.format(index, *frequencies, *frequencies_errors))

        
def compute_rel_error(a, b):
    if a == b:
        return np.finfo(float).eps

    return np.abs((a-b) / b)
        
        
def get_eigenvalues_errors(eigvals_1, eigvals_2):
    errors = []
    for i, __ in enumerate(eigvals_2):
        v_1 = eigvals_1[i]
        v_2 = eigvals_2[i]

        r_1, f_1 = v_1['growth_rate'], v_1['frequency']
        r_2, f_2 = v_2['growth_rate'], v_2['frequency']

        err_rate = compute_rel_error(r_1, r_2)
        err_freq = compute_rel_error(f_1, f_2)
        errors.append({'growth_rate': err_rate, 'frequency': err_freq})

    return errors


def run_analysis(Q=50, E_act=26.00, plot_eigenvalues=False, show_modes_list=False):
    plot_time_series(E_act)
    target_dirs, resolutions = get_target_dirs_and_resolutions(Q=Q, Eact=E_act)
    errors_LInf_abs = get_abs_LInf_errors(target_dirs)
    errors_LInf_rel = get_rel_LInf_errors(target_dirs)
    #print('********************')
    #print('Solution convergence')
    #print_convergence_table(resolutions, errors_LInf_abs, errors_LInf_rel)
    modes_list = get_modes_list(target_dirs)
    print('*******************************')
    print('Resolutions and number of modes')
    print_resolutions_and_number_of_modes(resolutions, modes_list)
    
    try:
        print()
        print()
        print('***********************************')
        print('Table of convergence of eigenvalues (odd rows are growth rates, even rows are frequencies)')
        print()
        print_eigenvalues_convergence_table(resolutions, modes_list, start_value=3)
    except AssertionError:
        print('ERROR: Cannot print convergence table. Probably, number of modes does not converge.')
    
    if plot_eigenvalues:
        plot_eigenvalue(resolutions, modes_list, 2, 'growth_rate')
        savefig('growth-rate-q={:2.0f}-e_act={:4.2f}.pdf'.format(Q, E_act))
        plot_eigenvalue(resolutions, modes_list, 2, 'frequency')
        savefig('frequency-q={:2.0f}-e_act={:4.2f}.pdf'.format(Q, E_act))
        
    if show_modes_list:
        print(dict(zip(resolutions, modes_list)))


def savefig(filename):
    """Save a figure to file in the `_assets` subdir if `SAVEFIG` is True."""
    if 'SAVE_FIGURES' in os.environ and os.environ['SAVE_FIGURES']:
        fig = plt.gcf()
        full_filename = os.path.join('_assets', filename)
        fig.savefig(full_filename)
