Makefile Tools
analiza.py
N-Delci_LJ_Simulacija/
├── src/
│   ├── main.cpp
│   ├── Delci.h         // Definicije struktur (Particle, State, Params)
│   ├── Dinamika.cpp    // Funkcije (IzracunSil, Verlet)
│   ├── Analiza.h
│   └── ...
├── data/               // Za shranjevanje izhodnih podatkov (CSV, XYZ)
├── lib/                // Če uporabljate zunanje knjižnice
├── .vscode/            // Konfiguracijske datoteke za VS Code
│   ├── tasks.json      // Nastavitve za prevajanje (g++)
│   └── launch.json     // Nastavitve za razhroščevanje
└── Makefile            // (Opcijsko, a zelo priporočljivo za večje projekte!)