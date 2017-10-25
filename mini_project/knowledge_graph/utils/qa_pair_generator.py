#-*- coding:utf8 -*-
#!/usr/bin/python2.7

from optparse import OptionParser

import os, sys
reload(sys)

sys.setdefaultencoding('utf-8')


if __name__ == "__main__":
    parser = OptionParser(usage="%prog [options]", version="%prog 0.1")
    parser.add_option("--triad_file", action="store", dest="triad_file")

    (options, args) = parser.parse_args()
    if len(args) != 0:
        parser.print_help()
        sys.exit()

    print "under construction"
