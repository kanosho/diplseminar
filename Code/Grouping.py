# -*- coding: utf-8 -*-
import numpy as np
import scipy as sp
import math
import codecs
from sklearn.cluster import KMeans
from textToVector import Data

# Multi-Prototype Vector-Space Model
class MPVSM:
    def __init__(self):
        self.dataset = None
        self.senses = dict()
        
    # only one sense per word for now
    # TODO: smart way to find ideal # of clusters
    def getBestK(self):
        return 1

    # for each word in vocabulary, cluster occurences.
    # every centroid then represents a sense; multiple senses per word
    def getSenses(self):
        for word in self.dataset.vocab:
            X = self.dataset.occurences[word]
            if len(X) >= self.getBestK():
                km = KMeans(n_clusters=self.getBestK(), init='k-means++').fit(X)
                self.senses[word] = km.cluster_centers_
            
    # find n most similar words to given word (target)
    # TODO: some smarter way
    def findSimilar(self, target, n, mode='AVG'):
        distances = []
        targetSenses = self.senses[target]

        similarity = lambda u,v: np.dot(u, v)/(math.sqrt(np.dot(u, u)) * math.sqrt(np.dot(v, v)))
        for word in self.dataset.vocab:
            similarities = [similarity(u,v) for u in targetSenses for v in self.senses[word]]
            if mode=='AVG':
                sim = sum(similarities)/len(targetSenses)**2
            elif mode=='MAX':
                sim = max(similarities)
            distances.append(sim)

        mostSimilar = list(np.array(self.dataset.vocab)[np.argsort(distances)[-n-1:]])
        mostSimilar.remove(target)
        return mostSimilar[::-1] #!!!!!!!!!!!!!!!

    # get n random words, print m most similar
    def test(self, n, m, mode):
        #out = codecs.open('out.txt', 'w')
        #out.write("TEST: "+str(n)+" random words, "+str(m)+" most similar\n\n")
        print "TEST: "+str(n)+" random words, "+str(m)+" most similar\n\n"
        sample = np.random.choice(self.dataset.vocab[50:500], n)
        for word in sample:
            similar = model.findSimilar(word, m, mode)
            #out.write('['+word+']' + '\n' + ' '.join(similar)+'\n\n')
            print '['+word+']' + '\n' + ' '.join(similar)+'\n'
        #out.close()

  
if __name__ == "__main__":

    model = MPVSM()
    #model.dataset = Data("data/Picard.txt") # for fast testing. text too short for meaningful results
    # options: picard.txt, nahodi.txt, 1984.txt
    model.dataset = Data("data/nahodi.txt", n=10, truncate=30000) # must truncate because memory error :<
    print "10 most common words:", ', '.join(model.dataset.vocab[:10])
    model.getSenses()
    model.test(20, 5, 'MAX')

    # Trenutni rezultat: vrati one rijeci s kojima je najcesce bila u recenici (npr djeca -> napustena)
