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
from string import maketrans

class Data:
    def __init__(self, filename, n=10, truncate=None):
        text = self.getCompleteWordList(filename)
        if truncate:
            text = text[:truncate]
        # TODO: lematizirati //MOLEX ?
        self.text = text
        self.vocab = self.getWords()
        #self.occurences = self.occurences(text, n)
        self.occurences = self.splitIntoContexts(n)

    # Read whole text, split into list of words, ignore new lines and punctuation
    def getCompleteWordList(self, filename):
        text = open(filename, "r")
        mypunctuation = string.punctuation.replace('-', '') # ignore all punctuation except '-'
        text = text.read().lower().replace('\n',' ')
        text = str(text).translate(None, mypunctuation).split(' ')
        return text

        # Returns list of unique words in text (sorted by how common they are, desc)
    def getWords(self):
        cnt = collections.Counter(self.text)
        return [c[0] for c in cnt.most_common(len(cnt.keys()))]
    
    # get +- n/2 words for each word as its context
    def splitIntoContexts(self, n):
        occurences = dict()
        for word in self.vocab:
            occurences[word] = []
            # get occurences (index) of word in text
            indexes = [i for i,j in zip(count(), self.text) if j==word]
            for i in indexes:
                chunk = self.text[max(0, i-n/2):i] +  self.text[i+1:min(i+n/2, len(self.text))]
                vector = np.zeros(shape=(len(self.vocab),))
                for w in chunk:
                    vector[self.vocab.index(w)] = 1
                occurences[word].append(vector)

        return occurences
                        
    # create list of occurences for each word (from pre-made chunks)
    def occurences(self, n):
        chunks = self.splitIntoChunks(self.text, n)
        self.vectors = self.toVectors(chunks)
        occurences = dict()
        for word in self.vocab:
            occurences[word] = []
        for x in self.vectors:
            for i in range(len(x)):
                if x[i]:
                    occurences[self.vocab[i]].append(x)
        return occurences

    # Splits list of words into lists of n words
    def splitIntoChunks(self, n=10):
        chunks = []
        for i in range(0, len(self.text), n):
            chunks.append(self.text[i:i+n])
        return chunks        

    # Transform chunks into vectors of length len(vocab) //one-hot
    def toVectors(self, chunks):
        temp = []
        n = len(self.vocab)
        for sentence in chunks:
            newVector = np.zeros(shape=(n,))
            for word in sentence:
                newVector[self.vocab.index(word)] = 1
            temp.append(newVector)
        return temp

if __name__ == "__main__":
    dataset = Data("picard.txt")
    print dataset.vocab[:10]
    print len(dataset.occurences[dataset.vocab[0]]), len(dataset.occurences[dataset.vocab[-1]])



