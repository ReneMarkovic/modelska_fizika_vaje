# Laboratorijski delovni list 4
## Molekularna dinamika: Lennard-Jonesova tekočina

Univerza v Mariboru · Fakulteta za naravoslovje in matematiko · Oddelek za fiziko

> [!IMPORTANT]
> **Programsko okolje: C++ in Python**
>
> Izjemoma je simulacija napisana v **C++** (hitrost pri $N^2$ parih delcev), analiza pa v **Pythonu** (virtualno okolje iz [vaje 00](../00_vaje/README.md)).
> - C++: prevajalnik `g++` (C++17), datoteke `src/main.cpp`, `src/Dinamika.cpp`, `src/Delci.h`
> - `numpy`: `np.round`, `np.linalg.norm`, `np.triu_indices`, `np.histogram`, `np.trapezoid`, `np.polyfit`
> - `pandas`: `pd.read_csv`; `matplotlib.pyplot`: `plot`, `loglog`, `axvline`
>
> Rešitev oddate kot Jupyter zvezek `.ipynb` z izvedenimi celicami in spremenjeno kodo C++.

PDF različica: [navodila/delovni_list_04.pdf](navodila/delovni_list_04.pdf)

---

## 1. Teoretične osnove in motivacija

Molekularna dinamika (MD) je metoda, pri kateri numerično rešujemo Newtonove enačbe za veliko število delcev, ki med seboj delujejo s parskimi silami. Iz trajektorij nato s statistično fiziko izračunamo makroskopske količine: temperaturo, energijo, tlak ali strukturo snovi. Danes bomo simulirali tekočino iz dveh vrst delcev, preverili ohranitev energije in izmerili strukturo tekočine.

> **Opis modela**
>
> $N$ delcev mase $m=1$ je v kocki z robom $L$ s periodičnimi robnimi pogoji. Delci med seboj delujejo z Lennard-Jonesovim potencialom. Polovica delcev je vrste A ($\sigma_A = 1$, $\varepsilon_A = 1$), polovica vrste B ($\sigma_B = 1{,}2$, $\varepsilon_B = 0{,}8$). Gibanje integriramo z metodo Verlet, temperaturo pa po potrebi uravnava Berendsenov termostat.

### Lennard-Jonesov potencial

Par delcev na razdalji $r$ ima potencialno energijo

$$
V(r) = 4\varepsilon\left[\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^{6}\right], \qquad F(r) = -\frac{\mathrm{d}V}{\mathrm{d}r} = \frac{24\varepsilon}{r}\left[2\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^{6}\right].
$$

Člen $r^{-12}$ opisuje odboj zaradi prekrivanja elektronskih oblakov, člen $r^{-6}$ pa van der Waalsov privlak. Za par različnih vrst uporabimo Lorentz-Berthelotovi pravili $\sigma_{AB} = (\sigma_A + \sigma_B)/2$ in $\varepsilon_{AB} = \sqrt{\varepsilon_A \varepsilon_B}$. Računamo v **reduciranih enotah**: dolžine v enotah $\sigma_A$, energije v enotah $\varepsilon_A$, $k_B = 1$.

### Periodični robovi, minimalna slika in odrez

Da se izognemo vplivu sten, prostor periodično ponovimo. Delec, ki zapusti škatlo, vstopi na nasprotni strani. Razdaljo med delcema računamo do najbližje periodične slike (**minimalna slika**):

$$
\Delta x \to \Delta x - L\,\mathrm{round}\!\left(\frac{\Delta x}{L}\right).
$$

Sile računamo le do **radija odreza** $r_c = 2{,}5\,\sigma$, ki mora biti manjši od $L/2$. Pri odrezanem potencialu ima energija ob prehodu delca čez $r_c$ skok $V(r_c)$. Skok odpravimo s **premaknjenim potencialom** $V_s(r) = V(r) - V(r_c)$ za $r<r_c$, ki sil ne spremeni.

### Metoda Verlet (velocity Verlet)

$$
\mathbf v\!\left(t+\tfrac{\Delta t}{2}\right) = \mathbf v(t) + \tfrac{\Delta t}{2}\,\mathbf a(t), \qquad \mathbf r(t+\Delta t) = \mathbf r(t) + \Delta t\,\mathbf v\!\left(t+\tfrac{\Delta t}{2}\right),
$$

