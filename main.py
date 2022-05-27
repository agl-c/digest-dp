import enum
from http.client import ImproperConnectionState
# import imp
from random import random
from turtle import st
from cv2 import mean
import matplotlib.pyplot as plt
from tdigest.dptdigest import TDigest
import numpy as np
import pickle
import pandas
import argparse
import sys
import time
import tracemalloc

# randomly select range queries or specify all the queries with ml, mr
np.random.seed(42)

PL = [1307,34,2660,332,125,159,152,3513,80,164,71,177,1702,
1769,246,502,411,1551,1719,73,86,493,289,164,157,212,46,376,
416,65,101,341,55,159,47,119,376,76,3347,101,37,99,163,144,
3366,41,341,478,79,718,1726,60,143,64,53,272,131,45,376,119,
1722,512,3347,188,1247,104,112,335,702,878,37,443,762,247,
826,878,1177,411,3422,108,83,120,87,1204,135,289,56,61,95,
118,163,61,36,42,341,103,723,69,1734,86 ]

PR = [1769,2556,3408,466,188,762,2660,4293,124,2298,314,463,
2556,2026,463,1442,3513,1721,3513,126,105,3422,492,1707,197,
1875,82,1725,1243,508,4180,3403,163,197,433,1725,1204,160,
3422,458,502,1110,1110,439,3408,1307,1726,538,502,723,2552,
163,678,215,3218,2026,137,313,458,224,1734,1091,3408,723,2591,
1110,2298,522,4569,2026,111,826,2556,262,1779,1726,3403,629,
3513,328,272,177,109,2015,177,4180,1442,72,479,139,250,362,
384,118,723,627,1875,136,2273,178 ]

AL = [57,57,19,28,55,42,50,58,33,23,60,29,34,20,21,33,60,38,
47,52,32,81,45,71,75,38,71,66,32,26,32,30,51,32,26,28,65,36,
44,46,29,75,78,41,29,72,23,15,56,27,55,78,59,29,15,70,77,32,
70,42,19,31,20,69,17,35,43,72,18,25,29,48,51,78,45,45,45,58,
77,56,77,32,75,47,70,40,81,52,74,62,24,68,33,52,38,68,63,39,
47,41]

AR = [63,64,74,67,74,75,65,73,84,49,61,45,64,31,36,34,67,56,
77,62,73,84,48,73,77,53,72,75,73,61,36,64,59,59,57,71,84,63,
62,71,71,81,81,46,39,84,34,21,74,70,57,81,62,50,65,74,84,38,
78,63,37,56,67,70,36,40,78,74,63,51,33,54,75,81,71,59,68,72,
78,65,84,37,84,68,77,46,84,58,75,84,47,77,70,56,60,70,71,63,
59,73]

NL = [62,100,73,90,62,111,73,52,97,57,44,124,90,113,92,57,93,
150,114,51,128,147,108,43,21,112,119,82,30,66,39,51,108,63,142,
98,96,141,100,71,56,93,82,64,69,130,104,107,76,108,65,83,147,
81,137,150,145,166,107,106,89,59,140,153,144,69,102,61,112,149,
122,125,111,80,88,70,43,169,121,73,133,43,110,38,148,80,113,64,
161,21,81,68,65,125,111,52,128,75,73,35]

NR = [131,148,153,161,65,169,140,150,105,95,150,159,118,142,133,
133,141,171,166,80,155,154,126,123,77,147,129,127,97,116,154,52,
117,132,145,142,122,147,110,132,113,150,94,123,104,171,156,155,
93,144,156,127,149,101,141,166,161,171,131,124,90,75,159,182,151,
105,147,154,150,150,129,141,141,146,96,79,107,171,147,78,140,72,
132,148,166,150,126,124,169,136,147,108,100,148,151,134,159,103,
111,135]

