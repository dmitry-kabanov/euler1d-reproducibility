exp    := eigval-neutral-curve
asset  := eigval-neutral-curve-gamma=1.2.pdf
script := plot-neutral-curve.py
data   := ${exp}/_output/results-gamma=1.2.txt

assets_list += ${exp}/_assets/${asset}

${exp} : ${BUILD_DIR}/${asset}

${BUILD_DIR}/${asset} : ${exp}/_assets/${asset}
	cp $< $@

${exp}/_assets/${asset} : ${exp}/${script} ${data} ${matplotlibrc_file}
	cd ${<D} && python ${<F} --save
