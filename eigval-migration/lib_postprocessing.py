import logging
import os

import numpy as np

from saf.euler1d_eigval.linear import ASCIIReader

MAX_NUMBER_OF_MODES = 6

# Format for :math:`Q_2`.
FMT = '8.4f'


logger = logging.getLogger(__name__)


def are_close(a, b, lb, ub):
    r"""Check if ratio of `a` to b` is within range `lb` to `ub`.

    Parameters
    ----------
    a, b : float
        Scalar quantities that we want to compare.
    lb, ub : float
        Lower and upper bounds on the ratio :math:`\frac{a}{b}`.

    Returns
    -------
    bool
        True, if `a` and `b` are close.

    """
    if a is np.nan or b is np.nan:
        return False
    return 0.9 <= np.abs(a) / np.abs(b) <= 1.2


def process_subsonic_subsonic(outdir):
    q_values = []

    dirs = os.listdir(outdir)
    dirs.sort()

    dirs_sorted = []

    for d in dirs:
        q = float(d.split('=')[1])
        q_values.append(q)

    dirs_sorted = [d for (q, d) in sorted(zip(q_values, dirs))]

    q_values = []
    rate_upper = np.empty(len(dirs_sorted))
    rate_lower = np.empty(len(dirs_sorted))
    rate_0 = np.empty(len(dirs_sorted))
    freq_0 = np.empty(len(dirs_sorted))
    rate_1 = np.empty(len(dirs_sorted))
    freq_1 = np.empty(len(dirs_sorted))
    rate_upper.fill(np.nan)
    rate_lower.fill(np.nan)
    rate_0.fill(np.nan)
    freq_0.fill(np.nan)
    rate_1.fill(np.nan)
    freq_1.fill(np.nan)
    rates = np.empty((MAX_NUMBER_OF_MODES, len(dirs_sorted)))
    freqs = np.empty((MAX_NUMBER_OF_MODES, len(dirs_sorted)))
    rates.fill(np.nan)
    freqs.fill(np.nan)

    mode_0_looses_dominance = {'q_2': None, 'new_dominant_mode': None}

    for j, d in enumerate(dirs_sorted):
        d_path = os.path.join(outdir, d)

        q = float(d.split('=')[1])
        q_values.append(q)

        if not os.path.isfile(d_path + '/stability.txt'):
            logger.warn('No stability.txt for {}'.format(d))
            continue

        r = ASCIIReader(d_path)
        modes = r.get_stability_info()
        # assert len(modes) <= MAX_NUMBER_OF_MODES

        growth_rates = np.zeros_like(modes)
        for i, m in enumerate(modes):
            if isinstance(m, list):
                # Implicit assumption that there only two branches.
                growth_rates[i] = m[1]['growth_rate']
            else:
                growth_rates[i] = m['growth_rate']

        if np.argmax(growth_rates) != 0:
            mode_0_looses_dominance['q_2'] = q
            tmp = np.argmax(growth_rates)
            mode_0_looses_dominance['new_dominant_mode'] = tmp

        mode_0_found = False
        mode_1_found = False
        mode_2_found = False
        mode_3_found = False
        mode_4_found = False
        mode_5_found = False

        # Manually choosing modes for Q_2 = -45.0 based on the results
        # that we obtained for subsonic-supersonic simulations.
        if j == 0:
            assert q == -45.0
            rate_lower[0] = modes[0][0]['growth_rate']
            rate_upper[0] = modes[0][1]['growth_rate']
            rates[1, 0] = modes[2]['growth_rate']
            freqs[1, 0] = modes[2]['frequency']
            rates[2, 0] = modes[4]['growth_rate']
            freqs[2, 0] = modes[4]['frequency']
            rates[3, 0] = modes[5]['growth_rate']
            freqs[3, 0] = modes[5]['frequency']
            rates[4, 0] = modes[6]['growth_rate']
            freqs[4, 0] = modes[6]['frequency']
            rates[5, 0] = modes[7]['growth_rate']
            freqs[5, 0] = modes[7]['frequency']

            # Skip to next iteration as we already determined modes manually.
            continue

        # Manually choosing mode 0 at the point where
        # it becomes oscillatory.
        if q == -2.5199999999999999e+01:
            m = modes[0]
            rate_0[j] = m['growth_rate']
            freq_0[j] = m['frequency']
            mode_0_found = True

        # Flatten modes.
        if isinstance(modes[0], list):
            modes = modes[0] + modes[1:]

        for mode in modes:
            rate, freq = mode['growth_rate'], mode['frequency']
            if freq == 0.0 and 0.9 <= rate / rate_lower[j-1] <= 1.1:
                rate_lower[j] = rate
            elif freq == 0.0 and rate < 0.45:
                rate_lower[j] = rate
            elif freq == 0.0 and 0.9 <= rate / rate_upper[j-1] <= 1.1:
                rate_upper[j] = rate
            elif 0 < freq < 0.15 and rate < 0.45 and len(modes) > 4:
                rate_lower[j] = rate
            elif 0 < freq < 0.15 and rate > 0.5 and len(modes) > 4:
                rate_upper[j] = rate
            elif not mode_0_found and (are_close(rate, rate_0[j-1], 0.9, 1.2) or
                                       are_close(freq, freq_0[j-1], 0.9, 1.2)):
                rate_0[j], freq_0[j] = rate, freq
                mode_0_found = True
            elif not mode_0_found and (are_close(rate, rate_0[j-2], 0.9, 1.2) or
                                       are_close(freq, freq_0[j-2], 0.9, 1.2)):
                rate_0[j], freq_0[j] = rate, freq
                mode_0_found = True
            elif not mode_1_found and (0.98 <= freq / freqs[1, j-1] <= 1.02):
                rates[1, j], freqs[1, j] = rate, freq
                mode_1_found = True
            elif not mode_1_found and (0.98 <= freq / freqs[1, j-2] <= 1.02):
                rates[1, j], freqs[1, j] = rate, freq
                mode_1_found = True
            elif not mode_2_found and (0.998 <= freq / freqs[2, j-1] <= 1.002):
                rates[2, j], freqs[2, j] = rate, freq
                mode_2_found = True
            elif not mode_2_found and (0.998 <= freq / freqs[2, j-2] <= 1.005):
                rates[2, j], freqs[2, j] = rate, freq
                mode_2_found = True
            elif not mode_3_found and (0.998 <= freq / freqs[3, j-1] <= 1.002):
                rates[3, j], freqs[3, j] = rate, freq
                mode_3_found = True
            elif not mode_2_found and (0.998 <= freq / freqs[3, j-2] <= 1.005):
                rates[3, j], freqs[3, j] = rate, freq
                mode_3_found = True
            elif not mode_4_found and (0.998 <= freq / freqs[4, j-1] <= 1.002):
                rates[4, j], freqs[4, j] = rate, freq
                mode_4_found = True
            elif not mode_4_found and (0.99 <= freq / freqs[4, j-2] <= 1.01):
                rates[4, j], freqs[4, j] = rate, freq
                mode_4_found = True
            elif not mode_5_found and (0.99 <= freq / freqs[5, j-1] <= 1.01):
                rates[5, j], freqs[5, j] = rate, freq
                mode_5_found = True
            elif not mode_5_found and (0.99 <= freq / freqs[5, j-2] <= 1.01):
                rates[5, j], freqs[5, j] = rate, freq
                mode_5_found = True
            else:
                continue

        # if len(modes) > 1:
        #    for i, m in enumerate(modes[1:]):
        #        assert isinstance(m, dict)

        #        other_freqs[i+1, j] = m['frequency']
        #        other_rates[i+1, j] = m['growth_rate']

    # Analysis
    # for i, __ in enumerate(conjugate_rates[:-1]):
    #     if conjugate_rates[i] is None or conjugate_rates[i+1] is None:
    #         continue
    #
    #     if conjugate_rates[i] > 0.0 and conjugate_rates[i+1] < 0.0:
    #         q_crit = q_values[i+1]
    #         msg = 'Switch from stable to unstable at q_2={:{fmt}}'
    #         print(msg.format(q_crit, fmt=FMT))
    #         break
    #
    # for i, __ in enumerate(rate_upper[:-1]):
    #     if (rate_upper[i] is not None and
    #             rate_upper[i+1] is None):
    #         q_crit = q_values[i+1]
    #         msg = 'Switch to purely exponential mode at q_2={:{fmt}}'
    #         print(msg.format(q_crit, fmt=FMT))
    #         break
    #
    # print('For q_2={:+6.2f} the fundamental mode stops being dominant. '
    #       'Mode with number {} is.'.format(
    #           mode_0_looses_dominance['q_2'],
    #           mode_0_looses_dominance['new_dominant_mode']))
    #
    # rates_1 = other_rates[1, :]
    # for i, __ in enumerate(rates_1):
    #     if rates_1[i] > 0.0 and rates_1[i+1] < 0.0:
    #         if np.abs(rates_1[i]) > np.abs(rates_1[i+1]):
    #             q_crit = q_values[i+1]
    #         else:
    #             q_crit = q_values[i]
    #
    #         msg = 'Mode 1 becomes unstable at q_2={:{fmt}}'
    #         print(msg.format(q_crit, fmt=FMT))
    #         break

    q_values = np.array(q_values)

    rate_0 = {
        'oscil': rate_0,
        'lower': rate_lower,
        'upper': rate_upper,
    }

    return q_values, rate_0, rates


