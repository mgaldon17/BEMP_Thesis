import sys
import time
from threading import Thread

from checkIfFolderExists import *
from Source import *
from Materials import *
import numpy as np
import os
import logging
from analysis import Analyzer
import queue

# Configuration
d_0 = 0.0005  # Lowest density value in g/cm3
d_f = 0.0025  # Highest density value in g/cm3
INPUT_FILE_NAME = "input.txt"
OUTPUT = "output"
q = queue.Queue()
datanames = []  # Datanames of the mctax files containing the dose info


class MCNP():

    def __init__(self, magnesiumDensity, argonDensity, tallies, source, materials, planes, mode, nps):

        self.magnesiumDensity = magnesiumDensity
        self.argonDensity = argonDensity
        self.tallies = tallies
        self.source = source
        self.materials = materials
        self.planes = planes
        self.mode = mode
        self.nps = nps
        self.input_file = '''MCNP Runfile for
                        C ****** 1.10.2022
                        C ****** Simulation of the ionization chamber type 33051
                        C ***************************************************************
                        C ******* Block A: Cells
                        101 0 100                                                   $Graveyard
                        11 1 -1.5914 -1                  $Chamber tail
                        113 1 -1.5914 -3:-21             $Central anode
                        114 2 -''' + self.argonDensity + ''' (-4:-22) (3 21)        $Cavity
                        115 7 -''' + self.magnesiumDensity + ''' (-6:-25) (4 22)    $Chamber wall
                        116 7 -''' + self.magnesiumDensity + ''' (-5:-24) (3 21)
                        117 1 -1.5914 (-2:-23) (6 25)
                        20 3 -0.001205 -100 1 2 23 #61 #62 #63 #64    $Space object-graveyard
    
                        ''' + self.planes + '''
                        
                        ''' + self.materials + '''
                        ''' + self.source + '''
                        ''' + self.tallies + '''
                        ''' + self.mode + '''
                        c PHYS:P 100.0 0.1 $max sigma table energy; analog capture below 100 keV
                        PRINT 110
                        nps ''' + self.nps + ''' $Number of particles
                        prdmp 2j 1 1 10E12 $Print and dump card; PRDMP NDP NDM MCT NDMP DMMP with 1 for writing tallies for plotting
                        '''

    def runMCNP(self, src, material, nps, gray, plot, DATAPATH):

        # Set environment variables
        os.environ['DATAPATH'] = DATAPATH
        argon_density_values = MCNP.setDensityValues(self, d_0, d_f)

        tallies, source, materials, planes, mode = MCNP.loadMCNPBlocks(self, src, material)

        logging.info("DATAPATH variable set to " + DATAPATH)

        # Read density of Magnesium from material input file
 
        magnesiumDensity = Materials(material).getDensityOfMg()
        solute_percentage = Materials(material).get_solute_percentage()
        particle_type = Source(src).getParticleType()

        # Change working dir to output
        checkIfFolderExists(OUTPUT)
        os.chdir(OUTPUT)
        logging.warning("Working directory changed to " + OUTPUT)

        for d in argon_density_values:
            argonDensity = str(d)

            mcnp = MCNP(magnesiumDensity, argonDensity, tallies, source, materials, planes, mode, nps)

            # Get the input file data from object
            input_file = mcnp.get_input_file()

            # Write to input.txt the input data of MCNP
            file = open(INPUT_FILE_NAME, 'w')
            file.write(input_file)
            file.close()

            # Format input file
            mcnp.format_input_file()

            # Run MCNP command
            os.system("mpiexec -np 96 mcnp6.mpi i = " + INPUT_FILE_NAME)
            # os.system("mcnp6 i = " + INPUT_FILE_NAME)
            datanames.append(q.get())

        tal = mcnp.getTallies(tallies)
        nps = mcnp.getNPS()
        analyzer = Analyzer(datanames, gray, plot, tal, nps, argon_density_values, particle_type, solute_percentage)
        analyzer.analyze()
        datanames.clear()
        os.chdir("..")
        logging.warning("Working directory changed back to root")
        logging.warning("----- END OF THE SCRIPT -----\n")
        time.sleep(3)

    def loadMCNPBlocks(self, source, material):
        # Open tally file and read the lines
        with open("input_files/tallies.txt") as tally_file:
            tallies = tally_file.read().rstrip()
        tally_file.close()

        with open("input_files/" + source) as src_file:
            source = src_file.read().rstrip()
        src_file.close()

        with open("input_files/" + material) as mat_file:
            materials = mat_file.read().rstrip()
        mat_file.close()

        with open("input_files/planesSrSource.txt") as planes_file:
            planes = planes_file.read().rstrip()
        planes_file.close()

        with open("input_files/mode.txt") as mode_file:
            mode = mode_file.read().rstrip()
        mode_file.close()

        return tallies, source, materials, planes, mode

    def setDensityValues(self, d_0, d_f):
        step = (d_f - d_0) / 25
        values = np.arange(d_0, d_f, step)

        if len(values) > 25:
            logging.warning("Density vector contains more values than MCNP can handle.")
            sys.exit()

        return values

    def getNPS(self):
        it = iter(open(INPUT_FILE_NAME))
        nps = 0
        for lines in it:
            if "nps" in lines:
                nps = lines.split(" ")[1]
        return nps

    def getTallies(self, tallies):

        tal_array = tallies.split("\n")
        t = []
        tal = []
        particle = []
        for s in tal_array:
            if "f" in s:
                t.append(s.split(' ')[0])

        for i in t:
            tal.append(i.split(":")[0])
            particle.append(i.split(":")[-1])

        return tal

    def get_input_file(self):
        return self.input_file

    def format_input_file(self):
        formatted_input = ''
        f0 = open(INPUT_FILE_NAME)
        n = 0
        s = "                        "
        for line in f0:

            n += 1
            if n == 1:
                formatted_input += line.strip() + "\n"

            elif n > 1 and s in line:
                formatted_input += line[24:]
                if len(line[24:]) == 0:
                    formatted_input += "\n"
            else:
                formatted_input += line
        with open(INPUT_FILE_NAME, 'w') as f:
            f.write(formatted_input)

        f.close()
        f0.close()
