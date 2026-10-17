# Laboratorijski delovni list 7
## Grafi I: podatkovna struktura in osnovne metrike

Univerza v Mariboru · Fakulteta za naravoslovje in matematiko · Oddelek za fiziko

> [!IMPORTANT]
> **Programsko okolje: Python**
>
> Vse naloge rešujete **izključno v Pythonu** (virtualno okolje iz [vaje 00](../00_vaje/README.md)).
> - standardna knjižnica: `dict`, `set`, `collections.deque`
> - `numpy`: `np.random.default_rng`, `np.unique`, `np.mean`
> - `scipy.stats`: `poisson.pmf`; `matplotlib.pyplot`: `bar`, `plot`
> - `networkx`: le za preverjanje rezultatov (`nx.average_clustering`, `nx.average_shortest_path_length`)
>
> Rešitev oddate kot Jupyter zvezek `.ipynb` z izvedenimi celicami.

PDF različica: [navodila/delovni_list_07.pdf](navodila/delovni_list_07.pdf)

---

## 1. Teoretične osnove in motivacija

Realni sistemi so pogosto sestavljeni iz velikega števila povezanih komponent: proteini v celici, nevroni v možganih, ljudje v družbenih omrežjih, elektrarne v elektroenergetskem omrežju. Ne glede na področje jih lahko opišemo z **grafom**: množico **vozlišč** (komponent) in množico **povezav** (interakcij). Struktura grafa pogosto odločilno vpliva na dinamiko procesov na njem, na primer na širjenje bolezni ali sinhronizacijo. Na tej vaji napišemo lastno podatkovno strukturo za graf in izračunamo njegove osnovne metrike. Na naslednji vaji bomo generirali grafe različnih topologij.

> **Opis modela**
>
> Obravnavamo neusmerjene grafe brez zank in večkratnih povezav. Graf $G = (V, E)$ ima $n = |V|$ vozlišč in $m = |E|$ povezav. Shranimo ga kot **seznam sosednosti**: slovar, ki vsakemu vozlišču priredi množico njegovih sosedov.

### Globalne metrike

**Povprečna stopnja** in **gostota** grafa sta

$$
\langle k\rangle = \frac{2m}{n}, \qquad D = \frac{2m}{n(n-1)} .
$$

**Razdalja** $d(u,v)$ je število povezav na najkrajši poti med vozliščema. Na povezanem grafu definiramo **povprečno najkrajšo pot** in **premer**:

$$
L = \frac{1}{n(n-1)}\sum_{u \ne v} d(u,v), \qquad d_{\max} = \max_{u,v} d(u,v).
$$

Razdalje od izbranega vozlišča do vseh ostalih izračunamo z **iskanjem v širino** (BFS): vozlišča obiskujemo po vrsti (FIFO), vsak nov sosed dobi razdaljo za 1 večjo od trenutnega vozlišča. Z BFS poiščemo tudi **povezane komponente** grafa.

### Lokalne metrike

**Stopnja** vozlišča $k_i$ je število njegovih sosedov. **Lokalna gručavost** pove, kolikšen delež parov sosedov je med seboj povezan:

$$
c_i = \frac{2e_i}{k_i(k_i - 1)}, \qquad C = \frac{1}{n}\sum_i c_i,
$$

kjer je $e_i$ število povezav med sosedi vozlišča $i$ (za $k_i < 2$ vzamemo $c_i = 0$). $C$ je **povprečna gručavost** grafa.

### Dva referenčna modela

V **naključnem grafu** Erdős-Rényi $G(n,p)$ je vsak par vozlišč povezan z verjetnostjo $p$. Stopnje so porazdeljene binomsko, za velike $n$ pa približno Poissonovo:

$$
P(k) = \frac{\langle k\rangle^k e^{-\langle k\rangle}}{k!}, \qquad \langle k\rangle = p(n-1), \qquad C \approx p, \qquad L \approx \frac{\ln n}{\ln\langle k\rangle}.
$$

V **pravilni obročasti mreži** je vsako od $n$ vozlišč povezano s $k/2$ najbližjimi sosedi na vsaki strani. Zanjo velja

$$
C = \frac{3(k-2)}{4(k-1)}, \qquad L \approx \frac{n}{2k}.
$$

Naključni graf ima majhno gručavost in kratke poti, obroč pa veliko gručavost in dolge poti.

---

