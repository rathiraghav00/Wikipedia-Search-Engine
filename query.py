<<<<<<< Updated upstream
#!/usr/bin/python
# -*- coding: utf-8 -*-

=======
>>>>>>> Stashed changes
import re
from collections import *
import sys
from nltk.stem.snowball import SnowballStemmer
import os
import time

<<<<<<< Updated upstream
tags = {
    1: 'title',
    2: 'text',
    3: 'category',
    4: 'infobox',
    }
=======
tags = {1: "title", 2: "text", 3: "category", 4: "infobox"}

>>>>>>> Stashed changes

dic = defaultdict(float)

# of the format this [something, tfidf score]
# [('187', 3.29), ('204', 3.29), ('387', 3.29)]

<<<<<<< Updated upstream
offsets = [open('offsets/title.txt', 'r', encoding='ISO-8859-1'),
           open('offsets/text.txt', 'r', encoding='ISO-8859-1'),
           open('offsets/category.txt', 'r', encoding='ISO-8859-1'),
           open('offsets/infobox.txt', 'r', encoding='ISO-8859-1')]

scores = [open('score/title.txt', 'r', encoding='ISO-8859-1'),
          open('score/text.txt', 'r', encoding='ISO-8859-1'),
          open('score/category.txt', 'r', encoding='ISO-8859-1'),
          open('score/infobox.txt', 'r', encoding='ISO-8859-1')]

title_file = open('doc_title.txt', 'r', encoding='ISO-8859-1')
=======
offsets = [
    open("offsets/title.txt", "r", encoding="ISO-8859-1"),
    open("offsets/text.txt", "r", encoding="ISO-8859-1"),
    open("offsets/category.txt", "r", encoding="ISO-8859-1"),
    open("offsets/infobox.txt", "r", encoding="ISO-8859-1"),
]

scores = [
    open("score/title.txt", "r", encoding="ISO-8859-1"),
    open("score/text.txt", "r", encoding="ISO-8859-1"),
    open("score/category.txt", "r", encoding="ISO-8859-1"),
    open("score/infobox.txt", "r", encoding="ISO-8859-1"),
]

title_file = open("doc_title.txt", "r", encoding="ISO-8859-1")
>>>>>>> Stashed changes
doc_offset = []
lines = title_file.readlines()
cur = 0
for line in lines:
    doc_offset.append(cur)
    cur += len(line) + 1

word_pos = [defaultdict(list) for i in range(4)]

for i in range(4):

    lines = offsets[i].readlines()
    for line in lines:
<<<<<<< Updated upstream
        temp = line.split(':')
        word = ''.join(temp[0:-1])

        # No pair of {doc_no, id} doesnot exist

=======
        temp = line.split(":")
        word = "".join(temp[0:-1])

        # No pair of {doc_no, id} doesnot exist
>>>>>>> Stashed changes
        if len(temp[-1]) == 0:
            continue

        # page is location of word in offset/{$tag}

        page = int(temp[-1].strip())
        word_pos[i][word] = page

<<<<<<< Updated upstream

 #   offsets[i].close()
=======
#   offsets[i].close()
>>>>>>> Stashed changes

# Regex to remove special characters

def remove_special_characters(text):

    # Define the pattern to keep
<<<<<<< Updated upstream

    pat = r'[^a-zA-z0-9.,!?/:;\"\'\s]'
    return re.sub(pat, ' ', text)


stemmer = SnowballStemmer(language='english')


def tagq(words, typ):

=======
    pat = r"[^a-zA-z0-9.,!?/:;\"\'\s]"
    return re.sub(pat, " ", text)


stemmer = SnowballStemmer(language="english")


def tagq(words, typ):

>>>>>>> Stashed changes
    if typ == 4:
        for i in range(4):
            tagq(words, i)
        return

    for word in words:
        word = stemmer.stem(word.lower())
<<<<<<< Updated upstream

        # word = remove_special_characters(word)

        if word in word_pos[typ]:

           # word = stemmer.stem(word.lower())
            # word = remove_special_characters(word)

=======
        # word = remove_special_characters(word)
        if word in word_pos[typ]:
            # word = stemmer.stem(word.lower())
            # word = remove_special_characters(word)
>>>>>>> Stashed changes
            page = word_pos[typ][word]
            scores[typ].seek(page)
            line = scores[typ].readline()
            line = line.split(" ")
            for w in line[1:]:
                if len(w) <= 1:
                    continue
                tmp = w.split(":")
                pg = tmp[0]
                tfidf = float(tmp[1])
                if pg not in dic:
                    dic[pg] = 0
                dic[pg] += tfidf


def process():

    # Sort in decreasing order by tf-idf score
<<<<<<< Updated upstream

    results = sorted(dic.items(), key=lambda item: item[1],
                     reverse=True)

    results = results[:min(10, len(results))]
=======
    results = sorted(dic.items(), key=lambda item: item[1], reverse=True)

    results = results[: min(10, len(results))]
>>>>>>> Stashed changes

    # print(results)

    for cur in results:
        cur = cur[0]
        pos = doc_offset[int(cur)]
        title_file.seek(pos)
        title = title_file.readline().strip()
<<<<<<< Updated upstream
        title = title.replace(' ', '_')
        print 'https://en.wikipedia.org/wiki/' + title
=======
        title = title.replace(" ", "_")
        print("https://en.wikipedia.org/wiki/" + title)
>>>>>>> Stashed changes


def query():

<<<<<<< Updated upstream
    print 'Any Queries?  (Yes or No) \n'

    q = input()

    if q == 'yes' or q == 'y' or q == 'Yes' or q == 'Y':

        clock_start = time.time()

        print 'Select Query Type:'
        print '1 - Search By Title'
        print '2 - Search By Text'
        print '3 - Search By Category'
        print '4 - Search By Infobox'
        print '5 - Widesearch'

        typ = int(input())

        print 'Type Your Query:\n'
        que = input().strip('\n').lower()
=======
    print("Any Queries?  (Yes or No) \n")

    q = input()

    if q == "yes" or q == "y" or q == "Yes" or q == "Y":

        clock_start = time.time()

        print("Select Query Type:")
        print("1 - Search By Title")
        print("2 - Search By Text")
        print("3 - Search By Category")
        print("4 - Search By Infobox")
        print("5 - Widesearch")

        typ = int(input())

        print("Type Your Query:\n")
        que = input().strip("\n").lower()
>>>>>>> Stashed changes

        words = que.split(" ")

        # Clear the dictionary

        dic.clear()

        tagq(words, typ - 1)

        # Processing

        process()

        # Print the time taken
<<<<<<< Updated upstream

        print 'Query time = ' + str(time.time() - clock_start)
=======
        print("Query time = " + str(time.time() - clock_start))
>>>>>>> Stashed changes

        # Recursive Call

        query()
<<<<<<< Updated upstream
    else:

=======

    else:
>>>>>>> Stashed changes
        return


query()
