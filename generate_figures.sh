#!/usr/bin/env bash

set -e
set -u

function die(){
    echo $*
    exit 1
}

#General figures
type inkscape &>/dev/null || die "Cannot find inkscape"
for i in figures/*.svg
do
    name=$(basename $i .svg)
    command="inkscape $i -o figures/${name}.pdf"
    echo ${command} 
    ${command} || die "Failed"
done

# single-threaded exp figures
for i in result/single/figures/*.svg
do
    name=$(basename $i .svg)
    command="inkscape $i -o result/single/figures/${name}.pdf"
    echo ${command}
    ${command} || die "Failed"
done

# multi-threaded exp figures
for i in result/multi/*.svg
do
    name=$(basename $i .svg)
    command="inkscape $i -o result/single/multi/${name}.pdf"
    echo ${command}
    ${command} || die "Failed"
done
