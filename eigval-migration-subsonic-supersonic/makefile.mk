exp    := eigval-migration-subsonic-supersonic
asset  := eigval-re-alpha-vs-q_2.pdf
script := plot.py
data   := ${exp}/_output/*/stability.txt

assets_list += ${exp}/_assets/${asset}

${exp} : ${BUILD_DIR}/${asset}

${BUILD_DIR}/${asset} : ${exp}/_assets/${asset}
	cp $< $@

${exp}/_assets/${asset} : ${exp}/${script} ${data} ${matplotlibrc_file}
	cd ${<D} && python ${<F} > _assets/info.txt
