import os

import numpy as np
import matplotlib.pyplot as plt

from saf.euler1d_eigval.linear import ASCIIReader


OUTPUT_DIR = '_output'

SUB_DIR = os.path.join(OUTPUT_DIR, 'subsonic-subsonic')
SUPER_DIR = os.path.join(OUTPUT_DIR, 'subsonic-supersonic')
TIME_STEP = 800  # Time step at which we plot profiles.

dirs = ['q_1=010.00',
        'q_1=020.00',
        'q_1=050.00']

for d in dirs:
    outdir_sub = os.path.join(SUB_DIR, d)
    outdir_super = os.path.join(SUPER_DIR, d)
    profile_fn = 'profiles/profile-{}.txt'.format(TIME_STEP)

    p_sub = os.path.join(outdir_sub, profile_fn)
    p_super = os.path.join(outdir_super, profile_fn)

    r_sub = ASCIIReader(outdir_sub)
    r_super = ASCIIReader(outdir_super)

    comp_vals_sub = r_sub.get_computed_values()
    comp_vals_super = r_super.get_computed_values()

    znd_lamda_1_sub = r_sub.get_znd_data()['lamda_1']
    znd_lamda_1_super = r_super.get_znd_data()['lamda_1']

    data_sub = np.loadtxt(p_sub)
    data_super = np.loadtxt(p_super)

    rho_sub = data_sub[:, 1]
    rho_super = data_super[:, 1]

    rho_sub = rho_sub[znd_lamda_1_sub < comp_vals_sub['lamda_1_star']]
    rho_super = rho_super[znd_lamda_1_super < comp_vals_super['lamda_1_star']]

    plt.figure()
    plt.semilogy(np.abs(rho_sub[::8] - rho_super), 'o')
    plt.show()
    print(np.linalg.norm(rho_sub[::8] - rho_super, np.Inf))


