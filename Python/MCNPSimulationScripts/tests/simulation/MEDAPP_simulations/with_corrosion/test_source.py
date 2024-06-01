import unittest
from unittest.mock import patch, mock_open
from Python.MCNPSimulationScripts.simulation.MEDAPP_simulations.with_corrosion.source import Source

class TestSource(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data="par 1")
    def test_get_particle_type_n(self, mock_open):
        source = Source('source')
        particle_type = source.get_particle_type()
        self.assertEqual(particle_type, 'N')

    @patch('builtins.open', new_callable=mock_open, read_data="par 2")
    def test_get_particle_type_p(self, mock_open):
        source = Source('source')
        particle_type = source.get_particle_type()
        self.assertEqual(particle_type, 'P')

    @patch('builtins.open', new_callable=mock_open, read_data="par 3")
    def test_get_particle_type_e(self, mock_open):
        source = Source('source')
        particle_type = source.get_particle_type()
        self.assertEqual(particle_type, 'E')

    @patch('builtins.open', new_callable=mock_open, read_data="MEDAPP")
    def test_get_particle_type_medapp(self, mock_open):
        source = Source('source')
        particle_type = source.get_particle_type()
        self.assertEqual(particle_type, 'MEDAPP')

if __name__ == '__main__':
    unittest.main()
