import time

import numpy as np
import os
import logging
from analysis import createVectors
import queue
# Configuration

os.environ["DATAPATH"] = "/Users/maga2/MCNP/MCNP_DATA"
values = np.arange(0.8E-3, 0.1, 0.05) #Density values
input_file_name = "input.txt"
PATH_TO_FILE = "input_files/density.txt"
OUTPUT = "output/"
q = queue.Queue()
datanames = [] #Datanames of the mctax files containing the dose info

class MCNP():

    def __init__(self, density, input_file):
        self.density = density
        self.input_file = '''MCNP Runfile for
                        C ****** 1.10.2022
                        C ****** Simulation of the ionization chamber type 33051
                        C ***************************************************************
                        C ******* Block A: Cells
                        7 2 -''' + self.density + ''' -1 6 -5 21                     $Cell of wall (water)
                        8 1 -1.127 -2 1 6 -5                                    $Cell of the outer wall (A-150)
                        9 1 -1.127 -4 3 5                                       $Cell of the outermost cask wall (A-150)
                        10 2 -''' + self.density + ''' -3 5 22                       $Internal cask wall
                        14 0 20                                                 $Graveyard
                        15 1 -1.127 -21 -5 6                                    $Innermost chamber
                        16 1 -1.127 -22 5                                       $Innermost sphere
                        17 4 -0.9 -24 -6 23
                        18 3 -0.001205 -20 #17 #19 #8 #9 #7 #15 #16 #10
                        19 1 -1.127 23 -25 24 -26
    
                        C ***************************************************************
                        C ***************************************************************
                        C Block B: Planes
                        C ***************************************************************
                        C Beginning of surfaces
                        1 CY 0.4
                        2 CY 0.7
                        3 SY 6.35 0.4
                        4 SY 6.35 0.7
                        5 PY 6.35
                        6 PY 4.25
                        21 CY 0.2
                        22 SY 6.35 0.2
                        23 PY 1
                        24 CY 0.75
                        25 CY 0.85
                        26 PY 1.5
                        20 RPP -1 55 -1 8 -3 3 $Outer world contour
    
                        C ***************************************************************
                        C ***************************************************************
                        C Block C: Materials and source
                        C ***************************************************************
                        C Plastic A-150 (d=1.127 g/cm3)
                        M1 1001.80c -0.101327
                                6000.80c -0.775501
                                7014.80c -0.035057
                                8016.80c -0.052316
                                9019.80c -0.017422
                                20000.60c -0.018378
                        C Tissue equivalent gas (d=1.06409E-03 g/cm3) $0.2E-3, 0.5E-3, 1.06409E-3, 1.5E-3, 2E-3, 4E-4 8E-3, 1E-2, 3E-2
                        M2 1001.80c -0.101869
                                6000.80c -0.456179
                                7014.80c -0.035172
                                8016.80c -0.406780
                        C Dry air (d=0.001205 g/cm3)
                        M3 6012.80c -0.000124
                                7014.80c -0.755267
                                8016.80c -0.231781
                                18040.80c -0.012827
                        C Polyethlyene (d=0.9 g/cm3)
                        M4 1001.80c -0.143711
                                6000.80c -0.856289
                        C ***************************************************************
                        C ******** Source ***********************************************
                        SDEF POS 50 3.7625 0 X=50 Y=D2 Z=D1 PAR=E ERG=1.9 VEC = -1 0 0 DIR = 1          $ position, particle type, energy
                        SI1 -3 3                                                $ sampling range Ymin to Ymax
                        SP1 0 1                                                 $ weighting for y sampling: here constant
                        SI2 2.525 5.0                                           $ sampling range ZYmin to Zmax
                        SP2 0 1                                                 $ weighting for z sampling: here constant
                        c +f106 10                                              $ Energy deposition in cell 10 [MeV/g] (dose)
                        c f16:N 10                                              $ Energy deposition in cell 10 for N [MeV/g] (dose)
                        f26:E 10                                                $ Energy deposition in cell 10 for E [MeV/g] (dose)
                        c f36:#,H 10                                            $ Energy deposition in cell 10 for heavy ions [MeV/g] (dose)
                        c E106 0.001 100i 10
                        c E16 0.001 100i 10
                        E26 1.9
                        c E36 0.001 100i 10
                        MODE N P E #
                        IMP:N 1 3r 0 2 4r
                        IMP:E 1 3r 0 1 4r
                        IMP:# 1 3r 0 1.5 4r
                        c PHYS:P 100.0 0.1 $max sigma table energy; analog capture below 100 keV
                        nps 10E4 $Number of particles
                        prdmp 2j 1 $Print and dump card; PRDMP NDP NDM MCT NDMP DMMP with 1 for writing tallies for plotting
                        C **************************************************************
                        C ******** TMESH ***********************************************
                        c --- mesh tally specification
                        c fmesh4:n geom=xyz origin= 3 3 -1
                        c                 imesh=5 iints=50
                        c                 jmesh=5 jints=100
                        c                 kmesh=1 kints=200
                        '''

    def get_input_file(self):
        return self.input_file

    def runMCNP():
        logging.info("DATAPATH variable set to " + """/Users/maga2/MCNP/MCNP_DATA""")
        # Change working dir to output for file creation purposes
        os.chdir(OUTPUT)
        logging.warning("Working directory changed to " + OUTPUT)

        for d in values:
            density = str(d)
            input_file = MCNP(density,'').get_input_file()

            file = open(input_file_name, 'w')
            file.write(input_file)
            file.close()
            MCNP.format_input_file(input_file_name)

            os.system("mcnp6 i = " + input_file_name)

            datanames.append(q.get())

        createVectors(datanames, gray=True)
        # Return to root working dir
        os.chdir("..")
        logging.warning("Working directory changed back to root")
        logging.warning("----- END OF THE SCRIPT -----")

    def format_input_file(input_file_name):
        formatted_input = ''
        f0 = open(input_file_name)
        n = 0
        for line in f0:
            n += 1
            if n == 1:
                formatted_input += line.strip() + "\n"
            elif n > 1:
                formatted_input += line[24:]
                if len(line[24:]) == 0:
                    formatted_input += "\n"

        with open(input_file_name, 'w') as f:
            f.write(formatted_input)

        f.close()
        f0.close()


