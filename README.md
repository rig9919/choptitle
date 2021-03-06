choptitle
=========

The choptitle suite of scripts is used to assist in the removal of television
show openings. It consists of 3 end-user scripts.

prerequisites
-------------
ffmpeg  
mkvtoolnix  
pHash

findscreen
----------
Used to search a video or group of videos for a certain screen(s). The output
can be read as follows:

    <video path>:<iframe number>:<timestamp>:hh:<hamming_dist+histogram_diff>
    <video path>:<iframe number>:<timestamp>:hist:<histogram_diff>
    <video path>:<iframe number>:<timestamp>:hash:<hamming_dist>

Hamming distance is derived from the differences in the perceptual hashes of
the screen and the iframe. A perceptual hash is a representation of the
signature of an image. If two images look similar to each other, they will
likely have a lower hamming distance than two different looking images. It is
more useful on shows with title sequences that are more likely to begin
directly on an iframe.  

Histogram difference is the difference between the colors of the screen and the
iframe. It is more useful on shows with title sequences that do not begin
directly on an iframe.  

Both measurements are normalized and added together to become hh which is just
shorthand for hamming+histogram.  __The hh measurement should be the most
accurate one to use for determining whether a screen and iframe match__.

takeshot
--------
Mostly useless now that choptitle has the --preview option.

choptitle
---------
Reads output generated by findscreen and creates a new video in the current
directory with the segment removed.

example usage
-------------

    findscreen -l 400 -s season1-title1.bmp -s season1-title2.bmp /path/to/video-s01e*.mkv >seas1times.txt
    grep hh seas1times.txt | choptitle -o -3 40

notes and bugs
--------------
* These tools are made specifically for my setup and as such currently only deal
with videos in the matroska container.
* They are very dependent on iframes so videos with fewer iframes will have less
accurate cut points.
* Results from findscreen may be off by 1 iframe on consecutive runs with nothing
changed. Not sure why.
