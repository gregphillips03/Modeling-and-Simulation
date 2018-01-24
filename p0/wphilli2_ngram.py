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
import sys; 

# ---------------------------------------- #
# --- Section 2 - Function Defintiions --- #
# ---------------------------------------- # 

def get_tokens(path):
	#set up stuff to kill the weird punctuation characters 
	#that aren't contained in the string constants
	deletechars =[]; 
	for c in string.punctuation:
		deletechars += [c];
	#These next two aren't contained in the string constant
	deletechars.insert(0, '“'); 
	deletechars.insert(0, '”')
	with open(path, 'r') as shake:
		text = shake.read();
		lower = text.lower();
		annoyed = lower.replace('\\xe2\\x80\\x94', '');
		annoyed2 = annoyed.replace('\\xE2\\x80\\x98', '');
		annoyed3 = annoyed2.replace('—', '');   
		kill_punctuation = annoyed3; 
		for i in deletechars:
			kill_punctuation = kill_punctuation.replace(i, ''); 
		kill_digits = kill_punctuation.translate(None, string.digits);
		tokens = kill_digits.split(); 
		return tokens; 

class Chain:
	#constructor to initiate a memory slot for a dictionary
	def __init__(self):
		self.memory = {};

	#check this object for the key value pair
	def _learn_key(self, key, value):
		if key not in self.memory:
			self.memory[key] = [];
		self.memory[key].append(value);

	#bigrams
	def learn_bi(self, tokens):
		bigrams = [(tokens[i], tokens[i + 1]) for i in range(0, len(tokens) - 1)];
		for bigram in bigrams:
			self._learn_key(bigram[0], bigram[1]);

	#trigrams
	def learn_tri(self, tokens):
		trigrams = [(tokens[i], tokens[i + 1], tokens[i + 2]) for i in range(0, len(tokens) - 2)]; 
		for trigram in trigrams:
			self._learn_key(trigram[1], trigram[2]);

	#quadgrams
	def learn_quad(self, tokens):
		quadgrams = [(tokens[i], tokens[i + 1], tokens[i + 2], tokens[i + 3]) for i in range(0, len(tokens) - 3)];              
		for quadgram in quadgrams:
			self._learn_key(quadgram[2], quadgram[3]); 

	#quingrams
	def learn_quin(self, tokens):
		quingrams = [(tokens[i], tokens[i + 1], tokens[i + 2], tokens[i + 3], tokens[i+4]) for i in range(0, len(tokens) - 4)];
		for quingram in quingrams:
			self._learn_key(quingram[3], quingram[4]);

	#hexagrams
	def learn_hexa(self, tokens):
		hexagrams = [(tokens[i], tokens[i + 1], tokens[i + 2], tokens[i + 3], tokens[i+4], tokens[i+5]) for i in range(0, len(tokens) - 5)];
		for hexagram in hexagrams:
			self._learn_key(hexagram[4], hexagram[5]);

	#septagrams
	def learn_septa(self, tokens):
		septagrams = [(tokens[i], tokens[i + 1], tokens[i + 2], tokens[i + 3], tokens[i+4], tokens[i+5], tokens[i+6]) for i in range(0, len(tokens) - 6)];
		for septagram in septagrams:
			self._learn_key(septagram[5], septagram[6]); 

	#octagrams
	def learn_octa(self, tokens):
		octagrams = [(tokens[i], tokens[i + 1], tokens[i + 2], tokens[i + 3], tokens[i+4], tokens[i+5], tokens[i+6], tokens[i+7]) for i in range(0, len(tokens) - 7)];
		for octagram in octagrams:
			self._learn_key(octagram[6], octagram[7]);

	#nonagrams
	def learn_nona(self, tokens):
		nonagrams = [(tokens[i], tokens[i + 1], tokens[i + 2], tokens[i + 3], tokens[i+4], tokens[i+5], tokens[i+6], tokens[i+7], tokens[i+8]) for i in range(0, len(tokens) - 8)];
		for nonagram in nonagrams:
			self._learn_key(nonagram[7], nonagram[8]);

	#simple way to slide across the dictionary in memory
	def _next(self, current_state):
		next_poss = self.memory.get(current_state);

		if not next_poss:
			next_poss = self.memory.keys();

		return random.sample(next_poss, 1)[0];

	#generate a chain of words
	def my_markov(self, amount, state=''):
		if not amount:
			return state;

		next_word = self._next(state);
		return state + ' ' + self.my_markov(amount - 1, next_word);

# ------------------------ #
# --- Section 3 - Main --- # 
# ------------------------ #

def p0(path):
	print(path); 
	tokens = get_tokens(path);
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
	print('\n'); 

	# ----------------------- #
	# --- Section 5 Bigram--- # 
	# ----------------------- #

	b = Chain(); 
	b.learn_bi(tokens);
	print('Bigram Build: \n') 
	print(b.my_markov(amount=100) + '\n'); 

	# ------------------------ #
	# --- Section 6 Trigram--- # 
	# ------------------------ #

	t = Chain(); 
	t.learn_tri(tokens); 
	print('Trigram Build: \n'); 
	print(t.my_markov(amount=100) + '\n'); 

	# ------------------------- #
	# --- Section 7 Quadgram--- # 
	# ------------------------- #

	qua = Chain(); 
	qua.learn_quad(tokens); 
	print('Quadgram Build: \n'); 
	print(qua.my_markov(amount=100) + '\n');

	# ------------------------- #
	# --- Section 8 Quingram--- # 
	# ------------------------- #

	qui = Chain(); 
	qui.learn_quin(tokens); 
	print('Quingram Build: \n'); 
	print(qui.my_markov(amount=100) + '\n');

	# ------------------------- #
	# --- Section 8 Hexagram--- # 
	# ------------------------- #

	hexa = Chain(); 
	hexa.learn_hexa(tokens); 
	print('Hexagram Build: \n'); 
	print(hexa.my_markov(amount=100) + '\n');

	# ------------------------- #
	# --- Section 9 Septagram--- # 
	# ------------------------- #

	septa = Chain(); 
	septa.learn_septa(tokens); 
	print('Septagram Build: \n'); 
	print(septa.my_markov(amount=100) + '\n');

	# ------------------------- #
	# --- Section 10 Octagram--- # 
	# ------------------------- #

	octa = Chain(); 
	octa.learn_octa(tokens); 
	print('Octagram Build: \n'); 
	print(octa.my_markov(amount=100) + '\n');

	# ------------------------- #
	# --- Section 10 Nonagram--- # 
	# ------------------------- #

	nona = Chain(); 
	nona.learn_nona(tokens); 
	print('Nonagram Build: \n'); 
	print(nona.my_markov(amount=100) + '\n'); 

if __name__ == "__main__":
	try:
		arg1 = sys.argv[1];
	except IndexError:
		print "Usage: wphilli2_ngram.py <arg1>"; 
		sys.exit(1);

    # start the program
p0(arg1); 