def load_input(density):
    input_file = '''MCNP Runfile for
            C ****** 1.10.2022
            C ****** Simulation of the ionization chamber type 33051
            C ***************************************************************
            C ******* Block A: Cells
            7 2 -''' + density + ''' -1 6 -5 21                     $Cell of wall (water)
            8 1 -1.127 -2 1 6 -5                                    $Cell of the outer wall (A-150)
            9 1 -1.127 -4 3 5                                       $Cell of the outermost cask wall (A-150)
            10 2 -''' + density + ''' -3 5 22                       $Internal cask wall
            14 0 20                                                 $Graveyard
            15 1 -1.127 -21 -5 6                                    $Innermost chamber
            16 1 -1.127 -22 5                                       $Innermost sphere
            17 4 -0.9 -24 -6 23
            18 3 -0.001205 -20 #17 #19 #8 #9 #7 #15 #16 #10
            19 1 -1.127 23 -25 24 -26

            C ***************************************************************
            C ***************************************************************
            C Block B: Planes
            C ***************************************************************
            C Beginning of surfaces
            1 CY 0.4
            2 CY 0.7
            3 SY 6.35 0.4
            4 SY 6.35 0.7
            5 PY 6.35
            6 PY 4.25
            21 CY 0.2
            22 SY 6.35 0.2
            23 PY 1
            24 CY 0.75
            25 CY 0.85
            26 PY 1.5
            20 RPP -1 55 -1 8 -3 3 $Outer world contour

            C ***************************************************************
            C ***************************************************************
            C Block C: Materials and source
            C ***************************************************************
            C Plastic A-150 (d=1.127 g/cm3)
            M1 1001.80c -0.101327
                    6000.80c -0.775501
                    7014.80c -0.035057
                    8016.80c -0.052316
                    9019.80c -0.017422
                    20000.60c -0.018378
            C Tissue equivalent gas (d=1.06409E-03 g/cm3) $0.2E-3, 0.5E-3, 1.06409E-3, 1.5E-3, 2E-3, 4E-4 8E-3, 1E-2, 3E-2
            M2 1001.80c -0.101869
                    6000.80c -0.456179
                    7014.80c -0.035172
                    8016.80c -0.406780
            C Dry air (d=0.001205 g/cm3)
            M3 6012.80c -0.000124
                    7014.80c -0.755267
                    8016.80c -0.231781
                    18040.80c -0.012827
            C Polyethlyene (d=0.9 g/cm3)
            M4 1001.80c -0.143711
                    6000.80c -0.856289
            C ***************************************************************
            C ******** Source ***********************************************
            SDEF POS 50 3.7625 0 X=50 Y=D2 Z=D1 PAR=E ERG=1.9 VEC = -1 0 0 DIR = 1          $ position, particle type, energy
            SI1 -3 3                                                $ sampling range Ymin to Ymax
            SP1 0 1                                                 $ weighting for y sampling: here constant
            SI2 2.525 5.0                                           $ sampling range ZYmin to Zmax
            SP2 0 1                                                 $ weighting for z sampling: here constant
            c +f106 10                                              $ Energy deposition in cell 10 [MeV/g] (dose)
            c f16:N 10                                              $ Energy deposition in cell 10 for N [MeV/g] (dose)
            f26:E 10                                                $ Energy deposition in cell 10 for E [MeV/g] (dose)
            c f36:#,H 10                                            $ Energy deposition in cell 10 for heavy ions [MeV/g] (dose)
            c E106 0.001 100i 10
            c E16 0.001 100i 10
            E26 1.9
            c E36 0.001 100i 10
            MODE N P E #
            IMP:N 1 3r 0 2 4r
            IMP:E 1 3r 0 1 4r
            IMP:# 1 3r 0 1.5 4r
            c PHYS:P 100.0 0.1 $max sigma table energy; analog capture below 100 keV
            nps 10E4 $Number of particles
            prdmp 2j 1 $Print and dump card; PRDMP NDP NDM MCT NDMP DMMP with 1 for writing tallies for plotting
            C **************************************************************
            C ******** TMESH ***********************************************
            c --- mesh tally specification
            c fmesh4:n geom=xyz origin= 3 3 -1
            c                 imesh=5 iints=50
            c                 jmesh=5 jints=100
            c                 kmesh=1 kints=200
            '''
    return input_file

