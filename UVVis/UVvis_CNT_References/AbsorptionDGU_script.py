import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add the root folder (where 'spectra' lives) to sys.path
ROOT = r"H:\FUBerlin\DataAnalysis"
if ROOT not in sys.path:
    sys.path.append(ROOT)

from spectra.io import load_absorption_csv  # now Python can find it

# === PROJECT AND DATA FOLDER ===


data_folder = r'H:\FUBerlin\Measurements\CNT Dispersions\Absorption UVVis\20260312_CNT_DGU_P2_NI_NoPo'

# === LOAD ALL CSV FILES IN THE FOLDER ===
spectra_dict = {}

for file in os.listdir(data_folder):
    if file.lower().endswith(".csv"):
        csv_path = os.path.join(data_folder, file)
        spectra = load_absorption_csv(csv_path)
        for s in spectra:
            spectra_dict[s.N] = s




import numpy as np
import copy


def Normalize(spectra_input, xmin, xmax, mode="I"):
    """
    Normalize spectra by integration or maximum within [xmin, xmax].
    If the spectrum has negative oscillations, it is first shifted above zero.

    Parameters
    ----------
    spectra_input : list or single spectrum object
    xmin : float
    xmax : float
    mode : str
        "I" -> normalize by integral
        "M" -> normalize by maximum

    Returns
    -------
    list of normalized spectrum objects
    """

    if not isinstance(spectra_input, list):
        spectra_input = [spectra_input]

    normalized_list = []

    for s in spectra_input:

        s_copy = copy.deepcopy(s)

        X = np.array(s_copy.X)
        Y = np.array(s_copy.Y)

        mask = (X >= xmin) & (X <= xmax)
        X_window = X[mask]
        Y_window = Y[mask]

        if len(X_window) == 0:
            print(f"Warning: No data in range for {s.N}")
            continue

        # ---- SHIFT SPECTRUM ABOVE ZERO ----
        min_val = np.min(Y_window)
        offset = -min_val if min_val < 0 else 0

        Y_shifted = Y + offset
        Y_window_shifted = Y_shifted[mask]

        # ---- NORMALIZATION ----
        if mode.upper() == "I":

            area = np.trapezoid(Y_window_shifted, X_window)

            if area != 0:
                Y_norm = Y_shifted / area
            else:
                print(f"Warning: Zero integral for {s.N}")
                Y_norm = Y_shifted

        elif mode.upper() == "M":

            max_val = np.max(Y_window_shifted)

            if max_val != 0:
                Y_norm = Y_shifted / max_val
            else:
                print(f"Warning: Zero max for {s.N}")
                Y_norm = Y_shifted

        else:
            raise ValueError("Mode must be 'I' (integration) or 'M' (maximum)")

        s_copy.Y = Y_norm.tolist()
        s_copy.N = s_copy.N + f"_norm{mode.upper()}"

        normalized_list.append(s_copy)

    return normalized_list













# === SUMMARY ===

print("\nAvailable spectra:\n")

for name in sorted(spectra_dict.keys()):
    print(name)

# === SELECT ====

selected_names = [
#"DOCH2O1pc_Baseline",

#"NI_DGU_3A_d1",
#"NI_DGU_3B_d1",
#"NI_DGU_3C_d1",
#"NI_DGU_3D_d1",

"NoPo_DGU_4B_d1",
"NoPo_DGU_4C_d1",
"NoPo_DGU_4D_d1",
#"NoPo_DGU_4E_d1",
#"NoPo_DGU_4F_d1",
"NoPo_DGU_4G_d1",

#"P2_DGU_1A_d1",
#"P2_DGU_1B_d1",
#"P2_DGU_1C_d1",
#"P2_DGU_1D_d1",
#"P2_DGU_1D_d2",
#"P2_DGU_1E_d1",

#"P2_DGU_2B_d1",
#"P2_DGU_2D_d1"
]



#selected_names = spectra_dict

# === OPTIONAL: simple plot ===
    

plt.figure(figsize=(5,5))
offset = 0.0

for name in selected_names:
    if name in spectra_dict:
        s = spectra_dict[name]
        plt.plot(s.X, s.Y, label=name)
    else:
        print(f"Warning: {name} not found!")

plt.xlabel("Wavelength (nm)")
plt.ylabel("Absorbance")
#plt.xlim(300,1100)
#plt.ylim(0,3)
plt.title("Absorption Spectra")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()





selected_spectra = [spectra_dict[name] for name in selected_names]

selected_spectra

spectra_list_normeda = Normalize(selected_spectra, 700, 750, mode="I")
spectra_list_normedb = Normalize(selected_spectra, 700, 750, mode="M")

spectra_list_normedb

plt.figure(figsize=(5,5))

offset_step = -0.75   # <-- adjust spacing here

for i, s in enumerate(spectra_list_normedb):
    y_offset = np.array(s.Y) + i * offset_step
    plt.plot(s.X, y_offset, label=s.N)

plt.xlabel("Wavelength (nm)")
plt.ylabel("Absorbance")
plt.title("Absorption Spectra (Integral Normalized)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
