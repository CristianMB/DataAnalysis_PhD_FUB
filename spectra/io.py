import csv
import os
from spectra.core import Spectrum


def load_absorption_csv(filepath, skip_rows=5, delimiter=';'):
    """
    Reads an absorption CSV file and returns a list of Spectrum objects.

    Parameters
    ----------
    filepath : str
        Path to CSV file
    skip_rows : int
        Number of metadata rows to skip before header
    delimiter : str
        Column delimiter

    Returns
    -------
    list of Spectrum objects
    """

    wavelength = []
    spectra_data = {}

    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)

        # Skip metadata rows
        for _ in range(skip_rows):
            next(reader)

        # Header row
        header = next(reader)
        header = [str(h).strip() for h in header]
        scan_names = header[1:]  # skip wavelength column

        # Initialize storage
        for name in scan_names:
            spectra_data[name] = []

        # Read data
        for row in reader:
            if not row or row[0].strip() == '':
                continue

            try:
                wavelength.append(float(row[0]))
            except ValueError:
                continue

            for i, name in enumerate(scan_names):
                try:
                    spectra_data[name].append(float(row[i + 1]))
                except (ValueError, IndexError):
                    spectra_data[name].append(0.0)

    # Create Spectrum objects
    spectra = []
    for name in scan_names:
        spec = Spectrum(wavelength.copy(), spectra_data[name], name)
        spectra.append(spec)

    return spectra