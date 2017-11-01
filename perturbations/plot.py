import os
import sys

import numpy as np
import matplotlib.pyplot as plt

from helpers import savefig


# In[12]:

OUTDIR = '_output'


# In[13]:

# Helper functions for "Perturbation profiles".
def plot_profiles_grouped_by_Q(vs_x=True):
    """Plot profiles of perturbations grouped by Q.

    Parameters
    ----------
    vs_x : bool (optional)
        If True, then profiles are plotted versus x, otherwise versus
        ZND reaction progress variable.

    """
    E_ACT = 30.00
    outdir_list = [
        'q=001.00',
        'q=010.00',
        'q=050.00',
    ]

    outdir_list = [os.path.join(OUTDIR, x) for x in outdir_list]

    fig, axes = plt.subplots(3, 2, figsize=(6, 6))

    styles = ['-', '--', '-.']

    for i, outdir in enumerate(outdir_list):
        profile_fn = os.path.join(outdir, 'profiles/profile-1000.txt')
        data = np.loadtxt(profile_fn)

        x = data[:, 0]
        rho = data[:, 1]
        u = data[:, 2]
        p = data[:, 3]
        lamda = data[:, 4]

        comp_vals = {}
        with open(os.path.join(outdir, 'computed-values.txt')) as f:
            for line in f.readlines():
                chunks = line.split('=')
                key = chunks[0].strip()
                value = float(chunks[1].strip())
                comp_vals[key] = value

        k = comp_vals['k']

        znd_data = np.loadtxt(os.path.join(outdir, 'znd-solution.txt'))

        znd_rho = znd_data[:, 2]
        znd_p = znd_data[:, 4]
        znd_lamda = znd_data[:, 5]

        dT_drho = - znd_p / znd_rho**2
        dT_dp = 1.0 / znd_rho

        T = dT_drho * rho + dT_dp * p

        exponent = np.exp(-E_ACT * znd_rho / znd_p)
        dr_drho = k * (1 - znd_lamda) * exponent * (-E_ACT/znd_p)
        dr_dp = k * (1 - znd_lamda) * exponent * E_ACT * znd_rho / znd_p**2
        dr_dlamda = -k * exponent

        rate = dr_drho * rho + dr_dp * p + dr_dlamda * lamda

        scaler_rho = np.max(np.abs(rho))
        scaler_u = np.max(np.abs(u))
        scaler_p = np.max(np.abs(p))
        scaler_lamda = np.max(np.abs(lamda))
        scaler_T = np.max(np.abs(T))
        scaler_rate = np.max(np.abs(rate))

        scaler_rho = 1
        scaler_u = 1
        scaler_p = 1
        scaler_lamda = 1
        scaler_T = 1
        scaler_rate = 1

        if not vs_x:
            x = znd_lamda

        axes[i, 0].plot(x, rho/scaler_rho, styles[0])
        axes[i, 0].plot(x, u/scaler_u, styles[1])
        axes[i, 0].plot(x, p/scaler_p, styles[2])
        axes[i, 1].plot(x, lamda/scaler_lamda, styles[0])
        axes[i, 1].plot(x, T / scaler_T, styles[1])
        axes[i, 1].plot(x, rate/scaler_rate, styles[2])

    axes[0, 0].set_ylabel(r'$Q = 1$')
    axes[1, 0].set_ylabel(r'$Q = 10$')
    axes[2, 0].set_ylabel(r'$Q = 50$')

    if vs_x:
        axes[2, 0].set_xlabel(r'$x$')
        axes[2, 1].set_xlabel(r'$x$')
    else:
        axes[2, 0].set_xlabel(r'$\bar{\lambda}$')
        axes[2, 1].set_xlabel(r'$\bar{\lambda}$')

    if vs_x:
        x_lim = -5
        axes[0, 0].set_xlim((x_lim, 0))
        axes[0, 1].set_xlim((x_lim, 0))
        axes[1, 0].set_xlim((-2, 0))
        axes[1, 1].set_xlim((-2, 0))
        axes[2, 0].set_xlim((x_lim, 0))
        axes[2, 1].set_xlim((x_lim, 0))

    fig.tight_layout(pad=0.1)

    if vs_x:
        outfile = 'perturbations-vs-x.pdf'
    else:
        outfile = 'perturbations-vs-znd-lambda.pdf'

    savefig(outfile)


if len(sys.argv) > 1:
    plot_profiles_grouped_by_Q(vs_x=True)
else:
    plot_profiles_grouped_by_Q(vs_x=False)
