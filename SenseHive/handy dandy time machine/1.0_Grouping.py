import numpy as np
import scipy as sp
import math
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from textToVector import Data
from prettytable import PrettyTable

# Multi-Prototype Vector-Space Model
class MPVSM:
    def __init__(self):
        self.dataset = None
        self.senses = dict()
        
    # only one sense per word for now
    # TODO: smart way to find ideal # of clusters
    def getBestK(self):
        return 1

    # find n most similar words to given word (target)
    # TODO: some smarter way
    def findSimilar(self, target, n):
        distances = []
        K = len(self.senses[target])
        targetSenses = self.senses[target]

        # AvgSim
        similarity = lambda u,v: np.dot(u, v)/(math.sqrt(np.dot(u, u)) * math.sqrt(np.dot(v, v)))
        for word in self.dataset.vocab:
            avgSim = sum([similarity(u,v) for u in targetSenses for v in self.senses[word]])/K**2
            distances.append(avgSim)

        mostSimilar = np.array(self.dataset.vocab)[np.argsort(distances)[-n:]]
        return mostSimilar[::-1]
        
    # for each word in vocabulary, cluster occurences.
    # every centroid then represents a sense; multiple senses per word
    def getSenses(self):
        for word in self.dataset.vocab:
            X = self.dataset.occurences[word]
            km = KMeans(n_clusters=self.getBestK()).fit(X)
            self.senses[word] = km.cluster_centers_

    # get 10 random words, print 5 most similar
    def test(self, n, m):
        pt = PrettyTable(['word', ''] + range(1, m+1))
        sample = np.random.choice(self.dataset.vocab, n)
        for word in sample:
            similar = model.findSimilar(word, m)
            pt.add_row([word, ''] + [str(s) for s in similar])
        print "\nTEST: "+str(n)+" random words, "+str(m)+" most similar"
        print pt

  
if __name__ == "__main__":

    model = MPVSM()
    model.dataset = Data("Picard.txt") # for fast testing. text too short for meaningful results
    #model.dataset = Data("nahodi.txt", n=20, truncate=10000) # must truncate because memory error :<
    model.getSenses()
    model.test(20, 5)

    # Trenutni rezultat: vrati one rijeci s kojima je najcesce bila u recenici (npr djeca -> napustena)
