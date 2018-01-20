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
from collections import defaultdict; 
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
	#print deletechars;  

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
total_count = len(tokens); 
#print(str(total_count) + '\n');  
#count = Counter(tokens); 
#print count.most_common(10); 

# ------------------------ #
# --- Section 4 Unigram--- # 
# ------------------------ #

unigram = list(tokens); 
unigram_cnts = Counter();

#figure out the unigram counts 
for word in unigram:
	unigram_cnts[word] += 1;
#switch to frequency
for word in unigram_cnts:
	unigram_cnts[word] /= float(total_count);  
#print unigram;
#print('Unigram Data\n'); 
#print unigram_cnts.most_common(25); 

#make a chain of words
text_from_unigram = []; 
for _ in range(100):
	r = random.random();
	accumulator = .0; 

	for word, freq in unigram_cnts.iteritems():
		accumulator += freq; 

		if accumulator >= r:
			text_from_unigram.append(word); 
			break; 
print ' '.join(text_from_unigram); 

# ----------------------- #
# --- Section 5 Bigram--- # 
# ----------------------- #

bigram = list(range_ngrams(tokens, ngramRange=(2, 3))); 
bigram_cnts = Counter(); 

#figure out the bigram counts
for word in bigram:
	bigram_cnts[word] += 1; 
#print bigram; 
#print('Bigram Data\n'); 
#print bigram_cnts.most_common(25); 

bi_model = defaultdict(lambda: defaultdict(lambda: 0)); 
for w1, w2 in bigram:
	bi_model[w1][w2] += 1;

#switch to freqs
for w1 in bi_model:
	total_count_bi = float(sum(bi_model[w1].values())); 
	for w2 in bi_model[w1]:
		bi_model[w1][w2] /= total_count_bi; 

print bi_model["i"]["will"]; 

# ------------------------ #
# --- Section 6 Trigram--- # 
# ------------------------ #

trigram = list(range_ngrams(tokens, ngramRange=(3, 4))); 
trigram_cnts = Counter(); 

#figure out the bigram counts
for word in trigram:
	trigram_cnts[word] += 1; 
#print trigram;
#print('Trigram Data\n'); 
#print trigram_cnts.most_common(25); 

#make a trigram model
tri_model = defaultdict(lambda: defaultdict(lambda: 0)); 
for w1, w2, w3 in trigram:
	tri_model[(w1, w2)][w3] += 1; 

#print tri_model["i", "will"]["not"];

#switch to freqs
for w1_w2 in tri_model:
	total_count_tri = float(sum(tri_model[w1_w2].values())); 
	for w3 in tri_model[w1_w2]:
		tri_model[w1_w2][w3] /= total_count_tri; 

print tri_model["i", "will"]["not"];



# text_from_trigram = [None, None]; 
# done = False; 

# #while not done:
# for _ in range(100):
# 	r = random.random(); 
# 	accumulator =.0; 

# 	for word in tri_model[tuple(text_from_trigram[-2:])].keys():
# 		accumulator +=tri_model[tuple(text_from_trigram[-2:])][word]; 

# 		if accumulator >= r:
# 			text_from_trigram.append(word); 
# 			break; 

# 	#if text_from_trigram[-2] == [None, None]:
# 		#done = True; 

# print ' '.join([text for text in text_from_trigram if text]); 