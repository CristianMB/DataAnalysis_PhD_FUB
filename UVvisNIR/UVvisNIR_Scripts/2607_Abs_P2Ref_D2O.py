import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === TXT DATA FOLDER ===

txt_folder = r'H:\FUBerlin\Measurements\UVvisNIR\CristianB\20260715_P2_Test'



# === LOAD ALL TXT FILES ===

txt_spectra = {}

for file in os.listdir(txt_folder):

    if file.lower().endswith(".txt"):

        path = os.path.join(txt_folder, file)

        try:
            df = pd.read_csv(
                path,
                sep="\t",
                decimal=",",
                skiprows=1
            )

            # rename columns for easier handling
            df.columns = ["Wavelength", "Abs"]

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
plt.xlim(200,2500)
plt.grid(True)
plt.legend(fontsize=8)
plt.tight_layout()
plt.show()


spec1 = txt_spectra["Absorption_P2_Full_150726.txt"]
spec2 = txt_spectra["BaselineFull_150726.txt"]

subtracted = pd.DataFrame()

subtracted["Wavelength"] = spec1["Wavelength"]
subtracted["Abs"] = spec1["Abs"] - spec2["Abs"]




plt.figure(figsize=(6,5))

plt.plot(
    subtracted["Wavelength"],
    subtracted["Abs"],
    label="Sample1 - Sample2", linewidth=1)

plt.xlabel("Wavelength (nm)")
plt.ylabel("Δ Absorbance")
plt.xlim(200,2500)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()