# From http://clarkgrubb.com/makefile-style-guide#prologue
MAKEFLAGS     += --warn-undefined-variables
SHELL         := bash
.SHELLFLAGS   := -eu -o pipefail
.DEFAULT_GOAL := all

.DELETE_ON_ERROR :

.SUFFIXES :
