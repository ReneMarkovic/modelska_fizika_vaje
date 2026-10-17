#include <iostream>
#include <fstream>
#include <iomanip>
#include <sstream> // Za ustvarjanje imena datoteke
#include "Delci.h"
#include "Dinamika.h"

using namespace MDSim;

// Funkcija za izračun kinetične energije in temperature
void IzracunEnergije(const std::vector<Particle>& delci, double& E_kin, double& Temp) {
    E_kin = 0.0;
    double N = static_cast<double>(delci.size());
    
    for (const auto& p : delci) {
        E_kin += 0.5 * p.masa * p.V.sqr_len();
    }
    
    // T = (2 * E_kin) / (3 * N * kB), kB = 1 (reducirane enote)
    if (N > 0.0) {
        Temp = (2.0 * E_kin) / (3.0 * N * KB); 
    } else {
        Temp = 0.0;
    }
}

// Funkcija za zapis pozicij v XYZ format (za 3D vizualizacijo)
void ZapisiXYZ(const std::vector<Particle>& delci, double time, int frame_num) {
    static std::ofstream traj_file("data/trajektorija.xyz");

    if (!traj_file.is_open()) {
        std::cerr << "NAPAKA: Ne morem odpreti datoteke data/trajektorija.xyz" << std::endl;
        return;
    }
    
    traj_file << delci.size() << "\n";
    traj_file << "Time=" << std::fixed << std::setprecision(4) << time 
              << ", Frame=" << frame_num << "\n";

    for (const auto& p : delci) {
        char tip_label = 'A' + p.tip; 
        traj_file << tip_label << " " 
                  << std::fixed << std::setprecision(6)
                  << p.R.x << " " 
                  << p.R.y << " " 
                  << p.R.z << "\n";
    }
}


int main() {
    
    // ----------------------------------------------------
    // I. KONFIGURACIJA SIMULACIJE
    // ----------------------------------------------------
    
    const double L = 5.0;            // Velikost škatle
    const double dt = 0.005;         // Časovni korak
    const double rc = 2.5;           // Cutoff radius
    const double target_temp = 1.0;  // Želena temperatura

    SimulationParams params(L, dt, rc);
    params.temp = target_temp;
    
    // Število delcev in tipov
    params.N_delcev = 2048*2; 
    params.N_tipov  = 2;   // tipa 0 in 1

    // Lennard-Jones parametri
    const double sigma_A   = 1.0;
    const double epsilon_A = 1.0;
    
    const double sigma_B   = 1.2;
    const double epsilon_B = 0.8;
    
    params.interakcije.resize(params.N_tipov, std::vector<LJPairParams>(params.N_tipov));
    
    params.interakcije[0][0] = {epsilon_A, sigma_A, 12, 6}; // A-A
    params.interakcije[1][1] = {epsilon_B, sigma_B, 12, 6}; // B-B
    
    double sigma_AB   = (sigma_A + sigma_B) / 2.0;
    double epsilon_AB = std::sqrt(epsilon_A * epsilon_B);
    
    params.interakcije[0][1] = {epsilon_AB, sigma_AB, 12, 6}; // A-B
    params.interakcije[1][0] = params.interakcije[0][1];      // B-A

    std::vector<Particle> delci;
    
    // ----------------------------------------------------
    // II. INITIALIZACIJA
    // ----------------------------------------------------
    
    Inicializacija(delci, params); 
    
    // Nastavimo tipe delcev (polovica A, polovica B)
    for (std::size_t i = 0; i < delci.size(); ++i) {
        if (i < delci.size() / 2) {
            delci[i].tip = 0; // A
        } else {
            delci[i].tip = 1; // B
        }
    }

    std::cout << "Zacetek simulacije z N=" << params.N_delcev 
              << " delcev (" << params.N_tipov << " tipov)." << std::endl;
    
    // Prvi izračun sil in potencialne energije (t = 0)
    double E_pot = 0.0;
    IzracunSil(delci, params, E_pot);

    // ----------------------------------------------------
    // III. GLAVNA ZANKA SIMULACIJE
    // ----------------------------------------------------

    const int max_korakov = 20000;
    const int log_interval = 100;    // zapis termodinamike
    const int viz_interval = 200;    // zapis trajektorije
    const bool use_thermostat = true;
    const double tau_T = 1.0;        // relaksacijski čas termostata

    double E_kin = 0.0;
    double Temp  = 0.0;
    int frame_counter = 0;

    // Priprava datotek (mapa 'data' mora obstajati!)
    std::ofstream out_log("data/energije.csv");
    if (!out_log.is_open()) {
        std::cerr << "NAPAKA: Ne morem odpreti data/energije.csv" << std::endl;
        return 1;
    }
    out_log << "Time,E_kin,E_pot,E_total,Temp\n";

    for (int t = 0; t < max_korakov; ++t) {
        
        // 1) Integracija (uporabi trenutne sile, posodobi R, V, A in E_pot)
        IntegracijaVerlet(delci, params, E_pot);
        
        // 2) Kinetična energija in trenutna temperatura
        IzracunEnergije(delci, E_kin, Temp);

        // 3) Berendsenov termostat (po želji)
        if (use_thermostat) {
            BerendsenThermostat(delci, params.temp, Temp, tau_T, dt);
            // ponovno izračunaj E_kin in Temp, ker smo spremenili hitrosti
            IzracunEnergije(delci, E_kin, Temp);
        }

        double E_total = E_kin + E_pot;
        
        // 4) Izhod podatkov
        if (t % log_interval == 0) {
            double time = t * dt;
            
            std::cout << "Korak " << t
                      << " | T=" << std::fixed << std::setprecision(4) << Temp 
                      << " | E_total=" << E_total << std::endl;
            
            out_log << time << "," << E_kin << "," << E_pot << "," << E_total << "," << Temp << "\n";
        }
        
        if (t % viz_interval == 0) {
            ZapisiXYZ(delci, t * dt, frame_counter++);
        }
    }

    std::cout << "Simulacija koncana. Trajektorija: data/trajektorija.xyz" << std::endl;
    return 0;
}
