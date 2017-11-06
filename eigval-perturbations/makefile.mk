exp      := eigval-perturbations
asset_1  := eigval-perturbations-sub-super.pdf
script_1 := ${exp}/plot-subsonic-supersonic.py
data_1   := _output/subsonic-supersonic/*
asset_2  := eigval-perturbations-sub-sub.pdf
script_2 := ${exp}/plot-subsonic-subsonic.py
data_2   := _output/subsonic-subersonic/*

assets_list += ${exp}/_assets/${asset_1}
assets_list += ${exp}/_assets/${asset_2}

${exp} : ${BUILD_DIR}/${asset_1}

${exp} : ${BUILD_DIR}/${asset_2}

${BUILD_DIR}/${asset_1} : ${exp}/_assets/${asset_1}
	cp $< $@

${BUILD_DIR}/${asset_2} : ${exp}/_assets/${asset_2}
	cp $< $@

${exp}/_assets/${asset_1} : ${script_1} 
	cd ${<D} && python ${<F}

${exp}/_assets/${asset_2} : ${script_2}
	cd ${<D} && python ${<F}

${exp}/${script_1} : $(addprefix ${exp}/, ${data_1}) ${matplotlibrc_file}

${exp}/${script_2} : $(addprefix ${exp}/, ${data_2}) ${matplotlibrc_file}
