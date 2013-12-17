choptitle
=========

prerequisites
-------------
ffmpeg  
mkvtoolnix  
pHash

The choptitle suite of scripts is used to assist in the removal of television
show openings. It consists of 3 end-user scripts.

findscreen
----------
Used to search a video or group of videos for a certain screen. The output can
be read as follows:

    <video path>:<iframe number>:<timestamp>:<hamming distance>

takeshot
--------
Mostly useless now that choptitle has the --preview option.

choptitle
---------
Reads output generated by findscreen and creates a new video in the current
directory with the segment removed.

notes and bugs
--------------
These are made specifically for my setup and as such currently only deal with
videos in the matroska container.
