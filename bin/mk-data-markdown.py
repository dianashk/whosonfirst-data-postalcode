#!/usr/bin/env python

import os
import sys
import logging

import csv
import json

import datetime

import mapzen.whosonfirst.utils

if __name__ == '__main__':

    import optparse
    opt_parser = optparse.OptionParser()

    opt_parser.add_option('-d', '--data', dest='data', action='store', default=None, help='The path to your data.json file')
    opt_parser.add_option('-o', '--out', dest='out', action='store', default=None, help='Where to write data (default is STDOUT)')

    opt_parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Be chatty (default is false)')
    options, args = opt_parser.parse_args()

    if options.verbose:	
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    whoami = sys.argv[0]
    whoami = os.path.abspath(whoami)

    bin = os.path.dirname(whoami)
    parent = os.path.dirname(bin)
    parent = os.path.basename(parent)

    data = os.path.abspath(options.data)
    fh = open(data, 'r')

    data = json.load(fh)
    codes = {}

    for details in data:
        name = details['name']
        parts = name.split('-')
        region = " ".join(parts[3:])
        codes[region] = details

    regions = codes.keys()
    regions.sort()

    fh = sys.stdout

    if options.out:
        out = os.path.abspath(options.out)
        fh = open(out, 'w')

    fh.write("# %s stats\n\n" % parent)

    dt = datetime.date.today()
    ymd = dt

    fh.write("_This file was generated by robots on %s, derived from the [data.json](data.json) file_\n\n" % (ymd))

    for code in regions:

        details = codes[code]
        count = details['count']
        count = int(count)

        fh.write("## %s\n\n" % details['description'])
        
        fh.write("* %s\n" % details['url'])

        if count == 0:
            fh.write("* _0 postal codes_\n")
        elif count == 1:
            fh.write("* one postal code\n")
        else:
            count = "{:,}".format(details['count'])
            fh.write("* %s postal codes\n" % count)

        fh.write("\n")