$$
\mathbf v(t+\Delta t) = \mathbf v\!\left(t+\tfrac{\Delta t}{2}\right) + \tfrac{\Delta t}{2}\,\mathbf a(t+\Delta t).
$$

Metoda je časovno obrnljiva in simplektična, zato skupna energija ne leze sistematično, ampak le niha z amplitudo, sorazmerno z $\Delta t^2$.

### Temperatura in termostat

Iz ekviparticijskega izreka sledi trenutna temperatura $T = \dfrac{2E_k}{3Nk_B}$. Berendsenov termostat v vsakem koraku pomnoži vse hitrosti s faktorjem

$$
\lambda = \sqrt{1 + \frac{\Delta t}{\tau}\left(\frac{T_0}{T} - 1\right)},
$$

kar temperaturo s časovno konstanto $\tau$ približuje želeni $T_0$. S termostatom simuliramo kanonični ansambel (NVT), brez njega mikrokanoničnega (NVE), kjer se ohranja skupna energija.

### Radialna porazdelitvena funkcija

Struktura tekočine je opisana z $g(r)$: razmerjem med povprečno gostoto delcev na razdalji $r$ od izbranega delca in povprečno gostoto $\rho = N/L^3$. Iz histograma razdalj vseh parov $n(r)$ v lupinah debeline $\Delta r$, povprečenega po $M$ okvirjih, dobimo

$$
g(r) = \frac{n(r)}{M\cdot\tfrac{1}{2}N\rho\cdot\tfrac{4\pi}{3}\left[(r+\Delta r)^3 - r^3\right]}, \qquad n_1 = 4\pi\rho\int_0^{r_{\min}} r^2 g(r)\,\mathrm{d}r .
$$

Za idealni plin je $g=1$. Pri tekočini ima $g(r)$ izrazite vrhove, ki označujejo lupine sosedov. **Koordinacijsko število** $n_1$ je povprečno število sosedov do prvega minimuma $r_{\min}$.

---

## 2. Pripravljalna naloga (analitični del)

**P1. Lennard-Jonesov potencial.** Izpeljite $F(r)$. Pri kateri razdalji je potencial najmanjši in kolikšna je tam energija? Kolikšen je skok energije $V(r_c)$ za $r_c = 2{,}5\,\sigma$?

$r_{\min}=$ `__________`  $V(r_{\min})=$ `__________`  $V(r_c)=$ `__________`

**P2. Škatla.** Izračunajte rob škatle za $N = 216$ delcev pri gostoti $\rho = 0{,}8$. Ali je $r_c < L/2$? Funkcija `Inicializacija` postavi delce na kubično mrežo $6\times6\times6$. Kolikšna je razdalja med sosedi na mreži in kaj to pomeni za delce B?

$L=$ `__________`  $L/2=$ `__________`  razdalja na mreži: `__________`

**P3. Temperatura in termostat.** Kolikšna je povprečna kinetična energija sistema z $N = 216$ delci pri $T = 1$? Izračunajte faktor $\lambda$ za $T = 1{,}5$, $T_0 = 1$, $\Delta t = 0{,}005$ in $\tau = 1$.

$E_k=$ `__________`  $\lambda=$ `__________`

**P4. Napaka metode Verlet.** Pri $\Delta t = 0{,}005$ je standardni odklon skupne energije $0{,}07$. Kolikšnega pričakujete pri $\Delta t = 0{,}01$ in pri $\Delta t = 0{,}002$?

$\sigma_E(0{,}01)\approx$ `__________`  $\sigma_E(0{,}002)\approx$ `__________`

---

## 3. Laboratorijske naloge na računalniku (Python)

> **Repozitorij**
>
> Simulacija je v mapi [`04_vaje/src/`](src/), začetna predloga za analizo pa v repozitoriju predmeta: [`04_vaje/vaje_04.ipynb`](vaje_04.ipynb). Simulacijo prevedete in zaženete v mapi `04_vaje`. Po vsakem zagonu datoteki `data/energije.csv` in `data/trajektorija.xyz` preimenujte, kot je navedeno pri nalogi, sicer ju naslednji zagon prepiše.

