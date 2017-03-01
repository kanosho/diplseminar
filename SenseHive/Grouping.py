# -*- coding: utf-8 -*-
import numpy as np
import scipy as sp
import math
import codecs
from sklearn.cluster import KMeans
from textToVector import Data
import progressbar

# Multi-Prototype Vector-Space Model
class MPVSM:
    def __init__(self):
        self.dataset = None
        self.senses = dict()
        
    # only one sense per word for now
    # TODO: smart way to find ideal # of clusters
    def getBestK(self):
        bestK = 1
        print "best K:", bestK
        return bestK

    # for each word in vocabulary, cluster occurences.
    # every centroid then represents a sense; multiple senses per word
    def getSenses(self):
        K = self.getBestK()
        i=0
        with progressbar.ProgressBar(max_value=50) as bar:
            for word in self.dataset.vocab:
                i+=1
                if i%(len(self.dataset.vocab)/50) == 0:
                    bar.update(i)
                X = self.dataset.occurences[word]
                if len(X) >= K:
                    km = KMeans(n_clusters=K, init='k-means++').fit(X)
                    self.senses[word] = km.cluster_centers_
            
    # find n most similar words to given word (target)
    def findSimilar(self, target, n, mode='AVG'):
        distances = []
        targetSenses = self.senses[target]
        for word in self.dataset.vocab:
            similarities = sp.spatial.distance.cdist(targetSenses, self.senses[word])
            if mode=='AVG':
                sim = float(np.avg(similarities))
            elif mode=='MAX':
                sim = float(max(similarities))
            distances.append(sim)
        mostSimilar = list(np.array(self.dataset.vocab)[np.array(distances).argsort()[::-1][:n+1]])
        if target in mostSimilar:
            mostSimilar.remove(target)
        return mostSimilar

    # get n random words, print m most similar
    def test(self, n, m, mode):
        print "TEST: "+str(n)+" random words, "+str(m)+" most similar\n\n"
        sample = np.random.choice(self.dataset.vocab[50:300], n)
        for word in sample:
            similar = model.findSimilar(word, m, mode)
            print '['+word+']' + '\n' + ' '.join(similar)+'\n'

  
if __name__ == "__main__":

    model = MPVSM()
    # options: picard.txt, nahodi.txt, 1984.txt
    #model.dataset = Data("data/Picard.txt") # for fast testing. text too short for meaningful results
    model.dataset = Data("data/nahodi.txt", n=10, truncate=30000) # must truncate because memory error :<
    print "Data ready."
    print "10 most common words:", ', '.join(model.dataset.vocab[:10])
    print "Vocabulary size:", len(model.dataset.vocab)
    print "Calculating senses"
    model.getSenses()
    print "Done"
    model.test(10, 5, 'MAX')
