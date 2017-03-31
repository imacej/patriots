# -*- coding: utf-8 -*-

import os, sys, codecs, json, re
from bookinfo import *

bookroot = 'data/doubook/'

books = os.listdir(bookroot)
count = 0


for book in books:
    if book[0] == '.':
        continue
    count = count + 1
    print book
    text = file(bookroot + book,'rU').read()
    bi = BookInfo()
    lines = text.split('\n')

    for line in lines:
        bi.addinfo(line)

    bi.description()

print 'Total ' + str(count) + ' books'
