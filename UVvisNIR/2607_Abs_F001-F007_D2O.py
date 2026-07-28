import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# ==========================
# TXT DATA FOLDER
# ==========================

txt_folder = r"H:\FUBerlin\Measurements\UVvisNIR\CristianB\20260728_D2ObasedSamples"



# ==========================
# LOAD ALL TXT FILES
# ==========================

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


            df.columns = [
                "Wavelength",
                "Abs"
            ]


            # Clean strings
            df["Wavelength"] = (
                df["Wavelength"]
                .str.strip()
                .str.replace(",", ".", regex=False)
            )


            df["Abs"] = (
                df["Abs"]
                .str.strip()
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


            # Remove empty rows
            df = df.dropna()


            txt_spectra[file] = df


            print("Loaded:", file)


        except Exception as e:

            print(
                f"Could not load {file}: {e}"
            )



# ==========================
# AVAILABLE SPECTRA
# ==========================

print("\nAvailable spectra:")

for name in txt_spectra:
    print(name)




# ==========================
# PLOT RAW SPECTRA
# ==========================

plt.figure(figsize=(7,5))


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




# ==========================
# BASELINE SUBTRACTION
# ==========================


baseline_name = "20260728_Baseline1pcDOCD2O.txt"


baseline = txt_spectra[baseline_name]


corrected_spectra = {}



for name, df in txt_spectra.items():


    # Skip baseline
    if name == baseline_name:
        continue


    corrected = pd.DataFrame()


    corrected["Wavelength"] = df["Wavelength"]


    corrected["Abs"] = (
        df["Abs"].values
        -
        baseline["Abs"].values
    )


    corrected_spectra[name] = corrected



print("\nCorrected spectra:")

for name in corrected_spectra:
    print(name)




# ==========================
# NORMALIZATION FUNCTION
# ==========================


def NormalizeSpectra(
        spectra_input,
        xmin,
        xmax,
        mode="M"
):

    """
    Normalize spectra.

    mode:
        M -> normalize by maximum
        I -> normalize by integral
    """


    normalized = {}


    for name, df in spectra_input.items():


        df_norm = df.copy()


        X = df_norm["Wavelength"].values
        Y = df_norm["Abs"].values


        mask = (
            (X >= xmin)
            &
            (X <= xmax)
        )


        X_window = X[mask]
        Y_window = Y[mask]


        if len(X_window) == 0:

            print(
                "No normalization range:",
                name
            )

            continue



        if mode.upper() == "M":

            factor = np.max(
                Y_window
            )


        elif mode.upper() == "I":

            factor = np.trapezoid(
                Y_window,
                X_window
            )


        else:

            raise ValueError(
                "Mode must be 'M' or 'I'"
            )



        if factor != 0:

            df_norm["Abs"] = (
                Y / factor
            )


        normalized[name] = df_norm



    return normalized




# ==========================
# PLOT FUNCTION WITH OFFSET
# ==========================


def PlotSpectra(
        spectra_dict,
        spectra_names,
        offset_step=0.0,
        xmin=None,
        xmax=None,
        ylabel="Absorbance"
):


    plt.figure(figsize=(7,5))


    for i, name in enumerate(spectra_names):


        df = spectra_dict[name]


        X = df["Wavelength"].values
        Y = df["Abs"].values


        Y_plot = (
            Y
            +
            i * offset_step
        )


        plt.plot(
            X,
            Y_plot,
            label=name
        )



    plt.xlabel(
        "Wavelength (nm)"
    )


    plt.ylabel(
        ylabel
    )


    if xmin is not None or xmax is not None:

        plt.xlim(
            xmin,
            xmax
        )


    plt.grid(True)


    plt.legend(
        fontsize=8
    )


    plt.tight_layout()

    plt.show()




# ==========================
# SELECT SPECTRA
# ==========================


spectra_to_plot = [

    ############ P2 vs Alkane filled
    #"20260728_RefP2_DOCD2O_d3.txt",
    #"20260728_CBS7DGU_Dode@P2_DOCD2O_d1.txt",
    #"20260728_CBS7CF_Dode@P2_DOCD2O_d3.txt",
    #"20260728_F007_1BrC18@P2_DOCD2O_d3.txt",  
  
  
    ############ P2 vs F6 and DMF
    "20260728_RefP2_DOCD2O_d3.txt",
    "20260728_F006_phDADQ@P2_DOCD2O_d3.txt",
    "20260728_RefDMF_DMF@P2_DOCD2O_d2.txt",

    ############ P2 vs Fluorobenzenes
    #"20260728_RefP2_DOCD2O_d3.txt",
    #"20260728_F001_FBz@P2_DOCD2O_d1.txt",
    #"20260728_F002_6FBz@P2_DOCD2O_d1.txt",
    #"20260728_F005LP_6FBz@P2_DOCD2O_d3.txt",

    ############ P2 vs Fluoroalcohols
    #"20260728_RefP2_DOCD2O_d3.txt",
    #"20260728_F003_TFE@P2_DOCD2O_d2.txt",
    #"20260728_F003_TFE@P2_DOCD2O_d3.txt",
    #"20260728_F004_6FIPA@P2_DOCD2O_d1.txt",
    


  

]




# ==========================
# NORMALIZE
# ==========================

normalized_spectra = corrected_spectra
normalized_spectra = NormalizeSpectra(corrected_spectra,xmin=600,xmax=700,mode="M")


# ==========================
# PLOT NORMALIZED SPECTRA
# ==========================


PlotSpectra(
    normalized_spectra,
    spectra_to_plot,
    offset_step=0.2,
    xmin=200,
    xmax=2400,
    ylabel="Normalized Δ Absorbance"
)