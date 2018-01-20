#!/usr/bin/env python
#-*- coding: utf-8 -*-

# p0 ngram
# William (Greg) Phillips
# Working

# ------------------------ #
# --- Section 0 - Meta --- #
# ------------------------ #

'''
NLTK was not allowed for use in this exercise
Written in Python 2.7, hence the magic statement on the 1st/2nd lines
Project Gutenberg file contains many characters that fall outside of the ASCII range
UTF-8 encoding is necessary to get rid of pesky 'weird' Shakespearean characters
'''

# --------------------------- #
# --- Section 1 - Imports --- #
# --------------------------- #

from collections import Counter;
from itertools import chain; 
import random; 
import string; 

# ---------------------------------------- #
# --- Section 2 - Function Defintiions --- #
# ---------------------------------------- #

def get_ngrams(tokens, n=1):
	moveToken = lambda i: (el for j, el in enumerate(tokens) if j>=i); 
	movedTokens = (moveToken(i) for i in range(n));  
	tupleNGrams = zip(*movedTokens); 
	return tupleNGrams

def range_ngrams(tokens, ngramRange=(1,2)):
	return chain(*(get_ngrams(tokens, i) for i in range(*ngramRange))); 

def get_tokens():
	#set up stuff to kill the weird punctuation characters 
	#that aren't contained in the string constants
	deletechars =[]; 
	for c in string.punctuation:
		deletechars += [c];
	#I decided I want the next two to be a part of tokens
	deletechars.remove("'"); 
	deletechars.remove('-'); 
	#These next two aren't contained in the string constant
	deletechars.insert(0, '“'); 
	deletechars.insert(0, '”')
	print deletechars;  

	with open('corpus.txt', 'r') as shake:
		text = shake.read();
		lower = text.lower();
		kill_punctuation = lower; 
		for i in deletechars:
			kill_punctuation = kill_punctuation.replace(i, ''); 
		kill_digits = kill_punctuation.translate(None, string.digits);
		tokens = kill_digits.split(); 
		return tokens; 

# ------------------------------- #
# --- Section 3 - Exploratory --- # 
# ------------------------------- #

tokens = get_tokens(); 
#count = Counter(tokens); 
#print count.most_common(10); 

# ------------------------ #
# --- Section 4 Unigram--- # 
# ------------------------ #

unigram = list(tokens); 
#print unigram;

# ----------------------- #
# --- Section 5 Bigram--- # 
# ----------------------- #

bigram = list(range_ngrams(tokens, ngramRange=(2, 3))); 
#print bigram; 

# ------------------------ #
# --- Section 6 Trigram--- # 
# ------------------------ #

trigram = list(range_ngrams(tokens, ngramRange=(3, 4))); 
#print trigram; 
