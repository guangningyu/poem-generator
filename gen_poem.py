#!/usr/bin/env python
# -*- coding: utf8 -*-

#----------Set Environment----------#

import os
import sys
import re
import collections
import pickle

reload(sys)
sys.setdefaultencoding('utf-8')

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

POEM = THIS_DIR + '/' + 'complete_tang_poems.txt'

#----------Functions----------#

def displayUnicode(char):
    # e.g. char = u'】'
    encoded = char.encode('utf-8')
    print 'The input char is \"%s\"' % encoded
    print 'The unicode is %s'        % repr(encoded)

def isTitle(line):

    if(line.find(u'】') >= 0):
        return True
    else:
        return False

def isVerse(line):

    if(line.find(u'，') >= 0):
        return True
    else:
        return False

def readPoems(poem_file):

    in_file = open(poem_file, 'r')

    poem_list = []
    poem = {}

    for line in in_file.readlines():

        line = line.decode('utf-8').strip()

        if(isTitle(line)):

            # add the previous poem into the list
            if(len(poem) > 0):
                poem_list.append(poem)

            # create a new poem
            poem = {}
            header_list = re.split(u'【|】', line)
            poem['title'] = header_list[-2]
            poem['author'] = header_list[-1]
            poem['verse'] = []

        elif(isVerse(line)):
            verse_list = re.split(u'，|。', line)
            for verse in verse_list:
                if verse != u'':
                    poem['verse'].append(verse)

    poem_list.append(poem)

    in_file.close()

    return poem_list

def histPoemNum(poem_list):

    poet_list = []

    for poem in poem_list:
        poet_list.append(poem['author'])

    return collections.Counter(poet_list).most_common()

def enumWords(verse):

    list = []
    l = len(verse)

    for pos in range(l):
        for step in range(l):
            if step > 0 and pos+step+1 <= l:
                list.append(verse[pos:pos+step+1])
    return list

def histWordFrequency(poem_list, author=""):
    if(author != ""):
        sub_poem_list = [poem for poem in poem_list if poem['author'] == author]
    else:
        sub_poem_list = poem_list

    words_list = []
    for poem in sub_poem_list:
        for verse in poem['verse']:
            words_list = words_list + enumWords(verse)

    return collections.Counter(words_list).most_common()

#----------Main----------#

# 1. read all the poems into a list
poem_list = readPoems(POEM)

# 2. histogram of number of poems per poet
poet_counter = histPoemNum(poem_list)

# 3. histogram of the frequency of each word for all the poets
word_counter = histWordFrequency(poem_list)
word_counter_pkl = open(THIS_DIR + '/' + 'word_counter.pkl', 'wb')
pickle.dump(word_counter, word_counter_pkl)
word_counter_pkl.close()

