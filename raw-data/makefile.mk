exp      := raw-data
asset_1  := raw-data-examples.pdf
script_1 := ${exp}/plot-time-series.py
data_1   := $(wildcard ${exp}/_output/*/detonation-velocity.txt)
asset_2  := raw-data-modes.tex
script_2 := ${exp}/generate-latex-table.py
data_2   := $(wildcard ${exp}/_output/*/n12=0640/stability.txt)
date_2   += $(wildcard ${exp}/_output/*/n12=1280/stability.txt)

assets_list += ${exp}/_assets/${asset_1}
assets_list += ${exp}/_assets/${asset_2}

${exp} : ${BUILD_DIR}/${asset_1}

${exp} : ${BUILD_DIR}/${asset_2}

${BUILD_DIR}/${asset_1} : ${exp}/_assets/${asset_1}
	cp $< $@

${exp}/_assets/${asset_1} : ${script_1} ${data_1} ${matplotlibrc_file}
	cd ${<D} && python ${<F}

${script_1} : ${exp}/lib_helpers.py

${BUILD_DIR}/${asset_2} : ${exp}/_assets/${asset_2}
	cp $< $@

${exp}/_assets/${asset_2} : ${script_2} ${data_2}
	cd ${<D} && python ${<F} $(@F)

${script_2} : ${exp}/lib_helpers.py
	touch $@
