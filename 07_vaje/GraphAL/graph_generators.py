from .graph_structure import Graph
import numpy as np
import random

def random_graph(n: int, p: float):
    G = Graph()
    [G.add_node(i) for i in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < p:
                G.add_edge(i, j)
    return G

def regular_graph(n: int, k: int):
    G = Graph()
    [G.add_node(i) for i in range(n)]
    for i in range(n):
        for j in range(1, k//2 + 1):
            G.add_edge(i, (i+j) % n)     # povezava (i, i-j) nastane pri vozlišču i-j
    return G

def Morita(delta,N,ka):
    pos = np.random(0,1,[N,2])   # namerna napaka: popravek je domača naloga vaje 08
    I=np.zeros([N,N],float)
    for i in range(N):
        for j in range(i+1,N,1):
            dx2=(pos[i,0]-pos[j,0])**2
            dy2=(pos[i,1]-pos[j,1])**2
            I[i,j]=pow(np.sqrt(dx2+dy2),delta)
            I[j,i]=I[i,j]

    #2) We need to define the fitness values
    fitness=np.zeros([N],float)
    for i in range(N):
        y=(float(i)+1)/float(N) #base value
        n=1/(1-float(2.5)) #exponent value
        fitness[i]=pow(y,n)

    #for speeding up the while loop
    for i in range(N):
        for j in range(i+1,N,1):
            I[i,j]=fitness[i]*fitness[j]/(I[i,j])
            I[j,i]=I[i,j]

    #3)We would like to build a network, which has on average 5 connections
    THETA=100.0
    kavg = 0.0#average connection of the network
    k = ka #desired connectivity of the network
    print("START TEST",abs(kavg - k)>0.1)
    while abs(kavg - k)>0.1:
        G=Graph()
        for i in range(N):
            G.add_node(i)
        for i in range(N):
            for j in range(i+1,N,1):
                if I[i,j]>THETA:
                    G.add_edge(i,j)
        kavg=np.mean([G.degree(i) for i in G])
        if kavg<k: #treshold is to large
            THETA*=0.98
        if kavg>k: #treshold is to low
            THETA*=1.01
    print("START TEST",abs(kavg - k)>0.1,kavg)
    return G