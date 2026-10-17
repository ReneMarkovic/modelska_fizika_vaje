# Laboratorijski delovni list 8
## Grafi II: generatorji topologij, izris in izvoz

Univerza v Mariboru · Fakulteta za naravoslovje in matematiko · Oddelek za fiziko

> [!IMPORTANT]
> **Programsko okolje: Python**
>
> Vse naloge rešujete **izključno v Pythonu** (virtualno okolje iz [vaje 00](../00_vaje/README.md)).
> - `numpy`: `np.random.default_rng`, `np.logspace`, `np.histogram`, `np.polyfit`, `np.add.at`
> - `json`: `json.dump`, `json.load`; `pathlib`: `Path`
> - `matplotlib.pyplot`: `semilogx`, `loglog`, `scatter`
> - `networkx`: `nx.gnm_random_graph`, `nx.write_graphml`, `nx.read_graphml` (primerjava in izvoz)
>
> Rešitev oddate kot Jupyter zvezek `.ipynb` z izvedenimi celicami.

PDF različica: [navodila/delovni_list_08.pdf](navodila/delovni_list_08.pdf)

---

## 1. Teoretične osnove in motivacija

Na vaji 7 smo videli, da ima naključni graf kratke poti in majhno gručavost, pravilni obroč pa veliko gručavost in dolge poti. Realna omrežja pogosto združujejo obe lastnosti (**mali svet**), poleg tega pa imajo nekaj vozlišč z zelo veliko povezavami (**zvezdišča**, angl. *hubs*). Danes napišemo generatorja, ki ti lastnosti pojasnita, grafe narišemo in jih izvozimo v standardne zapise.

> **Opis modela**
>
> Uporabimo razred `Graf` z vaje 7. Generiramo grafe Watts-Strogatz (prevezan obroč) in Barabási-Albert (rast s preferenčnim pripenjanjem), izmerimo njihove metrike, jih narišemo s krožno in silno usmerjeno razporeditvijo ter izvozimo v zapise CSV, JSON in GraphML.

### Model Watts-Strogatz (mali svet)

Začnemo s pravilnim obročem z $n$ vozlišči in stopnjo $k$. Vsako povezavo $(i, i+j)$ z verjetnostjo $p$ **prevežemo**: krajišče $i+j$ zamenjamo z naključnim vozliščem $w$, pri čemer se izognemo zankam in podvojenim povezavam. Število povezav se ne spremeni, pričakovano število prevezanih povezav je $p\,nk/2$. Pri $p = 0$ imamo obroč, pri $p = 1$ približno naključni graf. Že nekaj prevezanih povezav ustvari »bližnjice«, ki močno skrajšajo $L(p)$, gručavost $C(p)$ pa ostane skoraj nespremenjena. Za obroč velja

$$
C(0) = \frac{3(k-2)}{4(k-1)}, \qquad L(0) \approx \frac{n}{2k}.
$$

### Model Barabási-Albert (brezlestvična omrežja)

Začnemo s polnim grafom z $m+1$ vozlišči. V vsakem koraku dodamo novo vozlišče in ga povežemo z $m$ različnimi obstoječimi vozlišči. Verjetnost, da izberemo vozlišče $i$, je sorazmerna z njegovo stopnjo (**preferenčno pripenjanje**):

$$
\Pi(k_i) = \frac{k_i}{\sum_j k_j}.
$$

Izbiro izvedemo preprosto: hranimo seznam krajišč vseh povezav, v katerem se vozlišče $i$ pojavi $k_i$-krat, in iz njega enakomerno žrebamo. V zveznem približku stopnja vozlišča, dodanega v času $t_i$, raste kot $k_i(t) = m\sqrt{t/t_i}$, od koder sledi potenčna porazdelitev stopenj

$$
P(k) \approx 2m^2 k^{-3}, \qquad P(K \ge k) = \left(\frac{m}{k}\right)^2, \qquad k_{\max} \approx m\sqrt{n}.
$$

Ker je $P(k)$ pri velikih $k$ zelo majhen, ga ocenimo s histogramom z **logaritemskimi razredi** in vsako frekvenco delimo s širino razreda.

### Izris grafa

Pri **krožni razporeditvi** vozlišča enakomerno razporedimo po krožnici. Pri **Fruchterman-Reingoldovi** (silno usmerjeni) razporeditvi se vsi pari vozlišč odbijajo s silo $k_{\rm opt}^2/d$, povezana vozlišča pa se privlačijo s silo $d^2/k_{\rm opt}$, kjer je $k_{\rm opt}$ želena razdalja med vozlišči. Vozlišča premikamo v smeri rezultante, največji premik pa omejimo s »temperaturo«, ki jo postopoma zmanjšujemo.

