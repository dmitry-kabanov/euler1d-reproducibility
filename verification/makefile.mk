exp    := verification
asset  := verification.tex
script := generate-verification-table.py
data   := $(wildcard ${exp}/_output/*/detonation-velocity.txt)

assets_list += ${exp}/_assets/${asset}

${exp} : ${BUILD_DIR}/${asset}

${BUILD_DIR}/${asset} : ${exp}/_assets/${asset}
	cp $< $@

${exp}/_assets/${asset} : ${exp}/${script} ${data} ${matplotlibrc_file}
	cd ${<D} && python ${<F}
