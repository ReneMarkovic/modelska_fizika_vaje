# Laboratorijski delovni list 2
## Izstrelitev rakete I: model in enačbe gibanja

Univerza v Mariboru · Fakulteta za naravoslovje in matematiko · Oddelek za fiziko

> [!IMPORTANT]
> **Programsko okolje: Python**
>
> Vse naloge rešujete **izključno v Pythonu** (virtualno okolje iz [vaje 00](../00_vaje/README.md)).
> - `numpy`: `np.exp`, `np.log`, `np.linspace`, `np.maximum`
> - `pandas`: `pd.DataFrame`, `df.iloc`, `df.to_excel`
> - `matplotlib.pyplot`: `plot`, `set_yscale`, `legend`
>
> Rešitev oddate kot Jupyter zvezek `.ipynb` z izvedenimi celicami.

PDF različica: [navodila/delovni_list_02.pdf](navodila/delovni_list_02.pdf)

---

## 1. Teoretične osnove in motivacija

Navpični let rakete je preprost, a poučen zgled modela, v katerem sočasno deluje več sil, masa telesa pa se med gibanjem spreminja. Na tej in naslednji vaji bomo sestavili model izstrelitve, ga numerično rešili in analizirali. Danes postavimo enačbe gibanja in prvo simulacijo.

> **Opis modela**
>
> Raketa s suho maso $m_r$, tovorom $m_t$ in gorivom $m_g(t)$ vzleti navpično s površja Zemlje. Dokler ima gorivo, nanjo deluje konstantna sila potiska. Upoštevamo še gravitacijsko silo, ki pojema z višino, in zračni upor v ozračju, katerega gostota eksponentno pada z višino. Zanima nas, kako visoko raketa pride in koliko hitrosti »izgubi« zaradi gravitacije in upora.

### Sila potiska in raketna enačba

Motor izmetava pline s hitrostjo $v_e$ glede na raketo in pri tem porabi $\dot m$ goriva na sekundo. Sprememba gibalne količine izpuha da silo potiska

$$
F_p = \dot m\, v_e , \qquad m_g(t) = m_{g,0} - \dot m\, t \quad (t \le t_b = m_{g,0}/\dot m).
$$

Brez zunanjih sil iz ohranitve gibalne količine sledi **raketna enačba Ciolkovskega** za spremembo hitrosti, ko se masa zmanjša z $m_0$ na $m_k$:

$$
\Delta v = v_e \ln\frac{m_0}{m_k}.
$$

### Gravitacija

Na višini $h$ nad površjem deluje na raketo s skupno maso $m = m_r + m_t + m_g$ sila

$$
F_g = -\frac{G M_Z\, m}{(R_Z + h)^2}, \qquad g_0 = \frac{G M_Z}{R_Z^2} \approx 9{,}82\ \mathrm{m/s^2}.
$$

### Barometrska enačba in zračni upor

Iz hidrostatičnega ravnovesja $\mathrm{d}p/\mathrm{d}h = -\rho g$ in plinske enačbe $\rho = M p/(R T)$ za izotermno ozračje dobimo

$$
\rho(h) = \rho_0\, e^{-h/H}, \qquad H = \frac{R T}{M g_0},
$$

kjer je $H$ **višinska skala** ozračja. Sila upora je vedno nasprotna hitrosti:

$$
F_u = -\tfrac{1}{2}\,\rho(h)\, C_d\, S\, v\,|v| .
$$

### Enačbe gibanja in Eulerjeva metoda

Ker je potisk že zapisan kot sila, je gibanje opisano z

$$
m(t)\,\frac{\mathrm{d}v}{\mathrm{d}t} = F_p + F_g + F_u, \qquad \frac{\mathrm{d}h}{\mathrm{d}t} = v .
$$

Enačbe rešimo numerično z **eksplicitno Eulerjevo metodo** s časovnim korakom $\Delta t$:

$$
\begin{aligned} a_n &= \frac{F(h_n, v_n, m_n)}{m_n}, & h_{n+1} &= h_n + v_n\,\Delta t,\\ v_{n+1} &= v_n + a_n\,\Delta t, & m_{g,n+1} &= \max(m_{g,n} - \dot m\,\Delta t,\ 0). \end{aligned}
$$

Po izgorevanju raketa leti po vztrajnosti. Če zanemarimo upor, je najvišja točka določena z ohranitvijo energije:

$$
\frac{v_b^2}{2} - \frac{G M_Z}{R_Z + h_b} = -\frac{G M_Z}{R_Z + h_{\max}} ,
$$

