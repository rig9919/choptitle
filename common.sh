#! /bin/bash
VERSION="0.4"

list_iframes() {
    ffmpeg -i "$1" -vf select='eq(pict_type\,I)' -vsync 2 -f image2 "$tmp_path/%05d.bmp" -loglevel debug 2>&1 | awk '{ if ($10 == "pict_type:I" || $9 == "pict_type:I") print substr($6,3); fflush(stdout)}'
}

convertsecs() {
    h=$(echo "$1/3600" | bc)
    m=$(echo "scale=0; ($1%3600)/60" | bc)
    s=$(echo "scale=4; $1 - (($h*3600) + ($m*60))" | bc)
    printf "%02d:%02d:%f\n" $h $m $s
}

