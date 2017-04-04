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

class Data:
    def __init__(self, filename, n=10, p=4, truncate=None):
        self.text = self.get_complete_word_list(filename)
        if truncate:
            self.text = self.text[:truncate]
        # TODO: lematizirati //MOLEX ?
        self.vocab = self.get_words()
        self.occurences = self.occurences(n)
        #self.occurences = self.split_into_contexts(n,p)

    # Read whole text, split into list of words, ignore new lines and punctuation
    def get_complete_word_list(self, filename):
        text = open(filename, "r")
        mypunctuation = string.punctuation.replace('-', '') # ignore all punctuation except '-'
        mypunctuation += '0123456789'
        text = text.read().lower().replace('\n',' ').replace('\t',' ')
        text = str(text).translate(None, mypunctuation).split(' ') #.translate("čćšđž", "ccsdz") ?
        return text

    # Returns list of unique words in text // from most to least common
    def get_words(self):
        cnt = collections.Counter(self.text)
        return [c[0] for c in cnt.most_common(len(cnt.keys()))]
    
    # get n words for each word as its context
    # n=size, p=limiter. ex: n=6, p=3:  context = [word1 word2] (word) [word3 word4 word5 word6]
    # 1/p words before word, (p-1)/p after word
    def split_into_contexts(self, n, p):
        occurences = dict()
        for word in self.vocab:
            occurences[word] = []
            indexes = [i for i,j in zip(count(), self.text) if j==word] # get occurences (index) of word in text
            for i in indexes:
                chunk = self.text[max(0, i-n/p):i] +  self.text[i+1:min(i+(p-1)*(n/p), len(self.text))]
                vector = np.zeros(shape=(len(self.vocab),))
                for w in chunk:
                    vector[self.vocab.index(w)] = 1
                occurences[word].append(vector)
        # occurences[word] = list of vectors, each vector is one-hot coded words before and after word
        return occurences
                        
    # create list of occurences for each word (from pre-made chunks)
    def occurences(self, n):
        chunks = self.split_into_chunks(n)
        self.vectors = self.to_vectors(chunks)
        occurences = dict()
        for word in self.vocab:
            occurences[word] = []
        for x in self.vectors:
            for i in range(len(x)):
                if x[i]:
                    occurences[self.vocab[i]].append(x)
        return occurences

    # Splits list of words into lists of n words
    def split_into_chunks(self, n=10):
        chunks = []
        for i in range(0, len(self.text), n):
            chunks.append(self.text[i:i+n])
        return chunks        

    # Transform chunks into vectors of length len(vocab) //one-hot
    def to_vectors(self, chunks):
        temp = []
        n = len(self.vocab)
        for sentence in chunks:
            newVector = np.zeros(shape=(n,))
            for word in sentence:
                newVector[self.vocab.index(word)] = 1
            temp.append(newVector)
        return temp

if __name__ == "__main__":
    dataset = Data("data/picard.txt")
    print dataset.vocab[:10]
    print len(dataset.occurences[dataset.vocab[0]]), len(dataset.occurences[dataset.vocab[-1]])



