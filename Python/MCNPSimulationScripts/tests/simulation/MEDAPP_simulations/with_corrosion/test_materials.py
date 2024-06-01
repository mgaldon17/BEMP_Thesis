import unittest
from unittest.mock import patch, mock_open
from Python.MCNPSimulationScripts.simulation.MEDAPP_simulations.with_corrosion.materials import Materials

class TestMaterials(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data="target_material, d = 1.0 g/cm3")
    def test_get_solute_density(self, mock_open):
        materials = Materials('material', 'target_material')
        solute_density = materials.get_solute_density()
        self.assertEqual(solute_density, '1.0')

    @patch('builtins.open', new_callable=mock_open, read_data="target_material (50%)")
    def test_get_solute_percentage(self, mock_open):
        materials = Materials('material', 'target_material')
        solute_percentage = materials.get_solute_percentage()
        self.assertEqual(solute_percentage, '50')

if __name__ == '__main__':
    unittest.main()