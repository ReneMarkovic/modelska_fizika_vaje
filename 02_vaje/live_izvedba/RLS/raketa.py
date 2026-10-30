import numpy as np
import pandas as pd
from . import konstante as const
import time

class raketa:
    def __init__(self,
                 m_gorivo:float = const.m_goriva,
                 m_raketa:float = const.m_rakete,
                 m_tovor:float = const.m_tovora,
                 M:float = const.M_earth,
                 T_ozracja:float = const.T_ozracja,
                 rho:float = const.rho_0,
                 Mol_mas:float = const.Molska_masa_zraka,
                 h_start:float = const.R_earth):
        self.m_gorivo = m_gorivo
        self.m_raketa = m_raketa
        self.m_tovor = m_tovor
        self.M_planet = M
        self.R_planeta = const.R_earth
        self.T_ozracja = T_ozracja
        self.rho_planet = rho
        self.G = const.G
        self.g = const.G * self.M_planet / const.R_earth**2
        self.h0 = (Mol_mas)/(const.R_spk * const.T_ozracja)
        self.h = h_start
        
        self.time = 0
        self.v = 0
        self.a = 0
        
        self.enote={}
        self.enote["Čas"] = " s"
        self.enote["Višina"] = " m"
        self.enote["Hitrost"] = " m/s"
        self.enote["Pospešek"] = " m/s2"
        self.enote["Skupna masa"] = " kg"
        self.enote["Masa goriva"] = " kg"
        self.enote["Gravitacijska sila"] = " N"
        self.enote["Zračni upor"] = " N"
        self.enote["Sila potiska"] = " N"
        self.enote["Rezultanta sil"] = " N"
        self.enote["Gostota"] = " kg/m3"
        
        #podatkovna baza za rezultate -> DataFrame od pandas
        self.df = {key:[] for key in self.enote}
    
    def gravitacijska_sila(self):
        # Fg = G * m_planeta*m_sistema / r^2
        #!!!! pazi na maso goriva
        m_sis = self.m_gorivo + self.m_raketa + self.m_tovor
        h2 = self.h*self.h
        Fg = self.G * self.M_planet * m_sis / h2
        return -Fg
    
    def barometerska_enacba(self):
        gostota = self.rho_planet
        h = self.h - self.R_planeta
        return gostota * np.exp(-h * self.h0)
    
    def sila_upora(self):
        # Upoštevaj da je sila upora zmeraj usmerjena v nasprotno smer hitrosti. Torej
        # če se raketa premika gor je - če se premika dol pa je +
        # Fu = 1/2 * rho * S * c * v**2
        rho = self.barometerska_enacba()
        if self.v > 0:
            return -0.5 * rho * self.v**2 * const.C_d * const.S
        else:
            return 0.5 * rho * self.v**2 * const.C_d * const.S
    
    def sila_potiska(self):
    #Simuliraj let rakete in puporabi raketno enačbo
        if self.m_gorivo > 0:
            return const.F_potiska
        else:
            return 0
    
    def posodobi_maso(self, dt: float):
        if self.m_gorivo>0:
            self.m_gorivo = self.m_gorivo - const.burn_rate * dt
            return self.m_gorivo
        else:
            return 0.0
    
    def rezultanta_sil(self):
        rezultanta = self.sila_potiska() + self.sila_upora() + self.gravitacijska_sila()
        return rezultanta
    
    def pospešek(self, dt:float):
        # a = F/m
        F = self.rezultanta_sil()
        
        self.m_gorivo = self.posodobi_maso(dt)
        m = self.m_gorivo + self.m_raketa + self.m_tovor
        
        a = F/m
        return a
    
    def enote(self):
        return self.enote
    
    def simulacija_vzleta_rakete(self,dt:float):
        self.time = self.time + dt
        self.a = self.pospešek(dt)
        self.v = self.v + self.a*dt
        self.h = self.h + self.v*dt
        
        result={} #Prazen dictionary
        result["Čas"] = self.time
        result["Višina"] = self.h - self.R_planeta
        result["Hitrost"] = self.v
        result["Pospešek"] = self.a
        result["Skupna masa"] = self.m_raketa + self.m_tovor + self.m_gorivo
        result["Masa goriva"] = self.m_gorivo
        result["Gravitacijska sila"] = self.gravitacijska_sila()
        result["Zračni upor"] = self.sila_upora()
        result["Sila potiska"] = self.sila_potiska()
        result["Rezultanta sil"] = self.rezultanta_sil()
        result["Gostota"] = self.barometerska_enacba()
        return result
    
    def update_data(self,data):
        for key in data:
            self.df[key].append(data[key])
    
    def simuliraj(self,dt: float):
        stanje_rakete = self.simulacija_vzleta_rakete(dt)
        self.update_data(stanje_rakete)
        while stanje_rakete["Hitrost"] > 0 and stanje_rakete['Višina']<360_000_000:
            stanje_rakete = self.simulacija_vzleta_rakete(dt)
            self.update_data(stanje_rakete)
        return self.df
    
    def prva_kozmična_hitrost(self,h:float):
        return np.sqrt(const.G * self.M_planet / (self.R_planeta + self.h))
    
    def geostacionarna_orbita(self):
        micro = self.G*self.M_planet
        T = 24*60*60
        R_orbite = np.power(micro*T**2/(4*np.pi**2),1/3) - self.R_planeta
        v_orbite = 2*np.pi*R_orbite/T
        return R_orbite, v_orbite
    
    def druga_kozmična_hitrost(self):
        return np.sqrt(2 * const.G * self.M_planet / (self.R_planeta))
    
    def izvozi_rezultate(self):
        excel = pd.DataFrame.froam_dict(self.df)
        excel.to_excel("Rezultati_simulacije.xlsx")