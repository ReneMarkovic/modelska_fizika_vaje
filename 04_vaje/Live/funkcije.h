#ifndef FUNKCIJE_H
#define FUNKCIJE_H

#include <math.h>
#include <stdlib.h>

// Deklaracija zunanje spremenljivke L, ki je definirana v main.cpp
extern double L;


double abs_vek(double vektor[3]){
    double x, y, z;
    x = vektor[0];
    y = vektor[1];
    z = vektor[2];
    return sqrt(x*x + y*y + z*z);
}

double razdalja(int i, int j, double xyz[N][3]){
    double dx = xyz[i][0] - xyz[j][0];
    double dy = xyz[i][1] - xyz[j][1];
    double dz = xyz[i][2] - xyz[j][2];
    return sqrt(dx*dx + dy*dy + dz*dz);
}

// Popravljen zadnji parameter
double razdalja2(int i, int j, double xyz[N][3], double d[3]){
    double r2 = 0.0;
    for(int k = 0; k < 3; k++){
        d[k] = xyz[i][k] - xyz[j][k];
        d[k] -= L * round(d[k] / L); // Periodični robni pogoji (MIC)
        r2 += d[k] * d[k];
    }
    return r2;
}

double potencial(int i, int j, double xyz[N][3], double eps_AB[N]){
    double r = razdalja(i, j, xyz);
    double eps = sqrt(eps_AB[i] * eps_AB[j]);
    return 4.0 * eps * (pow(r, -12.0) - pow(r, -6.0));
}

double sila(int i, int j, double xyz[N][3], double eps_AB[N]){
    double r = razdalja(i, j, xyz);
    double eps = sqrt(eps_AB[i] * eps_AB[j]);
    return 24.0 * eps * (-2.0 * pow(r, -13.0) + pow(r, -7.0));
}


void Euler(double A[N][3], double B[N][3], double dt){
    // An+1 = An + B*dt  //
    int i;

    for(i = 0; i < N; i++){
        A[i][0] = A[i][0] + B[i][0]*dt;
        A[i][1] = A[i][1] + B[i][1]*dt;
        A[i][2] = A[i][2] + B[i][2]*dt;
    }
}



// Preimenovano, da se prepreči konflikt s stdlib random()
double nakljucno(){
    return (double)rand() / (double)RAND_MAX;
}

double pospeski(double xyz[N][3], double acc[N][3],
                double sig_AB[N], double eps_AB[N]){

    double Ep = 0.0, d[3];

    for(int i = 0; i < N; i++){
        for(int k = 0; k < 3; k++){
            acc[i][k] = 0.0;
        }
    }

    for(int i = 0; i < N - 1; i++){
        for(int j = i + 1; j < N; j++){

            double r2 = razdalja2(i, j, xyz, d);
            if(r2 >= RC * RC) continue;

            double sig = 0.5 * (sig_AB[i] + sig_AB[j]);
            double eps = sqrt(eps_AB[i] * eps_AB[j]);

            double s2 = (sig * sig) / r2;
            double s6 = s2 * s2 * s2;
            double s12 = s6 * s6;

            double c2 = (sig * sig) / (RC * RC);
            double c6 = c2 * c2 * c2;

            double f = 24.0 * eps * (2.0 * s12 - s6) / r2; // F/r
            
            for(int k = 0; k < 3; k++){
                acc[i][k] += f * d[k];
                acc[j][k] -= f * d[k];
            }

            Ep += 4.0 * eps * ((s12 - s6) - (c6 * c6 - c6));
        }
    }

    return Ep;
}

