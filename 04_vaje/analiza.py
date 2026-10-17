import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------
# KONFIGURACIJA
# ---------------------------------------------------------

# Pot do mape s podatki
DATA_DIR = Path("data")

ENERGY_FILE = DATA_DIR / "energije.csv"
XYZ_FILE    = DATA_DIR / "trajektorija.xyz"

# Dolžina roba simulacijske škatle (mora ustrezati C++ kodi)
BOX_LENGTH = 5.0  # L iz SimulationParams

# Parametri za g(r)
R_MAX      = BOX_LENGTH / 2.0
N_BINS     = 100

# Za RDF lahko uporabimo samo del okvirjev (npr. zadnjo polovico)
USE_LAST_FRACTION = 0.5  # uporabi zadnjih 50 % okvirjev


# ---------------------------------------------------------
# POMOŽNE FUNKCIJE
# ---------------------------------------------------------

def read_energies(csv_path):
    """
    Prebere energijski CSV iz simulacije.
    Pričakovana glava: Time,E_kin,E_pot,E_total,Temp
    """
    df = pd.read_csv(csv_path)
    return df


def plot_energies(df):
    """
    Nariše E_kin, E_pot, E_total in temperaturo skozi čas.
    """
    t = df["Time"].values
    E_kin = df["E_kin"].values
    E_pot = df["E_pot"].values
    E_tot = df["E_total"].values
    T     = df["Temp"].values

    fig, ax = plt.subplots(2, 1, figsize=(8, 8), sharex=True)

    ax[0].plot(t, E_kin, label="E_kin")
    ax[0].plot(t, E_pot, label="E_pot")
    ax[0].plot(t, E_tot, label="E_total")
    ax[0].set_ylabel("Energija (reduc. enote)")
    ax[0].legend()
    ax[0].grid(True, alpha=0.3)

    ax[1].plot(t, T, color="tab:red", label="T")
    ax[1].set_xlabel("Čas")
    ax[1].set_ylabel("Temperatura")
    ax[1].grid(True, alpha=0.3)
    ax[1].legend()

    plt.tight_layout()
    plt.show()

    print(f"⟨T⟩ = {np.mean(T):.4f} ± {np.std(T):.4f} (std)")


def minimal_image(dr, L):
    """
    Uporabi minimalno slikovno konvencijo za vektor razdalje dr v kubični škatli z robom L.
    dr: (3,) numpy array
    """
    half_L = 0.5 * L
    for k in range(3):
        if dr[k] >  half_L:
            dr[k] -= L
        elif dr[k] < -half_L:
            dr[k] += L
    return dr


def parse_xyz(xyz_path):
    """
    Prebere XYZ datoteko z več okvirji.
    Struktura vsakega okvirja:
      1. vrstica: N
      2. vrstica: komentar (Time=..., Frame=...)
      naslednjih N vrstic: tip x y z

    Vrne:
      types        : (N,) array tipov (iz prvega okvirja)
      positions    : (n_frames, N, 3) array pozicij
    """
    frames_positions = []
    frames_types = None

    with open(xyz_path, "r") as f:
        while True:
            line = f.readline()
            if not line:
                break  # konec datoteke

            line = line.strip()
            if line == "":
                break

            try:
                N = int(line)
            except ValueError:
                # napačna struktura
                break

            # komentar (ignoriramo, lahko bi parsali čas, če bi želeli)
            comment = f.readline()

            # pozicije
            types = []
            coords = []
            for _ in range(N):
                parts = f.readline().split()
                if len(parts) < 4:
                    raise ValueError("Nepričakovana struktura XYZ datoteke.")

                atom_type = parts[0]
                x, y, z = map(float, parts[1:4])
                types.append(atom_type)
                coords.append([x, y, z])

            if frames_types is None:
                frames_types = np.array(types)
            else:
                # preverimo, da je N konstanten
                if len(types) != len(frames_types):
                    raise ValueError("Število delcev se med okvirji spreminja.")

            frames_positions.append(np.array(coords))

    positions = np.stack(frames_positions, axis=0)  # (n_frames, N, 3)
    return frames_types, positions


def compute_rdf(positions, L, r_max, n_bins, use_last_fraction=1.0):
    """
    Izračun g(r) za 3D kubično škatlo z minimalno sliko.
    
    positions: (n_frames, N, 3)
    L        : dolžina roba škatle
    r_max    : maksimalni r za RDF (tipično L/2)
    n_bins   : število binov
    use_last_fraction: kateri del okvirjev uporabimo (0< f <=1)
    """
    n_frames, N, _ = positions.shape
    if n_frames == 0:
        raise ValueError("Ni okvirjev v positions.")

    # Omejimo se na zadnji del simulacije (po termalizaciji)
    start_index = int((1.0 - use_last_fraction) * n_frames)
    frames = positions[start_index:]
    M = frames.shape[0]

    rho = N / (L**3)  # gostota
    dr = r_max / n_bins
    bin_edges = np.linspace(0.0, r_max, n_bins+1)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    counts = np.zeros(n_bins, dtype=np.float64)

    # Loop po okvirjih
    for frame in frames:
        # frame shape: (N, 3)
        for i in range(N - 1):
            for j in range(i + 1, N):
                dr_vec = frame[i] - frame[j]
                dr_vec = minimal_image(dr_vec, L)
                r = np.linalg.norm(dr_vec)
                if r < r_max:
                    bin_idx = int(r / dr)
                    counts[bin_idx] += 1.0

    # normalizacija g(r)
    # counts ... število parov (i<j) v binu
    # idealno število parov v binu pri idealnem plinu:
    #   N_pairs_ideal_bin = M * 0.5 * N * rho * 4π r^2 dr
    # g(r) = counts / N_pairs_ideal_bin
    g_r = np.zeros_like(bin_centers)
    for k, r in enumerate(bin_centers):
        shell_volume = 4.0 * np.pi * (r**2) * dr
        ideal_pairs = M * 0.5 * N * rho * shell_volume
        if ideal_pairs > 0:
            g_r[k] = counts[k] / ideal_pairs
        else:
            g_r[k] = 0.0

    return bin_centers, g_r


def plot_rdf(r, g_r):
    """
    Nariše radialno porazdelitveno funkcijo g(r).
    """
    plt.figure(figsize=(6, 4))
    plt.plot(r, g_r, marker="", linestyle="-")
    plt.xlabel("r")
    plt.ylabel("g(r)")
    plt.title("Radialna porazdelitvena funkcija g(r)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------
# GLAVNI DEL
# ---------------------------------------------------------

def main():
    # --- Energije ---
    if ENERGY_FILE.exists():
        print(f"Berem energijski zapis: {ENERGY_FILE}")
        df = read_energies(ENERGY_FILE)
        plot_energies(df)
    else:
        print(f"POZOR: {ENERGY_FILE} ne obstaja, preskakujem energijsko analizo.")

    # --- Trajektorija / RDF ---
    if XYZ_FILE.exists():
        print(f"Berem XYZ trajektorijo: {XYZ_FILE}")
        types, positions = parse_xyz(XYZ_FILE)
        print(f"Najdenih okvirjev: {positions.shape[0]}, delcev: {positions.shape[1]}")
        print(f"Tipi (prvih nekaj): {types[:5]}")

        r, g_r = compute_rdf(
            positions,
            L=BOX_LENGTH,
            r_max=R_MAX,
            n_bins=N_BINS,
            use_last_fraction=USE_LAST_FRACTION
        )

        plot_rdf(r, g_r)
    else:
        print(f"POZOR: {XYZ_FILE} ne obstaja, preskakujem RDF analizo.")


if __name__ == "__main__":
    main()
