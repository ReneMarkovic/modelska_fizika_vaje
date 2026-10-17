# Laboratorijski delovni list 13
## Nevronske mreže: propagacija naprej in vzvratno razširjanje napake

Univerza v Mariboru · Fakulteta za naravoslovje in matematiko · Oddelek za fiziko

> [!IMPORTANT]
> **Programsko okolje: Python**
>
> Vse naloge rešujete **izključno v Pythonu** (virtualno okolje iz [vaje 00](../00_vaje/README.md)).
> - `numpy`: matrično množenje `@`, `np.tanh`, `np.exp`, `np.random.default_rng`, `np.ndindex`, `np.meshgrid`
> - `matplotlib.pyplot`: `plot`, `loglog`, `contourf`, `scatter`
>
> Knjižnic za strojno učenje (`scikit-learn`, `pytorch`) ne uporabljamo: mrežo napišemo sami. Rešitev oddate kot Jupyter zvezek `.ipynb` z izvedenimi celicami.

PDF različica: [navodila/delovni_list_13.pdf](navodila/delovni_list_13.pdf)

---

## 1. Teoretične osnove in motivacija

Umetne nevronske mreže so prilagodljivi modeli, ki se iz podatkov naučijo zveze med vhodom in izhodom. V fiziki jih uporabljamo za aproksimacijo funkcij, razvrščanje signalov (npr. v fiziki delcev), pospeševanje simulacij in reševanje inverznih problemov. Na tej vaji napišemo večplastni perceptron od začetka: propagacijo naprej, izračun gradienta z vzvratnim razširjanjem napake in učenje z gradientnim spustom, ki ga poznamo z vaje 6.

> **Opis modela**
>
> Mreža z arhitekturo $[n_0, n_1, \dots, n_L]$ ima $n_0$ vhodov, $L - 1$ skritih plasti in $n_L$ izhodov. Vsaka plast je polno povezana z naslednjo. Uteži poiščemo tako, da je izguba na učnih podatkih čim manjša.

### Propagacija naprej

Paket $N$ vhodnih vektorjev zložimo v matriko $\mathbf A_0 = X$ velikosti $N \times n_0$. Plast $l$ ima matriko uteži $W_l$ ($n_{l-1}\times n_l$), vektor pragov $\mathbf b_l$ in aktivacijsko funkcijo $f_l$:

$$
Z_l = A_{l-1}W_l + \mathbf b_l, \qquad A_l = f_l(Z_l), \qquad l = 1, \dots, L .
$$

Izhod mreže je $\hat Y = A_L$. Pogoste aktivacijske funkcije so

$$
\tanh z,\quad \sigma(z) = \frac{1}{1+e^{-z}},\quad \mathrm{ReLU}(z) = \max(0, z), \qquad \sigma' = \sigma(1-\sigma), \quad \tanh' = 1 - \tanh^2 .
$$

Brez nelinearnih aktivacij bi bila mreža le linearna preslikava, ne glede na število plasti.

### Izguba

Za regresijo uporabimo povprečno kvadratno napako, za razvrščanje v dva razreda (izhod s sigmoido) pa binarno navzkrižno entropijo:

$$
\mathcal L_{\rm MSE} = \frac{1}{N}\sum_{i}\left(\hat y_i - y_i\right)^2, \qquad \mathcal L_{\rm BCE} = -\frac{1}{N}\sum_i\left[y_i\ln\hat y_i + (1-y_i)\ln(1-\hat y_i)\right].
$$

### Vzvratno razširjanje napake

Gradient izgube po vseh utežeh izračunamo z verižnim pravilom od izhoda proti vhodu. Naj bo $\Delta_l = \partial\mathcal L/\partial Z_l$ (matrika $N\times n_l$). Potem je

$$
\Delta_L = \frac{\partial\mathcal L}{\partial A_L}\odot f_L'(Z_L), \qquad \Delta_{l-1} = \left(\Delta_l W_l^{\top}\right)\odot f_{l-1}'(Z_{l-1}),
$$

$$
\frac{\partial\mathcal L}{\partial W_l} = A_{l-1}^{\top}\Delta_l, \qquad \frac{\partial\mathcal L}{\partial \mathbf b_l} = \sum_{i=1}^{N}(\Delta_l)_{i,:},
$$

kjer je $\odot$ množenje po elementih. Uteži nato posodobimo z gradientnim spustom $W_l \leftarrow W_l - \eta\,\partial\mathcal L/\partial W_l$. Pravilnost implementacije preverimo z **numeričnim gradientom** (centralne diference, vaja 6).

### Inicializacija, posplošitev in prekomerno prilagajanje

