#! /bin/bash
VERSION="0.4"

list_iframes() {
	i=1
    ffmpeg -i "$1" -to $3 -vf select='eq(pict_type\,I)' -vsync 2 -f image2 "$2/%05d.bmp" -loglevel debug 2>&1 | awk '{ if ($10 == "pict_type:I" || $9 == "pict_type:I") print substr($6,3); fflush(stdout)}' | while read timestamp; do
		printf "%05d:%s\n" $i $timestamp
		let i=i+1
	done
}

convertsecs() {
    h=$(echo "$1/3600" | bc)
    m=$(echo "scale=0; ($1%3600)/60" | bc)
    s=$(echo "scale=4; $1 - (($h*3600) + ($m*60))" | bc)
    printf "%02d:%02d:%f\n" $h $m $s
}

