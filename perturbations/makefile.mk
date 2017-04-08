exp     := perturbations
asset_1 := perturbation-profiles-vs-x-grouped-by-Q.pdf
asset_2 := perturbation-profiles-vs-znd-lambda-grouped-by-Q.pdf

script := generate.py
data   := $(wildcard ${exp}/_output/*)

assets_list += ${exp}/_assets/${asset_1}
assets_list += ${exp}/_assets/${asset_2}

${exp} : ${BUILD_DIR}/${asset_1} ${BUILD_DIR}/${asset_2}


${BUILD_DIR}/${asset_1} : ${exp}/_assets/${asset_1}
	cp $< $@

${BUILD_DIR}/${asset_2} : ${exp}/_assets/${asset_2}
	cp $< $@

${exp}/_assets/${asset_1} : ${exp}/${script} ${data} ${matplotlibrc_file}
	cd ${<D} && python ${<F} 'vs_x'

${exp}/_assets/${asset_2} : ${exp}/${script} ${data} ${matplotlibrc_file}
	cd ${<D} && python ${<F}
