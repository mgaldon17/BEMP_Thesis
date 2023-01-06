import logging
import os

import matplotlib.pyplot as plt
import numpy as np
from self import self

import MCNP
from tally import Tally

# Conversion rate from MeV/g to Gray
# 1 gray in MeV/g is 6.24E9
con_rate = 6.24E9


class Analyzer:

    def __init__(self, dataname, gray, plot, tallies, nps, density):
        self.dataname = dataname
        self.gray = gray
        self.plot = plot
        self.tallies = tallies
        self.nps = nps
        self.density = density

    # Return the tally stored in the dict correspondint to the number read off the output_old file
    def getTallyWithN(self, tally_dict, n):
        return tally_dict["tally_" + str(n)]

    def analyze(self):

        density = self.density  # Density in g/cm3 (x)
        tally_dict = {}
        n = 0
        tal_6 = False

        # Create Tally objects
        for t in range(len(self.tallies)):
            tally_num = self.tallies[t].split("f")[1]
            if self.tallies[t].split("f")[0] == "+" and tally_num == str(6):
                tal_6 = True
            tally_dict["tally_" + str(tally_num)] = Tally(tally_num, [], [])

        # Iterate over Datanames list. Each Dataname = mcta.x
        for d in self.dataname:
            f = iter(open(d))
            for lines in f:
                if 'tally' in lines:
                    # Number of Tally of output_old file
                    n = lines.split('    ')[1]

                if 'vals' in lines:
                    vals = next(f).strip()
                    tally = self.getTallyWithN(tally_dict, n)
                    val = float(vals.split(' ')[0])
                    abs_error = float(vals.split(' ')[1])
                    rel_error = self.calculateRelError(val, abs_error)
                    #if n == "6":
                        #print(abs_error, ", ", rel_error)
                    tally.set_list_vals(val)
                    tally.set_list_errors(rel_error)

        if self.plot:
            self.savePlot(tally_dict, density, self.nps, tal_6)

    def calculateRelError(self, val, error):

        relative_error = float(error) * float(val)
        return relative_error

    def convertIntoGray(self, val, rel_error):

        val_gray = []
        rel_error_gray = []
        for v in (val):
            v /= con_rate
            val_gray.append(v)

        for r in rel_error:
            r /= con_rate
            rel_error_gray.append(r)

        return val_gray, rel_error_gray

    def savePlot(self, tally_dict, density, nps, tal_6):

        for tally in tally_dict:
            number = tally_dict[tally].get_number()

            if number != "6" or self.gray == False:
                y = tally_dict[tally].get_list_vals()
                y_err = tally_dict[tally].get_list_errors()
                plt.plot(density, y)
                plt.errorbar(density, y, y_err)  # Relative error of dose

            match number:
                case "1":
                    plt.ylabel('Current integrated over surface (particles)')
                    plt.title("Tally " + str(tally_dict[tally].get_number()) + ' Current vs. density')
                case "2":
                    plt.ylabel('Flux averaged over surface (particles/cm2)')
                    plt.title("Tally " + str(tally_dict[tally].get_number()) + ' Avg flux vs. density')
                case "4":
                    plt.ylabel('Flux (particles/cm2)')
                    plt.title("Tally " + str(tally_dict[tally].get_number()) + ' Flux vs. density')
                case "6":
                    if self.gray:
                        y, y_err = self.convertIntoGray(tally_dict["tally_6"].get_list_vals(),
                                                        tally_dict["tally_6"].get_list_errors())
                        print("Dose in Gray", y)
                        print("Abs error in Gray", y_err)

                        plt.plot(density, y)
                        plt.errorbar(density, y, y_err)  # Relative error of dose
                        dose_unit = "Gray"
                    else:
                        dose_unit = "MeV/g"

                    plt.ylabel('Dose (' + dose_unit + ')')
                    plt.title("Tally " + str(tally_dict[tally]) + ' Dose vs. density')

                    if tal_6:
                        plt.title('Tally +f6' + ' Dose vs. density')
                case "7":
                    if self.gray:
                        dose_unit = "Gray"
                    else:
                        dose_unit = "MeV/g"
                    plt.ylabel('Fission dose averaged over a cell (' + dose_unit + ')')
                    plt.title("Tally " + str(tally_dict[tally]) + ' Fission dose vs. density')
                case "8":
                    plt.ylabel('Energy distribution (pulses)')
                    plt.title("Tally " + str(tally_dict[tally]) + ' Energy distribution of pulses vs. density')
                case "+8":
                    plt.ylabel('Charge deposition')
                    plt.title("Tally " + str(tally_dict[tally]) + ' Charge deposition vs. density')

            plt.xlabel('Density (g/cm3)')
            plt.savefig(tally + " output @ nps" + str(nps) + ".jpg")
            plt.close()


if __name__ == '__main__':
    os.chdir(MCNP.OUTPUT)
    logging.warning("Working directory changed to " + MCNP.OUTPUT)
    datanames = ['mctal', 'mctam', 'mctan', 'mctao', 'mctap', 'mctaq', 'mctar', 'mctas', 'mctat', 'mctau',
                 'mctav', 'mctaw', 'mctax', 'mctay', 'mctaz', 'mctaa', 'mctab', 'mctac', 'mctad', 'mctae', 'mctaf',
                 'mctag', 'mctah', 'mctai', 'mctaj']

    step = (MCNP.d_f - MCNP.d_0) / 25
    values = np.arange(MCNP.d_0, MCNP.d_f, step)
    tallies = ["f4", "+f6"]

    analyzer = Analyzer(datanames, True, True, tallies, '10E7', values)
    analyzer.analyze()
