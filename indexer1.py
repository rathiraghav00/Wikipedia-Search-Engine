#indexer for XML data
from __future__ import print_function
import xml.etree.ElementTree as ET
import re
from collections import *
import sys
from nltk.stem.snowball import SnowballStemmer
import os
import heapq
import math

from platform import python_version

print(python_version())

XML_file_names = os.listdir('current')
print(XML_file_names)

# RE to remove urls
regExp1 = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',re.DOTALL)

# RE to remove tags & css
regExp2 = re.compile(r'{\|(.*?)\|}',re.DOTALL)

# Regular Expression to remove {{cite **}} or {{vcite **}}
regExp3 = re.compile(r'{{v?cite(.*?)}}',re.DOTALL)

# Regular Expression to remove [[file:]]
regExp4 = re.compile(r'\[\[file:(.*?)\]\]',re.DOTALL)

def remove_special_characters(text):
    # define the pattern to keep
    pat = r'[^a-zA-z0-9.,!?/:;\"\'\s]' 
    return re.sub(pat, ' ', text)

page_cnt = 0

text_dic = defaultdict(list)
text_cnt_dic ={}

category_dic =defaultdict(list)
category_cnt_dic ={}

infobox_dic =defaultdict(list)
infobox_cnt_dic ={}

title_dic = defaultdict(list)
title_cnt_dic ={}

link_dic =defaultdict(list)
link_cnt_dic = {}

# To store all the words present in the corpus
words_dic = {}

tags = {'title': 0, 'text': 1, 'category': 2,'infobox':3}

def clean():
    text_cnt_dic ={}
    category_cnt_dic ={}
    infobox_cnt_dic ={}
    title_cnt_dic ={}
    link_cnt_dic = {}
    words_dic = {}

def clean2():
    text_dic = defaultdict(list)
    category_dic =defaultdict(list)
    infobox_dic =defaultdict(list)
    title_dic = defaultdict(list)
    link_dic = defaultdict(list)

stopwords = {}
stemmer = SnowballStemmer(language = 'english',ignore_stopwords=True)

# Stemming stop words
with open('data/stopwords.txt','r') as file:
    words = file.read().split('\n')
    for word in  words:
        word = stemmer.stem(word.lower())
        stopwords[word]=1

# Update title_cnt_dic and text_dic_cnt

def update(s,tag):
    if s:
        words = re.split('[^A-Za-z0-9]', s)
        for word in words:
            word = stemmer.stem(word.lower())
            if len(word)>=2:
                words_dic[word]=1
                if(tag=='title'):
                    if word in title_cnt_dic:
                        title_cnt_dic[word]+=1
                    else :
                        title_cnt_dic[word]=1
                elif tag=='text':
                    if word in infobox_cnt_dic:
                        text_cnt_dic[word]+=1
                    else :
                        text_cnt_dic[word]=1

#done
def category_updater(text):
    rex = re.findall("\[\[Category:(.*?)\]\]", str(text))
    if rex:
      #  print(rex)
        for words in rex:
          #  print(words)
            #words = words.split(' ')
            pattern = re.compile("[^a-zA-Z0-9]")
            words = re.split(pattern, words)
            for word in words:
              #  print(word)
                word = stemmer.stem(word.lower())
                if len(word)>1:
                    words_dic[word]=1 
                    if word in category_cnt_dic:
                        category_cnt_dic[word]+=1
                    else :
                        category_cnt_dic[word]=1

#done
def infobox_updater(s):
    tempword = re.findall("{{Infobox((.|\n)*?)}}", str(s)) # get all data between infobox{{ ----- }}
    if tempword :
        for temp in tempword :
            for word in temp : 
                pattern = re.compile("[^a-zA-Z0-9]")
                temp = re.split(pattern, word)
                for t in temp :
                    t = stemmer.stem(t.lower())
                    if t :
                        if len(t) <= 2 :
                            continue
                        if  t not in stopwords :
                            words_dic[t]=1
                            if t not in infobox_cnt_dic :
                                infobox_cnt_dic[t] = 1
                            else :
                                infobox_cnt_dic[t] += 1

doc_no =0
doc_cnt = 0

doc_titles = open('doc_title.txt','a',encoding= 'utf-8')

file_no =1
for i in range(len(XML_file_names)):
    for event,element in ET.iterparse('current/'+XML_file_names[i],events=("start","end")):

        tag = element.tag
        #print(tag)

        # Check this out!!????
        #it is a namespace actually, and we use namespaces because for eg if we have a field ID both in
	#as well as teacher class then we use a namespace like a link in XML. But we need the end portion after that namespace
        tag = tag[tag.rfind('}')+1:] #namespace


