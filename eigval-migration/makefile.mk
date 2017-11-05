exp      := eigval-migration

asset_1  := eigval-re-alpha-vs-q_2-sub-super.pdf
script_1 := plot-subsonic-supersonic-case.py
data_1   := _output/subsonic-supersonic.tar.gz

asset_2  := eigval-re-alpha-vs-q_2-together.pdf
script_2 := plot-spectra-together.py
data_2   := _output/subsonic-supersonic.tar.gz \
            _output/subsonic-subsonic.tar.gz

assets_list += ${exp}/_assets/${asset_1}

${exp} : ${BUILD_DIR}/${asset_1}

${BUILD_DIR}/${asset_1} : ${exp}/_assets/${asset_1}
	cp $< $@

${exp}/_assets/${asset_1} : ${exp}/${script_1} $(addprefix ${exp}/, ${data_1}) ${matplotlibrc_file}
	cd ${<D} && python ${<F}

${exp}/${script_1} : ${exp}/lib_postprocessing.py

assets_list += ${exp}/_assets/${asset_2}

${exp} : ${BUILD_DIR}/${asset_2}

${BUILD_DIR}/${asset_2} : ${exp}/_assets/${asset_2}
	cp $< $@

${exp}/_assets/${asset_2} : ${exp}/${script_2} $(addprefix ${exp}/, ${data_2}) ${matplotlibrc_file}
	cd ${<D} && python ${<F}

${exp}/${script_2} : ${exp}/lib_postprocessing.py
