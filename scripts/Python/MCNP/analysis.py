import os
import MCNP

# Conversion rate from MeV/g to Gray
# 1 gray in MeV/g is 6.24E9
con_rate = 6.24E9


def createVectors(dataname, gray):
    dose = []  # Dose in MeV/g (y)
    error = []  # Absolute error
    density = MCNP.values  # Density in g/cm3 (x)

    for d in dataname:

        f = iter(open(d))

        for lines in f:
            if 'vals' in lines:
                vals = next(f).strip()
                dose.append(float(vals.split(' ')[0]))
                error.append(float(vals.split(' ')[1]))

        # Relative error
        rel_error = calculateRelError(dose, error)
        if gray:
            convertIntoGray(dose)

    print(density, dose, rel_error)


def calculateRelError(dose, error):
    rel_error = []
    for f, b in zip(dose, error):
        rel_error.append(float(f) * float(b))
    return rel_error


def convertIntoGray(dose):
    for d in range(len(dose)):
        x = float(dose[d])
        x /= con_rate


if __name__ == '__main__':
    createVectors(True)
