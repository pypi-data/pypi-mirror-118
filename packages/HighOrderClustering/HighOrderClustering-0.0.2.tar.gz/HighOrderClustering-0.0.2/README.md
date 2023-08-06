High order clustering algorithms
========

Author: Chen An, Cliburn Chan, Anru Zhang

This is the Python package for paper: "Exact Clustering in Tensor Block Model: Statistical Optimality and Computational Limit" by Rungang Han, Yuetian Luo, Miaoyan Wang and Anru Zhang (2020).

Usage:

from HighOrderClustering import clustering
clustering(y,r,T=10)
y: data
r: the number of clusters in each variable. If a variable is not to be clustered, set the corresponding value to be -1.


Citation:

@article{han2020exact, title={Exact Clustering in Tensor Block Model: Statistical Optimality and Computational Limit}, author={Han, Rungang and Luo, Yuetian and Wang, Miaoyan and Zhang, Anru R}, journal={arXiv preprint arXiv:2012.09996}, year={2020} }


Instruction:

prerequisite packages: numpy, scipy, pandas, sklearn.cluster.KMeans