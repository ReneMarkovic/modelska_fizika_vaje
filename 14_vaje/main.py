from helpers import generator, grouping
import matplotlib.pyplot as plt

N = 20
T = 400
K = 4
fs=0.005

t,X,group=generator.generiraj(N,K,T,fs)

dist_eu = grouping.dist_mat_M(X)
grouping.distance_cost_plot(dist_eu)