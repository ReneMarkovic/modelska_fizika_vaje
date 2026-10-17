# Laboratorijski delovni list 3
## Izstrelitev rakete II: numerična simulacija in analiza

Univerza v Mariboru · Fakulteta za naravoslovje in matematiko · Oddelek za fiziko

> [!IMPORTANT]
> **Programsko okolje: Python**
>
> Vse naloge rešujete **izključno v Pythonu** (virtualno okolje iz [vaje 00](../00_vaje/README.md)).
> - `numpy`: `np.gradient`, `np.argmax`, `np.polyfit`, `np.linspace`
> - `scipy.integrate`: `solve_ivp` (argumenta `events` in `dense_output`)
> - `scipy.optimize`: `brentq`
> - `pandas`: `pd.DataFrame`; `matplotlib.pyplot`: `plot`, `loglog`, `semilogx`
> - standardna knjižnica: `time.time`
>
> Rešitev oddate kot Jupyter zvezek `.ipynb` z izvedenimi celicami.

PDF različica: [navodila/delovni_list_03.pdf](navodila/delovni_list_03.pdf)

---

## 1. Teoretične osnove in motivacija

Na vaji 2 smo sestavili model navpičnega leta rakete in ga rešili z Eulerjevo metodo. Vsak numerični rezultat pa je le približek. Preden ga uporabimo za sklepanje, moramo vedeti, kako natančen je in kako je natančnost odvisna od izbire metode in časovnega koraka. Danes preverimo konvergenco, model rešimo z natančnejšo metodo in izvedemo študijo parametrov.

> **Opis modela**
>
> Uporabimo model z vaje 2: konstanten potisk $F_p = 845$ kN do porabe goriva, gravitacija $g(h)$ in zračni upor v izotermnem ozračju. Spreminjamo začetno maso goriva $m_{g,0}$ in maso tovora $m_t$ ter opazujemo najvišjo točko leta, pospešek in obremenitev rakete zaradi upora.

### Napaka Eulerjeve metode

Za enačbo $\dot y = f(t, y)$ naredi Eulerjeva metoda v vsakem koraku **lokalno napako** reda $\Delta t^2$. Do časa $t$ naredimo $t/\Delta t$ korakov, zato je **globalna napaka** reda $\Delta t$:

$$
|y_n - y(t_n)| \approx C\,\Delta t^{\,p}, \qquad p = 1 \ \text{(Euler)}.
$$

Red metode $p$ določimo iz naklona premice na grafu napake v odvisnosti od $\Delta t$ v log–log merilu. Ker točne rešitve ne poznamo, jo nadomestimo z **referenčno rešitvijo** z zelo majhnim korakom. Posebej moramo paziti na nezveznosti: ob izgorevanju se potisk skokovito spremeni. Če gorivo pošle sredi koraka, sme motor delovati le ustrezen del koraka.

### Metode višjega reda in dogodki

Funkcija `scipy.integrate.solve_ivp` privzeto uporablja Runge-Kutta metodo reda 5(4) s prilagodljivim korakom (RK45), ki korak izbira sama glede na zahtevano relativno natančnost `rtol`. Sistem zapišemo v obliki $\dot{\mathbf y} = \mathbf f(t, \mathbf y)$ z $\mathbf y = (h, v, m_g)$:

$$
\dot h = v, \qquad \dot v = \frac{F_p + F_g + F_u}{m}, \qquad \dot m_g = -\dot m .
$$

Konec leta (najvišjo točko) zaznamo z **dogodkom** (`events`): funkcijo $v(t)$, katere ničlo integrator poišče natančno. Nezveznost ob izgorevanju obidemo tako, da integracijo razdelimo na dva dela: $[0, t_b]$ in $[t_b, t_{\rm vrh}]$.

### Dinamični tlak (Max-Q)

Mehansko obremenitev rakete opisuje **dinamični tlak**

$$
q = \tfrac{1}{2}\,\rho(h)\,v^2 .
$$

Ob vzletu je hitrost majhna, na veliki višini pa je zrak redek, zato ima $q$ vmes izrazit maksimum (Max-Q). Rakete v tem delu leta pogosto zmanjšajo potisk.

### Študija parametrov in iskanje ničle

Najvišjo točko $h_{\max}(m_{g,0})$ dobimo kot rezultat simulacije, zato je to funkcija brez analitičnega zapisa. Najmanjšo maso goriva, pri kateri raketa doseže Kármánovo mejo vesolja ($100$ km), poiščemo z iskanjem ničle funkcije

$$
f(m_{g,0}) = h_{\max}(m_{g,0}) - 100\ \mathrm{km},
$$

na primer z metodo `brentq`, ki potrebuje interval, na katerem $f$ spremeni predznak.

---

## 2. Pripravljalna naloga (analitični del)

