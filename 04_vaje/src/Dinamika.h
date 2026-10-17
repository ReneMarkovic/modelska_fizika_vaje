#pragma once

#include "Delci.h" // Vključitev osnovnih struktur

namespace MDSim {

    // Izračuna minimalno slikovno razdaljo med dvema delcema v škatli z robom L
    Vec3 MinimalnaSlika(const Vec3& R1, const Vec3& R2, double L);

    // Glavna funkcija za izračun sil za vse delce.
    // E_pot se posodobi z novo potencialno energijo.
    void IzracunSil(
        std::vector<Particle>& delci, 
        const SimulationParams& params,
        double& E_pot 
    );

    // Numerična integracija gibalnih enačb (Velocity Verlet).
    // Posodobi R in V delcev.
    void IntegracijaVerlet(
        std::vector<Particle>& delci, 
        const SimulationParams& params,
        double& E_pot 
    );
    
    // Inicializacija pozicij (npr. na mrežo) in hitrosti (Maxwell-Boltzmann).
    void Inicializacija(
        std::vector<Particle>& delci, 
        SimulationParams& params
    );

    // Berendsenov termostat (mehko približevanje tarčni temperaturi).
    // T_target ... želena temperatura
    // T_inst   ... trenutna (izračunana) temperatura
    // tau      ... relaksacijski čas termostata
    // dt       ... časovni korak
    void BerendsenThermostat(
        std::vector<Particle>& delci,
        double T_target,
        double T_inst,
        double tau,
        double dt
    );

} // namespace MDSim