q = [84,93,98,76,92,21,94,18,27,49,95,30,78,5,12,40,14,44,19,45,
6,42,55,85,28,50,65,38,74,22,82,81,41,48,90,24,26,63,100,13,0,53,
54,33,15,72,97,86,67,83,16,77,2,75,69,10,39,25,35,29,11,8,87,57,
60,59,61,37,71,51,34,4,52,91,20,3,66,58,79,89,23,32,56,73,1,70,
7,88,43,17,68,99,80,46,9,31,96,62,64,47,84,93,98,76,92,21,94,18,
27,49,95,30,78,5,12,40,14,44,19,45,6,42,55,85,28,50,65,38,74,22,
82,81,41,48,90,24,26,63,100,13,0,53,54,33,15,72,97,86,67,83,16,
77,2,75,69,10,39,25,35,29,11,8,87,57,60,59,61,37,71,51,34,4,52,
91,20,3,66,58,79,89,23,32,56,73,1,70,7,88,43,17,68,99,80,46,9,
31,96,62,64,47]

parser=argparse.ArgumentParser(description='exp of t-digest queries')
parser.add_argument('--K', type=float, default=25, help='specify the K factor in t-digest restrictions')
parser.add_argument('--delta', type=float, default=0.01, help='specify the delta factor in t-digest restrictions')
parser.add_argument('--dataset',type=str, default= 'normal_data_200000r', help='specify the name of data in result file')
parser.add_argument('--name',type=str, default='normal', help='specify the name of data in result file')
parser.add_argument('--n', type=int, default=200000, help="specify the num of total samples")
parser.add_argument('--type', type=str, default='uniform', help="specify the range query type")
parser.add_argument('--num', type=int, default=100, help="specify the num of queries to run")
parser.add_argument('--x', type=str, default='x', help='specify the name of x value')
args = parser.parse_args()


# redirect output to txt file
# accidential_drug_deaths  normal_data_5000r 49733rows_link_ping  normal_data_200000r
res_name = f'{args.dataset}_K_{args.K}delta_{args.delta}_[).txt'
sys.stdout = open(res_name, 'w')

# sys.stdout = open("Age_5000rows_0.01_25.txt",'w')
# sys.stdout = open('ping_5000rows_0.01_25.txt','w')
# sys.stdout = open('normal_5000rows_0.01_50.txt','w')

# load and preprocess data
# df = pandas.read_csv("./data/accidential_drug_deaths.csv", usecols=['Age'], nrows=5000)
df = pandas.read_csv(f"../data/{args.dataset}.csv", usecols=[args.x],nrows=args.n)
# df = pandas.read_csv('./data/normal_data_5000r.csv', usecols = ['x'], nrows = 5000)


data_o = df.to_numpy() 
n = len(data_o)
print('the total number of raw samples is %d' % n)

data = []
for i in range(n):
    # since it has only one column, we get the last part 'link_ping' and translate it into int value
    # value = data_o[i][0].split(';')[-1]
    value = data_o[i][0]
    # if(value == ''):
    #     n-=1
    #     continue
    # if(int(value)>1500):
    #     print("replace one sample with extrmely large value as 1500")
    #     data.append(1500)
    #     continue
    # if(int(value)>1500):
    #     n-=1 
    #     continue
    data.append(int(value))

print("the num of valid elements in data is %d" % len(data))
sorted_data = np.sort(data)
len = len(sorted_data)
unique_data = np.unique(data)

def range_query_creator(pre=200):
    type = args.type
    num = args.num
    l_array = np.zeros(pre)
    r_array = np.zeros(pre,int)

    if type == "uniform":
        l_array = np.random.choice(unique_data,pre,replace=True)
        for i in range(pre):
            # make sure r is > l, the problem is when l==r, always ans 0, but that's wrong
            # choose from unique, cannot be the same
            while(r_array[i] < l_array[i]):
                r_array[i]=np.random.choice(unique_data)
            # print('create a range query [%d,%d]' % (l_array[i],r_array[i]))
        
        tot = 0 
        L = []
        R = []
        for i in range(pre):
            if r_array[i] == l_array[i]:
                continue
            L.append(l_array[i])
            R.append(r_array[i])
            tot += 1
            if(tot == 100):
                break

    return L, R


def run_range_queries(l_array, r_array):
    num = args.num
    err = []
    tot = 0 
    for i in range(num):
        l = l_array[i]
        r = r_array[i]
        if(l == r):
            continue
        tot += 1
        print('now we run the query [%d,%d)' % (l,r))
     
        sp = np.where(sorted_data == l)
        s = sp[0][0]
        ep = np.where(sorted_data == r)
        e = ep[0][0]
        true_count = e-s
        print('the true count is %d' % true_count)

        est_count = digest.range_count(l,r)
        print('the t-digest estimated count is %d' % est_count)
        err.append(np.abs(true_count-est_count))

    mean_err = np.mean(err)
    mse = np.var(err)
    print("in %d range queries, the mean absolute err is %f, and the var of err is %f" % (tot, mean_err, mse))

    return    


