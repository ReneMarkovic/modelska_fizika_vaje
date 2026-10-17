# Idejna osnova

## Vhodni podatki za generiranje mreže

### Arhitekttura -> list [2,3,4,5,6,5,3,2]

Koliko vozlišč želimo imeti v določeni plasti nevronske mreže. V navedenem primeru imamo:
-  vhodno plast: 2 podatka
-  Skrita plast: ima skupaj 6 plasti, v katerih je [3,4,5,6,5,3] nevronov.
-  Izhodna plast

### Aktivacijska funkcija

Možnost, da uporabnik izbere katero aktivacijsko funkcijo želi uporabiti v posameznih nevronih.

### Metrika učenja (loss function)

Uporanik lahko izbere, katera metrika bo uporabljena za vrednotenje natančnosti nevronske mreže.

# Opis funkcij v datoteki layer.py

Funkcija activation_function vsebuje nabor aktivacijskih funksij in njihovih odvodo.

```Python
#Definicija aktivacijskih funkcij
def activation_function(x, func_name, derivative=False):
    functions = {
        "tanh": (np.tanh(x), 1 - np.tanh(x)**2),
        "sigmoid": (1 / (1 + np.exp(-x)), (1 / (1 + np.exp(-x))) * (1 - (1 / (1 + np.exp(-x))))),
        "relu": (np.maximum(0, x), np.where(x > 0, 1, 0)),
        "linear": (x, np.ones_like(x)),
    }
    return functions[func_name][int(derivative)]
```