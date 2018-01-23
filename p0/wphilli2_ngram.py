#!/usr/bin/env python
#-*- coding: utf-8 -*-

# p0 ngram
# William (Greg) Phillips
# Ready for Review

# ------------------------ #
# --- Section 0 - Meta --- #
# ------------------------ #

'''
NLTK was not allowed for use in this exercise
Written in Python 2.7, hence the magic statement on the 1st/2nd lines
Project Gutenberg file contains many characters that fall outside of the ASCII range
UTF-8 encoding is necessary to get rid of pesky 'weird' Shakespearean'istical characters
'''

# --------------------------- #
# --- Section 1 - Imports --- #
# --------------------------- #

import random; 
import string; 

# ---------------------------------------- #
# --- Section 2 - Function Defintiions --- #
# ---------------------------------------- # 

def get_tokens():
	#set up stuff to kill the weird punctuation characters 
	#that aren't contained in the string constants
	deletechars =[]; 
	for c in string.punctuation:
		deletechars += [c];
	#These next two aren't contained in the string constant
	deletechars.insert(0, '“'); 
	deletechars.insert(0, '”')
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

# ------------------------ #
# --- Section 4 Unigram--- # 
# ------------------------ #

unigrams = {};
for word in tokens:
	if word in unigrams:
		unigrams[word] += 1; 
	else:
		unigrams[word] = 1; 

#switch to frequency
for word in unigrams:
	unigrams[word] /= float(total_count); 

#make a chain of words
out = []; 
for _ in range(100):
	r = random.random();
	accumulator = .0; 

	for word, freq in unigrams.iteritems():
		accumulator += freq; 

		if accumulator >= r:
			out.append(word); 
			break; 

print('Unigram Build: \n')
print ' '.join(out);

# ----------------------- #
# --- Section 5 Bigram--- # 
# ----------------------- #

bigrams = {}; 
prev = 'X'; 

for word in tokens:
	bigram = prev + ' ' + word; 
	if bigram in bigrams:
		bigrams[bigram] += 1; 
	else:
		bigrams[bigram] = 1; 
	prev = word;  

#switch to frequency
for pair in bigrams:
	bigrams[pair] /= float(total_count); 

#make a chain of words
out = []; 
for _ in range(100):
	r = random.random();
	accumulator = .0; 

	for word, freq in bigrams.iteritems():
		accumulator += freq; 

		if accumulator >= r:
			out.append(word); 
			break; 

print('Bigram Build: \n')
print ' '.join(out);

# ------------------------ #
# --- Section 6 Trigram--- # 
# ------------------------ #

trigrams = {}; 
prev1 = 'XX'; 
prev2 = 'X'

for word in tokens:
	trigram = prev1 + ' ' + prev2 + ' ' + word; 
	if trigram in trigrams:
		trigrams[trigram] += 1; 
	else:
		trigrams[trigram] = 1; 
	prev1 = prev2; 
	prev2 = word; 

#switch to frequency
for triplet in trigrams:
	trigrams[triplet] /= float(total_count); 

#make a chain of words
out = []; 
for _ in range(100):
	r = random.random();
	accumulator = .0; 

	for word, freq in trigrams.iteritems():
		accumulator += freq; 

		if accumulator >= r:
			out.append(word); 
			break; 
print('Trigram Build: \n')
print ' '.join(out);