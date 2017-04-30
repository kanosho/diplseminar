from sklearn.datasets import fetch_20newsgroups_vectorized
import logging

logging.basicConfig()
data = fetch_20newsgroups_vectorized().data

print "samples, features =",data.shape
print data[0]
