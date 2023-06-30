import logging
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import MCNP
from tally import Tally

# Conversion rate from MeV/g to Gray
# 1 gray in MeV/g is 6.24E9
con_rate = 6.24E9


def outputToTxt(tally_dict, particleType, water_percentage):
    f = open("result.txt", "w+")

    # The purpose of this method is to send raw output data to txt for further processing in an external tool
    # Dose results come in MeV/g. Conversion into Gy must be done separately
    for tally in tally_dict:
        y = tally_dict[tally].get_list_vals()
        f.write("y_" + tally_dict[tally].get_number() + particleType + "_" + water_percentage + " = " + str(y))

        f.write("\n")
    f.write("\n")
    f.write("\n")

    # Errors
    for tally in tally_dict:
        y_err = tally_dict[tally].get_list_errors()
        f.write("y_err_" + tally_dict[tally].get_number() + particleType + "_" + water_percentage + " = " + str(y_err))
        f.write("\n")


    pass


class Analyzer:

    def __init__(self, dataname, gray, plot, tallies, nps, argon_density_values, particleType, water_percentage):
        self.dataname = dataname
        self.gray = gray
        self.plot = plot
        self.tallies = tallies
        self.nps = nps
        self.argon_density_values = argon_density_values
        self.particleType = particleType
        self.water_percentage = water_percentage

    # Return the tally stored in the dict corresponding to the number read off the output_old file
    def getTallyWithN(self, tally_dict, n):
        return tally_dict["tally_" + str(n)]

    def analyze(self):

        argon_density_values = self.argon_density_values  # Density of Argon in g/cm3 (x)
        tally_dict = {}
        n = 0
        tal_plus = False

        # Create Tally objects
        for t in range(len(self.tallies)):

            tally_num = self.tallies[t].split("f")[1]
            # Next line is intended to match the '+' of the +F6 tally
            if self.tallies[t].split("f")[0] == "+" and tally_num[-1] == str(6):
                tal_plus = True
            elif tally_num[-1] == str(6):
                pass
            # Remove the 0 of the possible tally f06 or f08
            if tally_num[0] == str(0):
                tally_num = tally_num[1]

            # Create the Tally instance
            tally_dict["tally_" + str(tally_num)] = Tally(tally_num, [], [])

        # Iterate over Datanames list. Each Dataname = mcta.x
        for d in self.dataname:
            f = iter(open(d))
            for lines in f:
                if 'tally' in lines:
                    # Number of Tally of output_old file
                    n = lines.split()[1]

                if 'vals' in lines:
                    vals = next(f).strip()
                    tally = self.getTallyWithN(tally_dict, n)
                    val = float(vals.split(' ')[0])
                    rel_error = float(vals.split(' ')[1])
                    abs_error = self.calculateAbsError(val, rel_error)
                    if self.gray:
                        val_list, err_list = self.convertIntoGray([val], [abs_error])
                        val = val_list[0]
                        abs_error = err_list[0]
                    tally.set_list_vals(val)
                    tally.set_list_errors(abs_error) # List of absolute errors

        outputToTxt(tally_dict, self.particleType, self.water_percentage)

        if self.plot:
            self.savePlot(tally_dict, argon_density_values, self.nps, tal_plus)

    def calculateAbsError(self, val, rel_error):

        absolute_error = float(rel_error) * float(val)
        return absolute_error

    def convertIntoGray(self, val, abs_error):

        val_gray = []
        abs_error_gray = []
        for v in (val):
            v /= con_rate
            val_gray.append(v)

        for r in abs_error:
            r /= con_rate
            abs_error_gray.append(r)

        return val_gray, abs_error_gray

    def savePlot(self, tally_dict, density, nps, tal_plus):

        fig = make_subplots(rows=1, cols=2)
        for tally in tally_dict:
            number = tally_dict[tally].get_number()[-1]
            # print(number)

            # The next block prevents the plot from showing the tally in MeV/g and Gray if tally is 6
            if number != str(6):
                y = tally_dict[tally].get_list_vals()
                y_err = tally_dict[tally].get_list_errors()
                plt.plot(density, y)
                plt.errorbar(density, y, y_err)  # Absolute error of dose

                fig = go.Figure(go.Scatter(
                    x=density,
                    y=y,
                    error_y=dict(
                        type='data',
                        array=y_err,
                        visible=True)))

                fig.update_layout(
                    title="Tally " + str(tally_dict[tally].get_number()),
                    xaxis_title="Density in g/cm3",
                    yaxis_title="Dose in Gray",
                    legend_title="Legend Title",
                    font=dict(
                        family="Courier New, monospace",
                        size=18,
                        color="Black"

                    ))
                fig.show()
            #####

            ####
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
                        y, y_err = self.convertIntoGray(tally_dict[tally].get_list_vals(),
                                                        tally_dict[tally].get_list_errors())
                        plt.plot(density, y)
                        plt.errorbar(density, y, y_err)  # Absolute error of dose
                        dose_unit = "Gray"

                    else:
                        dose_unit = "MeV/g"

                    fig = go.Figure(go.Scatter(
                        x=density,
                        y=y,
                        error_y=dict(
                            type='data',
                            array=y_err,
                            visible=True)))

                    fig.update_layout(
                        title="Tally " + str(tally_dict[tally].get_number()) + ' Dose vs. density',
                        xaxis_title="Density in g/cm3",
                        yaxis_title="Dose in Gray",
                        legend_title="Legend Title",
                        font=dict(
                            family="Courier New, monospace",
                            size=18,
                            color="Black"

                        ))
                    fig.show()

                    plt.ylabel('Dose (' + dose_unit + ')')
                    plt.title("Tally " + str(tally_dict[tally].get_number()) + ' Dose vs. density')

                    if tal_plus:
                        plt.title('Tally +f6' + ' Total Dose vs. density')
                        tal_plus = False

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
            # plt.show()
            plt.savefig(tally + " output @ nps" + str(nps) + ".jpg")
            plt.close()


if __name__ == '__main__':
    os.chdir("P source/0")
    logging.warning("Working directory changed to " + MCNP.OUTPUT)
    datanames = ['mctal', 'mctam', 'mctan', 'mctao', 'mctap', 'mctaq', 'mctar', 'mctas', 'mctat', 'mctau',
                 'mctav', 'mctaw', 'mctax', 'mctay', 'mctaz', 'mctaa', 'mctab', 'mctac', 'mctad', 'mctae', 'mctaf',
                 'mctag', 'mctah', 'mctai', 'mctaj']

    step = (MCNP.d_f - MCNP.d_0) / 25
    values = np.arange(MCNP.d_0, MCNP.d_f, step)
    tallies = ["f06", "f16", "f26", "f36", "f46", "f56"]

    analyzer = Analyzer(datanames, True, False, tallies, '10E8', values, "P", "0")
    analyzer.analyze()