**P1. Euler na roke.** Telo vržemo navpično navzgor z $v_0 = 50$ m/s ($g = 10\ \mathrm{m/s^2}$, brez upora). Z Eulerjevo metodo s korakom $\Delta t = 1$ s izračunajte $h$ in $v$ po treh korakih in jih primerjajte s točno rešitvijo.

| $n$ | $t_n$ [s] | $h_n$ (Euler) | $v_n$ (Euler) | $h(t_n)$ (točno) |
|---|---|---|---|---|
| 0 | 0 | 0 | 50 | 0 |
| 1 | 1 | `______` | `______` | `______` |
| 2 | 2 | `______` | `______` | `______` |
| 3 | 3 | `______` | `______` | `______` |

*Preglednica P1: Eulerjeva metoda za navpični met.*

**P2. Red metode.** Pokažite, da pri konstantnem pospešku $a$ Eulerjeva metoda da $h_n = v_0 t_n + \tfrac{1}{2} a\, t_n (t_n - \Delta t)$. Kolikšna je napaka $h_n - h(t_n)$ in kako je odvisna od $\Delta t$? Ocenite napako za prosti let ($a = -g_0$) do $t = 240$ s s korakom $\Delta t = 10$ s.

$h_n - h(t_n)=$ `__________`  ocena napake: `__________`

**P3. Max-Q.** Raketa naj se dviga s konstantnim pospeškom $a$ iz mirovanja, tako da je $v^2 = 2 a h$. Pokažite, da ima $q(h)$ maksimum pri $h = H$, in izračunajte $q_{\max}$ za $a = 17{,}4\ \mathrm{m/s^2}$ (začetni pospešek rakete z 20 t goriva) in $H = 8{,}42$ km.

$h(q_{\max})=$ `__________`  $q_{\max}=$ `__________`

**P4. Do orbite?** Izračunajte prvo in drugo kozmično hitrost na površju Zemlje. Za tirnico tik nad ozračjem potrebuje raketa skupaj z izgubami okoli $\Delta v \approx 9{,}4$ km/s. Kolikšno razmerje mas $m_0/m_k$ bi to zahtevalo pri $v_e = 2500$ m/s? Primerjajte s hitrostjo ob izgorevanju z vaje 2.

$v_1=$ `__________`  $v_2=$ `__________`  $m_0/m_k=$ `__________`

---

## 3. Laboratorijske naloge na računalniku (Python)

> **Repozitorij**
>
> Začetna predloga je v repozitoriju predmeta: [`03_vaje/vaje_03.ipynb`](vaje_03.ipynb). Model z vaje 2 je že vnesen (funkciji `pospesek` in `simulacija_euler`). V razdelku *Funkcije* dopolnite telesa funkcij z oznako `TODO`, v razdelku *Testno območje* pa preverite rezultata nalog P1 in P3.

### Naloga 1: Vpliv časovnega koraka (25 min)

Za $m_{g,0} = 20$ t izračunajte referenčno rešitev z Eulerjevo metodo in korakom $\Delta t = 0{,}001$ s. Nato simulacijo ponovite za $\Delta t \in \{10, 5, 2, 1, 0{,}1, 0{,}01\}$ s in izpolnite preglednico.

- **Slika 1** (dva panela): (A) $h(t)$ za $\Delta t = 10$, $1$ in $0{,}01$ s, (B) napaka $|h_{\max} - h_{\rm ref}|$ v odvisnosti od $\Delta t$ v log–log merilu.
- Iz naklona premice (`np.polyfit`) določite red metode in ga primerjajte s P2.
- Kako se čas izvajanja spreminja z $\Delta t$?

| $\Delta t$ [s] | $h_{\max}$ [km] | $t_{\rm vrh}$ [s] | napaka [m] | čas izvajanja [s] |
|---|---|---|---|---|
| 10 | `______` | `______` | `______` | `______` |
| 5 | `______` | `______` | `______` | `______` |
| 2 | `______` | `______` | `______` | `______` |
| 1 | `______` | `______` | `______` | `______` |
| 0,1 | `______` | `______` | `______` | `______` |
| 0,01 | `______` | `______` | `______` | `______` |

*Preglednica 1: Konvergenca Eulerjeve metode ($m_{g,0} = 20$ t).*

### Naloga 2: Rešitev s `solve_ivp` (20 min)

1. Dopolnite funkcijo `desna_stran(t, y)`, ki vrne $[\dot h, \dot v, \dot m_g]$.
2. Dopolnite funkcijo `simulacija_ivp(m_g0)`: prvi del leta integrirajte od $0$ do $t_b$, drugi del od $t_b$ do dogodka `dogodek_vrh`. Uporabite `dense_output=True` in rešitev obeh delov združite v `DataFrame` s stolpci `t, h, v, m_g`.
3. Dopolnite funkcijo `analiza_leta(df)`, ki vrne $h_{\max}$, $t_{\rm vrh}$, $a_{\max}$, $q_{\max}$ in višino $h_q$, pri kateri je $q$ največji.

