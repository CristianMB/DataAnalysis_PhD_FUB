class Spectrum:
    def __init__(self, x, y, name):
        self.X = x
        self.Y = y
        self.N = str(name)

    def __repr__(self):
        return f"Spectrum(name={self.N}, points={len(self.X)})"