```bash
g++ -std=c++17 -O3 -Isrc src/*.cpp -o simulacija.exe
./simulacija.exe
```

### Naloga 1: Nastavitev in prvi zagon (20 min)

1. V `src/main.cpp` nastavite $N = 216$ (`params.N_delcev`) in rob škatle iz gostote $\rho = 0{,}8$ (P2), na primer `const double L = std::cbrt(216 / 0.8);`. Ostale parametre pustite: $\Delta t = 0{,}005$, $T_0 = 1$, $20\,000$ korakov, termostat vklopljen.
2. Prevedite in zaženite. Rezultata preimenujte v `data/nvt_T1.0.csv` in `data/traj_T1.0.xyz`.
3. V zvezku dopolnite `L`, `lj_potencial` in `lj_sila` ter v *Testnem območju* preverite P1 in P2.
4. **Slika 1** (dva panela): (A) $E_k/N$, $E_p/N$ in $E/N$ v odvisnosti od časa, (B) $T(t)$.

| Količina | Vrednost |
|---|---|
| $E_p/N$ ob $t = 0$ | `__________` |
| čas ekvilibracije | `__________` |
| $\langle T\rangle \pm \sigma_T$ ($t > 10$) | `__________` |
| $\langle E_p\rangle/N$ ($t > 10$) | `__________` |
| $\langle E_k\rangle/N$ ($t > 10$) in primerjava s P3 | `__________` |

*Preglednica 1: Prvi zagon simulacije ($N = 216$, $\rho = 0{,}8$, $T_0 = 1$).*

### Naloga 2: Ohranitev energije (25 min)

1. V `main.cpp` vpeljite `const int N_ekv = max_korakov / 2;` in termostat omejite na ekvilibracijo: `if (use_thermostat && t < N_ekv)`. Druga polovica simulacije je tako NVE. Nastavite `log_interval` tako, da se energija zapiše vsakih $0{,}05$ časovne enote.
2. Pri $\Delta t = 0{,}005$ in $4000$ korakih zaženite simulacijo in rezultat shranite kot `data/nve_neprem_dt0.005.csv`.
3. V `src/Dinamika.cpp` (funkcija `IzracunSil`) uvedite premaknjen potencial:

```cpp
double s_div_rc = sigma / std::sqrt(rc_sq);
double V_rc = 4.0 * epsilon * (std::pow(s_div_rc, n) - std::pow(s_div_rc, m));
E_pot += V_r - V_rc;      // namesto E_pot += V_r;
```

4. Simulacijo dolžine $20$ časovnih enot ($10$ NVT + $10$ NVE) ponovite za $\Delta t =$ 0,002; 0,005; 0,01 in 0,015 ter rezultate shranite kot `data/nve_dt{dt}.csv`.
5. **Slika 2** (dva panela): (A) $E/N$ v odvisnosti od časa za vse $\Delta t$, (B) $\sigma_E$ v delu NVE v odvisnosti od $\Delta t$ v log–log merilu z naklonom premice.

| $\Delta t$ | potencial | $\langle E\rangle$ | $\sigma_E$ | $\sigma_E/\lvert\langle E\rangle\rvert$ |
|---|---|---|---|---|
| 0,005 | odrezan | `______` | `______` | `______` |
| 0,002 | premaknjen | `______` | `______` | `______` |
| 0,005 | premaknjen | `______` | `______` | `______` |
| 0,01 | premaknjen | `______` | `______` | `______` |
| 0,015 | premaknjen | `______` | `______` | `______` |

*Preglednica 2: Nihanje skupne energije v delu NVE.*

### Naloga 3: Radialna porazdelitvena funkcija (25 min)

1. Dopolnite funkcijo `minimalna_slika(dr, L)` brez zank (`np.round`).
2. Dopolnite funkcijo `rdf(poz, L, r_max)`: za vsak okvir izračunajte razdalje vseh parov $i<j$ z minimalno sliko (`np.triu_indices`), jih razvrstite v histogram in normirajte s številom parov idealnega plina.
3. Dopolnite funkcijo `koordinacijsko_stevilo` (`np.trapezoid`).
4. **Slika 3** (dva panela): (A) $g(r)$ iz druge polovice `traj_T1.0.xyz` do $L/2$ z označenim prvim minimumom, (B) ločeno $g_{AA}(r)$ in $g_{BB}(r)$.

