from Python.MCNPSimulationScripts.simulation.MCNP_simulation_base import MCNPSimulationBase


class MCNP(MCNPSimulationBase):
    """Class to represent a MCNP simulation."""

    def __init__(self, solute_density, argon_density, tallies, source, materials, planes, mode, nps):
        """Initialize a MCNP instance."""
        super().__init__()
        self.solute_density = solute_density
        self.argon_density = argon_density
        self.tallies = tallies
        self.source = source
        self.materials = materials
        self.planes = planes
        self.mode = mode
        self.nps = nps
        self.input_file = self.generate_input_file()

    def generate_input_file(self):
        """Generate the input file for the MCNP simulation."""
        return f'''MCNPSimulationScripts Runfile for
                    C ****** Simulation of the ionization chamber type 33051
                    C ***************************************************************
                    C ******* Block A: Cells
                    101 0 100                           $Graveyard
                    11 1 -1.5914 -1                     $Chamber tail
                    113 1 -1.5914 -3:-21                $Central anode
                    114 2 -{self.argon_density} (-4:-22) (5 24)        $Cavity
                    115 7 -2.18 (-6:-25) (4 22)    $Chamber wall
                    116 7 -2.18 (-5:-24) (3 21)
                    117 1 -1.5914 (-2:-23) (6 25)
                    118 7 -2.18 (-7:-26) (2 23)
                    20 3 -0.001205 -100 1 2 23 #61 #62 #63 #64 #65 #66 #67 #68 #69 #70 $Space object-graveyard
                    61 5 -8.07 53 -52 (-55:-51) 58 56
                    62 3 -0.001205 51 -59 -52 55
                    63 LIKE 61 BUT TRCL=(0 0 0 -1 0 0 0 1 0 0 0 -1 1)
                    64 LIKE 62 BUT TRCL=(0 0 0 -1 0 0 0 1 0 0 0 -1 1)
                    65 5 -8.07 -56 -57 53
                    66 8 -4.785 -56 -51 57 -51
                    67 LIKE 65 BUT TRCL=(0 0 0 -1 0 0 0 1 0 0 0 -1 1)
                    68 LIKE 66 BUT TRCL=(0 0 0 -1 0 0 0 1 0 0 0 -1 1)
                    69 5 -8.07 -58 56 53
                    70 LIKE 69 BUT TRCL=(0 0 0 -1 0 0 0 1 0 0 0 -1 1)

                    {self.planes}

                    {self.materials}
                    {self.source}
                    {self.tallies}
                    {self.mode}
                    c PHYS:P 100.0 0.1 $max sigma table energy; analog capture below 100 keV
                    PRINT 110
                    nps {self.nps} $Number of particles
                    prdmp 2j 1 1 10E12 $Print and dump card; PRDMP NDP NDM MCT NDMP with 1 for writing tallies for plotting
                    '''
