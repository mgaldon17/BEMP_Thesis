import matplotlib.pyplot as plt
import MCNP

# Conversion rate from MeV/g to Gray
# 1 gray in MeV/g is 6.24E9
con_rate = 6.24E9


class Analyzer:

    def __init__(self, dataname, gray, plot):
        self.dataname = dataname
        self.gray = gray
        self.plot = plot

    def analyze(self):

        dose = []  # Dose in MeV/g (y)
        error = []  # Absolute error
        density = list(MCNP.values)  # Density in g/cm3 (x)

        for d in self.dataname:

            f = iter(open(d))

            for lines in f:
                if 'vals' in lines:
                    vals = next(f).strip()
                    dose.append(float(vals.split(' ')[0]))
                    error.append(float(vals.split(' ')[1]))

                rel_error = self.calculateRelError(dose, error)

            if self.gray:
                self.convertIntoGray(dose, rel_error)

            else:
                pass

        if self.plot:
            self.savePlot(density, dose, rel_error)

        return dose, density, rel_error

    def calculateRelError(self, dose, error):
        rel_error = []
        for f, b in zip(dose, error):
            rel_error.append(float(f) * float(b))

        return rel_error

    def convertIntoGray(self, dose, rel_error):
        for d in range(len(dose)):
            x = float(dose[d])
            x /= con_rate

        for r in range(len(rel_error)):
            x = float(rel_error[r])
            x /= con_rate

    def savePlot(self, X, Y, rel_error):

        plt.plot(X, Y)

        plt.errorbar(X, Y, rel_error)  # Relative error of dose
        plt.ylabel('Dose (Gray)')
        plt.xlabel('Density (g/cm3)')
        plt.title('Dose vs. density @1.9 MeV')

        plt.savefig("output.jpg")
