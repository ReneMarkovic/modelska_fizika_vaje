#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define Nx 5
#define Ny 5
#define Nz 5

// Odstranjeni enačaji (=)
#define EPS_A 1.0
#define EPS_B 2.0

#define SIG_A 1.0
#define SIG_B 1.2

// Dodani oklepaji okoli izraza
#define N ((Nx) * (Ny) * (Nz))
#define RHO 0.8
#define T0 0.3
#define RC 2.5

// Globalne spremenljivke definiramo pred vključitvijo funkcije.h
double V = (double)N / RHO;
double L = pow((double)N / RHO, 1.0 / 3.0);

double pos[N][3];
double vel[N][3];
double acc[N][3];
double eps_AB[N];
double sig_AB[N];

#include "funkcije.h"

int main(){
    // Inicializacija sistema: ekvidistančna porazdelitev N delcev v kocki
    double frac = 0.7;

    double Ep0 = inicializacija(pos, vel, acc, sig_AB, eps_AB, L, frac);

    zapisi_stanje_mikro(pos, vel, acc, sig_AB, eps_AB, L, frac);
    zapisi_stanje_makro(pos, vel, acc, sig_AB, eps_AB);

    printf("Sistem uspesno inicializiran.\n");
    printf("Stevilo delcev N = %d, L = %f\n", N, L);
    printf("Zacetna potencialna energija: Ep = %f\n", Ep0);

    // Tukaj sledi integracija gibalnih enacb (npr. Velocity-Verlet algoritem)

    return 0;
}