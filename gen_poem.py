#!/usr/bin/env python
# -*- coding: utf8 -*-

#----------Set Environment----------#

import os
import sys
import re
import collections

reload(sys)
sys.setdefaultencoding('utf-8')

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
POEM = THIS_DIR + '/' + 'complete_tang_poems.txt'

#----------Functions----------#

def readPoems(poem_file):

    in_file = open(poem_file, 'r')

    poem_list = []
    poem = {}

    for line in in_file.readlines():

        line = line.decode('utf-8').strip()

        if(line.find(u'】') >= 0):
            # This line contains the title
            if len(poem)>0:
                poem_list.append(poem)

            poem = {}
            header_list = re.split(u'【|】', line)
            poem['title'] = header_list[-2]
            poem['author'] = header_list[-1]
            poem['verse'] = []

        elif(line.find(u'，') >= 0):
            # This line contains the verse
            verse_list = re.split(u'，|。', line)
            for verse in verse_list:
                if verse != u'':
                    poem['verse'].append(verse)

    poem_list.append(poem)

    in_file.close()

    return poem_list

def enumVerse(verse):
    list = []
    l = len(verse)
    for pos in range(l):
        for step in range(l):
            if step > 0 and pos+step+1 <= l:
                list.append(verse[pos:pos+step+1])
    return list

#----------Main----------#

# # Display the unicode
# s = u'】'
# encoded = s.encode('utf-8')
# print encoded
# print repr(encoded)

poem_list = readPoems(POEM)

verse_list = []
for poem in poem_list:
    for verse in poem['verse']:
        verse_list = verse_list + enumVerse(verse)

hist = collections.Counter(verse_list).most_common(10000)

for i in hist:
    print i[0], i[1]

