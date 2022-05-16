import enum
from http.client import ImproperConnectionState
from random import random
from cv2 import mean
import matplotlib.pyplot as plt
from tdigest.dptdigest import TDigest
import numpy as np
import pickle
import pandas
import argparse
import sys

# randomly select range queries or specify all the queries with ml, mr
np.random.seed()
ml = [ 42, 54,  55,  82,  41,  67,  38,  62,  60, 137,  65,  54,  67,  88,  68,  50,  65,  39,
  72,  69]
mr = [ 67, 105,  69, 402,  69,  70,  77,  82,  67, 402,  72,  69,  82, 114,
 137, 228,  75,  75, 105,  77]


# redirect output to txt file
sys.stdout = open("res_5000rows_0.01_25_cutting_tail.txt",'w')

# load and preprocess data
# df = pandas.read_csv("./data/accidential_drug_deaths.csv", usecols=['Age'])
df = pandas.read_csv("./data/wifi_on_ice.csv", nrows=5000)
data_o = df.to_numpy() 
n = len(data_o)
print('the total number of raw samples is %d' % n)

data = []
for i in range(n):
    # since it has only one column, we get the last part 'link_ping' and translate it into int value
    value = data_o[i][0].split(';')[-1]
    if(value == ''):
        n-=1
        continue
    # if(int(value)>1500):
    #     print("replace one sample with extrmely large value as 1500")
    #     data.append(1500)
    #     continue
    if(int(value)>1500):
        n-=1 
        continue
    data.append(int(value))

print("the num of valid elements in data is %d" % len(data))
sorted_data = np.sort(data)
len = len(sorted_data)
unique_data = np.unique(data)

# then create the t-digest
digest = TDigest()
for i in range(n):
    digest.update(data[i])


parser=argparse.ArgumentParser(description='exp of t-digest range queries')
parser.add_argument('--n', type=int, default=500, help="specify the num of total samples")
parser.add_argument('--type', type=str, default='uniform', help="specify the range query type")
parser.add_argument('--num', type=int, default=20, help="specify the num of queries to run")
args = parser.parse_args()


def range_query_creator():
    type = args.type
    num = args.num
    l_array = np.zeros(num)
    r_array = np.zeros(num)

    if type == "uniform":
        l_array = np.random.choice(unique_data,num,replace=True)
        for i in range(num):
            # make sure r is > l, the problem is when l==r, always ans 0, but that's wrong
            # choose from unique, cannot be the same
            while(r_array[i] <= l_array[i]):
                r_array[i]=np.random.choice(unique_data)
            print('create a range query [%d,%d]' % (l_array[i],r_array[i]))
    print("now we create the range queries",l_array,r_array)
    return l_array, r_array


def run_range_queries(l_array, r_array):
    num = args.num
    err = []
    for i in range(num):
        l = l_array[i]
        r = r_array[i]
        print('now we run the query [%d,%d]' % (l,r))
     
        sp = np.where(sorted_data == l)
        s = sp[0][0]
        ep = np.where(sorted_data == r)
        e = ep[0][-1]
        true_count = e-s+1
        print('the true count is %d' % true_count)

        est_count = digest.range_count(l,r)
        print('the t-digest estimated count is %d' % est_count)
        err.append(np.abs(true_count-est_count))

    mean_err = np.mean(err)
    mse = np.var(err)
    print("in %d range queries, the mean absolute err is %f, and the var of err is %f" % (num, mean_err, mse))
 

def percentile_query_creator():
    num = args.num
    # different percentiles
    q = np.random.choice(101,num,replace=False)
    print("now we create the percentile queries", q)
    return q 

def run_percentile_queries(q):
    index = [int(j/100.0*(len-1)) for j in q]
    err = []
    num = args.num
    for i in range(num):
        est = digest.percentile(q[i])
        true_res = sorted_data[index[i]]
        err.append(np.abs(true_res-est))
        print('the quantile %d returns estimate %f and true res %d' % (q[i], est, true_res))
    mean_err = np.mean(err)
    var_err = np.var(err)
    print('in %d quantile queries, the mean err is %f, and the var of err is %f' % (num, mean_err, var_err))



# percentile queries
q = percentile_query_creator()
run_percentile_queries(q)

# range queries
l_array, r_array = range_query_creator()
print('now we run the queries with ml, mr')
run_range_queries(ml, mr)




# display some features
num_centroids = digest.__len__()
print('num of centroids is %d' % num_centroids)

print('we can see 1500ms is around the percentile')
print(digest.cdf(3000))

print("Now we want to give an empirical graph of CDF displaying the centroids")
sys.stdout.close()

# we use lines (x=mean, y= np.linspace(0,count,10000))
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