## 2. Pripravljalna naloga (analitični del)

**P1. Majhen graf.** Graf ima 6 vozlišč in povezave $(0,1)$, $(0,2)$, $(1,2)$, $(2,3)$, $(3,4)$, $(3,5)$, $(4,5)$. Narišite ga in izračunajte $n$, $m$, $\langle k\rangle$, $D$ ter stopnje vseh vozlišč.

$n=$ `______`  $m=$ `______`  $\langle k\rangle=$ `______`  $D=$ `______`

**P2. Gručavost.** Za graf iz P1 izračunajte lokalne gručavosti vseh vozlišč in povprečno gručavost $C$.

| vozlišče | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $k_i$ | `____` | `____` | `____` | `____` | `____` | `____` |
| $c_i$ | `____` | `____` | `____` | `____` | `____` | `____` |

*Preglednica P2: Stopnje in lokalne gručavosti grafa iz P1.*

$C=$ `__________`

**P3. Razdalje.** Za graf iz P1 zapišite razdalje od vozlišča 0 do vseh ostalih. Kolikšen je premer? Izračunajte $L$ (vseh urejenih parov je 30). Kaj se zgodi, če odstranimo povezavo $(2,3)$?

$L=$ `__________`  $d_{\max}=$ `__________`

**P4. Referenčna modela.** Za $n = 200$ izračunajte $\langle k\rangle$, $C$ in $L$ za $G(n,p)$ s $p = 0{,}05$ ter $C$ in $L$ za obroč s $k = 4$ in $k = 10$.

$G(n,p)$: `______________`  obroč $k=4$: `__________`  obroč $k=10$: `__________`

---

## 3. Laboratorijske naloge na računalniku (Python)

> **Repozitorij**
>
> Začetna predloga je v repozitoriju predmeta: [`07_vaje/vaje_07.ipynb`](vaje_07.ipynb). V razdelku *Funkcije* dopolnite metode razreda `Graf` in funkcije z oznako `TODO`, v razdelku *Testno območje* pa sestavite graf iz P1.

### Naloga 1: Podatkovna struktura grafa (20 min)

1. Dopolnite metode razreda `Graf`: `dodaj_vozlisce`, `dodaj_povezavo` (zank ne dodajamo, manjkajoča vozlišča dodamo samodejno), `odstrani_povezavo`, `odstrani_vozlisce` in `m`.
2. Dopolnite funkciji `povprecna_stopnja` in `gostota`.
3. Preverite, da podvojena povezava in zanka ne spremenita grafa iz P1. Na kopiji grafa odstranite povezavo $(2,3)$ in vozlišče 5 ter izpišite seznam sosednosti.

```python
class Graf:
    def __init__(self):
        self.sosedje = {}          # vozlišče -> množica sosedov
    def dodaj_povezavo(self, u, v):
        ...                        # TODO
```

| Količina | P1 (ročno) | Numerično |
|---|---|---|
| $n$, $m$ | `______` | `______` |
| $\langle k\rangle$ | `______` | `______` |
| $D$ | `______` | `______` |
| $n$, $m$ po odstranitvi | `______` | `______` |

*Preglednica 1: Osnovne lastnosti grafa iz P1.*

### Naloga 2: Gručavost (15 min)

Dopolnite funkciji `lokalna_grucavost(G, v)` in `povprecna_grucavost(G)`. Rezultate za graf iz P1 primerjajte s P2 in s funkcijo `nx.average_clustering`.

| Količina | P2 (ročno) | Numerično | `networkx` |
|---|---|---|---|
| $c_2$ | `______` | `______` | `______` |
| $c_3$ | `______` | `______` | `______` |
| $C$ | `______` | `______` | `______` |

*Preglednica 2: Gručavost grafa iz P1.*

### Naloga 3: Najkrajše poti in komponente (25 min)

1. Dopolnite funkcijo `bfs(G, izvor)`, ki vrne slovar razdalj od izvora, z vrsto `collections.deque`.
2. Funkcija `komponente(G)` z BFS poišče povezane komponente. Dopolnite funkcijo `razdalje(G)`, ki na največji komponenti izračuna $L$ in premer.
3. Rezultate primerjajte s P3 in z `nx.average_shortest_path_length`. Preverite, koliko komponent ima graf brez povezave $(2,3)$.

