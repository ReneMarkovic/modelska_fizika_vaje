import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def Minkowski(X,Y,p):
    diff=[np.power(X[i]-Y[i],p) for i in range(len(X))]
    return np.sum(diff)/len(X)

def dist_mat_M(X:np.array):
    '''
    Funkcija nam izračuna matriko razdalj med časovnimi vrstami.
    '''
    N=len(X)
    dist_M=np.zeros([N,N],float)
    for i in range(N):
        for j in range(i+1,N,1):
            dist_M[i,j]=Minkowski(X[i,:],X[j,:],2.0)
            dist_M[j,i]=dist_M[i,j]
    return dist_M

def distance_cost_plot(distances,TH=0.01,cmap='jet'):
    fig,(ax1,ax2) = plt.subplots(1,2,figsize=(12,5))
   
    im = ax1.imshow(distances, interpolation='nearest', cmap=cmap,origin='lower') 
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    fig.colorbar(im, ax=ax1)
    
    im2=ax2.imshow(distances<TH, cmap='Greys', interpolation='none',origin='lower') 
    fig.colorbar(im2, ax=ax2)
    plt.tight_layout()
    plt.show()

def correlarion(X,Y):
    mx=np.mean(X)
    my=np.mean(Y)
    dx=X-mx
    dy=Y-my
    
    dx2=dx**2
    dy2=dy**2

    return np.sum(dx*dy)/np.sqrt((np.sum(dx2)*np.sum(dy2)))