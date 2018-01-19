# p0 ngram
# William (Greg) Phillips
# Working

# --------------------------- #
# --- Section 0 - Imports --- #
# --------------------------- #

from collections import Counter;
import random;
import nltk; 
import string; 

# ---------------------------------------- #
# --- Section 1 - Function Defintiions --- #
# ---------------------------------------- #

def get_tokens():
	with open('corpus.txt', 'r') as shake:
		text = shake.read();
		lower = text.lower();
		kill_punctuation = lowers.translate(None, string.punctuation); 
		tokens = nltk.word_tokenize(kill_punctuation); 
		return tokens; 

# ------------------------------- #
# --- Section 2 - Exploratory --- # 
# ------------------------------- #

tokens = get_tokens(); 
count = Counter(tokens); 
print count.most_common(10); 