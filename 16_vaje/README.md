# Laboratorijski delovni list 16
## Energijska bilanca Zemlje: topla greda, led in snežna kepa (dodatna vaja)

Univerza v Mariboru · Fakulteta za naravoslovje in matematiko · Oddelek za fiziko

> [!IMPORTANT]
> **Programsko okolje: Python**
>
> Vse naloge rešujete **izključno v Pythonu** (virtualno okolje iz [vaje 00](../00_vaje/README.md)).
> - `numpy`: `np.clip`, `np.where`, `np.nonzero`, rezine
> - `scipy`: `scipy.integrate.solve_ivp`, `scipy.optimize.brentq`
> - `matplotlib.pyplot`: `plot`, `fill_between`
>
> Rešitev oddate kot Jupyter zvezek `.ipynb` z izvedenimi celicami.

PDF različica: [navodila/delovni_list_16.pdf](navodila/delovni_list_16.pdf)

---

## 1. Teoretične osnove in motivacija

Vreme in podnebje poganja Sonce. Zemlja v povprečju izseva toliko energije, kolikor je absorbira, sicer bi se segrevala ali ohlajala. Na tej vaji iz te preproste bilance sestavimo dva modela: model 0D za povprečno temperaturo Zemlje in model 1D, v katerem je temperatura odvisna od geografske širine, toploto pa proti polom prenašata ozračje in ocean. Modela sta zelo preprosta, a pokažeta učinek tople grede, povratno zanko ledu in albeda, več ravnovesnih podnebij in histerezo, ki jo povezujemo z obdobji »Zemlje kot snežne kepe« pred okoli 700 milijoni let.

> **Opis modela**
>
> Zemlja s polmerom $R$ prestreže sončni tok na preseku $\pi R^2$, seva pa s celotne površine $4\pi R^2$. Povprečna vpadna gostota toka je zato $Q = S_0/4 = 340\ \mathrm{W/m^2}$ ($S_0 = 1361\ \mathrm{W/m^2}$). Del $\alpha$ (albedo) se odbije. Temperaturo spreminja razlika med absorbiranim in izsevanim tokom:
>
> $$C\,\frac{\mathrm{d}T}{\mathrm{d}t} = \mu\,Q\,(1 - \alpha) - \varepsilon\sigma T^4 ,$$
>
> kjer je $C$ toplotna kapaciteta na enoto površine (vrhnja plast oceana), $\sigma$ Stefan-Boltzmannova konstanta, $\varepsilon$ efektivna emisivnost, ki opisuje učinek tople grede, $\mu = S/S_0$ pa relativna jakost Sonca.

### Model 0D: učinek tople grede in časovna konstanta

Pri stalnem albedu je ravnovesna temperatura

$$
T_r = \left(\frac{\mu Q (1 - \alpha)}{\varepsilon\sigma}\right)^{1/4}.
$$

Brez ozračja ($\varepsilon = 1$) in pri $\alpha = 0{,}3$ je $T_r$ precej pod izmerjeno povprečno temperaturo površja 288 K. Ozračje (vodna para, CO$_2$) absorbira del infrardečega sevanja površja, zato v vesolje uide le delež $\varepsilon < 1$. Majhen odmik od ravnovesja $\delta T$ se zmanjšuje eksponentno s časovno konstanto

$$
\tau = \frac{C}{4\varepsilon\sigma T_r^3}.
$$

Podvojitev koncentracije CO$_2$ zmanjša izsevani tok za približno $\Delta F = 3{,}7\ \mathrm{W/m^2}$ (sevalni prisilni vpliv). Brez povratnih zank se temperatura zato dvigne za $\Delta T = \Delta F/(4\varepsilon\sigma T_r^3)$.

### Povratna zanka ledu in albeda

Led in sneg odbijeta več svetlobe kot ocean in kopno. Model 0D zato dopolnimo z albedom, odvisnim od temperature:

$$
\alpha(T) = \begin{cases} 0{,}62 & T \le 250\ \mathrm{K} \\ \text{linearno} & 250\ \mathrm{K} < T < 280\ \mathrm{K} \\ 0{,}30 & T \ge 280\ \mathrm{K} \end{cases}
$$

Ravnovesja so presečišča krivulj absorbiranega $\mu Q(1-\alpha(T))$ in izsevanega toka $\varepsilon\sigma T^4$. Ravnovesje je **stabilno**, če je $\frac{\mathrm{d}}{\mathrm{d}T}\left[\mu Q(1-\alpha) - \varepsilon\sigma T^4\right] < 0$: ob rahlem segretju izsevani tok naraste bolj od absorbiranega in temperatura se vrne.

