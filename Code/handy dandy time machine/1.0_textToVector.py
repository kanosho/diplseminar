# read all text
# use counter to count all unique words
# take most frequent N to learn
# change each sentece (or M words) into vectors
# return vectors as training set
#---------------------------------------------------------------
import numpy as np
import collections
import string

class Data:
    def __init__(self, filename, n=10, truncate=None):
        text = self.getCompleteWordList(filename)
        if truncate:
            text = text[:truncate]
        # TODO: lematizirati //MOLEX ?
        self.vocab = self.getWords(text)
        self.occurences = self.occurences(text, n)

    def occurences(self, text, n):
        chunks = self.splitIntoChunks(text, n)
        self.vectors = self.toVectors(chunks)

        # create list of occurences for each word
        occurences = dict()
        for word in self.vocab:
            occurences[word] = []
        for x in self.vectors:
            for i in range(len(x)):
                if x[i]:
                    occurences[self.vocab[i]].append(x)
        return occurences

    # Read whole text, split into list of words, ignore new lines and punctuation
    def getCompleteWordList(self, filename):
        text = open(filename, "r")
        mypunctuation = string.punctuation.replace('-', '') # ignore all punctuation except '-'
        text = text.read().lower().replace('\n',' ')
        text = text.translate(None, mypunctuation).split(' ')
        print text[:100]
        return text

    # Split list of words into lists of n words
    # TODO: ne po redu po 10 rijeci, nego za svaku rijec traziti 10 rijeci koji ih okruzuju
    def splitIntoChunks(self, text, n=10):
        chunks = []
        for i in range(0, len(text), n):
            chunks.append(text[i:i+n])
        return chunks        

    def splitIntoContexts(self, text, n=10):
        pass

        
    # Returns list of unique words in text (sorted by how common they are, desc)
    def getWords(self, text):
        cnt = collections.Counter(text)
        return [c[0] for c in cnt.most_common(len(cnt.keys()))]

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



