1. 因为如果加入一个新的数据点，可能value不是现在已有的一个centroid的mean (更复杂的情况是，如果新加入的是weight很大的数据点，更可能造成大的波动)
- 如果这样，甚至可能centroid数目过多，要缩减它的数目，做一个压缩，生成新的tdigest
- 这种情况过于复杂，不适合在过程中间加入差分隐私，合适的时间点应该是生成一个tdigest之后，可以将其模糊化发布
- 将所有的mean理解为attribute value, 将每个bin的count，理解为要模糊的数值，在它上面加上noise
- 转变为发布histogram的问题，global sensentivity是1，最经典的噪音就是Laplace(1/\epsilon),满足\epsilon dp,
2. 现在实现其算法：
借助了开源的t-digest实现，发现它借助了python数据包AccumulationTree来管理所有的centroid
为了给每一个centroid加上噪音，需要遍历所有的centroid，得到每个count，加上噪音
先写一个metafunction，加噪音的，把之前的dp元算法文件夹直接放过来作为utils
给tdigest类加函数，传参就是\epsilon, 
3. 为了感受tdigest的效果，除了原始数据包支持的求percentile的功能，可以加上画图可视化，展示tdigest，但是这可能需要限制一下有多少个centroid, 从小型数据，应该可以先实现，到规模更大的时候再说（从简单入手也是research的一般操作啊）

How to implement：
对count值加噪音
Q:
1. 输入去建立tdigest的数据，此处只用了random(), 用什么别的分布的数据/ 真实的数据？
2. 加入的噪音，现在只用了Laplace
3. 如何衡量？对比实验怎么设计：
- 比较不同噪音的效果 （咋比较？现在得到了结果数据，怎么分析和展示呢）
- 比较加噪音前后计算出的percentile
- 在不同分布的数据上做实验
- 

论文组织：
1. 介绍tdigest，dp的理论基础
2. 介绍工程的组成部分
3. 介绍各个实验，结果分析
4. 不足和有待解决的问题

