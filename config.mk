# From http://clarkgrubb.com/makefile-style-guide#prologue
MAKEFLAGS     += --warn-undefined-variables
# Next two lines are commented out because somehow now $(shell ...)
# function works, as bash fails with `No such file or directory` error.
# SHELL         := bash
# .SHELLFLAGS   := -eu -o pipefail
.DEFAULT_GOAL := all

.DELETE_ON_ERROR :

.SUFFIXES :
