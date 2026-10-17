#pragma once

#include <cmath>
#include <vector>

namespace MDSim {

    // ------------------------------------------------------------------
    // I. OSNOVNE STRUKTURE
    // ------------------------------------------------------------------
    // V Lennard-Jones reduciranih enotah je Boltzmannova konstanta 1.
    const double KB = 1.0;
    // 3D Vektor struktura
    struct Vec3 {
        double x = 0.0, y = 0.0, z = 0.0;
        
        // Operatorji za enostavno delo z vektorji
        Vec3 operator+(const Vec3& other) const { return {x + other.x, y + other.y, z + other.z}; }
        Vec3 operator-(const Vec3& other) const { return {x - other.x, y - other.y, z - other.z}; }
        Vec3 operator*(double scalar) const { return {x * scalar, y * scalar, z * scalar}; }
        Vec3 operator/(double scalar) const { return {x / scalar, y / scalar, z / scalar}; }

        // Množenje z vektorjem (skalarni produkt - dot product)
        double dot(const Vec3& other) const { return x * other.x + y * other.y + z * other.z; }

        // Kvadrirana dolžina (za razdaljo, hitrejše kot uporaba korena)
        double sqr_len() const { return x*x + y*y + z*z; }
    };
    
    // Lastnosti in Trenutno Stanje delca
    struct Particle {
        int id = 0;
        int tip = 0; // Tip delca (npr. 0, 1, 2)
        double masa = 1.0; 
        
        Vec3 R; // Pozicija
        Vec3 V; // Hitrost
        Vec3 A; // Pospešek (trenutno izračunane sile / masa)
    };

    // ------------------------------------------------------------------
    // II. PARAMETRI INTERAKCIJE
    // ------------------------------------------------------------------

    // LJ parametri za določen par tipov delcev
    struct LJPairParams {
        double epsilon; // Globina potencialne jame
        double sigma;   // Razdalja, pri kateri je potencial 0
        int n = 12;     // Eksponent odbijanja
        int m = 6;      // Eksponent privlačnosti
    };
    
    // ------------------------------------------------------------------
    // III. SIMULACIJSKI PARAMETRI
    // ------------------------------------------------------------------

    // Glavni parametri, ki določajo simulacijsko okolje
    struct SimulationParams {
        double L;           // Dolžina stranice simulacijske škatle (kubična)
        double dt;          // Časovni korak (delta t)
        double rc_sq;       // Kvadrirani "cutoff" radij (r_c^2)
        double temp;        // Željena temperatura (za inicializacijo/termostat)
        int N_delcev;       // Skupno število delcev
        int N_tipov;        // Število različnih tipov delcev
        
        // Matrika (N_tipov x N_tipov) parametrov
        std::vector<std::vector<LJPairParams>> interakcije;
        
        // Konstruktor za lažjo inicializacijo
        SimulationParams(double box_size, double time_step, double cutoff)
            : L(box_size), dt(time_step), rc_sq(cutoff * cutoff) {}
    };

} // namespace MDSim