| Količina | P3 (ročno) | Numerično | `networkx` |
|---|---|---|---|
| razdalje od vozlišča 0 | `______` | `______` | – |
| $L$ | `______` | `______` | `______` |
| premer | `______` | `______` | – |
| komponente brez $(2,3)$ | `______` | `______` | – |

*Preglednica 3: Razdalje v grafu iz P1.*

### Naloga 4: Naključni graf in obroč (30 min)

1. Dopolnite generatorja `nakljucni_graf(n, p)` in `obroc(n, k)`.
2. Za $n = 200$ izračunajte metrike za $G(n,p)$ s $p \in \{0{,}01;\ 0{,}02;\ 0{,}05;\ 0{,}1\}$ in za obroča s $k = 4$ in $k = 10$. Primerjajte jih s teoretičnimi napovedmi.
3. **Slika 1**: porazdelitev stopenj $P(k)$ za $G(1000;\ 0{,}01)$ in Poissonova porazdelitev z enakim $\langle k\rangle$.

| Graf | $\langle k\rangle$ (teor.) | $\langle k\rangle$ | $C$ (teor.) | $C$ | $L$ (teor.) | $L$ | največja komp. |
|---|---|---|---|---|---|---|---|
| $G(n;\ 0{,}01)$ | `____` | `____` | `____` | `____` | `____` | `____` | `____` |
| $G(n;\ 0{,}02)$ | `____` | `____` | `____` | `____` | `____` | `____` | `____` |
| $G(n;\ 0{,}05)$ | `____` | `____` | `____` | `____` | `____` | `____` | `____` |
| $G(n;\ 0{,}1)$ | `____` | `____` | `____` | `____` | `____` | `____` | `____` |
| obroč $k=4$ | 4 | `____` | `____` | `____` | `____` | `____` | `____` |
| obroč $k=10$ | 10 | `____` | `____` | `____` | `____` | `____` | `____` |

*Preglednica 4: Metrike naključnih grafov in obročev ($n = 200$).*

---

## 4. Vprašanja za razpravo in zaključni zagovor

> **Razmislek 1: Izbira podatkovne strukture**
>
> Zakaj smo sosede shranili v množice in ne v sezname? Koliko pomnilnika potrebuje seznam sosednosti in koliko matrika sosednosti za graf z $n = 10^6$ vozlišči in $\langle k\rangle = 10$? Kdaj je matrika sosednosti vseeno ugodnejša?

> **Razmislek 2: Zahtevnost algoritmov**
>
> Kakšna je časovna zahtevnost BFS iz enega vozlišča in kakšna izračuna $L$ za cel graf? Kako se z $\langle k\rangle$ spreminja čas izračuna lokalne gručavosti? Kako bi $L$ ocenili za zelo velik graf?

> **Razmislek 3: Povezanost naključnega grafa**
>
> Pri $p = 0{,}01$ graf ni povezan. Pri kateri vrednosti $\langle k\rangle$ se v $G(n,p)$ pojavi velika (»orjaška«) komponenta? Zakaj se pri $p = 0{,}1$ izmerjeni $L$ precej razlikuje od ocene $\ln n/\ln\langle k\rangle$?

> **Razmislek 4: Realna omrežja (domača naloga)**
>
> Realna omrežja imajo pogosto veliko gručavost kot obroč in kratke poti kot naključni graf. Poiščite podatke o enem realnem omrežju (npr. omrežje sodelovanja ali prijateljstev) in ocenite, ali ima to lastnost. Kako bi tak graf generirali? (Odgovor bomo iskali na vaji 8.)

---

### Dodatno gradivo

- [`resitve/vaje_07_resitev.ipynb`](resitve/vaje_07_resitev.ipynb): rešitev z izvedenimi celicami
- [`navodila/README_izvirni.md`](navodila/README_izvirni.md): izvirna navodila z uvodom v grafe in predlogo modula `GraphAL`
- [`GraphAL/`](GraphAL/) in [`main.py`](main.py): začetek modula `GraphAL`, napisan med vajami 2024 (nedokončan: datoteke `example.py`, `graph_export.py`, `graph_operations.py` in `graph_visualization.py` so prazne; napake v `Graph.add_node`, `regular_graph`, `graph_density` in `clustering_coefficient` so popravljene, funkcija `Morita` pa ima namerno napako za domačo nalogo vaje 08)
- [`navodila/figures.svg`](navodila/figures.svg): slike za predavanje
