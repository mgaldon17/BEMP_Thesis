
import logging


class MCNP():

    def __init__(self, soluteDensity, argonDensity, tallies, source, materials, planes, mode, nps):

        self.soluteDensity = soluteDensity
        self.argonDensity = argonDensity
        self.tallies = tallies
        self.source = source
        self.materials = materials
        self.planes = planes
        self.mode = mode
        self.nps = nps
        self.input_file = '''MCNP Runfile for
                        C ****** Simulation of the ionization chamber type 33051
                        C ***************************************************************
                        C ******* Block A: Cells
                        101 0 100                           $Graveyard
                        11 1 -1.5914 -1                     $Chamber tail
                        113 1 -1.5914 -3:-21                $Central anode
                        114 2 -''' + self.argonDensity + ''' (-4:-22) (5 24)        $Cavity
                        115 7 -''' + self.soluteDensity + ''' (-6:-25) (4 22)    $Chamber wall
                        116 7 -''' + self.soluteDensity + ''' (-5:-24) (3 21)
                        117 1 -1.5914 (-2:-23) (6 25)
                        118 7 -''' + self.soluteDensity + ''' (-7:-26) (2 23)
                        20 3 -0.001205 -100 1 7 26     $Space object-graveyard
    
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



    def getNPS(self):
        it = iter(open("input.txt"))
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

        with open("input.txt", 'r') as f0:
            n = 0
            s = "                        "

            for line in f0:
                n += 1
                if n == 1:
                    formatted_input += line.strip() + "\n"
                elif n > 1 and s in line:
                    formatted_input += line[24:].rstrip() + "\n"
                else:
                    formatted_input += line

        with open("input.txt", 'w') as f:
            f.write(formatted_input)

        f0.close()
