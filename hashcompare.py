#!/usr/bin/env python
import sys
import os
import math
import operator
import Image
phash_dir="/home/kyle/src/choptitle/py-phash/build/lib.linux-x86_64-2.7/pHash.so"
path, filename = os.path.split(phash_dir)
filename, ext = os.path.splitext(filename)
sys.path.append(path)
module = __import__(filename)
reload(module)

import pHash
def compare(file1, file2):
    hash1 = pHash.imagehash(file1)
    hash2 = pHash.imagehash(file2)
    return pHash.hamming_distance(hash1, hash2)

def radial_compare(file1, file2):
    digest1 = pHash.image_digest(file1)
    digest2 = pHash.image_digest(file2)
    cc = pHash.crosscorr(digest1, digest2)[1]
    if cc == cc:
        return int(round(cc * -100))
    else:
        return 0

def hist_compare(file1, file2):
    im = Image.open(file1)
    h1 = im.histogram()
    h2 = Image.open(file2).resize(im.size, Image.ANTIALIAS).histogram()
    rms = math.sqrt(reduce(operator.add, map(lambda a,b: (a-b)**2, h1, h2))/len(h1))
    return int(round(rms))

if __name__=='__main__':
    import sys
    file1 = sys.argv[1]
    for f in sys.argv[2:]:
        print f + ' (hash): ' + str(compare(file1, f))
        print f + ' (digest): ' + str(radial_compare(file1, f))
        print f + ' (hist): ' + str(hist_compare(file1, f))
    #print compare(file1, file2)
