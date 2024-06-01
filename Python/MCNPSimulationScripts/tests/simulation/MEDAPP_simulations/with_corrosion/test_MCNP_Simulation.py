import unittest
from unittest.mock import patch
from Python.MCNPSimulationScripts.simulation.strontium_simulations.with_corrosion.MCNP_simulation import MCNP

class TestMCNPSimulation(unittest.TestCase):
    @patch('Python.MCNPSimulationScripts.simulation.strontium_simulations.with_corrosion.MCNP_simulation.MCNPSimulationBase')
    def test_init(self, mock_base):
        mcnp = MCNP(1.0, 2.0, 'tallies', 'source', 'materials', 'planes', 'mode', '10E8')
        self.assertEqual(mcnp.solute_density, 1.0)
        self.assertEqual(mcnp.argon_density, 2.0)
        self.assertEqual(mcnp.tallies, 'tallies')
        self.assertEqual(mcnp.source, 'source')
        self.assertEqual(mcnp.materials, 'materials')
        self.assertEqual(mcnp.planes, 'planes')
        self.assertEqual(mcnp.mode, 'mode')
        self.assertEqual(mcnp.nps, '10E8')
        #mock_base.assert_called_once()

    @patch('Python.MCNPSimulationScripts.simulation.strontium_simulations.with_corrosion.MCNP_simulation.MCNPSimulationBase')
    def test_generate_input_file(self, mock_base):
        mcnp = MCNP(1.0, 2.0, 'tallies', 'source', 'materials', 'planes', 'mode', '10E8')
        input_file = mcnp.generate_input_file()
        self.assertIn('MCNPSimulationScripts Runfile for', input_file)
        self.assertIn('C ****** Simulation of the ionization chamber type 33051', input_file)
        self.assertIn('C ***************************************************************', input_file)
        self.assertIn('C ******* Block A: Cells', input_file)
        self.assertIn('nps 10E8 $Number of particles', input_file)
        self.assertIn('prdmp 2j 1 1 10E12 $Print and dump card; PRDMP NDP NDM MCT NDMP with 1 for writing tallies for plotting', input_file)

if __name__ == '__main__':
    unittest.main()