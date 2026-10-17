# Modelska fizika – laboratorijske vaje

Univerza v Mariboru · Fakulteta za naravoslovje in matematiko · Oddelek za fiziko
1. letnik MAG / Fizika

Vsaka vaja ima svojo mapo `XX_vaje/` z naslednjimi deli:

- `README.md`: delovni list (teorija, pripravljalna naloga, naloge, vprašanja za razpravo),
- `navodila/`: delovni list v PDF obliki (`delovni_list_XX.pdf`) ter slike, podatki in drugo gradivo,
- `vaje_XX.ipynb`: začetna predloga za delo na računalniku (mesta za dopolnitev so označena s `TODO`),
- `resitve/vaje_XX_resitev.ipynb`: rešitev z izvedenimi celicami.

Naloge rešujemo v **Pythonu** (≥ 3.10) s knjižnicami `numpy`, `scipy`, `pandas`, `matplotlib`, `seaborn`, `opencv-python`, `scikit-image`, `astropy` in `networkx`. Izjema je vaja 04, kjer simulacijo pišemo v C++. Ena vaja traja **2 šolski uri (90 min)**.

Zbirka vseh delovnih listov je v [`vaje_MF.pdf`](vaje_MF.pdf).

## Priprava okolja

```bash
python -m venv venv
```

Aktivacija okolja:

```bash
# Windows (PowerShell)
.\venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

Namestitev knjižnic:

```bash
python -m pip install -U pip
pip install -r req.txt
```

Podrobna navodila in preizkus okolja: [00_vaje/README.md](00_vaje/README.md).

## Pregled vaj

| Vaja | Tema | Vsebina |
|---|---|---|
| [00](00_vaje/README.md) | Priprava okolja | virtualno okolje, namestitev knjižnic, preizkus, prvi zvezek |
| [01](01_vaje/README.md) | Model peščene sipine | samoorganizirana kritičnost, rekurzija, porazdelitev velikosti plazov |
| [02](02_vaje/README.md) | Izstrelitev rakete I | Newtonovi zakoni, gravitacija, zračni upor, barometrska enačba |
| [03](03_vaje/README.md) | Izstrelitev rakete II | numerična simulacija, vpliv časovnega koraka, analiza rezultatov |
| [04](04_vaje/README.md) | Molekularna dinamika | Lennard-Jonesov potencial, Verletova metoda (C++), analiza v Pythonu |
| [05](05_vaje/README.md) | Mehanski model celice | celica kot poligon, relaksacija z metodo Monte Carlo |
| [06](06_vaje/README.md) | Model tkiva | gradientni spust, rast in delitev celice |
| [07](07_vaje/README.md) | Grafi I | podatkovna struktura grafa, globalne in lokalne metrike |
| [08](08_vaje/README.md) | Grafi II | generatorji topologij, izris in izvoz grafov |
| [09](09_vaje/README.md) | Segmentacija slik I | barvni kanali, histogram, pragovna segmentacija, Otsu, N4/N8 |
| [10](10_vaje/README.md) | Segmentacija slik II | segmentacija eksperimentalne slike, morfološke operacije |
| [11](11_vaje/README.md) | Sonce na nebu | lega Sonca, dolžina dneva, obsevanje v jasnem vremenu |
| [12](12_vaje/README.md) | Energijska bilanca plastenjaka | obsevanje ploskev, segrevanje, analiza vremenskih podatkov |
| [13](13_vaje/README.md) | Nevronske mreže | propagacija naprej, vzvratno razširjanje napake, regresija in razvrščanje |
| [14](14_vaje/README.md) | Grupiranje podatkov *(dodatna vaja)* | mere podobnosti, razdalje, grupiranje časovnih vrst |
| [15](15_vaje/README.md) | Prevajanje toplote *(dodatna vaja)* | difuzijska enačba, stabilnost FTCS, tla, plošča/valj/krogla, toplotni most |
| [16](16_vaje/README.md) | Energijska bilanca Zemlje *(dodatna vaja)* | učinek tople grede, povratna zanka ledu in albeda, Budyko-Sellersov model, histereza |
