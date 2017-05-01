# -*- coding: utf-8 -*-
import numpy as np
import scipy as sp
import math
import codecs
from sklearn.cluster import MiniBatchKMeans

#from spherecluster import VonMisesFisherMixture
from preprocess import Data

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
        f = open('data\centroids', 'w')
        for word in self.dataset.vocab:
            X = np.array(self.dataset.contexts[word])
            if len(X)>= 1:
                #vmf_soft = VonMisesFisherMixture(n_clusters=self.K, posterior_type='soft').fit(X)
                kmeans = MiniBatchKMeans(n_clusters=self.K, init='k-means++').fit(X)
                self.senses[word] = kmeans.cluster_centers_
                self.temp_vocab.append(word)
                f.write(str(word))
                for C in kmeans.cluster_centers_:
                    f.write("\n$")
                    for x in C: 
                        f.write(" "+str(x))
                f.write("\n")
        f.write('#')
        f.close()

  
if __name__ == "__main__":

    model = MPVSM()
    # options: picard.txt, nahodi.txt, 1984.txt
    model.dataset = Data("data/hrv/picard.txt", N=10, truncate=20000) # must truncate because memory error :<
    print "10 most common words:", ', '.join(model.dataset.vocab[:10])
    model.get_senses()

    # Trenutni rezultat: vrati one rijeci s kojima je najcesce bila u recenici (npr djeca -> napustena)
