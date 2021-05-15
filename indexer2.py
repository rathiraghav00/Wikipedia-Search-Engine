#!/usr/bin/python
# -*- coding: utf-8 -*-
import heapq
import math
from heapq import heappush as push, heappop as pop
from collections import *
import os

tags = ['title', 'category', 'infobox', 'text']

# doc_no is not equal to pages!!!

total_pages = 360986


# probably same as doc no

def writeit(tag, data):
    offset_file_path = 'offsets/' + str(tag) + '.txt'
    offsets_file = open(offset_file_path, 'a')
    score_file_path = 'score/' + str(tag) + '.txt'
    score_file = open(score_file_path, 'a')
    offset = 0
    for key in sorted(data):
        values = data[key]
        idf = 0
        if len(values) > 0:
            idf = math.log10(float(total_pages) / float(len(values)))
        curr = str(key) + ' '
        for x in values:

            s = x.split(':')
            doc = s[0]
            cnt = s[1]

            # Check why we add a +1
            # Probably wrong

            tfidf = (1 + math.log10(float(cnt))) * idf

            tfidf = '%.2f' % tfidf

            curr += str(doc) + ':' + str(tfidf) + ' '

        offsets_file.write(str(key) + ':' + str(offset) + '\n')

        # 2 for ":" and "\n"

        offset += 2 + len(curr)

        score_file.write(str(curr))
        score_file.write('\n')


for tag in tags:
    all_files = {}
    first_lines = {}
    path = 'final/' + str(tag)

    all_words = defaultdict(list)
    heap = []
    data = defaultdict(list)
    filenames = os.listdir(path)
    flag = [0] * len(filenames)
    i = 0
    for file in filenames:
        all_files[i] = open(str(path) + '/' + str(file), 'r')
        first_lines[i] = all_files[i].readline().split('  ')

        # print(first_lines[i])

        flag[i] = 1
        if first_lines[i][0] not in heap:
            push(heap, first_lines[i][0])
        i += 1

    cnt = len(filenames)
    cur = 0
    no = 0

    # Follows sorted fashion of lexographical words

    while any(flag) == 1:
        top = pop(heap)
        cur += 1
        for i in range(len(filenames)):
            if flag[i]:
                if first_lines[i][0] == top:

                    # Append in data[top]

                    data[top].extend((first_lines[i])[1:])
                    first_lines[i] = all_files[i].readline().split('  ')

                    if first_lines[i][0] == '':
                        flag[i] = 0
                    else:

                        if first_lines[i][0] not in heap:
                            push(heap, first_lines[i][0])

        if cur >= 50000:

          # print(data)

            writeit(tag, data)
            print (tag, no)
            data = defaultdict(list)
            no += 1
            cur = 0

    if cur > 0:
        writeit(tag, data)
        print (tag, no)
        data = defaultdict(list)
        no += 1
        cur = 0