```python
dr = minimalna_slika(okvir[:, None, :] - okvir[None, :, :], L)   # (N, N, 3)
r = np.linalg.norm(dr, axis=-1)[np.triu_indices(N, k=1)]
```

| Količina | Vrednost |
|---|---|
| lega prvega vrha $r_1$ (primerjava z $r_{\min}$ iz P1) | `__________` |
| višina prvega vrha $g(r_1)$ | `__________` |
| prvi minimum $r_{\min}$ | `__________` |
| koordinacijsko število $n_1$ | `__________` |
| lega prvega vrha $g_{AA}$ in $g_{BB}$ | `__________` |

*Preglednica 3: Struktura tekočine pri $T = 1$.*

### Naloga 4: Vpliv temperature (20 min)

Simulacijo (s premaknjenim potencialom in termostatom ves čas) ponovite pri $T_0 = 0{,}5$ in $T_0 = 2{,}0$ ter rezultate shranite kot `data/nvt_T{T}.csv` in `data/traj_T{T}.xyz`. Vse tri $g(r)$ narišite na skupen graf (**Slika 4**).

| $T_0$ | $\langle T\rangle$ | $\langle E_p\rangle/N$ | $r_1$ | $g(r_1)$ | $n_1$ |
|---|---|---|---|---|---|
| 0,5 | `______` | `______` | `______` | `______` | `______` |
| 1,0 | `______` | `______` | `______` | `______` | `______` |
| 2,0 | `______` | `______` | `______` | `______` | `______` |

*Preglednica 4: Vpliv temperature na energijo in strukturo.*

---

## 4. Vprašanja za razpravo in zaključni zagovor

> **Razmislek 1: Začetno stanje**
>
> Zakaj je potencialna energija ob $t = 0$ pozitivna in zelo velika? Kam se ta energija porazgubi? Kaj bi se zgodilo brez termostata? Pojasnite, zakaj je prvotna nastavitev v `main.cpp` ($N = 4096$, $L = 5$) privedla do »eksplozije« simulacije.

> **Razmislek 2: Simplektični integrator**
>
> Zakaj pri metodi Verlet energija niha, a ne leze, medtem ko bi pri Eulerjevi metodi s časom sistematično naraščala? Zakaj pri odrezanem potencialu nihanje energije ni več odvisno od $\Delta t$? Kateri $\Delta t$ bi izbrali za produkcijske simulacije in zakaj?

> **Razmislek 3: Struktura**
>
> Zakaj $g(r)$ pri majhnih $r$ izgine in pri velikih $r$ teži k 1? Kako se z naraščajočo temperaturo spreminjajo vrhovi $g(r)$? Kakšno $g(r)$ bi pričakovali za kristal s ploskovno centrirano kubično mrežo, kjer je $n_1 = 12$?

> **Razmislek 4: Zahtevnost in optimizacija (domača naloga)**
>
> Izračun sil zahteva $N(N-1)/2$ parov. Kolikokrat dlje traja korak pri $N = 4096$ kot pri $N = 216$? Opišite metodo celičnih seznamov (*cell lists*) in ocenite, kako se z njo zahtevnost spremeni.

---

### Dodatno gradivo

- [`resitve/vaje_04_resitev.ipynb`](resitve/vaje_04_resitev.ipynb): rešitev z izvedenimi celicami
- [`src/`](src/): simulacija v C++ (`Delci.h`: strukture, `Dinamika.cpp`: sile, Verlet, inicializacija, termostat, `main.cpp`: nastavitve in glavna zanka)
- [`Makefile`](Makefile): prevajanje z `make` (Linux/macOS; na Windows uporabite ukaz `g++` zgoraj)
- [`analiza.py`](analiza.py): samostojen skript za analizo energij in $g(r)$
- [`navodila/struktura_projekta.md`](navodila/struktura_projekta.md): predlagana struktura projekta C++
