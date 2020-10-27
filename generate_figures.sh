#!/usr/bin/env bash

set -e
set -u

function die(){
    echo $*
    exit 1
}
type inkscape &>/dev/null || die "Cannot find inkscape"
for folder in figures result/single/figures result/multi/figures
do
    for i in $folder/*.svg
    do
        name=$(basename $i .svg)
        command="inkscape $i -o ${folder}/${name}.pdf"
        echo ${command}
        ${command} || die "Failed"
    done
done
