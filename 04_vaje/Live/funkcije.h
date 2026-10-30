//Funkcije.h

double razdalja(int i, int j, double xyz[N][3]){
    double dx = xyz[i][0] - xyz[j][0];
    double dy = xyz[i][1] - xyz[j][1];
    double dz = xyz[i][2] - xyz[j][2];
    return sqrt(dx*dx + dy*dy + dz*dz);
}

double razdalja2(int i, int j, double xyz[N][3], double d[3]){
    double r2 = 0.0;
    for(int k = 0; k < 3; k++){
        d[k] = xyz[i][k] - xyz[j][k];
        d[k] -= L * round(d[k] / L); //!  ! 
        r2 += d[k] * d[k];
    }
    return r2;
}

double potencial(int i, int j, double xyz[N][3], double eps_AB[N]){
    double r = razdalja(i,j,xyz );
    double eps = sqrt(eps_AB[i]*eps_AB[j]);
    return 4*eps*(pow(r,-12.0)-pow(r,-6.0));
}

double sila(int i, int j, double xyz[N][3], double eps_AB[N]){
    double r = razdalja(i,j,xyz );
    double eps = sqrt(eps_AB[i]*eps_AB[j]);
    return 24*eps*(-2.0*pow(r,-13.0)+pow(r,-7.0));
}

double random(){
    return (double)(rand())/(double)(RAND_MAX);
}


double pospeski(double xyz[N][3], double acc[N][3],
                double sig_AB[N], double eps_AB[N]){

    double Ep = 0.0, d[3];

    for(int i = 0; i < N; i++){
        for(int k = 0; k < 3; k++){
            acc[i][k] = 0.0;   //!!! Zelo pomemben
        }
    }

    for(int i = 0; i < N - 1; i++){
        for(int j = i + 1; j < N; j++){

            double r2 = razdalja2(i, j, xyz, d); //We will define now
            if(r2 >= RC * RC) continue;

            double sig = 0.5 * (sig_AB[i] + sig_AB[j]);
            double eps = sqrt(eps_AB[i] * eps_AB[j]);

            double s2 = sig * sig / r2;
            double s6 = s2 * s2 * s2;
            double s12 = s6 * s6;

            double c2 = sig * sig / (RC * RC);
            double c6 = c2 * c2 * c2;

            double f = 24.0 * eps * (2.0 * s12 - s6) / r2;   // F/r
            
            
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
    double L, double frac){
    //HW: porazdeli delce v kocki
    int i,j,k;

    double dx = L/(double)(Nx), dy = L/(double)(Ny), dz = L/(double)(Nz);
    double x = 0.0, y = 0.0, z = 0.0;

    int id = 0;
    for(i = 0; i< Nx; i++){
        x = dx/2.0 + (double)(i)*dx;

        for(j = 0; j< Ny; j++){
            y = dy/2.0 + (double)(j)*dy;

            for(k = 0; k < Nz;k++){
                z = dz/2.0 + (double)(k)*dz;

                xyz[id][0] = x;
                xyz[id][1] = y;
                xyz[id][2] = z;

                int B = random() < frac;

                eps_AB[id] = B ? EPS_A : EPS_B;
                sig_AB[id] = B ? SIG_A : SIG_B;


                id += 1;
            }
        }
    }

    //HW: določi hitrosti
    for(id = 0; id < N; id++){
        vel[id][0] = 0.0;
        vel[id][1] = 0.0;
        vel[id][2] = 0.0;
    }
    
    pospeski(xyz,acc,sig_AB, eps_AB);
    
}