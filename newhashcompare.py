#!/usr/bin/env python
import sys
import os
import math
import operator
import argparse
import subprocess
import Image
phash_dir="/home/kyle/src/choptitle/py-phash/build/lib.linux-x86_64-2.7/pHash.so"
path, filename = os.path.split(phash_dir)
filename, ext = os.path.splitext(filename)
sys.path.append(path)
module = __import__(filename)
reload(module)

import pHash
def compare(file1, file2):
    # <hamming distance of image vs its negative> = 62
    max_phash = 62
    hash1 = pHash.imagehash(file1)
    hash2 = pHash.imagehash(file2)
    return pHash.hamming_distance(hash1, hash2)/62.0*100
    #return pHash.hamming_distance(hash1, hash2)

def radial_compare(file1, file2):
    digest1 = pHash.image_digest(file1)
    digest2 = pHash.image_digest(file2)
    cc = pHash.crosscorr(digest1, digest2)[1]
    if cc == cc:
        return int(round(cc * -100))
    else:
        return 0

def hist_compare(file1, file2):
    # <rms of white canvas vs black canvas> / <size of canvas> = ~0.0884
    max_rms_per_pixel = 183282.0/(1920*1080)
    im = Image.open(file1)
    h1 = im.histogram()
    h2 = Image.open(file2).resize(im.size, Image.ANTIALIAS).histogram()
    max_rms = im.size[0] * im.size[1] * max_rms_per_pixel
    rms = math.sqrt(reduce(operator.add, map(lambda a,b: (a-b)**2, h1, h2))/len(h1))
    return float(rms/max_rms) * 100
    #return int(round(rms))

def init_parser():
    parser = argparse.ArgumentParser(prog='hashcompare', add_help=False,
               usage='%(prog)s [lm] -s screen videos...',
               description='Compare screen with I-frames of videos')
    parser.add_argument('videos', type=str, nargs='+')
    required_args = parser.add_argument_group('requirements',
               'at least one is required')
    required_args.add_argument('-s', '--screen', action='append')
    optional_args = parser.add_argument_group('options',
               'optional')
    optional_args.add_argument('-l', '--limit', default=200, type=int)
    optional_args.add_argument('-m', '--method', default='hh')
    optional_args.add_argument('-d', '--temporary-dir', default='/var/tmp/findscreen')
    args = parser.parse_args()
    return args

if __name__=='__main__':
    args = init_parser()
    if not args.videos:
        print 'Must specifiy at least one video'
        exit()

    if not args.screen:
        print 'Must specify at least one screen'
        exit()

    toc = []
    for screen in args.screen:
        for video in args.videos:
            output = subprocess.check_output("source ./common.sh; list_iframes " + video.replace(" ", "\ ") + " " + args.temporary_dir.replace(" ", "\ ") + " " + str(args.limit), shell=True, executable="/bin/bash")
            if not output:
                print 'error detecting i-frames'
                exit()
            for line in output.split('\n'):
                if line:
                    iframe, timestamp = line.split(':')
                    iframe_path = args.temporary_dir + '/' + str(iframe) + '.bmp'
                    if not os.path.exists(iframe_path):
                        break
                    ph = compare(screen, iframe_path)
                    hist = hist_compare(screen, iframe_path)
                    toc.append([screen, video, iframe, timestamp, ph, hist])
            #print f, '(hash):', ph
            #print f, '(hist):', hist
            #print f, '(hh):', ph+hist
            #sys.stdout.write(str(hist) + ',')

    #print compare(file1, file2)
    f_sum_of_squares = lambda x, y: x+y**2
    _, _, _, _, ph_list, hist_list = zip(*toc)
    ph_sqrt_sos = math.sqrt(reduce(f_sum_of_squares, ph_list[1:], ph_list[0]**2))
    hist_sqrt_sos = math.sqrt(reduce(f_sum_of_squares, hist_list[1:], hist_list[0]**2))
    # normalize the phash and histogram values
    for item in toc:
        item[4] /= ph_sqrt_sos
        item[5] /= hist_sqrt_sos
        item.append(item[4] + item[5])

    # display
    splitted_toc = []
    # get set that lists the unique videos in toc
    uniq_v_set=set(zip(*toc)[1])
    # splitted_toc seperates the data by video 
    for uniq_v in uniq_v_set:
        splitted_toc.append(filter(lambda x: x[1]==uniq_v, toc))
    # sep_toc is a list that contains lists of data from a single video
    for sep_toc in sorted(splitted_toc):
        sorted_toc = sorted(sep_toc, key=operator.itemgetter(6))
        print '%s:%05d:%s:%s:%06d' % ( sorted_toc[0][1], int(sorted_toc[0][2]), sorted_toc[0][3], 'hh', sorted_toc[0][6]*100000)
    
    #sorted_toc = sorted(toc, key=operator.itemgetter(6))
    #print sorted_toc
    #print '%s:%05d:%s:%s:%06d' % ( sorted_toc[0][1], int(sorted_toc[0][2]), sorted_toc[0][3], 'hh', sorted_toc[0][6]*100000)
    #for s, v, i, t, ph, hist, hh in sorted(toc, key=operator.itemgetter(6)):
    #    print '%s:%05d:%s:%s:%06d' % ( v, int(i), t, 'hh', hh*100000)
    #    print '%s:%05d:%s:%s:%06d' % ( v, int(i), t, 'hash', ph*100000)
    #    print '%s:%05d:%s:%s:%06d' % ( v, int(i), t, 'hist', hist*100000)
