1. 因为如果加入一个新的数据点，可能value不是现在已有的一个centroid的mean (更复杂的情况是，如果新加入的是weight很大的数据点，更可能造成大的波动)
- 如果这样，甚至可能centroid数目过多，要缩减它的数目，做一个压缩，生成新的tdigest
- 这种情况过于复杂，不适合在过程中间加入差分隐私，合适的时间点应该是生成一个tdigest之后，可以将其模糊化发布
- 将所有的mean理解为attribute value, 将每个bin的count，理解为要模糊的数值，在它上面加上noise
- 转变为发布histogram的问题，global sensentivity是1，最经典的噪音就是Laplace(1/\epsilon),满足\epsilon dp (x)
2. 现在实现其算法：
借助了开源的t-digest实现，发现它借助了python数据包AccumulationTree来管理所有的centroid
为了给每一个centroid加上噪音，需要遍历所有的centroid，得到每个count，加上噪音
先写一个metafunction，加噪音的，把之前的dp元算法文件夹直接放过来作为utils
给tdigest类加函数，传参就是\epsilon, 
3. 为了感受tdigest的效果，除了原始数据包支持的求percentile的功能，可以加上画图可视化，展示tdigest，但是这可能需要限制一下有多少个centroid, 从小型数据，应该可以先实现，到规模更大的时候再说（从简单入手也是research的一般操作啊）
A:
  Kaggle
  streaming data  like (购物金额，dns query数目统计，) 
https://dl.acm.org/doi/pdf/10.1145/3460120.3484750
https://github.com/dp-cont/dp-cont

https://github.com/dp-cont/dp-cont/tree/main/data/dns￼

https://github.com/dp-cont/dp-cont/tree/main/user￼

How to implement：
对count值加噪音
Q:
1. 输入去建立tdigest的数据，此处只用了random(), 用什么别的分布的数据/ 真实的数据？
2. 加入的噪音，现在只用了Laplace
3. 如何衡量？对比实验怎么设计：
VS 
uniform-binning: histogram
hirachy dp  (bin-tree 最底层是histogram)
TianhaoWang
https://github.com/dp-cont/dp-cont/blob/main/range_estimator/hierarchy.py￼
TianhaoWang
http://www.vldb.org/pvldb/vol6/p1954-qardaji.pdf￼

- 比较不同噪音的效果 （咋比较？现在得到了结果数据，怎么分析和展示呢）
- 比较加噪音前后计算出的percentile
- 在不同分布的数据上做实验

2022.4.26
1.至少naive办法说得不要错啊;(虽然改变为了pub histogram的问题)
Q: 我发现第一步的bin step依赖数据集本身，这就不符合在bin value上加noise的前提条件？
这个本质矛盾怎么克服？
相比之下，一般的histogram发布，它bin这一步是和数据集无关的，所以可以后面加上噪音，以及涉及怎么分配budget
2.忽然在预感自己成为k, epsilon之类的调参侠。。。
3.还要勇于搞数据去尝试，注意下实验里面的比较是怎么做的

2022.5.15
开始coding抢救
对比实验，是不是还需要原始的数据的正确的结果。
我明白了，它对数据集采取了划分的办法，使用前一段不动，只采纳了后一段数据运行算法，

但是看明白了，TODO:
用存在数值大小的一维数据，才可以用t-digest，先给它建立实验仓库吧：
向其投喂数据，使用range询问，VS  (我发现hierarchy那边的range询问似乎并没有要求底层数据是从小到大的，只是按照index顺序选取了一段而已)

还是当数据集中有一些极值出现会有很大的干扰，怎么100行效果很好，10000行效果就稀烂呢？
1000行也还好

0.01 25:  delta影响的是centroid的极限size，K影响的是centroid的数目的极限
纠结要不要裁掉极值
有的办法是大于某个值我就全设成那个值
感觉可以都写
就阐述我的实验条件和实验结果

500行，各自20个询问，裁尾与不裁尾都做了
试一试替代，发现效果更差了，这是因为，尾部很长一块处理成了1500，但是centriod插值求解的时候其实会用到靠近左边一点点的数值，于是就差别很大。

这部分算啥？
小规模数据集，测试25,0.01设置下，t-digest对两种询问的回答情况。