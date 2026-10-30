#include <stdio.h>
#include <stdlib.h>
#include <math.h>


#define Nx 5
#define Ny 5
#define Nz 5

#define EPS_A = 1.0
#define EPS_B = 2.0

#define SIG_A = 1.0
#define SIG_B = 1.2

#define N Nx*Ny*Nz
#define RHO 0.8
#define T0 0.3
#define RC 2.5

#include "funkcije.h"

double V = N/RHO;
double L = pow(V, 1.0/3.0);

double pos[N][3];
double vel[N][3];
double acc[N][3];
double eps_AB[N];
double sig_AB[N];


int main(){
    //Inicializacija sistema: ekvidistančna porazdelitev N delcev v kocki
    
    inicializacija(pos, vel, acc, sig_AB, eps_AB, L, 0.7);
    //Simuliraj dinamiko
        


    return 0;
}