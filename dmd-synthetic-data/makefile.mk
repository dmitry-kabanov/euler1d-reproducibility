exp    := dmd-synthetic-data
asset  := dmd-synthetic-data.tex
script := generate-dmd-synthetic-data-table.py
asset_2  := dmd-synthetic-data-spectrum.pdf

assets_list += ${exp}/_assets/${asset}
assets_list += ${exp}/_assets/${asset_2}

${exp} : ${BUILD_DIR}/${asset}
${exp} : ${BUILD_DIR}/${asset_2}

${BUILD_DIR}/${asset} : ${exp}/_assets/${asset}
	cp $< $@

${BUILD_DIR}/${asset_2} : ${exp}/_assets/${asset_2}
	cp $< $@

${exp}/_assets/${asset} : ${exp}/${script}
	@# OMP_NUM_THREADS=1 forces serial linear algebra.
	@# Redirection to /dev/null is used to avoid script's output.
	cd ${<D} && OMP_NUM_THREADS=1 python ${<F} > /dev/null

${exp}/_assets/${asset_2} : ${exp}/${script}
	@# OMP_NUM_THREADS=1 forces serial linear algebra.
	@# Redirection to /dev/null is used to avoid script's output.
	@# Argument 1 tells the script to generate amplitude-spectrum figure.
	cd ${<D} && OMP_NUM_THREADS=1 python ${<F} 1 > /dev/null

${exp}/${script} : helpers.py