### Model 1D: Budyko-Sellersov model

Temperatura je zdaj odvisna od geografske širine $\varphi$. Namesto $\varphi$ uporabimo $x = \sin\varphi$, ker je pas med $x$ in $x + \mathrm{d}x$ ploščinsko enakomeren: povprečje po površini Zemlje je navadno povprečje po $x$. Model zaradi simetrije rešujemo le na severni polobli ($0 \le x \le 1$):

$$
C\,\frac{\partial T}{\partial t} = \mu Q\,s(x)\,a(x, T) - (A + BT) + D\,\frac{\partial}{\partial x}\left[(1 - x^2)\frac{\partial T}{\partial x}\right],
$$

kjer je $T$ v °C in:

- $s(x) = 1 + s_2 P_2(x)$ porazdelitev letne osončenosti po širini, $P_2(x) = (3x^2 - 1)/2$, $s_2 = -0{,}482$;
- $a(x, T)$ koalbedo (absorbirani delež): $a_0 + a_2 P_2(x)$ brez ledu ($a_0 = 0{,}681$, $a_2 = -0{,}202$) in $b_0 = 0{,}38$ na ledu, ki prekriva pasove s $T < -10$ °C;
- $A + BT$ izsevani tok, umerjen na satelitske meritve ($A = 203{,}3\ \mathrm{W/m^2}$, $B = 2{,}09\ \mathrm{W/(m^2K)}$);
- zadnji člen opisuje prenos toplote proti polom kot difuzijo na krogli ($D = 0{,}649\ \mathrm{W/(m^2K)}$); na ekvatorju in polu je tok nič.

Enačbo rešujemo s shemo FTCS kot na vaji 15. Pas $i$ s središčem $x_i$ in robovoma $x_{i \pm 1/2}$ izmenja s sosedoma tok

$$
F_{i+1/2} = (1 - x_{i+1/2}^2)\,\frac{T_{i+1} - T_i}{\Delta x}, \qquad
T_i^{n+1} = T_i^n + \frac{\Delta t}{C}\left[\mu Q s_i a_i - (A + BT_i^n) + D\,\frac{F_{i+1/2} - F_{i-1/2}}{\Delta x}\right].
$$

Če je led povsod, je $a = b_0$ in rešitev ima obliko $T(x) = T_0 + T_2 P_2(x)$, kjer je

$$
T_0 = \frac{\mu Q b_0 - A}{B}, \qquad T_2 = \frac{s_2\,\mu Q b_0}{B + 6D}.
$$

> **Predpostavke o parametrih**
>
> - $C = 2{,}1\cdot10^8\ \mathrm{J/(m^2K)}$ (50 m oceana). Ravnovesna stanja od $C$ niso odvisna, od nje je odvisen le čas prilagajanja.
> - Model 0D: $Q = S_0/4 = 340{,}25\ \mathrm{W/m^2}$, $\varepsilon$ izberemo tako, da je pri $\alpha = 0{,}3$ ravnovesje 288 K.
> - Model 1D: parametri so iz članka North, Cahalan in Coakley (1981, glej literaturo), kjer je model umerjen pri $Q = 334{,}4\ \mathrm{W/m^2}$. Za trenutno podnebje uporabimo $\mu = 1$ glede na to vrednost. Mreža ima 60 pasov v $x$.
> - Modela ne upoštevata letnih časov, oblakov, vodnega kroga in kopnega.

---

## 2. Pripravljalna naloga (analitični del)

**P1. Učinek tople grede.** Izračunajte ravnovesno temperaturo Zemlje brez ozračja ($\varepsilon = 1$, $\alpha = 0{,}3$). Kolikšna mora biti efektivna emisivnost, da je ravnovesje 288 K? Koliko °C k temperaturi površja prispeva učinek tople grede?

$T_r(\varepsilon = 1)=$ `________`  $\varepsilon\,(288\ \mathrm{K})=$ `________`  $\Delta T_{\rm TG}=$ `________`

**P2. Časovna konstanta in občutljivost.** Izračunajte $4\varepsilon\sigma T^3$ pri 288 K, časovno konstanto $\tau$ za 50 m oceana in dvig temperature ob podvojitvi CO$_2$ brez povratnih zank. Primerjajte $4\varepsilon\sigma T^3$ s parametrom $B$ modela 1D. Katera povratna zanka (ki je model 0D ne vsebuje) je skrita v manjši vrednosti $B$?

