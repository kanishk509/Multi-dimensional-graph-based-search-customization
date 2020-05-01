import yake
import sys
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import requests
import time
from IPy import IP
from collections import defaultdict
import itertools  #used to slice a dictionary

import json
import pickle

from pprint import pprint

#Functions used for extraction of text from the url provided

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

def text_from_title(body):
    soup = BeautifulSoup(body, 'html.parser')
    title_text = soup.find('title').text
    return title_text

def keywordExtractor(url, max_keywords = 20):
    url = url.strip()
    headers={'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(url, headers=headers, timeout=3) 
    if resp.status_code >= 300:
        return {}
    html = resp.text
    text = text_from_html(html)
    title_text = text_from_title(html).lower()
    max_ngram_size = 1
    simple_kwextractor = yake.KeywordExtractor(lan="en", n = max_ngram_size, dedupLim=0.9, dedupFunc='seqm', windowsSize=1, top=max_keywords, features=None)
    keywords = simple_kwextractor.extract_keywords(text)
    title_keywords = simple_kwextractor.extract_keywords(title_text)
    title_words = dict([(t[1], t[0]) for t in title_keywords])  #to swap the term and its score to get {term:score}
    title_words = title_words.keys()
    
    keywords2 = []
    for kw in keywords:
        #since the order of term and score is reversed
        if kw[1] in title_words:
            kw2 = (kw[0]/4, kw[1])
        else:
            kw2 = kw
        keywords2.append(kw2)   #should be inside for loop so that all words are appended
    keywords2 = dict([(t[1], t[0]) for t in keywords2]) #to make a dictionary(as given in description) and also to reverse the order to {term:score}
    return keywords2