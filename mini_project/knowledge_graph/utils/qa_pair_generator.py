#-*- coding:utf8 -*-
#!/usr/bin/python2.7

from optparse import OptionParser

import os, sys
reload(sys)

sys.setdefaultencoding('utf-8')

# set parser
parser = OptionParser(usage="%prog [options]", version="%prog 0.1")
parser.add_option("--triad_path", action="store", dest="triad_path")
parser.add_option("--template", action="store", dest="template")

def CheckRet(ret):
    if 0 == ret:
        return
    print "err return code %d" % ret
    exit(1)

def CheckOption(option, option_str):
    if option is None:
        print "Please specify %s with --%s option" % (option_str, option_str)
        parser.print_help()
    return 0


if __name__ == "__main__":

    (options, args) = parser.parse_args()
    if len(args) != 0:
        parser.print_help()
        sys.exit()

    # if there is no triad path, ask the user to specify it
    CheckRet(CheckOption(options.template, "template"))
    CheckRet(CheckOption(options.triad_path, "triad_path"))


    print "Step 1 Load Sentence Template from %s" % options.template

    print "Step 2 Load Triad Data from %s" % options.triad_path

    print "Generating training data"
