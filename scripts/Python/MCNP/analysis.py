import matplotlib.pyplot as plt
import MCNP
from tally import Tally

# Conversion rate from MeV/g to Gray
# 1 gray in MeV/g is 6.24E9
con_rate = 6.24E9

class Analyzer:

    def __init__(self, dataname, gray, plot, tallies, nps):
        self.dataname = dataname
        self.gray = gray
        self.plot = plot
        self.tallies = tallies
        self.nps = nps

    # Return the tally stored in the dict correspondint to the number read off the output file
    def getTallyWithN(self, tally_dict, n):
        return tally_dict["tally_" + str(n)]

    def analyze(self):

        density = list(MCNP.values)  # Density in g/cm3 (x)
        tally_dict = {}
        n = 0

        # Create Tally objects
        for t in range(len(self.tallies)):
            tally_num = self.tallies[t].split("f")[1]
            tally_dict["tally_" + str(tally_num)] = Tally(tally_num, [], [])

        # Iterate over Datanames list. Each Dataname = mcta.x
        for d in self.dataname:
            f = iter(open(d))
            for lines in f:
                if 'tally' in lines:
                    # Number of Tally of output file
                    n = lines.split('    ')[1]

                if 'vals' in lines:
                    vals = next(f).strip()
                    tally = self.getTallyWithN(tally_dict, n)
                    val = float(vals.split(' ')[0])
                    abs_error = float(vals.split(' ')[1])
                    rel_error = self.calculateRelError(val, abs_error)

                    if n == 6 and self.gray:
                        val, rel_error = self.convertIntoGray(val, rel_error)
                        tally.set_list_vals(val)
                        tally.set_list_errors(rel_error)
                        dens_unit = "Gray"

                    else:
                        dens_unit = "MeV/g"
                        tally.set_list_vals(val)
                        tally.set_list_errors(rel_error)

        if self.plot:
            self.savePlot(tally_dict, density, self.nps, dens_unit)

    def calculateRelError(self, val, error):

        relative_error = float(val) * float(error)
        return relative_error

    def convertIntoGray(self, val, rel_error):

        val /= con_rate
        rel_error /= con_rate
        return val, rel_error

    def savePlot(self, tally_dict, density, nps, dens_unit):

        for tally in tally_dict:
            #print(tally, '->', tally_dict[tally])
            y = tally_dict[tally].get_list_vals()
            y_err = tally_dict[tally].get_list_errors()
            plt.plot(density, y)
            plt.errorbar(density, y, y_err)  # Relative error of dose
            number = tally_dict[tally].get_number()

            match number:
                case "1":
                    plt.ylabel('Current integrated over surface (particles)')
                    plt.title(tally + ' Current vs. density')
                case "2":
                    plt.ylabel('Flux averaged over surface (particles/cm2)')
                    plt.title(tally + ' Avg flux vs. density')
                case "4":
                    plt.ylabel('Flux (particles/cm2)')
                    plt.title(tally + ' Flux vs. density')
                case "6":
                    plt.ylabel('Dose (' + dens_unit + ')')
                    plt.title(tally + ' Dose vs. density')
                case "7":
                    plt.ylabel('Fission dose averaged over a cell (' + dens_unit + ')')
                    plt.title(tally + ' Fission dose vs. density')
                case "8":
                    plt.ylabel('Energy distribution (pulses)')
                    plt.title(tally + ' Energy distribution of pulses vs. density')
                case "+8":
                    plt.ylabel('Charge deposition')
                    plt.title(tally + ' Charge deposition vs. density')

            plt.xlabel('Density (g/cm3)')
            plt.savefig(tally + " output @ nps" + str(nps) + ".jpg")
            plt.close()
