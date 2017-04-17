exp    := comparison-with-normal-modes
asset  := comparison-with-normal-modes.tex
script := generate-latex-table.py
data   := $(wildcard ${exp}/_output/*/stability.txt)

assets_list += ${exp}/_assets/${asset}

${exp} : ${BUILD_DIR}/${asset}

${BUILD_DIR}/${asset} : ${exp}/_assets/${asset}
	cp $< $@

${exp}/_assets/${asset} : ${exp}/${script} ${data} ${matplotlibrc_file}
	cd ${<D} && python ${<F} --save
