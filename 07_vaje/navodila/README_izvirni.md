# Generator mrež različnih topoloogij

## Osnovna ideja

Realni procesi so izid kompleksnih interakcij med velikim številom komponent. Te komponente so lahko med seboj povezane na različne načine. Naša zmožnost modeliranja naravnih proces je tako pogojena tudi s tem, kako dobro razumemo strukturo in interakcije med komponentami. V realnosti se s takšnimi sklopljenimi sistemi srečujemo na različnih področjih:
- v biologiji, kjer so komponente proteini, geni, celice, organizmi, populacije, ...
- v ekologiji, kjer so komponente različne vrste organizmov, ekosistemi, ...
- v družboslovju, kjer so komponente posamezniki, skupine, organizacije, ...
- v računalništvu, kjer so komponente računalniki, usmerjevalniki, strežniki, ...
- v fiziki, kjer so komponente atomi, molekule, snovi, ...
- v kemiji, kjer so komponente elementi, spojine, ...
- v ekonomiji, kjer so komponente firme, trgi, ...

<table width="600px">
    <tr>
        <td>
            <img src="https://static.vecteezy.com/system/resources/thumbnails/000/160/501/small/free-referral-network-vector.jpg" alt="Social" width="200"/>
        </td>
        <td>
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSnPXZ6GhpBscPzuR1HIydeW67_u-IONAObO1ohFAjao6QQoXCetjERUDACOrMNRgGoG7M&usqp=CAU" alt="topologija_2" width="200"/>
        </td>
    <td>
    <img src="https://www.researchgate.net/publication/335777874/figure/fig3/AS:11431281272883865@1724265689727/Course-community-network-The-above-directed-network-represents-the-network-seen-in-Fig-2.tif" alt="topologija_3" width="200"/>
    </td>
    </tr>
</table>

Neodvisno od področja raziskovanja, je zelo pomembno, da razumemo strukturo in interakcije med komponentami. Gradnike določenega sistema bomo imenovali **Vozlišča** (*ang. nodes*). V določen par vozlišč obravnavamo kot sklopljena oz. povezana, med njima ustvarimo *povezavo* (*ang. edge*). Vozlišča in povezave lahko predstavimo z *grafi*. Grafi so matematični objekti, ki jih sestavljajo vozlišča in povezave. Vozlišča so predstavljena s krogi, povezave pa z črtami, ki povezujejo vozlišča. Grafi so torej sestavljeni iz dveh množic: ***množice vozlišč*** in ***množice povezav***. Vozlišča so lahko povezana med seboj z eno ali več povezavami. Vozlišča, ki so povezana z določenim vozliščem, imenujemo **Sosedje** (*ang. neighbors*).

## Osnovne metrike

### Globalne lastnosti grafov

Na najosnovnejši ravni lahko graf opišemo s **številom vozlišč $(n)$** in **številom povezav $(m)$**. Razmerje med številom vozlišč in številom povezav v grafu imenujemo **povprečna povezast** (*ang. average degree*) $k_{avg}$. Obstajajo še druge metrike, ki opisujejo makrostrukturne lastnosti grafa:

> **Gustota** (*ang. density*) je razmerje med številom povezav in maksimalno možnim številom povezav. Gustota grafa $D$ je definirana kot $D = \frac{2m}{n(n-1)}$, kjer je $n$ število vozlišč, $m$ število povezav.

> **Povprečna najkrajša pot** (*ang. average shortest path*) je povprečna dolžina najkrajše poti med dvema vozliščema v grafu. Povprečna najkrajša pot grafa $L$ je definirana kot $L = \frac{1}{n(n-1)} \sum_{u,v \in V} d(u,v)$, kjer je $d(u,v)$ dolžina najkrajše poti med vozliščema $u$ in $v$.

> **Klastering** (*ang. clustering coefficient*) je mera, ki opisuje, kako so vozlišča v grafu povezana med seboj. Klastering grafa $C$ je definiran kot $C = \frac{1}{n} \sum_{u \in V} C(u)$, kjer je $C(u)$ klastering koeficient vozlišča $u$.

Obstaja še veliko drugih metrik, ki opisujejo strukturo grafa. V nadaljevanju bomo spoznali nekaj osnovnih topologij grafov in njihove lastnosti.

### Lokalne lastnosti grafov

Ob makrostrukturi grafa lahko opazimo tudi lokalne lastnosti grafa. Lokalne lastnosti grafa so lastnosti, ki se nanašajo na posamezna vozlišča v grafu. Lokalne lastnosti grafa so:

> **Stopnja vozlišča** (*ang. degree*) je število povezav, ki so povezane z določenim vozliščem. Stopnja vozlišča $k_i$ je število povezav, ki so povezane z vozliščem $i$. Stopnja vozlišča je definirana kot $k_i = \sum_{j=1}^{n} a_{ij}$, kjer je $a_{ij}$ element matrike povezav.

> **Sosedje vozlišča** (*ang. neighbors*) so vozlišča, ki so povezana z določenim vozliščem. Sosedje vozlišča $i$ so vsa vozlišča, ki so povezana z vozliščem $i$.

> **Lokalni klastering** (*ang. local clustering*) je mera, ki opisuje, kako so sosedje vozlišča povezani med seboj. Lokalni klastering vozlišča $i$ je definiran kot $C(i) = \frac{2e_i}{k_i(k_i-1)}$, kjer je $e_i$ število povezav med sosednjimi vozlišči vozlišča $i$. Lokalno gručavost izračunamo po enačbi:
$$ c_i = \frac{2e_i}{k_i(k_i-1)} $$
kjer je $e_i$ število vseh možnih povezav med vozliščem $i$ sosednjimi vozlišči vozlišča in $k_i$ povezanost $i$-tega vozlišča $i$.

## Naloga

Vokviru vaj bomo izdelali python modul, imenovan GraphAL (Graphs and Algorithms Library), ki bo omogočal:

- Strukturranje podatkov v pomembne za delo z grafi.
- Možnost dodajanja vozlišč in povezav.
- Možnost brisanja vozlišč in povezav.
- Generiranje grafov različnih topologij.
- Izračun osnovnih globalnih in lokalnih metrik grafov.
- Možnost izrisa grafov.
- Možnost za izvoz grafov v različne formate.

Predlagam naslednjo strukturo modula:

```python
GraphAL/
│
├── __init__.py
├── graph_operations.py
├── graph_generators.py
├── graph_metrics.py
├── graph_visualization.py
├── graph_export.py
└── example.py
```