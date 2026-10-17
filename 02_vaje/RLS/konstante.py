import numpy as np

# Konstante
G = 6.67430e-11  # gravitacijska konstanta [m^3 kg^-1 s^-2]
M_earth = 5.972e24  # masa Zemlje [kg]
R_earth = 6371e3  # polmer Zemlje [m]

g = G*M_earth/R_earth**2  # pospešek prostega pada na površini [m/s^2]

rho_0 = 1.225  # gostota zraka na površini [kg/m^3]
Molska_masa_zraka = 28.96  # molska masa zraka [kg/kmol]
R_spk = 8314.46 #Splošna plinska konstanta [J/(K kmol)]
T_ozracja = 288.15  # temperatura ozračja na površini [K]

h_0 = (Molska_masa_zraka * g)/(R_spk * T_ozracja)# 8400  # karakteristična višina za barometrsko enačbo [m]

C_d = 0.2  # koeficient zračnega upora
S = 10  # površina rakete [m^2]
v_exhaust = 3000  # hitrost izpušnih plinov [m/s]
burn_rate = 100  # izgorevalna hitrost [kg/s]

# Začetni pogoji
m_rakete = 10_000  # masa rakete brez goriva [kg]
m_goriva = 20_000  # začetna masa goriva [kg]
m_tovora = 1_000  # masa tovora [kg]


'''
The Merlin 1D engine used on SpaceX's Falcon 9 rocket produces a sea-level thrust of 845 kN and a vacuum thrust of 981 kN.
The F-1 engine used on the Saturn V rocket, which took astronauts to the Moon, produced a thrust of 6,770 kN.
'''
F_potiska = 845_000  # sila potiska [N]
k_goriva = 2_500  # koeficient potiska [N/kg]

'''
https://www.quora.com/How-much-fuel-does-a-rocket-use-in-kg

'''