def process_subsonic_supersonic(outdir):
    q_values = []

    dirs = os.listdir(outdir)
    dirs.sort()

    dirs_sorted = []

    for d in dirs:
        q = float(d.split('=')[1])
        q_values.append(q)

    dirs_sorted = [d for (q, d) in sorted(zip(q_values, dirs))]

    q_values = []
    conjugate_rates = []
    exponential_rates_upper = []
    exponential_rates_bottom = []
    freq_0 = []
    other_rates = np.empty((MAX_NUMBER_OF_MODES, len(dirs_sorted)))
    other_freqs = np.empty((MAX_NUMBER_OF_MODES, len(dirs_sorted)))
    other_rates.fill(np.nan)
    other_freqs.fill(np.nan)

    for j, d in enumerate(dirs_sorted):
        d_path = os.path.join(outdir, d)

        if not os.path.isfile(d_path + '/stability.txt'):
            logger.warn('No `stability.txt` for {}', d)
            continue

        q = float(d.split('=')[1])
        q_values.append(q)

        r = ASCIIReader(d_path)
        modes = r.get_stability_info()
        assert len(modes) <= MAX_NUMBER_OF_MODES
        msg = 'For q_2={:{fmt}} number of modes {}'.format(q, len(modes),
                                                           fmt=FMT)
        logger.debug(msg)

        growth_rates = np.zeros_like(modes)
        for i, m in enumerate(modes):
            if isinstance(m, list):
                # Implicit assumption that there only two branches.
                growth_rates[i] = m[1]['growth_rate']
            else:
                growth_rates[i] = m['growth_rate']

        if np.argmax(growth_rates) != 0:
            msg = 'For q_2={:{fmt}} the dominant mode is mode {}'
            logger.debug(msg.format(q, np.argmax(growth_rates), fmt=FMT))

        mode = modes[0]

        if isinstance(mode, list):
            assert len(mode) == 2
            conjugate_rates.append(None)

            exponential_rates_bottom.append(mode[0]['growth_rate'])
            exponential_rates_upper.append(mode[1]['growth_rate'])
            freq_0.append(mode[0]['frequency'])
        else:
            conjugate_rates.append(mode['growth_rate'])
            exponential_rates_upper.append(None)
            exponential_rates_bottom.append(None)
            freq_0.append(mode['frequency'])

        if len(modes) > 1:
            for i, m in enumerate(modes[1:]):
                assert isinstance(m, dict)

                other_freqs[i+1, j] = m['frequency']
                other_rates[i+1, j] = m['growth_rate']

    # Analysis
    for i, __ in enumerate(conjugate_rates):
        if conjugate_rates[i] is None or conjugate_rates[i+1] is None:
            continue

        if conjugate_rates[i] > 0.0 and conjugate_rates[i+1] < 0.0:
            q_crit = q_values[i+1]
            msg = 'Mode 0 becomes unstable at q_2={:{fmt}}'
            logger.info(msg.format(q_crit, fmt=FMT))
            break

    for i, __ in enumerate(exponential_rates_upper):
        if (exponential_rates_upper[i] is not None and
                exponential_rates_upper[i+1] is None):
            q_crit = q_values[i+1]
            msg = 'Mode 0 becomes purely exponential at q_2={:{fmt}}'
            logger.info(msg.format(q_crit, fmt=FMT))
            break

    rates_1 = other_rates[1, :]
    for i, __ in enumerate(rates_1):
        if rates_1[i] > 0.0 and rates_1[i+1] < 0.0:
            if np.abs(rates_1[i]) > np.abs(rates_1[i+1]):
                q_crit = q_values[i+1]
            else:
                q_crit = q_values[i]

            msg = 'Mode 1 becomes unstable at q_2={:{fmt}}'
            logger.info(msg.format(q_crit, fmt=FMT))
            break

    rate_0 = {
        'oscil': conjugate_rates,
        'lower': exponential_rates_bottom,
        'upper': exponential_rates_upper,
    }

    return q_values, rate_0, other_rates