### Zapisi grafov

- **seznam povezav (CSV)**: vrstica `vir,cilj` za vsako povezavo, preprost in kompakten zapis,
- **JSON**: slovar s seznamom vozlišč in seznamom povezav, preprost za branje v različnih jezikih,
- **GraphML**: zapis XML, ki ga berejo programi za analizo omrežij (npr. Gephi, Cytoscape) in lahko hrani tudi atribute vozlišč in povezav.

---

## 2. Pripravljalna naloga (analitični del)

**P1. Obroč in prevezovanje.** Za obroč z $n = 500$ in $k = 10$ izračunajte $C(0)$, $L(0)$ in število povezav. Koliko povezav v povprečju prevežemo pri $p = 0{,}01$?

$C(0)=$ `________`  $L(0)=$ `________`  $m=$ `________`  prevezanih: `________`

**P2. Barabási-Albert.** Za $n = 2000$ in $m = 2$ ocenite število povezav, $\langle k\rangle$, $k_{\max}$ in pričakovano število vozlišč s stopnjo $k \ge 20$. Koliko takih vozlišč bi pričakovali v naključnem grafu z enakim $\langle k\rangle$?

$\langle k\rangle=$ `________`  $k_{\max}\approx$ `________`  $N(k \ge 20)\approx$ `________`

**P3. Potenčni zakon.** Iz $k_i(t) = m\sqrt{t/t_i}$ pokažite, da je delež vozlišč s stopnjo večjo od $k$ enak $(m/k)^2$, in od tod izpeljite $P(k) \propto k^{-3}$. Kateri naklon pričakujete na grafu $P(k)$ v log–log merilu?

naklon: `__________`

**P4. Razporeditev in pomnilnik.** Pri kateri razdalji sta sili med dvema povezanima vozliščema v Fruchterman-Reingoldovi razporeditvi v ravnovesju? Koliko elementov ima matrika sosednosti za graf iz P2 in koliko vrstic seznam povezav?

$d_{\rm ravn}=$ `________`  matrika: `________`  seznam: `________`

---

## 3. Laboratorijske naloge na računalniku (Python)

> **Repozitorij**
>
> Začetna predloga je v repozitoriju predmeta: [`08_vaje/vaje_08.ipynb`](vaje_08.ipynb). Razred `Graf` in metrike z vaje 7 so že vneseni. V razdelku *Funkcije* dopolnite telesa funkcij z oznako `TODO`, v razdelku *Testno območje* pa preverite rezultata nalog P1 in P2.

### Naloga 1: Mali svet (25 min)

1. Dopolnite funkcijo `watts_strogatz(n, k, p)`. V *Testnem območju* preverite število prevezanih povezav pri $p = 0{,}01$.
2. Za $n = 500$, $k = 10$ in $13$ vrednosti $p$ med $10^{-4}$ in $1$ (`np.logspace`) izračunajte $C(p)/C(0)$ in $L(p)/L(0)$, povprečeni po dveh ponovitvah.
3. **Slika 1**: obe razmerji v odvisnosti od $p$ (logaritemska os $x$). V katerem območju $p$ je graf »mali svet«?

| $p$ | $10^{-3}$ | $10^{-2}$ | $10^{-1}$ | $1$ |
|---|---|---|---|---|
| $C(p)/C(0)$ | `______` | `______` | `______` | `______` |
| $L(p)/L(0)$ | `______` | `______` | `______` | `______` |

*Preglednica 1: Gručavost in povprečna pot v modelu Watts-Strogatz ($n = 500$, $k = 10$).*

### Naloga 2: Preferenčno pripenjanje (25 min)

1. Dopolnite funkcijo `barabasi_albert(n, m)` s seznamom krajišč.
2. Generirajte graf z $n = 2000$ in $m = 2$ ter naključni graf z enakim številom vozlišč in povezav (`nx.gnm_random_graph`).
3. **Slika 2**: porazdelitev stopenj obeh grafov v log–log merilu. Za BA uporabite logaritemske razrede in prilagodite premico. Primerjajte naklon s P3.

```python
robovi = np.unique(np.logspace(np.log10(2), np.log10(k_max + 1), 15).astype(int))
h, _ = np.histogram(stopnje, bins=robovi)
P = h / np.diff(robovi) / len(stopnje)
```

