#! /bin/bash
VERSION="0.3"

convertsecs() {
    h=$(echo "$1/3600" | bc)
    m=$(echo "scale=0; ($1%3600)/60" | bc)
    s=$(echo "scale=4; $1 - (($h*3600) + ($m*60))" | bc)
    printf "%02d:%02d:%f\n" $h $m $s
}

