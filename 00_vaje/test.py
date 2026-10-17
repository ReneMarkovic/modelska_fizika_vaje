# test.py: preizkus okolja za vaje Modelska fizika
# Uporaba (v korenu repozitorija, z aktiviranim okoljem):  python 00_vaje/test.py
import importlib
import sys

# ime modula za uvoz: ime paketa v req.txt
MODULI = {
    "numpy": "numpy",
    "scipy": "scipy",
    "pandas": "pandas",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "openpyxl": "openpyxl",
    "cv2": "opencv-python",
    "skimage": "scikit-image",
    "astropy": "astropy",
    "tqdm": "tqdm",
    "networkx": "networkx",
    "sympy": "sympy",
    "ipykernel": "ipykernel",
}

print(f"Python {sys.version.split()[0]} ({sys.executable})")
manjka = []
for modul, paket in MODULI.items():
    try:
        m = importlib.import_module(modul)
        print(f"  {paket:15s} {getattr(m, '__version__', '?')}")
    except ImportError:
        print(f"  {paket:15s} MANJKA")
        manjka.append(paket)

if sys.version_info < (3, 10):
    print("Opozorilo: vaje predpostavljajo Python 3.10 ali novejši.")
if manjka:
    print("Manjkajoči paketi:", ", ".join(manjka), "-> pip install -r req.txt")
    sys.exit(1)
print("Vse BP")
