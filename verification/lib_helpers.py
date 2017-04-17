import os

import numpy as np
import matplotlib.pyplot as plt

from functools import lru_cache

from scipy import linalg

from saf.euler1d.linear.asciireader import ASCIIReader


@lru_cache()
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
        
        
def get_abs_LInf_errors(target_dirs):
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
        
        error = linalg.norm(d_1 - d_2, np.Inf)
        errors_LInf.append(error)
        
    assert len(target_dirs) == len(errors_LInf)

    errors_LInf_array = np.asarray(errors_LInf)
    
    return errors_LInf_array
        
        
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


def get_modes_list(target_dirs):
    modes_list = []

    for outdir in target_dirs:
        full_outdir = os.path.join('_output', outdir)
        r = ASCIIReader(full_outdir)
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
        
