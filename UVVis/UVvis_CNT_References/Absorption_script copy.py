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


data_folders = [
    r'H:\FUBerlin\Measurements\UVVis\CristianB\20260330_CNT_CF_PLE_P2_NoPo_CoMoCat',
    r'H:\FUBerlin\Measurements\UVVis\CristianB\20260430_CNT_6FBz',
]

# === LOAD ALL CSV FILES IN THE FOLDERS ===
spectra_dict = {}

for data_folder in data_folders:
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

    # Ensure input is always a list
    if not isinstance(spectra_input, list):
        spectra_input = [spectra_input]

    normalized_list = []

    for s in spectra_input:

        # Deep copy so original data stays untouched
        s_copy = copy.deepcopy(s)

        X = np.array(s_copy.X)
        Y = np.array(s_copy.Y)

        # Select wavelength window
        mask = (X >= xmin) & (X <= xmax)
        X_window = X[mask]
        Y_window = Y[mask]

        if len(X_window) == 0:
            print(f"Warning: No data in range for {s.N}")
            continue

        if mode.upper() == "I":
            # Integration normalization
            area = np.trapezoid(Y_window, X_window)
            if area != 0:
                Y = Y / area
            else:
                print(f"Warning: Zero integral for {s.N}")

        elif mode.upper() == "M":
            # Max normalization
            max_val = np.max(Y_window)
            if max_val != 0:
                Y = Y / max_val
            else:
                print(f"Warning: Zero max for {s.N}")

        else:
            raise ValueError("Mode must be 'I' (integration) or 'M' (maximum)")

        s_copy.Y = Y.tolist()
        s_copy.N = s_copy.N + f"_norm{mode.upper()}"

        normalized_list.append(s_copy)

    return normalized_list














# === SUMMARY ===

print("\nAvailable spectra:\n")

for name in sorted(spectra_dict.keys()):
    print(name)

# === SELECT ====

selected_names = [
"BaselineA",
"BaselineB",
"CoMoB_TS_R1_d1",
"CoMoB_TS_R2_d1",
"CoMoY_TS_R1_d1",
"CoMoY_TS_R2_d1",
"NI_BS_d4",
"NI_BS_d8",
"NI_TS_R1_d2",
"NI_TS_R2_d2",
"NoPo_TS_R1_d1",
"NoPo_TS_R2_d1",
"P2R2A",
"P2R2B",
"P2R2C",
"P2R2D",
"P2_TS_R1_d1",
"P2_TS_R2_d1"
]
selected_names = [

#"P2_TS_R1_d1",
#"P2_TS_R2_d1"

#"NI_BS_d4",
#"NI_BS_d8",

"CoMoB_TS_R1_d1",
"CoMoB_TS_R2_d1",

"CoMoY_TS_R1_d1",
"CoMoY_TS_R2_d1",

#"NI_TS_R1_d2",
#"NI_TS_R2_d2",

#"NoPo_TS_R1_d1",
#"NoPo_TS_R2_d1",


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

spectra_list_normeda = Normalize(selected_spectra, 600, 700, mode="I")
spectra_list_normedb = Normalize(selected_spectra, 600, 700, mode="M")

spectra_list_normedb

plt.figure(figsize=(5,5))

offset_step = 0   # <-- adjust spacing here

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
