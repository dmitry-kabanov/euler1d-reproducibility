# About

This is a reproducibility repository for paper "Linear stability of detonations
via numerical computation and dynamic mode decomposition" submitted to
*Physical Review Fluids* and authored by Dmitry Kabanov (me) and Aslan Kasimov.

To be able to run the scripts in this repository, you need to clone it:

    git clone --depth=1 git@github.com:dmitry-kabanov/euler1d-reproducibility.git

change current directory to the repository directory:

    cd euler1d-repository

and switch to branch `physical-review-fluids`:

    git checkout -b physical-review-fluids

Besides, you need Python along with several scientific libraries, such as
NumPy, SciPy, and Matplotlib.
We recommend to use Anaconda Python distribution 4.2 to achieve this, as we
used it for development.
It can be downloaded from `https://repo.continuum.io/archive/`.
Alternatively, you can get Python and the libraries from other places.
In this case, you need Python 3.5, NumPy 1.11, SciPy 0.18, and Matplotlib
1.5.3.

This repository was developed under Ubuntu 16.04 and should work under other
flavors of Unix without any modification (macOS, Centos, Fedora, and so on).
Using this repository under Windows operating system may or may not work as it
depends on `make` utility.

To generate assets (figures and LaTeX tables), use

    make BUILD_DIR=<path to directory for generated assets>

where `<path to directory for generated assets>` must exist before running the
command.
For example:

    mkdir _build
    make BUILD_DIR=_build

will create `_build` directory inside the repository and generate the assets
inside that directory.
