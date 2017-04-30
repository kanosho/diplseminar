# -*- coding: utf-8 -*-
import numpy as np
import scipy as sp
import math
import codecs
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics.pairwise import cosine_similarity
from spherecluster import VonMisesFisherMixture
from textToVector_temp import Data

# Multi-Prototype Vector-Space Model
class MPVSM:
    def __init__(self, K=1):
        self.K=K
        self.dataset = None
        self.senses = dict()
        self.temp_vocab = []

    # for each word in vocabulary, cluster contexts.
    # every centroid then represents a sense; multiple senses per word
    def get_senses(self):
        for word in self.dataset.vocab:
            X = np.array(self.dataset.contexts[word])
            if len(X)>= 1:
                #vmf_soft = VonMisesFisherMixture(n_clusters=self.K, posterior_type='soft').fit(X)
                kmeans = MiniBatchKMeans(n_clusters=self.K, init='k-means++').fit(X)
                self.senses[word] = kmeans.cluster_centers_
                self.temp_vocab.append(word)
                
            
    # find n most similar words to given word (target)
    def find_similar(self, target, n, mode='AVG'):
        X = self.senses[target]
        D = []
        for word in self.temp_vocab:
            Y = self.senses[word]
            sim = cosine_similarity(X,Y)
            if mode == 'AVG':
                sim = sum(sim)/(len(X)*len(Y))
            elif mode == 'MAX':
                sim = max(sim)
            D.append(sim[0])

        mostSimilar = list(np.array(self.temp_vocab)[np.argsort(D)[-n-1:]])
        mostSimilar.remove(target)
        return mostSimilar[::-1]

    # get n random words, print m most similar
    def test(self, n, m, mode):
        #out = codecs.open('out.txt', 'w')
        #out.write("TEST: "+str(n)+" random words, "+str(m)+" most similar\n\n")
        print "TEST: "+str(n)+" random words, "+str(m)+" most similar\n\n"
        sample = np.random.choice(self.temp_vocab[50:500], n)
        for word in sample:
            similar = model.find_similar(word, m, mode)
            #out.write('['+word+']' + '\n' + ' '.join(similar)+'\n\n')
            print '[',word,']','\n',' '.join(similar),'\n'
        #out.close()

  
if __name__ == "__main__":

    model = MPVSM()
    # options: picard.txt, nahodi.txt, 1984.txt
    model.dataset = Data("data/hrv/nahodi.txt", N=10) # must truncate because memory error :<
    print "10 most common words:", ', '.join(model.dataset.vocab[:10])
    model.get_senses()
    model.test(20, 5, 'MAX')

    # Trenutni rezultat: vrati one rijeci s kojima je najcesce bila u recenici (npr djeca -> napustena)