Uteži začetno izberemo naključno, sicer bi vsi nevroni v plasti ostali enaki. Pri Xavierjevi inicializaciji je $W_{ij} \sim \mathcal N(0, 1/n_{l-1})$, pragovi so nič. Uspešnost mreže merimo na **testnih podatkih**, ki jih pri učenju nismo uporabili. Mreža z (pre)velikim številom parametrov se lahko nauči šuma v učnih podatkih (prekomerno prilagajanje), zato je testna napaka večja od učne.

---

## 2. Pripravljalna naloga (analitični del)

**P1. Aktivacijske funkcije.** Izračunajte vrednosti in odvode funkcij $\tanh$, $\sigma$ in ReLU pri $z = 0$. Pokažite, da je $\sigma'(z) = \sigma(z)[1 - \sigma(z)]$. Kje je odvod ReLU nedefiniran?

| | $\tanh$ | $\sigma$ | ReLU |
|---|---|---|---|
| $f(0)$ | `______` | `______` | `______` |
| $f'(0)$ | `______` | `______` | `______` |

*Preglednica P1: Aktivacijske funkcije pri $z = 0$.*

**P2. Število parametrov.** Koliko uteži in pragov imajo mreže z arhitekturo $[1, 10, 1]$, $[2, 8, 1]$ in $[2, 2, 1]$? Zapišite splošno formulo.

$[1,10,1]$: `______`  $[2,8,1]$: `______`  $[2,2,1]$: `______`

**P3. En nevron na roke.** Nevron s sigmoido ima uteži $\mathbf w = (0{,}5;\ -1)$ in prag $b = 0{,}2$. Za vhod $\mathbf x = (1;\ 2)$ in želeni izhod $y = 1$ izračunajte $z$, $\hat y$, $\mathcal L_{\rm MSE}$ ter gradienta $\partial\mathcal L/\partial\mathbf w$ in $\partial\mathcal L/\partial b$.

$z=$ `______`  $\hat y=$ `______`  $\mathcal L=$ `______`  $\partial\mathcal L/\partial\mathbf w=$ `____________`  $\partial\mathcal L/\partial b=$ `______`

**P4. Linearna ločljivost.** Pokažite, da en nevron (brez skrite plasti) ne more pravilno razvrstiti točk dveh koncentričnih obročev. Najmanj koliko skritih nevronov s funkcijo $\tanh$ bi po vašem mnenju potrebovali, da bi odločitvena meja obdala notranji obroč?

odgovor: `____________________`

---

## 3. Laboratorijske naloge na računalniku (Python)

> **Repozitorij**
>
> Začetna predloga je v repozitoriju predmeta: [`13_vaje/vaje_13.ipynb`](vaje_13.ipynb). V razdelku *Funkcije* dopolnite telesa funkcij z oznako `TODO`, v razdelku *Testno območje* pa preverite rezultate nalog P1–P3.

### Naloga 1: Aktivacijske funkcije (15 min)

Dopolnite funkcijo `aktivacija(z, ime, odvod)` za funkcije `tanh`, `sigmoid`, `relu` in `linear`. **Slika 1** (dva panela): funkcije in njihovi odvodi na intervalu $[-4, 4]$. Analitične odvode primerjajte z numeričnimi (`np.gradient`).

| Funkcija | $\tanh$ | $\sigma$ | ReLU | linearna |
|---|---|---|---|---|
| mediana napake odvoda | `______` | `______` | `______` | `______` |
| največja napaka odvoda | `______` | `______` | `______` | `______` |

*Preglednica 1: Primerjava analitičnih in numeričnih odvodov.*

### Naloga 2: Propagacija naprej in nazaj (25 min)

1. Dopolnite funkcije `ustvari_mrezo` (Xavierjeva inicializacija), `naprej`, `izguba` (MSE) in `nazaj`.
2. Na mreži $[2, 3, 1]$ (skrita plast $\tanh$, izhod linearen) s petimi naključnimi vzorci primerjajte gradient, izračunan z vzvratnim razširjanjem, z numeričnim gradientom (funkcija `numericni_gradient`). Izračunajte relativno napako $\lVert g_{\rm bp} - g_{\rm num}\rVert / \lVert g_{\rm bp} + g_{\rm num}\rVert$.

```python
for l in reversed(range(len(mreza))):
    grad[l] = (As[l].T @ delta, delta.sum(axis=0))
    if l > 0:
        delta = ...      # TODO: (delta W_l^T) * f'(Z_{l-1})
```

| Plast | $\lVert\partial\mathcal L/\partial W\rVert$ | rel. napaka $\partial\mathcal L/\partial W$ | rel. napaka $\partial\mathcal L/\partial\mathbf b$ |
|---|---|---|---|
| 1 (skrita) | `______` | `______` | `______` |
| 2 (izhodna) | `______` | `______` | `______` |

