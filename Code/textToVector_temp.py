# -*- coding: utf-8 -*-
# read all text
# use counter to count all unique words
# take most frequent N to learn
# change each sentece (or M words) into vectors
# return vectors as training set
#---------------------------------------------------------------
import numpy as np
import collections
import string
from itertools import izip as zip, count
import math

class Data:
    def __init__(self, filename, N=10, truncate=None):
        f = open(filename, "r")
        self.text = self.text_to_list(f, truncate)
        self.N = N
        self.vocab = self.get_vocab()
        self.contexts = self.get_contexts(N)
        self.to_vectors()

    def get_tf_idf_weights(self):
        #TF = [float(c[1])/len(self.text) for c in cnt.most_common(len(cnt.keys()))]
        #IDF = math.log() #need more files
        pass

    def dumb_stemmer(self):
        pass
    
    def to_vectors(self):
        for word in self.vocab:
            for i, context in enumerate(self.contexts[word]):
                self.contexts[word][i] = [1 if w in context else 0 for w in self.vocab] # one hot

    # gets context for each word (N-word window)
    def get_contexts(self, N):
        n = int(N/2)
        contexts = dict()
        for word in self.vocab:
            contexts[word] = []
            indices = [i for i,x in enumerate(self.text) if x == word]
            for i in indices:
                if i >= n and i < len(self.text)-n:
                    ctx = self.text[i-n:i+n]
                    contexts[word].append(ctx)
        return contexts
        
    # reads file, returns list of words in text
    def text_to_list(self, f, truncate):
        mypunctuation = string.punctuation + '0123456789'
        text = f.read().lower().replace('\n',' ').replace('\t',' ')
        text = text.translate(None, mypunctuation).split(' ')
        if truncate:
            text = text[:truncate]
        for t in text:
            if len(t)<1: text.remove(t)
        return text

    # Returns list of unique words in text // from most to least common
    def get_vocab(self):
        cnt = collections.Counter(self.text)
        vocab = [c[0] for c in cnt.most_common(len(cnt.keys()))]
        return vocab


if __name__ == "__main__":
    dataset = Data("data\hrv\picard.txt")
    print dataset.vocab[:10]
    print len(dataset.contexts[dataset.vocab[0]]), len(dataset.contexts[dataset.vocab[-1]])



