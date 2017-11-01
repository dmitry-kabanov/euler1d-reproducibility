exp      := neutral-curves
asset_1  := LeeStewart-comparison.pdf
script_1 := ${exp}/plot-leestewart-comparison.py
data_1   := ${exp}/_output/results-gamma=1.2.txt \
            ${exp}/_output/lee-stewart-fig7-digitized-data.txt
asset_2  := neutral-stability.pdf
script_2 := ${exp}/plot-neutral-curves-var-gamma.py
data_2   := ${exp}/_output/results-gamma=1.1.txt \
            ${exp}/_output/results-gamma=1.2.txt \
            ${exp}/_output/results-gamma=1.3.txt \
            ${exp}/_output/results-gamma=1.4.txt
asset_3  := neutral-stability-gamma=1.1-two-modes.pdf
script_3 := ${exp}/plot-curves-gamma\=1.1-two-modes.py
data_3   := ${exp}/_output/results-gamma=1.1.txt \
            ${exp}/_output/results-gamma=1.1-mode=1.txt

assets_list += ${exp}/_assets/${asset_1}
assets_list += ${exp}/_assets/${asset_2}
assets_list += ${exp}/_assets/${asset_3}

${exp} : ${BUILD_DIR}/${asset_1}

${exp} : ${BUILD_DIR}/${asset_2}

${exp} : ${BUILD_DIR}/${asset_3}

${BUILD_DIR}/${asset_1} : ${exp}/_assets/${asset_1}
	cp $< $@

${exp}/_assets/${asset_1} : ${script_1} ${data_1} ${matplotlibrc_file}
	cd ${<D} && python ${<F}

${BUILD_DIR}/${asset_2} : ${exp}/_assets/${asset_2}
	cp $< $@

${exp}/_assets/${asset_2} : ${script_2} ${data_2} ${matplotlibrc_file}
	cd ${<D} && python ${<F}

${BUILD_DIR}/${asset_3} : ${exp}/_assets/${asset_3}
	cp $< $@

${exp}/_assets/${asset_3} : ${script_3} ${data_3} ${matplotlibrc_file}
	cd ${<D} && python ${<F}