```python
r1 = solve_ivp(desna_stran, (0, t_b), [0.0, 0.0, m_g0],
               rtol=1e-8, atol=1e-6, dense_output=True)
```

| Metoda | $h_{\max}$ [km] | $t_{\rm vrh}$ [s] | čas izvajanja [s] |
|---|---|---|---|
| Euler, $\Delta t = 0{,}01$ s | `______` | `______` | `______` |
| Euler, $\Delta t = 0{,}001$ s | `______` | `______` | `______` |
| `solve_ivp` (RK45, `rtol=1e-8`) | `______` | `______` | `______` |

*Preglednica 2: Primerjava metod. Za `solve_ivp` zapišite še $q_{\max} =$ `______` pri $h_q =$ `______` in primerjajte s P3.*

### Naloga 3: Študija mase goriva (25 min)

S funkcijo `simulacija_ivp` izračunajte let za $m_{g,0} \in \{1, 2, 4, 8, 16, 32, 64\}$ t.

- **Slika 2** (dva panela): (A) $h_{\max}$ v odvisnosti od $m_{g,0}$ (logaritemska os $x$), (B) dinamični tlak $q(h)$ za vse mase goriva do višine 60 km.
- Zakaj $h_{\max}$ pri velikih masah goriva narašča počasneje? Zakaj je $q_{\max}$ največji pri srednjih masah goriva?

| $m_{g,0}$ [t] | $h_{\max}$ [km] | $t_{\rm vrh}$ [s] | $a_{\max}$ [m/s²] | $q_{\max}$ [kPa] | $h_q$ [km] |
|---|---|---|---|---|---|
| 1 | `______` | `______` | `______` | `______` | `______` |
| 2 | `______` | `______` | `______` | `______` | `______` |
| 4 | `______` | `______` | `______` | `______` | `______` |
| 8 | `______` | `______` | `______` | `______` | `______` |
| 16 | `______` | `______` | `______` | `______` | `______` |
| 32 | `______` | `______` | `______` | `______` | `______` |
| 64 | `______` | `______` | `______` | `______` | `______` |

*Preglednica 3: Vpliv mase goriva na let rakete.*

### Naloga 4: Do Kármánove meje (20 min)

Z metodo `brentq` poiščite najmanjšo maso goriva $m_{g,\min}$, pri kateri raketa doseže višino 100 km, za različne mase tovora. Funkcija `simulacija_ivp` sprejme maso tovora kot drugi argument.

```python
f = lambda m: simulacija_ivp(m, m_t)["h"].max() - 100e3
m_min = brentq(f, 500, 60_000, xtol=1.0)
```

| $m_t$ [t] | $m_{g,\min}$ [t] | $t_b$ [s] | $m_{g,\min}/(m_r + m_t)$ |
|---|---|---|---|
| 0 | `______` | `______` | `______` |
| 1 | `______` | `______` | `______` |
| 5 | `______` | `______` | `______` |
| 10 | `______` | `______` | `______` |

*Preglednica 4: Najmanjša masa goriva za dosego višine 100 km.*

---

## 4. Vprašanja za razpravo in zaključni zagovor

> **Razmislek 1: Kdaj je korak dovolj majhen?**
>
> Pri $\Delta t = 10$ s je napaka višine več deset kilometrov, pri $\Delta t = 0{,}01$ s pa nekaj deset metrov. Kako bi izbrali korak, če točne rešitve ne bi poznali? Zakaj je dejanska napaka pri $\Delta t = 10$ s precej večja od ocene iz P2?

> **Razmislek 2: Nezveznosti in dogodki**
>
> Kaj bi se zgodilo z redom Eulerjeve metode, če bi motor v zadnjem koraku deloval ves korak, čeprav gorivo pošle sredi koraka? Zakaj integracijo s `solve_ivp` razdelimo na dva dela, namesto da bi pustili integratorju, da sam »preskoči« izgorevanje?

> **Razmislek 3: Več goriva ni vedno bolje**
>
> Zakaj se $h_{\max}$ pri podvojitvi mase goriva ne podvoji? Kako se z maso goriva spreminja začetni pospešek? Pri kateri masi goriva raketa sploh ne bi več vzletela?

> **Razmislek 4: Tovor in nosilnost (domača naloga)**
>
> Razširite študijo iz naloge 4: za fiksno maso goriva 20 t narišite $h_{\max}$ v odvisnosti od mase tovora. Kolikšen tovor raketa še ponese čez Kármánovo mejo?

---

### Dodatno gradivo

- [`resitve/vaje_03_resitev.ipynb`](resitve/vaje_03_resitev.ipynb): rešitev z izvedenimi celicami
