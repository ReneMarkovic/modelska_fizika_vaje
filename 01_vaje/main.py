import numpy as np
import matplotlib.pyplot as plt
import sys
from TWB import model

sys.setrecursionlimit(100_000)  # plazovi so rekurzivni in lahko presežejo privzeto globino 1000

## Globalni parametri simulacije
Velikost_plazu = 0
Nx = 21
Ny = 21
T_FIN = 10_000
Sth = 4 # Mejna strmina sipine

cx = Nx//2 #Lokacija na katero pada pesek v smeri x
cy = Ny//2 #Lokacija na katero pada pesek v smeri y
pos = [cx,cy]

st_zrn = 4 # koliko zrn bo ob času t padlo na mesto x,y

#model.run_model(Nx = Nx, Ny = Ny, pos = pos, st_zrn = st_zrn, TFIN = T_FIN, Sth = Sth)
model.run_model(Nx, Ny, pos, st_zrn, T_FIN, Sth)