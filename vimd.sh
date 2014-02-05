#!/bin/bash

md=$1

if [ -z "$md" ]; then
    echo "You must supply a filename" >&2
    exit
fi

html=$(mktemp --suffix=.html)

markdown $md > $html

python2.7 vimd.py $md $html

rm $html