double inicializacija(
    double xyz[N][3], double vel[N][3], double acc[N][3],
    double sig_AB[N], double eps_AB[N],
    double L_box, double frac){

    int i, j, k;

    double dx = L_box / (double)(Nx);
    double dy = L_box / (double)(Ny);
    double dz = L_box / (double)(Nz);
    double x = 0.0, y = 0.0, z = 0.0;

    int id = 0;
    for(i = 0; i < Nx; i++){
        x = dx / 2.0 + (double)(i) * dx;

        for(j = 0; j < Ny; j++){
            y = dy / 2.0 + (double)(j) * dy;

            for(k = 0; k < Nz; k++){
                z = dz / 2.0 + (double)(k) * dz;

                xyz[id][0] = x;
                xyz[id][1] = y;
                xyz[id][2] = z;

                int B = nakljucno() < frac;

                eps_AB[id] = B ? EPS_A : EPS_B;
                sig_AB[id] = B ? SIG_A : SIG_B;

                id++;
            }
        }
    }

    // Začetne hitrosti
    for(id = 0; id < N; id++){
        vel[id][0] = 0.0;
        vel[id][1] = 0.0;
        vel[id][2] = 0.0;
    }
    
    return pospeski(xyz, acc, sig_AB, eps_AB);
}


double avg_r_min(double xyz[N][3]){
    int i,j;
    double d[3];
    double r, r_min = 0.0, r_avg_min = 0.0;
    for(i = 0; i < N; i++){
        r_min = 1000000.0;
        for(j = 0; j < N; j++){
            if( i!=j ){
                r = razdalja2(i, j, xyz, d);
                r = sqrt(r);

                if(r < r_min){
                    r_min = r;
                }
            }
        }
        r_avg_min += r_min;
    }
    r_avg_min = r_avg_min / ((double)(N));
    return r_avg_min;
}


void zapisi_stanje_makro(double xyz[N][3], double vel[N][3], double acc[N][3],
    double sig_AB[N], double eps_AB[N]){
    
    FILE* datoteka;
    datoteka = fopen("data/stanje_sistema_avg.txt","w+"); // r, w, w+, a
    //Zanima me <T>, <v>, <E>/N, <rmin>
    double v_avg, T_avg, Ek, Ep, rmin;
    int i;

    v_avg = 0.0;

    for(i = 0; i < N; i++){
        v_avg += abs_vek(vel[i]);
    }

    v_avg = v_avg / (double)(N);
    Ek = 0.5*v_avg*v_avg;
    T_avg = 2* Ek / (3*(double)(N)); 
    Ep = pospeski(xyz,acc,sig_AB,eps_AB);
    rmin = avg_r_min(xyz);

    fprintf(datoteka,"%f\t%f\t%f\t%f\t%f\n",v_avg,Ek,T_avg,Ep,rmin);

    fclose(datoteka);
}


void zapisi_stanje_mikro(double xyz[N][3], double vel[N][3], double acc[N][3],
    double sig_AB[N], double eps_AB[N],
    double L_box, double frac){
    
    FILE* datoteka;
    datoteka = fopen("data/stanje_sistema.txt","w+"); // r, w, w+, a
    int i;
    for(i = 0; i < N;  i++){
        fprintf(datoteka,"%d\t",i);
        fprintf(datoteka,"%f\t%f\t%f\t",xyz[i][0],xyz[i][1],xyz[i][2]);//Lokacije
        fprintf(datoteka,"%f\t%f\t%f\t",vel[i][0],vel[i][1],vel[i][2]);//Hitrosti
        fprintf(datoteka,"%f\t%f\t%f\t",acc[i][0],acc[i][1],acc[i][2]);//Hitrosti
        fprintf(datoteka,"%f\t%f\n",sig_AB[i],eps_AB[i]);//Potencial
    }
    fclose(datoteka);
}


double simuliraj_dinamiko(double xyz[N][3], double vel[N][3], double acc[N][3],
    double sig_AB[N], double eps_AB[N], double stop, double dt){
        
        double t = 0.0, Ep;
        int iteracija = 0;

        for(t = 0.0; t < stop; t++){
            Ep = pospeski(xyz, acc, sig_AB, eps_AB);
            Euler(vel, acc, dt);
            Euler(xyz, vel, dt); //!!!!!!!!

            for(int i = 0; i < N; i++){
                for(int k = 0; k < 3; k++){
                    if(xyz[i][k] > L) xyz[i][k] = xyz[i][k] - L;
                    if(xyz[i][k] < 0) xyz[i][k] = xyz[i][k] + L;
                }
            }

            iteracija++;
            if(iteracija%10==0){
                zapisi_stanje_makro(xyz,vel, acc,sig_AB, eps_AB);
            }
        }

}


#endif