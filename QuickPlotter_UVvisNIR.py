import os
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilenames


# ============================================================
# FIXED DATA FOLDER
# ============================================================

txt_folder = r"H:\FUBerlin\Measurements\UVvisNIR"


# ============================================================
# SELECT FILES FROM FIXED FOLDER
# ============================================================

root = Tk()
root.withdraw()

filenames = askopenfilenames(
    initialdir=txt_folder,
    title="Select TXT spectra",
    filetypes=[
        ("TXT files", "*.txt")
    ]
)

if not filenames:
    print("No files selected. Exiting.")
    exit()


# ============================================================
# LOAD SELECTED TXT FILES
# ============================================================

txt_spectra = {}

for path in filenames:

    file = os.path.basename(path)

    try:

        df = pd.read_csv(
            path,
            sep="\t",
            skiprows=1,
            dtype=str
        )

        # Take first two columns
        df = df.iloc[:, :2]
        df.columns = ["Wavelength", "Abs"]

        # Remove hidden spaces
        df["Wavelength"] = df["Wavelength"].str.strip()
        df["Abs"] = df["Abs"].str.strip()

        # Convert comma decimals to dots
        df["Wavelength"] = (
            df["Wavelength"]
            .str.replace(",", ".", regex=False)
        )

        df["Abs"] = (
            df["Abs"]
            .str.replace(",", ".", regex=False)
        )

        # Convert to numbers
        df["Wavelength"] = pd.to_numeric(
            df["Wavelength"],
            errors="coerce"
        )

        df["Abs"] = pd.to_numeric(
            df["Abs"],
            errors="coerce"
        )

        # Remove invalid rows
        df = df.dropna()

        txt_spectra[file] = df

        print(f"Loaded: {file}")

    except Exception as e:

        print(f"Could not load {file}: {e}")


# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(6, 5))

for name, df in txt_spectra.items():

    plt.plot(
        df["Wavelength"],
        df["Abs"],
        label=name,
        linewidth=1.5
    )

plt.xlabel("Wavelength (nm)")
plt.ylabel("Absorbance")

# plt.xlim(200, 2500)

plt.grid(True)
plt.legend(fontsize=8)
plt.tight_layout()

plt.show()