$4\varepsilon\sigma T^3=$ `________`  $\tau=$ `________`  $\Delta T_{2\times}=$ `________`

**P3. Stabilnost ravnovesij.** Skicirajte krivulji absorbiranega in izsevanega toka v modelu 0D z ledeno povratno zanko pri $\mu = 1$. Koliko je presečišč? Z utemeljitvijo na skici označite stabilna in nestabilna ravnovesja. Kaj se zgodi s presečišči, ko $\mu$ povečujemo?

**P4. Model 1D brez ledu in snežna kepa.** (a) S $\langle P_2 \rangle = 0$ in $\langle P_2^2 \rangle = 1/5$ pokažite, da je povprečna temperatura v modelu 1D brez ledu $\langle T\rangle = (Q\langle s a \rangle - A)/B$, kjer je $\langle s a \rangle = a_0 + s_2 a_2/5$, in jo izračunajte. (b) Izračunajte povprečno temperaturo Zemlje, ki je povsem pod ledom, pri $\mu = 1$. (c) Iz $T(x=0) = T_0 - T_2/2 = -10$ °C izračunajte, pri katerem $\mu$ se snežna kepa začne taliti na ekvatorju.

$\langle T\rangle_{\rm brez\ ledu}=$ `________`  $\langle T\rangle_{\rm kepa}=$ `________`  $\mu_{\rm odtalitev}=$ `________`

---

## 3. Laboratorijske naloge na računalniku (Python)

> **Repozitorij**
>
> Začetna predloga je v repozitoriju predmeta: [`16_vaje/vaje_16.ipynb`](vaje_16.ipynb). Parametri obeh modelov, albedo `alfa_led`, koalbedo `koalbedo`, integracija do ravnovesja `ravnovesje_1d` in `ledena_meja` so že napisani. V razdelku *Funkcije* dopolnite telesa funkcij z oznako `TODO`, v razdelku *Testno območje* pa preverite rezultate nalog P1, P2 in P4.

### Naloga 1: Model 0D s stalnim albedom (20 min)

1. Dopolnite funkcije `T_ravn(alfa, eps)`, `neto_0d(T, mu, eps, alfa)` in `potek_0d(T0, t_kon)`.
2. Izračunajte ravnovesno temperaturo in časovno konstanto za $\varepsilon = 1$ in $\varepsilon$ iz P1. Simulirajte potek temperature v 15 letih iz $T_0 = 200$, 288 in 330 K.
3. Emisivnost zmanjšajte tako, da je izsevani tok pri 288 K manjši za 3,7 W/m² (podvojitev CO$_2$), in izračunajte novo ravnovesje.
4. **Slika 1** (dva panela): potek temperature in krivulje absorbiranega ter izsevanega toka.

| $\varepsilon$ | $T_r$ [K] | $T_r$ [°C] | $\tau$ [leta] |
|---|---|---|---|
| 1 | `______` | `______` | `______` |
| `______` | `______` | `______` | `______` |
| 2×CO$_2$: `______` | `______` | $\Delta T=$ `______` | |

*Preglednica 1: Ravnovesja modela 0D s stalnim albedom $\alpha = 0{,}3$.*

### Naloga 2: Ledena povratna zanka in več ravnovesij (20 min)

1. Dopolnite funkcijo `ravnovesja_0d(mu, eps)`, ki poišče vse ničle neto toka z `brentq` in iz predznaka odvoda določi stabilnost.
2. Poiščite ravnovesja za $\mu = 0{,}9$, 1,0 in 1,1.
3. **Slika 2** (dva panela): krivulje absorbiranega toka za vse tri $\mu$ z izsevanim tokom in označenimi ravnovesji (polni krog stabilno, prazen nestabilno) ter potek temperature pri $\mu = 1$ iz začetnih temperatur 200–320 K.

| $\mu$ | ravnovesja [K] | stabilnost |
|---|---|---|
| 0,9 | `______________` | `______________` |
| 1,0 | `______________` | `______________` |
| 1,1 | `______________` | `______________` |

*Preglednica 2: Ravnovesja modela 0D z ledeno povratno zanko. Meja med območjema privlaka pri $\mu = 1$: `______` K.*

### Naloga 3: Temperatura po geografski širini (25 min)

