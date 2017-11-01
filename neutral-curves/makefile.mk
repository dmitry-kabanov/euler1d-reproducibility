exp      := neutral-curves
asset_1  := LeeStewart-comparison.pdf
script_1 := ${exp}/plot-leestewart-comparison.py
data_1   := ${exp}/_output/results-gamma=1.2.txt \
            ${exp}/_output/lee-stewart-fig7-digitized-data.txt

assets_list += ${exp}/_assets/${asset_1}

${exp} : ${BUILD_DIR}/${asset_1}

${BUILD_DIR}/${asset_1} : ${exp}/_assets/${asset_1}
	cp $< $@

${exp}/_assets/${asset_1} : ${script_1} ${data_1} ${matplotlibrc_file}
	cd ${<D} && python ${<F}