#         original {http://www.mediawiki.org/xml/export-0.10/}mediawiki
# after r.find mediawiki
# original {http://www.mediawiki.org/xml/export-0.10/}siteinfo
# after r.find siteinfo
# original {http://www.mediawiki.org/xml/export-0.10/}sitename
# after r.find sitename
# original {http://www.mediawiki.org/xml/export-0.10/}sitename
# after r.find sitename
# original {http://www.mediawiki.org/xml/export-0.10/}dbname
# after r.find dbname
# original {http://www.mediawiki.org/xml/export-0.10/}dbname

        if tag == 'page' and event =='end':  #one page at a time

            for w in words_dic:
                #w = remove_special_characters(w)
                for t in tags:
                    if t=='title':
                        if w in title_cnt_dic :

                            # $(tags)_cnt_dic has already beeen calculated
                            s = " "+ str(doc_no)+":" + str(title_cnt_dic[w])
                            title_dic[w].append(s)
                    elif t=='text':
                        if w in text_cnt_dic:
                            s = " "+ str(doc_no)+":" + str(text_cnt_dic[w])
                            text_dic[w].append(s)
                    elif t=='category':
                        if w in category_cnt_dic:
                            s = " "+ str(doc_no)+":" + str(category_cnt_dic[w])
                            category_dic[w].append(s)
                    elif t=='infobox':
                        if w in infobox_cnt_dic:
                            s = " "+ str(doc_no)+":" + str(infobox_cnt_dic[w])
                            infobox_dic[w].append(s)

            doc_no+=1
            doc_cnt+=1

            element.clear()
            title_cnt_dic.clear()
            text_cnt_dic.clear()
            category_cnt_dic.clear()
            infobox_cnt_dic.clear()
            words_dic.clear()

        elif tag =='title' and event =='end':
            text = element.text
            text.strip()
            text.replace(" ","_")
            text = re.sub("\s+", "_", text.strip())
            doc_titles.write(str(text)+'\n')
            update(str(text),tag)
        elif tag =='text' and event =='end':
                text = str(element.text)
                text = regExp1.sub('',text)
                text = regExp2.sub('',text)
                text = regExp3.sub('',text)
                text = regExp4.sub('',text)
                update(str(text),tag)
                category_updater(str(text))
                infobox_updater(str(text))

        if doc_cnt>=20000:
            doc_cnt=0
            title_path = 'final/title/' + str(file_no) +'.txt'
            
            file = open(title_path,'w',encoding='utf-8')
            s= ""
            for word in sorted(title_dic):
                s= word + ' '
                for vl in title_dic[word]:
                    s+= vl +' '
                s+= '\n'
                file.write(s)
            file.close()
            title_dic.clear()
            
            
            
            
            print('title',file_no)

            text_path = 'final/text/' + str(file_no) +'.txt'
            file = open(text_path,'w',encoding='utf-8')
            s= ""
            for word in sorted(text_dic):
                s= word + ' '
                for vl in text_dic[word]:
                    s+= vl +' '
                s+= '\n'
                file.write(s)
            file.close()
            
            text_dic.clear()
            
            print('text',file_no)

            cat_path = 'final/category/' + str(file_no) +'.txt'
            file = open(cat_path,'w',encoding='utf-8')
            s= ""
            for word in sorted(category_dic):
                s= word + ' '
                for vl in category_dic[word]:
                    s+= vl +' '
                s+= '\n'
                file.write(s)
            file.close()
            
            category_dic.clear()
            
            
            print('cat',file_no)

            info_path = 'final/infobox/' + str(file_no) +'.txt'
            file = open(info_path,'w',encoding='utf-8')
            s= ""
            for word in sorted(infobox_dic):
                s= word + ' '
                for vl in infobox_dic[word]:
                    s+= vl +' '
                s+= '\n'
                file.write(s)
            file.close()
            
            infobox_dic.clear()

            print('info',file_no)
            file_no+=1
            

#since the number of documents may not be a multiple of 20000 so I need to write one more if statement like above
if doc_cnt>0:
    print(doc_cnt)
    doc_cnt=0
    #file_no = doc_no%5000 + 1
    
    title_path = 'final/title/' + str(file_no) +'.txt'
    
    file = open(title_path,'w',encoding='utf-8')
    s= ""
    for word in sorted(title_dic):
        s= word + ' '
        for vl in title_dic[word]:
            s+= vl +' '
        s+= '\n'
        file.write(s)
    file.close()
    print('title',file_no)
    
    title_dic.clear()

    text_path = 'final/text/' + str(file_no) +'.txt'
    file = open(text_path,'w',encoding='utf-8')
    s= ""
    for word in sorted(text_dic):
        s= word + ' '
        for vl in text_dic[word]:
            s+= vl +' '
        s+= '\n'
        file.write(s)
    file.close()
    
    text_dic.clear()

    print('text',file_no)

    cat_path = 'final/category/' + str(file_no) +'.txt'
    file = open(cat_path,'w',encoding='utf-8')
    s= ""
    for word in sorted(category_dic):
        s= word + ' '
        for vl in category_dic[word]:
            s+= vl +' '
        s+= '\n'
        file.write(s)
    file.close()
    
    category_dic.clear()

    print('cat',file_no)

    info_path = 'final/infobox/' + str(file_no) +'.txt'
    file = open(info_path,'w',encoding='utf-8')
    s= ""
    for word in sorted(infobox_dic):
        s= word + ' '
        for vl in infobox_dic[word]:
            s+= vl +' '
        s+= '\n'
        file.write(s)
    file.close()
    
    infobox_dic.clear()

    print('info',file_no)
    file_no +=1
    clean2()        

print(doc_no)