exp    := dmd-synthetic-data
asset  := dmd-synthetic-data.tex
script := generate-dmd-synthetic-data-table.py

assets_list += ${exp}/_assets/${asset}

${exp} : ${BUILD_DIR}/${asset}

${BUILD_DIR}/${asset} : ${exp}/_assets/${asset}
	cp $< $@

${exp}/_assets/${asset} : ${exp}/${script}
	@# OMP_NUM_THREADS=1 forces serial linear algebra.
	@# Redirection to /dev/null is used to avoid script's output.
	cd ${<D} && OMP_NUM_THREADS=1 python ${<F} > /dev/null
