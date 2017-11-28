import os

import matplotlib.pyplot as plt

from saf.euler1d_eigval.linear import ASCIIReader

from helpers import FIGSIZE_SIX_SUBPLOTS as figsize


# Format for floating-point numbers.
FMT = '+22.16e'


def znd_read_data(q_vals, outdir):
    dirs = ['q_2={:{fmt}}'.format(q, fmt=FMT) for q in q_vals]
    dirs = [os.path.join(outdir, d) for d in dirs]

    x = []
    rho = []
    u = []
    p = []
    lamda_1 = []
    lamda_2 = []

    for d in dirs:
        r = ASCIIReader(d)

        znd = r.get_znd_data()
        x.append(znd['x'])
        rho.append((d, znd['rho']))
        u.append((d, znd['u_lab']))
        p.append((d, znd['p']))
        lamda_1.append((d, znd['lamda_1']))
        lamda_2.append((d, znd['lamda_2']))

    return x, rho, u, p, lamda_1, lamda_2


def _znd_plot_quantity(x, quantity, axis, k, R):
    line_styles = ['-', '--', ':', '-o', '-*']
    assert k >= 0
    assert k < len(line_styles)
    if k != 3 and k != 4:
        axis.plot(x, quantity, line_styles[k])
    else:
        ls = line_styles[k]
        s1 = ls[0]
        s2 = ls[1]
        line, = axis.plot(x, quantity, s1)
        color = line.get_color()
        axis.plot(x[::R], quantity[::R], s2, color=color, markeredgecolor=color)


def znd_plot_data(x, rho, u, p, lamda_1, lamda_2, r=50):
    # Number of rows and columns in figures
    m, n = 3, 2
    X_LIM = -8

    fig, axes = plt.subplots(nrows=m, ncols=n, figsize=figsize)

    # Density
    ax = axes[0, 0]
    for k, __ in enumerate(rho):
        cur_x = x[k]
        cur_rho = rho[k][1]
        cur_rho = cur_rho/cur_rho[-1]

        _znd_plot_quantity(cur_x, cur_rho, ax, k, r)
    ax.set_ylabel(r'$\bar{\rho}/\bar{\rho}_{\mathrm{s}}$')
    ax.set_xlabel(r'$x$')
    ax.set_xlim((X_LIM, 0))
    ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylim((0, 1.0))

    # Velocity
    ax = axes[0, 1]
    for k, __ in enumerate(u):
        cur_x = x[k]
        cur_u = u[k][1]
        cur_u = cur_u/cur_u[-1]

        _znd_plot_quantity(cur_x, cur_u, ax, k, r)
    ax.set_ylabel(r'$\bar{u}/\bar{u}_{\mathrm{s}}$')
    ax.set_xlabel(r'$x$')
    ax.set_xlim((X_LIM, 0))
    ax.set_ylim((0.0, 1.0))

    # Pressure
    ax = axes[1, 0]
    for k, __ in enumerate(p):
        cur_x = x[k]
        cur_p = p[k][1]
        cur_p = cur_p/cur_p[-1]

        _znd_plot_quantity(cur_x, cur_p, ax, k, r)
    ax.set_ylabel(r'$\bar{p}/\bar{p}_{\mathrm{s}}$')
    ax.set_xlabel(r'$x$')
    ax.set_xlim((X_LIM, 0))
    ax.set_ylim((0.0, 1.0))

    # Temperature
    ax = axes[1, 1]
    for k, __ in enumerate(p):
        cur_x = x[k]
        cur_p = p[k][1]
        cur_p = cur_p / cur_p[-1]
        cur_rho = rho[k][1]
        cur_rho = cur_rho / cur_rho[-1]
        cur_T = cur_p / cur_rho
        _znd_plot_quantity(cur_x, cur_T, ax, k, r)
    ax.set_ylabel(r'$\bar{T}/\bar{T}_{\mathrm{s}}$')
    ax.set_xlabel(r'$x$')
    ax.set_xlim((X_LIM, 0))
    ax.set_ylim((0.95, 2.8))

    # Progress variable 1
    ax = axes[2, 0]
    for k, __ in enumerate(lamda_1):
        cur_x = x[k]
        cur_lamda = lamda_1[k][1]

        _znd_plot_quantity(cur_x, cur_lamda, ax, k, r)
    ax.set_ylabel(r'$\bar{\lambda_1}$')
    ax.set_xlabel(r'$x$')
    ax.set_xlim((X_LIM, 0))
    ax.set_ylim((0, 1.0))

    # Progress variable 2
    ax = axes[2, 1]
    for k, __ in enumerate(lamda_2):
        cur_x = x[k]
        cur_lamda = lamda_2[k][1]

        _znd_plot_quantity(cur_x, cur_lamda, ax, k, r)
    ax.set_ylabel(r'$\bar{\lambda_2}$')
    ax.set_xlabel(r'$x$')
    ax.set_xlim((X_LIM, 0))
    ax.set_ylim((0, 1.0))

    # # Reaction rate
    # ax = axes[2, 1]
    # for k, __ in enumerate(p):
    #     cur_x = x[k]
    #     cur_p = p[k][1]
    #     cur_rho = rho[k][1]
    #     cur_lamda = lamda[k][1]
    #     r = (1 - cur_lamda) * np.exp(-E_ACT*cur_rho/(cur_p))
    #     r = r / np.max(r)

    #     _znd_plot_quantity(cur_x, r, ax, k)
    # ax.set_ylabel(r'$\bar{\omega}/\bar{\omega}_{\mathrm{max}}$')
    # ax.set_xlabel(r'$x$')
    # ax.set_xlim((X_LIM, 0))
    # ax.set_ylim((0, 1.0))

    fig.tight_layout(pad=0.1, h_pad=0.55)

