import numpy as np
import time

def init_S(Nx:int = 21, Ny:int = 21):
    """
    S to funkcijo inicializiram polje za zrna peska.
    
    Nx in Ny definirata velikost matrike.
    """
    S = np.zeros([Nx,Ny],int)
    return S

def init_F(Nx:int, Ny:int, pos, st_zrn:int):
    F = np.zeros([Nx,Ny],int)
    F[pos[0],pos[1]]=st_zrn
    return F

def TBW_model(i:int,j:int,S:np.array, Sth:int):
    global Velikost_plazu
    ip = i + 1
    im = i - 1
    jp = j + 1
    jm = j - 1
    Nx, Ny = S.shape
    if S[i,j]>Sth:
        Velikost_plazu += 1
        
        S[i,j] -= 4
        
        if im>-1:
            S[im,j] += 1
            TBW_model(im,j,S,Sth)
        
        if ip < Nx:
            S[ip,j] += 1
            TBW_model(ip,j,S,Sth)
        
        if jm > -1:
            S[i,jm] += 1
            TBW_model(i,jm,S,Sth)
        
        if jp<Ny:
            S[i,jp] += 1
            TBW_model(i,jp,S,Sth)
    return S

def print_control(end_time, start_time, seznam_plazov, iteracija, S):
    dt = end_time - start_time # rezultat je v sekundah
    Zasedena_polja = np.sum(S>0)
    Nx = S.shape[0]
    Ny = S.shape[1]
    frac = Zasedena_polja/(Nx*Ny)
    print(f"Čas izvedbe 100 iteracij je {dt:.2f} s. Delež zasedenih polj je {frac:.3f}.")

def run_model(Nx:int, Ny:int, pos, st_zrn:int, TFIN:int, Sth:int):
    global Velikost_plazu
    S = init_S(Nx,Ny)
    F = init_F(Nx, Ny, pos, st_zrn)
    
    start_time = time.time()
    lag = 100
    dt = []
    seznam_plazov = []
    
    for iteracija in range(TFIN):
        S = S + F
        Velikost_plazu = 0
        S = TBW_model(pos[0],pos[1],S,Sth)
        
        if Velikost_plazu > 0:
            seznam_plazov.append(Velikost_plazu)


        if iteracija%lag == 0:
            end_time = time.time()
            print_control(end_time, start_time, seznam_plazov, iteracija, S)
            start_time = time.time()
    return S, seznam_plazov