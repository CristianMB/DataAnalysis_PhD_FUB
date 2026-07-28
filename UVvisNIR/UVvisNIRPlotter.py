import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === TXT DATA FOLDER ===

###PYRENE FILLING BY ALEXANDRA
#txt_folder = r"H:\FUBerlin\Measurements\UVvisNIR\Alexandra\20240724"
#txt_folder = r"H:\FUBerlin\Measurements\UVvisNIR\Alexandra\20240725"
#txt_folder = r"H:\FUBerlin\Measurements\UVvisNIR\Alexandra\20240805"
#txt_folder = r"H:\FUBerlin\Measurements\UVvisNIR\Alexandra\20240819\Small Cuvette"
#txt_folder = r"H:\FUBerlin\Measurements\UVvisNIR\Alexandra\20240920"

####ALPHONSE RHODAMINE
#txt_folder = r"H:\FUBerlin\Measurements\UVvisNIR\Alphonse\20230713"


txt_folder = r"H:\FUBerlin\Measurements\UVvisNIR\CristianB\All"

# === LOAD ALL TXT FILES ===


txt_spectra = {}

for file in os.listdir(txt_folder):

    if file.lower().endswith(".txt"):

        path = os.path.join(txt_folder, file)

        try:
            df = pd.read_csv(
                path,
                sep="\t",
                skiprows=1,
                dtype=str
            )

            df.columns = ["Wavelength", "Abs"]

            # remove hidden spaces
            df["Wavelength"] = df["Wavelength"].str.strip()
            df["Abs"] = df["Abs"].str.strip()

            # convert comma decimals to dots
            df["Wavelength"] = (
                df["Wavelength"]
                .str.replace(",", ".", regex=False)
            )

            df["Abs"] = (
                df["Abs"]
                .str.replace(",", ".", regex=False)
            )

            # convert to numbers, invalid values become NaN
            df["Wavelength"] = pd.to_numeric(
                df["Wavelength"], errors="coerce"
            )

            df["Abs"] = pd.to_numeric(
                df["Abs"], errors="coerce"
            )

            # remove empty rows
            df = df.dropna()

            txt_spectra[file] = df

            print(f"Loaded: {file}")

        except Exception as e:
            print(f"Could not load {file}: {e}")

# === SUMMARY ===

print("\nAvailable TXT spectra:")
for name in txt_spectra:
    print(name)



# === PLOT ALL ===

plt.figure(figsize=(6,5))

for name, df in txt_spectra.items():

    plt.plot(
        df["Wavelength"],
        df["Abs"],
        label=name
    )


plt.xlabel("Wavelength (nm)")
plt.ylabel("Absorbance")
#plt.xlim(200,2500)
plt.grid(True)
plt.legend(fontsize=8)
plt.tight_layout()
plt.show()
