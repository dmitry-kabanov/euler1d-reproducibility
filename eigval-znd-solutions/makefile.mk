exp       := eigval-znd-solutions
asset_1   := eigval-znd-solutions-subsonic-supersonic.pdf
script_1  := plot-znd-solutions-subsonic-supersonic.py
data_1    := ${exp}/_output/subsonic-supersonic/*/detonation-velocity.txt
asset_2   := eigval-znd-solutions-subsonic-subsonic.pdf
script_2  := plot-znd-solutions-subsonic-subsonic.py
data_2    := ${exp}/_output/subsonic-subsonic/*/detonation-velocity.txt

assets_list += ${exp}/_assets/${asset_1}

${exp} : ${BUILD_DIR}/${asset_1}

${exp} : ${BUILD_DIR}/${asset_2}

${BUILD_DIR}/${asset_1} : ${exp}/_assets/${asset_1}
	cp $< $@

${BUILD_DIR}/${asset_2} : ${exp}/_assets/${asset_2}
	cp $< $@

${exp}/_assets/${asset_1} : ${exp}/${script_1} ${data_1} ${matplotlibrc_file}
	cd ${<D} && python ${<F}

${exp}/_assets/${asset_2} : ${exp}/${script_2} ${data_2} ${matplotlibrc_file}
	cd ${<D} && python ${<F}

${exp}/${script_1} : ${exp}/lib_eigval_znd_solutions.py

${exp}/${script_2} : ${exp}/lib_eigval_znd_solutions.py