| Količina | BA (P2) | BA | naključni graf |
|---|---|---|---|
| $\langle k\rangle$ | `______` | `______` | `______` |
| $k_{\max}$ | `______` | `______` | `______` |
| delež vozlišč s $k \ge 20$ | `______` | `______` | `______` |
| $C$ | – | `______` | `______` |
| naklon $P(k)$ | `______` | `______` | – |

*Preglednica 2: Primerjava grafa Barabási-Albert in naključnega grafa ($n = 2000$, $m = 2$).*

### Naloga 3: Izris grafov (20 min)

1. Dopolnite izračun sil v funkciji `fr_razporeditev(G)`: odbojne sile med vsemi pari (z `numpy` brez zank) in privlačne sile po povezavah (`np.add.at`).
2. **Slika 3** (dve vrsti po štiri panele): obroč ($n = 60$, $k = 4$), WS s $p = 0{,}1$, BA z $m = 1$ in BA z $m = 2$, zgoraj v krožni, spodaj v Fruchterman-Reingoldovi razporeditvi. Velikost in barva vozlišča naj ustrezata stopnji.
3. Katera razporeditev bolje pokaže strukturo posameznega grafa? Kje opazite zvezdišča?

| Graf | najvišja stopnja | opis strukture (FR) |
|---|---|---|
| obroč | `______` | `____________________` |
| WS $p = 0{,}1$ | `______` | `____________________` |
| BA $m = 1$ | `______` | `____________________` |
| BA $m = 2$ | `______` | `____________________` |

*Preglednica 3: Izris grafov z 60 vozlišči.*

### Naloga 4: Izvoz in uvoz (20 min)

1. Dopolnite funkcije `izvozi_csv`, `uvozi_csv`, `izvozi_json` in `uvozi_json`.
2. Graf BA iz naloge 2 izvozite v mapo `izvoz/` v zapisih CSV, JSON in GraphML (`nx.write_graphml`), ga ponovno uvozite in preverite, da je enak izvirniku.
3. Primerjajte velikosti datotek z velikostjo matrike sosednosti (1 bajt na element). Datoteko GraphML lahko odprete v programu Gephi.

| Zapis | velikost [kB] | uvoženi $n$, $m$ | enak izvirniku |
|---|---|---|---|
| CSV | `______` | `______` | `______` |
| JSON | `______` | `______` | `______` |
| GraphML | `______` | `______` | `______` |
| matrika sosednosti | `______` | – | – |

*Preglednica 4: Zapisi grafa BA ($n = 2000$, $m = 2$).*

---

## 4. Vprašanja za razpravo in zaključni zagovor

> **Razmislek 1: Zakaj mali svet?**
>
> Zakaj nekaj prevezanih povezav močno skrajša povprečno pot, gručavosti pa skoraj ne spremeni? Navedite primer realnega omrežja z lastnostmi malega sveta in pojasnite, kaj to pomeni za širjenje informacij ali bolezni po njem.

> **Razmislek 2: Zvezdišča**
>
> Zakaj preferenčno pripenjanje ustvari zvezdišča? Kaj se zgodi z grafom BA, če odstranimo 5 % naključno izbranih vozlišč, in kaj, če odstranimo 5 % vozlišč z največjo stopnjo? Zakaj je izmerjeni naklon $P(k)$ nekoliko drugačen od $-3$?

> **Razmislek 3: Razporeditev in zahtevnost**
>
> Kakšna je časovna zahtevnost enega koraka Fruchterman-Reingoldove razporeditve? Zakaj je za grafe z več tisoč vozlišči neuporabna brez izboljšav? Zakaj krožna razporeditev pri grafu BA ne pokaže njegove strukture?

> **Razmislek 4: Prostorski graf (domača naloga)**
>
> V mapi [`GraphAL/graph_generators.py`](../07_vaje/GraphAL/graph_generators.py) je osnutek funkcije `Morita`: vozlišča imajo naključne lege in »uspešnost« $f_i$, povezavo $(i,j)$ pa ustvarimo, če je $f_i f_j / d_{ij}^{\delta} > \Theta$, prag $\Theta$ pa nastavimo tako, da je $\langle k\rangle = 5$. Popravite funkcijo (npr. `np.random(0, 1, [N, 2])` ni veljaven klic) in raziščite, kako je porazdelitev stopenj odvisna od $\delta$.

---

### Dodatno gradivo

- [`resitve/vaje_08_resitev.ipynb`](resitve/vaje_08_resitev.ipynb): rešitev z izvedenimi celicami
- Modul `GraphAL` (začet na vajah 2024) je v mapi [`../07_vaje/GraphAL/`](../07_vaje/GraphAL/)
