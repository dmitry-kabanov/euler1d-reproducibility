exp    := eigval-thermicity
asset  := eigval-thermicity.pdf
script := plot-thermicity.py
data   := _output/eigval-q=10.txt _output/simple-q=10.txt

assets_list += ${exp}/_assets/${asset}

${exp} : ${BUILD_DIR}/${asset}

${BUILD_DIR}/${asset} : ${exp}/_assets/${asset}
	cp $< $@

${exp}/_assets/${asset} : ${exp}/${script}
	cd ${<D} && python ${<F}

${exp}/${script} : $(addprefix ${exp}/, ${data})
