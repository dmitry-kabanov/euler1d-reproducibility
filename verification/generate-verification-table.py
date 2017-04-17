from lib_helpers import (get_target_dirs_and_resolutions,
                         get_rel_LInf_errors,
                         print_convergence_table_latex)


def generate_table():
    target_dirs, resolutions = get_target_dirs_and_resolutions(Q=50, Eact=50)
    errors_LInf_rel = get_rel_LInf_errors(target_dirs)
    print_convergence_table_latex(
        resolutions, errors_LInf_rel, filename='verification.tex')


if __name__ == '__main__':
    generate_table()
