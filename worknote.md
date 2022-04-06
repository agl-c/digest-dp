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
发现一个函数  
def centroids_to_list(self):
        """
        Returns a Python list of the TDigest object's Centroid values.

        """
        centroids = []
        for key in self.C.keys():
            tree_values = self.C.get_value(key)
            centroids.append({'m':tree_values.mean, 'c':tree_values.count})
        return centroids
可以方便地对它操作吧

对于count值加了噪音的结果，难道不会是浮点数，那会不会很奇怪

