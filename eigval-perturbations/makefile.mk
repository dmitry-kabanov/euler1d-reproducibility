exp     := eigval-perturbations
asset_1 := eigval-perturbations.pdf
asset_2 := eigval-perturbations-vs-znd-lambda.pdf

script := ${exp}/plot.py
data   := $(wildcard ${exp}/_output/*)

assets_list += ${exp}/_assets/${asset_1}
assets_list += ${exp}/_assets/${asset_2}

${exp} : ${BUILD_DIR}/${asset_1} ${BUILD_DIR}/${asset_2}

${BUILD_DIR}/${asset_1} : ${exp}/_assets/${asset_1}
	cp $< $@

${BUILD_DIR}/${asset_2} : ${exp}/_assets/${asset_2}
	cp $< $@

${exp}/_assets/${asset_1} : ${script} ${data} ${matplotlibrc_file}
	cd ${<D} && python ${<F} 'vs_x'

${exp}/_assets/${asset_2} : ${script} ${data} ${matplotlibrc_file}
	cd ${<D} && python ${<F}
