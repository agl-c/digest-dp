from tdigest import TDigest
from numpy.random import random

digest = TDigest()
for x in range(500):
    digest.update(random())

print(digest.percentile(15))  # about 0.15, as 0.15 is the 15th percentile of the Uniform(0,1) distribution

print(digest)