kjer sta $h_b$ in $v_b$ višina in hitrost ob izgorevanju.

> **Parametri modela**
>
> $G = 6{,}674\cdot10^{-11}\ \mathrm{m^3\,kg^{-1}\,s^{-2}}$, $M_Z = 5{,}972\cdot10^{24}$ kg, $R_Z = 6371$ km, $\rho_0 = 1{,}225\ \mathrm{kg/m^3}$, $M = 28{,}96$ kg/kmol, $R = 8314{,}46$ J/(kmol K), $T = 288{,}15$ K, $C_d = 0{,}2$, $S = 10\ \mathrm{m^2}$, $F_p = 845$ kN (motor Merlin 1D na morski gladini), $v_e = 2500$ m/s, $m_r = 10$ t, $m_t = 1$ t, $m_{g,0} = 20$ t.

---

## 2. Pripravljalna naloga (analitični del)

**P1. Barometrska enačba.** Izpeljite $\rho(h)$ iz hidrostatičnega ravnovesja in plinske enačbe. Izračunajte višinsko skalo $H$ ter gostoto zraka na višini 10 km in 100 km.

$H=$ `__________`  $\rho(10\ \mathrm{km})=$ `__________`  $\rho(100\ \mathrm{km})=$ `__________`

**P2. Raketna enačba.** Raketa z maso $m$ in hitrostjo $v$ v času $\mathrm{d}t$ izvrže maso $|\mathrm{d}m|$ s hitrostjo $v_e$ glede na raketo. Iz ohranitve gibalne količine izpeljite $\Delta v = v_e \ln(m_0/m_k)$. Koliko je $\Delta v$ za našo raketo?

$\Delta v=$ `__________`

**P3. Vzlet.** Izračunajte porabo goriva $\dot m$, čas izgorevanja $t_b$ ter pospešek tik po vzletu in tik pred izgorevanjem (brez upora). Največ koliko goriva lahko natočimo, da raketa sploh vzleti?

$\dot m=$ `__________`  $t_b=$ `__________`  $a(0)=$ `__________`  $a(t_b)=$ `__________`  $m_{g,\max}=$ `__________`

**P4. Najvišja točka.** Iz ohranitve energije izrazite $h_{\max}$ s $h_b$ in $v_b$. Ocenite $h_{\max}$ za $h_b = 46{,}5$ km in $v_b = 2010$ m/s: (a) s konstantnim $g_0$, (b) z $g(h)$. Za koliko se oceni razlikujeta?

(a) `__________`  (b) `__________`

---

## 3. Laboratorijske naloge na računalniku (Python)

> **Repozitorij**
>
> Začetna predloga je v repozitoriju predmeta: [`02_vaje/vaje_02.ipynb`](vaje_02.ipynb). V razdelku *Funkcije* dopolnite telesa funkcij z oznako `TODO`, v razdelku *Testno območje* pa preverite rezultate nalog P1 in P3.

### Naloga 1: Sile in ozračje (20 min)

1. V razdelku *Imports* dopolnite višinsko skalo `H`.
2. Dopolnite funkcije `gravitacijska_sila(h, m)`, `gostota(h)`, `sila_upora(h, v)` in `sila_potiska(m_g)`. Sila upora mora imeti vedno nasprotni predznak od hitrosti.
3. **Slika 1** (dva panela): (A) $\rho(h)$ v logaritemskem merilu in (B) $g(h)$ za $0 \le h \le 100$ km.

| Količina | Analitično (P1, P3) | Numerično |
|---|---|---|
| $H$ | `______` | `______` |
| $\rho(10\ \mathrm{km})$ | `______` | `______` |
| $g(100\ \mathrm{km})$ | `______` | `______` |
| $t_b$ | `______` | `______` |

*Preglednica 1: Preverjanje funkcij za sile in ozračje.*

### Naloga 2: Simulacija leta (30 min)

Dopolnite funkcijo `korak(st, dt)`, ki izvede en korak Eulerjeve metode za stanje `st = {"t", "h", "v", "m_g"}`. Funkcija `simulacija` jo kliče, dokler raketa ne doseže najvišje točke ($v<0$), in vrne `DataFrame` s stolpci `t, h, v, a, m, m_g, F_g, F_u, F_p`.

```python
nov = {"t": st["t"] + dt,
       "h": st["h"] + st["v"] * dt,
       "v": ...,          # TODO
       "m_g": ...}        # TODO: gorivo ne sme postati negativno
```

