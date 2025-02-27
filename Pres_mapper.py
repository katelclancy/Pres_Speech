# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 20:08:44 2025

@author: KateClancy
"""

import re
import string
import requests
import os
import sys

stopwords_list = requests.get(("https://gist.githubusercontent.com/rg089/35e00abf8941d72d419224cfd5b5925d/"
                 "raw/12d899b70156fd0041fa9778d657330b024b959c/stopwords.txt")).content
stopwords = list(set(stopwords_list.decode().splitlines()))

def remove_stopwords(words):
    list_ = re.sub(r'[^a-zA-Z0-9]', " ", words.lower()).split()
    return [itm for itm in list_ if itm not in stopwords]

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text)
    text = re.sub(r'[\d]+', ' ', text)
    return ' '.join(remove_stopwords(text))

def load_afinn(url="https://raw.githubusercontent.com/fnielsen/afinn/master/afinn/data/AFINN-en-165.txt"):
    afinn = {}
    response = requests.get(url)
    for line in response.text.splitlines():
        if line.strip():
            word, score = line.split('\t')
            afinn[word] = int(score)
    return afinn

afinn = load_afinn()

def calc_valence(clean_words):
    words = clean_words.split()
    if not words:
        return 0.0

    total_valence = 0
    count = 0
    for word in words:
        if word in afinn:
            total_valence += afinn[word]
            count += 1
    # If none of the words have a valence, return 0.
    if count > 0:
        return (total_valence / count) 
    else:
        return 0

def valence(text):
    # Ensure text is a proper string
    if isinstance(text, bytes):
        text = text.decode('utf-8', errors='ignore')
    elif not isinstance(text, str):
        text = str(text)
    return calc_valence(clean_text(text))

def mapper():
    president = os.environ['mapreduce_map_input_file'].split('/')[-1][:-7]
    for line in sys.stdin:
        sentiment_score = valence(line)
        print(f"{president}\t{sentiment_score}")

if __name__ == "__main__":
    mapper()
