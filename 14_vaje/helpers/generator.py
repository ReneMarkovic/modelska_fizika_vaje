import numpy as np
import matplotlib.pyplot as plt


def f(to:float,A:float,T:float,theta:float):
    return A*np.sin(np.pi*2.0/to*np.arange(0,T,1)+theta)+np.random.normal(0,0.05,T)

def generiraj(N:int, K: int, T:int, fs:float=0.1,plot:bool=False)->list:
    '''
    Ustvarili bomo N časovnih vrst. Vsaka časovna vrsta bo sestavljena iz Nt točk.
    Ki jih porazdelimo v K skupin. Za vsako časovno vrsto bomo izbrali naključno
    frekvenco o[k] in amplitudo a[k]. Pri čemer bodo frekvence znotraj skupine bolj 
    homogene. Funkcija nam vrne seznam, ki vsebuje:
    - t: polje časovnih točk
    - X: matrika časovnih vrst
    - group: slovar, ki pove kateri časovni vrsti pripada k-ta časovna vrsta
    '''
    group={}
    t=np.linspace(0,T*fs,T)
    o=np.zeros([K],float)
    for k in range(K):
        o[k]=1+19.0*np.random.random()
        print(o[k])
    X=np.zeros([N,T],float)
    for kk in range(N):
        k=kk%K
        a=0.5*np.random.random()+0.2
        scale=o[k]*(1+0.1*(np.random.random()-0.5))

        oo=o[k]*scale
        X[kk]=a*np.sin(o[k]*t)+np.random.randn(T)*a/10
        group[kk]=f'C{k}'
        
        
    if plot:
        plt.figure(figsize=(15,5))
        for k in range(N):
            plt.plot(t,X[k],color=f'{group[k]}')
        plt.legend()
        plt.show()
    return [t,X,group]
