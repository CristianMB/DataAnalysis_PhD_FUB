import csv
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# === PARAMETERS ===
offset = 0.0  # vertical offset between spectra

# === SAMPLE CLASS ===
class Sample:
    def __init__(self, name, x, y):
        self.n = str(name)  # Force label to be a string
        self.x = x
        self.y = y

# === FILE SELECTION DIALOG ===
Tk().withdraw()  # hide main tkinter window
filename = askopenfilename(title="Select CSV file", filetypes=[("CSV files","*.csv")])
if not filename:
    print("No file selected. Exiting.")
    exit()

# === READ CSV ===
wavelength = []
spectra_data = {}

with open(filename, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    
    # Skip metadata (5 lines before header in your file)
    for _ in range(5):
        next(reader)
    
    # Read header row
    header = next(reader)
    header = [str(h).strip() for h in header]
    print("Available sample labels:", header[1:])
    scan_names = header[1:]  # skip first column (wavelength)
    
    # Initialize dictionary
    for name in scan_names:
        spectra_data[name] = []

    # Read data rows
    for row in reader:
        if not row or row[0].strip() == '':
            continue
        try:
            wavelength.append(float(row[0]))
        except ValueError:
            continue
        for i, name in enumerate(scan_names):
            try:
                spectra_data[name].append(float(row[i+1]))
            except ValueError:
                spectra_data[name].append(0.0)

# === CREATE SAMPLE OBJECTS ===
samples = [Sample(name, wavelength, spectra_data[name]) for name in scan_names]

# === PLOT ===
plt.figure(figsize=(10,6))
for idx, sample in enumerate(samples):
    y_offset = [val + idx*offset for val in sample.y]
    plt.plot(sample.x, y_offset, label=sample.n)

plt.xlabel('Wavelength (nm)')
plt.ylabel('Absorbance')
plt.title('Absorption Spectra')
plt.legend()
plt.grid(True)
plt.tight_layout()
#plt.xlim(300,1100)
plt.show()
input("Press Enter to exit...")