# import sys
# print(sys.path)

import enum
import matplotlib.pyplot as plt
import numpy as np
from tdigest.dptdigest import TDigest
#from numpy.random import random


digest = TDigest()
# we have to decide what values to feed?
for x in range(100):
    value = np.random.normal(0,1)  # -3 to 3 whp
#    digest.update(random())
    digest.update(value)

print("just a demo, percentile(15) should be around ??? ")
print(digest.percentile(15))  # about 0.15, as 0.15 is the 15th percentile of the Uniform(0,1) distribution

# C is a Accumulation Tree, one element in C is mean, centroid
print("look at the AVL tree")
print(digest.C) 

print("******************* here are original centroids******************")
centroids = digest.centroids_to_list()
print(centroids)

print("Now we want to give an empirical graph of CDF displaying the centroids")
# we use lines (x=mean, y= np.linspace(0,count，10000))
for i, key in enumerate(digest.C.keys()):
    # count = digest.C[key]
    cdf = digest.cdf(key)
    y = np.linspace(0, cdf, 10000)
    x = [key for i in range(10000)]
    plt.plot(x, y, color = 'xkcd:sky blue')

plt.xlabel('X value')
plt.ylabel('Cumulative Probability')
plt.title('Empirical Cumulative Density Function')
plt.gca().yaxis.set_label_coords(-0.1,0.8)
plt.show()




# digest.debug()

# print("******************* Then we add noise *********************")
# digest.anonymize()

# noisy_centroids = []
# for key in digest.noisy_C.keys():
#     tree_values = digest.noisy_C.get_value(key)
#     noisy_centroids.append({'m':tree_values.mean, 'c':tree_values.count})
# print(noisy_centroids)