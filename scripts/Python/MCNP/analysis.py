import os

import runMCNP


def createVectors():

    data = [] # Dose in MeV/g (y)
    error = [] #TODO: Multiply by the value to get the rel error
    density = runMCNP.values # Density in g/cm3 (x)

    f = iter(open('mctal'))

    for lines in f:
        if 'vals' in lines:
            vals = next(f).strip()
            data.append(vals.split(' ')[0])
            error.append(vals.split(' ')[1])

    rel_error = calculateRelError(data, error)
    print(density, data, rel_error)

def calculateRelError(data, error):

    rel_error = []
    for f, b in zip(data, error):

        rel_error.append(float(f)*float(b))
    return rel_error

if __name__ == '__main__':
    createVectors()