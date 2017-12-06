
# coding: utf-8

# # Experiment "DMD with synthetic data"

# In[11]:

import os
import sys
import timeit

import numpy as np
import matplotlib.pyplot as plt

from saf.linear.postprocessor import Postprocessor
from saf.linear import dmd

from helpers import FIGSIZE_TWO_SUBPLOTS_ONE_ROW as figsize, savefig


# In[13]:

def print_latex_table(true_eigvals_list, appr_eigvals_list):
    print(r'\begin{tabular}{crrrr}')
    print(r'\toprule')
    print(r'\multicolumn{1}{c}{Example} & '
          r'\multicolumn{1}{c}{\(\hat{\alpha}_\text{re}\)} & '
          r'\multicolumn{1}{c}{\(\hat{\alpha}_\text{im}\)} & '
          r'\multicolumn{1}{c}{\(e_\text{re}\)} & '
          r'\multicolumn{1}{c}{\(e_\text{im}\)} \\')
    for k in range(2):
        print(r'\midrule')
        true_eigvals = true_eigvals_list[k]
        appr_eigvals = appr_eigvals_list[k]
        assert len(true_eigvals) == len(appr_eigvals),             'Different number of true and appr. eigenvalues for k={}'.format(k)
        print_latex_table_section(true_eigvals, appr_eigvals, k)

    print(r'\bottomrule')
    print(r'\end{tabular}')


def print_latex_table_section(true_eigvals, appr_eigvals, k):
    size = len(appr_eigvals)
    for i, __ in enumerate(appr_eigvals):
        true_eigval = true_eigvals[i]
        appr_eigval = appr_eigvals[i]

        error_real = abs(true_eigval.real - appr_eigval.real) / true_eigval.real
        error_imag = abs(true_eigval.imag - appr_eigval.imag) / true_eigval.imag

        if i == 0:
            first_part = r'\multirow{{{:d}}}{{*}}{{{:}}}'
            second_part =  r'& {:9.2f} & {:14.2f} & {:14.2e} & {:14.2e} \\'
            string = first_part + second_part
            print(string.format(
                size, k+1, appr_eigval.real, appr_eigval.imag, error_real, error_imag))    
        else:
            string = r'                   & {:9.2f} & {:14.2f} & {:14.2e} & {:14.2e} \\'
            print(string.format(
                    appr_eigval.real, appr_eigval.imag, error_real, error_imag))


def dmd_synth_data():
    """Generate synthetic data and compute errors on found eigenvalues."""
    # Important constants
    AMPLITUDE = 1e-10
    NOISE_AMPLITUDE = 1e-13
    FREQ = 100
    
    def generate_synthetic_example(tfinal, true_eigvals):
        t = np.linspace(0, tfinal, num=tfinal*FREQ+1)
        y = np.zeros_like(t)

        for i in range(len(true_eigvals)):
            gamma = true_eigvals[i].real
            omega = true_eigvals[i].imag
            y = y + AMPLITUDE * np.exp(gamma*t) * np.sin(omega*t)

        y = y * (1 + NOISE_AMPLITUDE * np.random.randn(len(y)))
        
        return t, y
    
    
    print('First example')
    tfinal_1 = 21
    true_eigvals_1 = np.array([
        0.3 + 0.2 * 1j,
    ])
    t_1, y_1 = generate_synthetic_example(tfinal_1, true_eigvals_1)

    p_1 = Postprocessor(t_1, y_1)
    appr_eigvals_1, error_res_1, error_fit_1 = p_1.extract_stability_info()

    print('Second example')
    tfinal_2 = 21
    true_eigvals_2 = np.array([
        0.7 + 0.1 * 1j,
        0.8 + 1.57 * 1j,
        0.6 + 2.76 * 1j,
        0.5 + 3.88 * 1j,
        0.01 + 15.62 * 1j,
    ])

    t_2, y_2 = generate_synthetic_example(tfinal_2, true_eigvals_2)

    p_2 = Postprocessor(t_2, y_2)
    appr_eigvals_2, error_res_2, error_fit_2 = p_2.extract_stability_info()

    if len(sys.argv) > 1:
        L = p_2._L
        amps = p_2.amps
        spectrum_dmd = dmd.get_amplitude_spectrum(appr_eigvals_2, amps, L)
        freq_dmd, amps_dmd = spectrum_dmd

        N = len(y_1)
        dt = (t_2[-1] - t_2[0])/(len(t_2) - 1.0)
        yhat = np.fft.rfft(y_2)
        freq_fft = np.fft.rfftfreq(N, dt)
        # We multiply by 2, because positive and negative sides, but we plot
        # only positive side.
        # See http://www.mathworks.com/matlabcentral/answers/162846-amplitude-of-signal-after-fft-operation
        amps_fft = 2 * abs(yhat) / N

        # Rescale frequencies to be angular frequencies instead of linear.
        freq_dmd *= 2 * np.pi
        freq_fft *= 2 * np.pi

        fig, (ax_1, ax_2) = plt.subplots(nrows=1, ncols=2, figsize=figsize)
        ax_1.ticklabel_format(style='scientific')
        ax_1.plot(t_2, y_2, '-')
        ax_1.set_xlim(0, 21)
        ax_1.set_xlabel(r'$t$')
        ax_1.set_ylabel(r'$y_2$')
        ax_1.text(0.85, 0.8, '(a)', transform=ax_1.transAxes)
        ax_2.semilogy(freq_fft, amps_fft, '-')
        ax_2.semilogy(spectrum_dmd[0], spectrum_dmd[1], 'o')
        ax_2.set_xlim(0, 16)
        ax_2.set_ylim(1e-12, None)
        ax_2.set_xlabel('Frequency')
        ax_2.set_ylabel('Amplitude')
        ax_2.set_yticks(np.logspace(-1, -11, num=6))
        ax_2.text(0.85, 0.8, '(b)', transform=ax_2.transAxes)
        fig.tight_layout(pad=0.1, w_pad=1)
        savefig('dmd-synthetic-data-spectrum.pdf')
    else:
        print('Saving results into `_assets/dmd-synthetic-data.tex`')
        cur_stdout = sys.stdout
        filename = os.path.join('_assets', 'dmd-synthetic-data.tex')
        sys.stdout = open(filename, 'w')
        print_latex_table([true_eigvals_1, true_eigvals_2], [appr_eigvals_1, appr_eigvals_2])
        sys.stdout = cur_stdout
    
    print('Timing algorithm using Example 1')
    REPEAT = 3
    NUMBER = 2
    times_cum = timeit.Timer(p_1.extract_stability_info).repeat(
        repeat=REPEAT, number=NUMBER)
    times = [x / NUMBER for x in times_cum]
    print('{} loops; best of {}: {} s per loop'.format(NUMBER, REPEAT, min(times)))
    
dmd_synth_data()


# In[ ]:



