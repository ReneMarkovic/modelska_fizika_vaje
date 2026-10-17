#include "Dinamika.h"
#include <iostream>
#include <cmath>
#include <random>
#include <numeric>

namespace MDSim {

    // ----------------------------------------------------
    // FUNKCIJA 1: MINIMALNA SLIKA (PBC - Periodic Boundary Conditions)
    // ----------------------------------------------------
    Vec3 MinimalnaSlika(const Vec3& R1, const Vec3& R2, double L) {
        Vec3 dR = R1 - R2;
        
        // Uporaba PBC: razdalja mora biti v območju [-L/2, L/2]
        double L_pol = L * 0.5;

        if (dR.x >  L_pol) dR.x -= L;
        if (dR.x <= -L_pol) dR.x += L;

        if (dR.y >  L_pol) dR.y -= L;
        if (dR.y <= -L_pol) dR.y += L;

        if (dR.z >  L_pol) dR.z -= L;
        if (dR.z <= -L_pol) dR.z += L;
        
        return dR;
    }

    // ----------------------------------------------------
    // FUNKCIJA 2: IZRAČUN SIL (Lennard-Jones)
    // ----------------------------------------------------
    void IzracunSil(
        std::vector<Particle>& delci, 
        const SimulationParams& params,
        double& E_pot
    ) {
        // Ponastavi pospeške in potencialno energijo
        E_pot = 0.0;
        for (auto& p : delci) {
            p.A = {0.0, 0.0, 0.0};
        }

        const int N = params.N_delcev;
        const double L = params.L;
        const double rc_sq = params.rc_sq;

        for (int i = 0; i < N; ++i) {
            for (int j = i + 1; j < N; ++j) {
                
                // 1. Parametri interakcije
                int tip_i = delci[i].tip;
                int tip_j = delci[j].tip;
                const auto& param_ij = params.interakcije[tip_i][tip_j];
                const double epsilon = param_ij.epsilon;
                const double sigma   = param_ij.sigma;
                const int n = param_ij.n; 
                const int m = param_ij.m; 

                // 2. Minimalna slika
                Vec3 dR = MinimalnaSlika(delci[i].R, delci[j].R, L);
                double r_sq = dR.sqr_len();
                if (r_sq >= rc_sq) continue;

                double r_inv = 1.0 / std::sqrt(r_sq);
                double s_div_r = sigma * r_inv;      // sigma/r

                double pow_n = std::pow(s_div_r, n); // (sigma/r)^n
                double pow_m = std::pow(s_div_r, m); // (sigma/r)^m

                // V(r) = 4 * epsilon * [ (sigma/r)^n - (sigma/r)^m ]
                double V_r = 4.0 * epsilon * (pow_n - pow_m);

                // |F|/r = 4 * epsilon * [ n (sigma/r)^n - m (sigma/r)^m ] / r^2
                double r_inv2 = 1.0 / r_sq;
                double factor_F_over_r = 4.0 * epsilon * (n * pow_n - m * pow_m) * r_inv2;

                // F_vektor = (F/r) * dR
                Vec3 F_vec = dR * factor_F_over_r;

                // akcija/reakcija
                delci[i].A = delci[i].A + (F_vec / delci[i].masa);
                delci[j].A = delci[j].A - (F_vec / delci[j].masa);

                E_pot += V_r;
            }
        }
    }


    // ----------------------------------------------------
    // FUNKCIJA 3: INICIALIZACIJA (Postavitev na mrežo in hitrosti)
    // ----------------------------------------------------
    void Inicializacija(
        std::vector<Particle>& delci, 
        SimulationParams& params
    ) {
        delci.clear();
        int N_dim = static_cast<int>(std::cbrt(params.N_delcev));
        if (N_dim * N_dim * N_dim < params.N_delcev) {
            N_dim++; 
        }
        
        double L = params.L;
        double spacing = L / N_dim; 
        
        int particle_count = 0;
        for (int i = 0; i < N_dim; ++i) {
            for (int j = 0; j < N_dim; ++j) {
                for (int k = 0; k < N_dim; ++k) {
                    if (particle_count < params.N_delcev) {
                        Particle p;
                        p.id = particle_count;
                        p.R.x = (i + 0.5) * spacing;
                        p.R.y = (j + 0.5) * spacing;
                        p.R.z = (k + 0.5) * spacing;
                        p.tip = 0; 
                        p.masa = 1.0; 
                        p.V   = {0.0, 0.0, 0.0};
                        p.A   = {0.0, 0.0, 0.0};
                        delci.push_back(p);
                        particle_count++;
                    }
                }
            }
        }

        params.N_delcev = static_cast<int>(delci.size()); 

        // Maxwell-Boltzmann hitrostna porazdelitev
        std::random_device rd;
        std::mt19937 gen(rd());

        Vec3 center_of_mass_V = {0.0, 0.0, 0.0};
        double total_mass = 0.0;
        
        for (auto& p : delci) {
            // če bi bile mase različne, bi tu lahko uporabil p.masa
            double sigma_v = std::sqrt(KB * params.temp / p.masa);
            std::normal_distribution<> d(0.0, sigma_v);

            p.V.x = d(gen);
            p.V.y = d(gen);
            p.V.z = d(gen);

            center_of_mass_V = center_of_mass_V + (p.V * p.masa);
            total_mass += p.masa;
        }

        // odstrani celoten gibalni količnik
        if (total_mass > 0.0) {
            Vec3 CM_V = center_of_mass_V / total_mass; 
            for (auto& p : delci) {
                p.V = p.V - CM_V;
            }
        }
    }

    // ----------------------------------------------------
    // FUNKCIJA 4: INTEGRACIJA VERLET (Velocity Verlet)
    // ----------------------------------------------------
    void IntegracijaVerlet(
        std::vector<Particle>& delci, 
        const SimulationParams& params,
        double& E_pot 
    ) {
        double dt = params.dt;
        double dt_pol = dt * 0.5;

        // 1) half-kick + drift
        for (auto& p : delci) {
            p.V = p.V + (p.A * dt_pol); 
            p.R = p.R + (p.V * dt);

            // Periodične robne razmere
            if (p.R.x < 0.0)      p.R.x += params.L;
            else if (p.R.x >= params.L) p.R.x -= params.L;

            if (p.R.y < 0.0)      p.R.y += params.L;
            else if (p.R.y >= params.L) p.R.y -= params.L;

            if (p.R.z < 0.0)      p.R.z += params.L;
            else if (p.R.z >= params.L) p.R.z -= params.L;
        }

        // 2) nove sile in potencialna energija
        IzracunSil(delci, params, E_pot);

        // 3) drugi half-kick
        for (auto& p : delci) {
            p.V = p.V + (p.A * dt_pol);
        }
    }

    // ----------------------------------------------------
    // FUNKCIJA 5: BERENDSENOV TERMOSTAT
    // ----------------------------------------------------
    void BerendsenThermostat(
        std::vector<Particle>& delci,
        double T_target,
        double T_inst,
        double tau,
        double dt
    ) {
        if (T_inst <= 0.0 || tau <= 0.0) {
            return;
        }

        // lambda^2 = 1 + (dt/tau)*(T_target/T_inst - 1)
        double lambda2 = 1.0 + (dt / tau) * (T_target / T_inst - 1.0);
        if (lambda2 <= 0.0) {
            return; // numerična zaščita
        }

        double lambda = std::sqrt(lambda2);

        for (auto& p : delci) {
            p.V = p.V * lambda;
        }
    }

} // namespace MDSim
