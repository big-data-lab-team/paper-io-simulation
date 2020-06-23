#!/usr/bin/env bash

set -e
set -u

function die(){
    echo $*
    exit 1
}

type inkscape &>/dev/null || die "Cannot find inkscape"
for i in figures/*.svg
do
    name=$(basename $i .svg)
    command="inkscape $i --export-pdf=figures/${name}.pdf"
    echo ${command} 
    ${command} || die "Failed"
done