*Preglednica 2: Preverjanje gradienta.*

### Naloga 3: Regresija (25 min)

1. Dopolnite funkcijo `uci` (gradientni spust na celotnem paketu).
2. Mrežo $[1, 10, 1]$ (skrita plast $\tanh$, izhod linearen) naučite funkcije $y = \sin 2\pi x$ iz 40 šumnih točk ($\sigma_{\rm šum} = 0{,}1$) s 5000 epohami pri $\eta \in \{0{,}01;\ 0{,}05;\ 0{,}2\}$. Testno napako izračunajte na 200 točkah brez šuma.
3. **Slika 2** (dva panela): (A) učna izguba v odvisnosti od epohe (log–log), (B) napovedi mrež in učni podatki.
4. Pri $\eta = 0{,}05$ ponovite učenje za 1, 3, 10 in 30 skritih nevronov.

| Mreža | $\eta$ | MSE učna | MSE testna |
|---|---|---|---|
| $[1, 10, 1]$ | 0,01 | `______` | `______` |
| $[1, 10, 1]$ | 0,05 | `______` | `______` |
| $[1, 10, 1]$ | 0,2 | `______` | `______` |
| $[1, 1, 1]$ | 0,05 | `______` | `______` |
| $[1, 3, 1]$ | 0,05 | `______` | `______` |
| $[1, 30, 1]$ | 0,05 | `______` | `______` |

*Preglednica 3: Regresija funkcije $\sin 2\pi x$.*

### Naloga 4: Razvrščanje (25 min)

Generirajte dva koncentrična obroča (polmera 1 in 2, šum $0{,}15$, 200 točk vsak). Mreže $[2, n, 1]$ s skrito plastjo $\tanh$ in izhodom s sigmoido naučite z izgubo BCE ($\eta = 1$, 3000 epoh) za $n = 1, 2, 4, 8$. **Slika 3**: odločitvene meje ($\hat y = 0{,}5$) in podatki za vse štiri mreže.

| Skritih nevronov $n$ | 1 | 2 | 4 | 8 |
|---|---|---|---|---|
| število parametrov | `______` | `______` | `______` | `______` |
| $\mathcal L_{\rm BCE}$ | `______` | `______` | `______` | `______` |
| točnost | `______` | `______` | `______` | `______` |

*Preglednica 4: Razvrščanje dveh koncentričnih obročev.*

---

## 4. Vprašanja za razpravo in zaključni zagovor

> **Razmislek 1: Zakaj vzvratno razširjanje?**
>
> Koliko izračunov izgube bi potrebovali za numerični gradient mreže z $10^6$ utežmi in koliko za gradient z vzvratnim razširjanjem? Zakaj je preverjanje z numeričnim gradientom kljub temu pomembno?

> **Razmislek 2: Učni korak**
>
> Zakaj se mreža pri $\eta = 0{,}01$ v 5000 epohah ne nauči funkcije, pri $\eta = 0{,}2$ pa je rezultat slabši kot pri $\eta = 0{,}05$? Primerjajte z ugotovitvami o stabilnosti gradientnega spusta z vaje 6.

> **Razmislek 3: Kapaciteta mreže**
>
> Kako se z naraščanjem števila skritih nevronov spreminjata učna in testna napaka? Kdaj pride do prekomernega prilagajanja? Zakaj ena skrita plast z dovolj nevroni v principu lahko aproksimira poljubno zvezno funkcijo, v praksi pa uporabljamo globlje mreže?

> **Razmislek 4: Fizikalna uporaba (domača naloga)**
>
> Z mrežo $[1, n, 1]$ aproksimirajte Lennard-Jonesov potencial z vaje 4 na intervalu $r \in [0{,}95;\ 2{,}5]$. Kako bi zagotovili, da je sila, izračunana kot odvod naučene mreže, dovolj natančna za simulacijo molekularne dinamike?

---

### Dodatno gradivo

- [`resitve/vaje_13_resitev.ipynb`](resitve/vaje_13_resitev.ipynb): rešitev z izvedenimi celicami
- [`navodila/README_izvirni.md`](navodila/README_izvirni.md): izvirna navodila (ideja modula za nevronske mreže)
- [`main.py`](main.py) in paket [`silicon_mind/`](silicon_mind/): objektna različica mreže z razredi plasti, začeta na vajah 2023; popravljena sta odvod izgube v `Network.use` in odvečna plast v `ustvari_nevronsko_mrezo` (pragovi se posodabljajo s celotnim `output_error`, učenje poteka po en vzorec naenkrat)
