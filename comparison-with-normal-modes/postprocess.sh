#!/usr/bin/env bash

for i in _output/**; do
    for j in ${i}/*; do
        saf postprocess --save ${j}
    done
done
