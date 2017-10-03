exp    := raw-data
asset  := raw-data-examples.pdf
script := plot-time-series.py
data   := $(wildcard ${exp}/_output/*/detonation-velocity.txt)

assets_list += ${exp}/_assets/${asset}

${exp} : ${BUILD_DIR}/${asset}

${BUILD_DIR}/${asset} : ${exp}/_assets/${asset}
	cp $< $@

${exp}/_assets/${asset} : ${exp}/${script} ${exp}/lib_helpers.py \
                          ${data} ${matplotlibrc_file}
	cd ${<D} && python ${<F}