- Simulirajte let z $m_{g,0} = 20$ t in $\Delta t = 0{,}01$ s.
- **Slika 2** (štirje paneli): $h(t)$, $v(t)$, $a(t)$ ter sile $F_p$, $F_g$, $F_u$ v odvisnosti od časa.
- Pojasnite skok pospeška ob izgorevanju in obliko krivulje $F_u(t)$.
- Rezultate izvozite z `df.to_excel("rezultati_simulacije.xlsx")`.

| Količina | Vrednost |
|---|---|
| Čas izgorevanja $t_b$ | `__________` |
| Višina ob izgorevanju $h_b$ | `__________` |
| Hitrost ob izgorevanju $v_b$ | `__________` |
| Največji pospešek $a_{\max}$ (v enotah $g_0$) | `__________` |
| Najvišja točka $h_{\max}$ | `__________` |
| Čas do najvišje točke | `__________` |

*Preglednica 2: Rezultati simulacije ($m_{g,0}=20$ t, $\Delta t = 0{,}01$ s).*

### Naloga 3: Izgube hitrosti (20 min)

Funkcija `simulacija` ima stikali `gravitacija` in `upor` ter možnost `konec="izgorevanje"`. Simulirajte let do izgorevanja v treh primerih in primerjajte hitrost ob izgorevanju z raketno enačbo (funkcija `ciolkovski`). Gravitacijsko izgubo primerjajte z oceno $g_0 t_b$.

| Primer | $v_b$ [m/s] | Izguba glede na Ciolkovskega [m/s] |
|---|---|---|
| brez gravitacije in upora | `______` | `______` |
| z gravitacijo | `______` | `______` |
| z gravitacijo in uporom | `______` | `______` |
| raketna enačba (P2) | `______` | 0 |

*Preglednica 3: Hitrost ob izgorevanju in izgube zaradi gravitacije ter upora.*

### Naloga 4: Najvišja točka (20 min)

Dopolnite funkcijo `visina_vrha(h_b, v_b)` (P4). Za simulacijo brez upora in simulacijo z uporom vzemite $h_b$ in $v_b$ iz zadnjega koraka s potiskom in primerjajte napoved ohranitve energije z doseženo višino.

| Primer | $h_b$ [km] | $v_b$ [m/s] | $h_{\max}$ (energija) [km] | $h_{\max}$ (simulacija) [km] |
|---|---|---|---|---|
| brez upora | `______` | `______` | `______` | `______` |
| z uporom | `______` | `______` | `______` | `______` |

*Preglednica 4: Najvišja točka leta: ohranitev energije in simulacija.*

---

## 4. Vprašanja za razpravo in zaključni zagovor

> **Razmislek 1: Spremenljiva masa**
>
> Zakaj smemo pisati $m(t)\,\mathrm{d}v/\mathrm{d}t = F$, čeprav se masa rakete spreminja? Kje v modelu je upoštevana gibalna količina izpuha? Kaj bi šlo narobe, če bi pisali $\mathrm{d}(mv)/\mathrm{d}t = F_g + F_u$?

> **Razmislek 2: Kje se izgubi hitrost**
>
> Gravitacijska izguba je sorazmerna s časom izgorevanja. Kako bi jo zmanjšali? Zakaj je upor največji nekje vmes in ne ob vzletu ali na veliki višini? Zakaj se pri vrhu po izgorevanju napoved ohranitve energije za primer z uporom ujema s simulacijo bolje, kot bi pričakovali?

> **Razmislek 3: Meje modela**
>
> Motor Merlin 1D ima na morski gladini potisk 845 kN, v vakuumu pa 981 kN. Kako bi to vključili v model? Je izotermno ozračje s $T = 288$ K dober približek do višine 100 km? Katere druge poenostavitve smo naredili?

> **Razmislek 4: Več stopenj (domača naloga)**
>
> Raketa Falcon 9 ima ob vzletu maso približno 549 t, od tega okoli 25 t suhe mase. Ocenite $\Delta v$ po raketni enačbi, če bi bila raketa enostopenjska. Zakaj uporabljamo večstopenjske rakete?

---

### Dodatno gradivo

- [`resitve/vaje_02_resitev.ipynb`](resitve/vaje_02_resitev.ipynb): rešitev z izvedenimi celicami
- [`main.py`](main.py) in paket [`RLS/`](RLS/) (`raketa.py`, `konstante.py`, `analiza.py`): objektna različica modela, začeta med vajami 2024
