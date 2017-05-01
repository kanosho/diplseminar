from train import MPVSM
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# read file with centroids
def read_data(filename):
    f = open(filename, 'r')
    model = MPVSM()
    word = f.readline()
    model.senses[word]=[]
    model.temp_vocab.append(word)
    counting = True
    K = 0
    while True:
        line = f.readline()
        line = line.split(' ')
        if line[0] == '$':
            if counting: K += 1
            centroid = np.array(map(float, line[1:]))
            model.senses[word].append(centroid)
        elif line[0] == '#':
            break
        else:
            word = line[0]
            model.temp_vocab.append(word)
            self.K = K
            counting = False
    return model

# find n most similar words to given word (target)
def find_similar(model, target, n, mode='AVG'):
    X = model.senses[target]
    D = []
    for word in model.temp_vocab:
        Y = model.senses[word]
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
def test(model, n, m, mode):
    #out = codecs.open('out.txt', 'w')
    #out.write("TEST: "+str(n)+" random words, "+str(m)+" most similar\n\n")
    print "TEST: "+str(n)+" random words, "+str(m)+" most similar\n\n"
    sample = np.random.choice(model.temp_vocab[50:500], n)
    for word in sample:
        similar = find_similar(model, word, m, mode)
        #out.write('['+word+']' + '\n' + ' '.join(similar)+'\n\n')
        print '[',word,']','\n',' '.join(similar),'\n'
        
if __name__ == "__main__":
    model = read_data('data\centroids')
    test(model, 20, 5, 'MAX')
