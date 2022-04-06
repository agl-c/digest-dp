from tdigest.dptdigest import TDigest
from numpy.random import random

digest = TDigest()
for x in range(50):
    digest.update(random())

print(digest.percentile(15))  # about 0.15, as 0.15 is the 15th percentile of the Uniform(0,1) distribution

# print(digest.C)
centroids = digest.centroids_to_list()
print(centroids)

digest.debug()

print("******************* Then we add noise *********************")
digest.anonymize()

noisy_centroids = []
for key in digest.noisy_C.keys():
    tree_values = digest.noisy_C.get_value(key)
    noisy_centroids.append({'m':tree_values.mean, 'c':tree_values.count})
print(noisy_centroids)