def run_range_queries1(l_array, r_array):
    print('this version true count is num of samples in (l,r)')
    num = args.num
    err = []
    tot = 0 
    for i in range(num):
        l = l_array[i]
        r = r_array[i]
        if(l == r):
            continue
        tot += 1
        print('now we run the query (%d,%d)' % (l,r))
     
        sp = np.where(sorted_data == l)
        s = sp[0][-1]
        ep = np.where(sorted_data == r)
        e = ep[0][0]
        true_count = e-s-1
        print('the true count is %d' % true_count)

        est_count = digest.range_count(l,r)
        print('the t-digest estimated count is %d' % est_count)
        err.append(np.abs(true_count-est_count))

    mean_err = np.mean(err)
    mse = np.var(err)
    print("in %d range queries, the mean absolute err is %f, and the var of err is %f" % (tot, mean_err, mse))

    return        


def run_range_queries2(l_array, r_array):
    print('this version true count is num of samples in (l,r]')
    num = args.num
    err = []
    tot = 0 
    for i in range(num):
        l = l_array[i]
        r = r_array[i]
        if(l == r):
            continue
        tot += 1
        print('now we run the query (%d,%d]' % (l,r))
     
        sp = np.where(sorted_data == l)
        s = sp[0][-1]
        ep = np.where(sorted_data == r)
        e = ep[0][-1]
        true_count = e-s
        print('the true count is %d' % true_count)

        est_count = digest.range_count(l,r)
        print('the t-digest estimated count is %d' % est_count)
        err.append(np.abs(true_count-est_count))

    mean_err = np.mean(err)
    mse = np.var(err)
    print("in %d range queries, the mean absolute err is %f, and the var of err is %f" % (tot, mean_err, mse))

    return        


def percentile_query_creator():
    num = args.num
    # different percentiles
    q = np.random.choice(101,num,replace=False)
    print("now we create the percentile queries")
    for i in range(num):
        print(q[i], end=',')
    return q 

def run_percentile_queries(q):
    print('run percentile queries')
    index = [int(j/100.0*(len-1)) for j in q]
    err = []
    num = args.num
    for i in range(num):
        est = digest.percentile(q[i])
        true_res = sorted_data[index[i]]
        err.append(np.abs(true_res-est))
        print('the percentile %d returns estimate %f and true res %d' % (q[i], est, true_res))
    mean_err = np.mean(err)
    var_err = np.var(err)
    print('in %d percentile queries, the mean err is %f, and the var of err is %f' % (num, mean_err, var_err))


# q = percentile_query_creator()
# run_percentile_queries(q)

l_array, r_array = range_query_creator()

st = time.time()
tracemalloc.start()
# then create the t-digest
digest = TDigest()
for i in range(n):
    digest.update(data[i])
run_range_queries(l_array, r_array)
# run_range_queries1(NL,NR)

ed = time.time()
elapse = (ed-st)*1000
print('the elpased time in t-digest range-exp is',elapse, "milliseconds")

print(tracemalloc.get_traced_memory())
tracemalloc.stop()


# display some features
num_centroids = digest.__len__()
print('num of centroids is %d' % num_centroids)

# print('we can see 1500ms is around the percentile', digest.cdf(1500))
sys.stdout.close()


def display_cdf():
    print("Now we want to give an empirical graph of CDF displaying the centroids")
    # we use lines (x=mean, y= np.linspace(0,count,10000))
    for i, key in enumerate(digest.C.keys()):
    # count = digest.C[key]
        cdf = digest.cdf(key)
        y = np.linspace(0, cdf, 10000)
        x = [key for i in range(10000)]
        plt.plot(x, y, color = 'xkcd:sky blue')

    plt.xlabel('X value')
    plt.ylabel('Cumulative Probability')
    plt.title('Empirical CDF display of ping Data t-digest')
    plt.gca().yaxis.set_label_coords(-0.1,0.8)
    plt.show()

# display_cdf()