1. Dopolnite funkcijo `korak_1d(T, mu, dt, D, A)`.
2. Iz začetne temperature 15 °C izračunajte ravnovesni profil za današnje podnebje ($\mu = 1$), brez prenosa ($D = 0$), s petkrat močnejšim prenosom ($5D$) in ob podvojitvi CO$_2$ ($A \to A - 3{,}7\ \mathrm{W/m^2}$).
3. **Slika 3** (dva panela): profili $T(\varphi)$ za vse štiri primere ter absorbirani in izsevani tok za današnje podnebje. Kje Zemlja energijo pridobiva in kje izgublja?

| Primer | $\langle T\rangle$ [°C] | $T_{\rm ekv}$ [°C] | $T_{\rm pol}$ [°C] | ledena meja [°] |
|---|---|---|---|---|
| $D$ (danes) | `______` | `______` | `______` | `______` |
| $D = 0$ | `______` | `______` | `______` | `______` |
| $5D$ | `______` | `______` | `______` | `______` |
| 2×CO$_2$ | `______` | `______` | `______` | `______` |

*Preglednica 3: Ravnovesni profili modela 1D. $\Delta\langle T\rangle_{2\times}=$ `______` (primerjava s P2 in s $3{,}7/B$: `______`).*

### Naloga 4: Histereza in snežna kepa (25 min)

1. Začnite z današnjim podnebjem in $\mu$ v korakih po 0,02 zmanjšujte od 1,40 do 0,80, nato pa ga povečujte nazaj do 1,40. Za vsak $\mu$ izračunajte ravnovesje (15 let), pri čemer je začetni profil prejšnje ravnovesje.
2. **Slika 4** (dva panela): $\langle T\rangle(\mu)$ in ledena meja $\varphi_l(\mu)$ za obe smeri.
3. Odčitajte prage in primerjajte prag odtalitve s P4.

| Količina | vrednost |
|---|---|
| $\mu$, pri katerem se pri zmanjševanju pojavi led | `______` |
| najnižja ledena meja pred popolno poledenitvijo [°] | `______` |
| $\mu$ popolne poledenitve (zmanjševanje) | `______` |
| $\mu$ odtalitve (povečevanje), P4 | `______`, `______` |
| $\langle T\rangle$ pri $\mu = 1$: topla veja / snežna kepa [°C] | `______` |

*Preglednica 4: Histereza modela 1D.*

---

## 4. Vprašanja za razpravo in zaključni zagovor

> **Razmislek 1: Zakaj ni preprosto**
>
> Model 0D ob podvojitvi CO$_2$ napove segretje 1,1 K, model 1D z vodno paro (v parametru $B$) in ledom več kot 2 K, podnebni modeli pa 2,5–4 K. Katere povratne zanke dodatno ojačajo ali oslabijo segrevanje (oblaki, ledeni pokrovi, vegetacija)?

> **Razmislek 2: Prenos toplote**
>
> Kako bi izgledalo podnebje brez prenosa toplote proti polom ($D = 0$)? Kateri procesi v resnici prenašajo toploto (Hadleyjeva celica, cikloni, morski tokovi)? Zakaj je to vprašanje povezano z vremenom v srednjih širinah?

> **Razmislek 3: Nestabilnost majhne ledene kape**
>
> Zakaj model ne dopušča stabilne ledene kape z mejo nad približno 72°? Kaj to pomeni za odziv modela na podvojitev CO$_2$? Zakaj je ta napoved za resnično Arktiko verjetno pretirana (letni časi, toplotna vztrajnost oceana)?

> **Razmislek 4: Snežna kepa (domača naloga)**
>
> Geološki dokazi kažejo, da je bila Zemlja pred okoli 700 milijoni let skoraj povsem poledenela, čeprav je bilo Sonce le za okoli 6 % šibkejše. Kako je lahko Zemlja ušla iz snežne kepe, če model zahteva $\mu \approx 1{,}3$? Namig: kaj se pod ledom zgodi s CO$_2$ iz vulkanov, ki ga ne porabljata preperevanje kamnin in fotosinteza?

---

### Literatura

- G. R. North, R. F. Cahalan, J. A. Coakley: *Energy balance climate models*, Reviews of Geophysics 19 (1981) 91–121.
- Vaja nadaljuje sončno obsevanje z [vaje 11](../11_vaje/README.md) in shemo FTCS z [vaje 15](../15_vaje/README.md).

---

### Dodatno gradivo

- [`resitve/vaje_16_resitev.ipynb`](resitve/vaje_16_resitev.ipynb): rešitev z izvedenimi celicami
