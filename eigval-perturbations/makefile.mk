exp     := eigval-perturbations
asset_1 := eigval-perturbations-vs-x.pdf
asset_2 := eigval-perturbations-vs-znd-lambda.pdf

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
