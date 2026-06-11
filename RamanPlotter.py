from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog

# =====================
# PARAMETERS
# =====================
offset = 0.0  # vertical offset between spectra
normalize = True  # set False if you don't want normalization

# =====================
# FILE CLASS
# =====================
class RamanSpectrum:
    def __init__(self, name, x, y):
        self.name = str(name)
        self.x = x
        self.y = y

# =====================
# SELECT FOLDER
# =====================
Tk().withdraw()
folder = filedialog.askdirectory(title="Select Raman folder")

if not folder:
    print("No folder selected. Exiting.")
    exit()

folder = Path(folder)

# accept common Raman formats
files = sorted(list(folder.glob("*.txt")) + list(folder.glob("*.csv")))

if not files:
    print("No Raman files found in folder.")
    exit()

print(f"Found {len(files)} files")

# =====================
# LOAD SPECTRA
# =====================
spectra = []

for f in files:
    try:
        df = pd.read_csv(f, sep="\t", comment="#", header=None, encoding="latin1")

        x = df.iloc[:, 0].values
        y = df.iloc[:, 1].values

        # optional normalization
        if normalize and y.max() != 0:
            y = y / y.max()

        spectra.append(RamanSpectrum(f.stem, x, y))

    except Exception as e:
        print(f"Skipping {f.name}: {e}")

# =====================
# PLOT
# =====================
plt.figure(figsize=(10, 6))

for i, s in enumerate(spectra):
    y_off = s.y + i * offset
    plt.plot(s.x, y_off, label=s.name, linewidth=1)
    plt.scatter(s.x, y_off, s=0.2)

plt.xlabel("Raman shift (cm⁻¹)")
plt.ylabel("Intensity (a.u.)")
plt.title("Batch Raman Spectra")
plt.legend(fontsize=8)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

input("Press Enter to exit...")