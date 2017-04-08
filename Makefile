# Main Makefile for the repository of computational experiments
# based on euler1d code.
 
# Check that BUILD_DIR is given by a user as a command-line argument.
ifndef BUILD_DIR
$(error 'BUILD_DIR is not set. USAGE: make BUILD_DIR=<dirname>.')
endif

# List of all numerical experiments.
experiments := znd-solutions \
               dmd-synthetic-data \
               perturbations

# Set PYTHONPATH to be able to use the solver's code and helpers.
export PYTHONPATH := ../code:..

# Set SAVE_FIGURES such that the figures are saved.
export SAVE_FIGURES := 1

# Used by matplotlib to determine parameters for plotting.
export MATPLOTLIBRC := ${CURDIR}/

# Used as a dependency for scripts that generate figures.
export matplotlibrc_file := ${MATPLOTLIBRC}/matplotlibrc

RM := rm -f

# List of assets.
assets_list :=


.PHONY : all ${experiments}

all : ${experiments} | ${BUILD_DIR}

${BUILD_DIR} :
	mkdir -p $@

.PHONY : clean
clean :
	${RM} ${assets_list}

include znd-solutions/makefile.mk
include dmd-synthetic-data/makefile.mk
include perturbations/makefile.mk
