import unittest
from unittest.mock import patch, MagicMock
from Python.MCNPSimulationScripts.simulation.MEDAPP_simulations.with_corrosion import run
from Python.MCNPSimulationScripts.simulation.MEDAPP_simulations.with_corrosion.MCNP_simulation import MCNP

class TestRun(unittest.TestCase):
    @patch('Python.MCNPSimulationScripts.simulation.MEDAPP_simulations.with_corrosion.run.Thread')
    @patch('Python.MCNPSimulationScripts.simulation.MEDAPP_simulations.with_corrosion.run.Observer')
    @patch('Python.MCNPSimulationScripts.simulation.MEDAPP_simulations.with_corrosion.run.Timer')
    @patch('Python.MCNPSimulationScripts.simulation.MEDAPP_simulations.with_corrosion.run.ensure_directory_exists')
    @patch('Python.MCNPSimulationScripts.simulation.MEDAPP_simulations.with_corrosion.run.check_system')
    def test_run(self, mock_check_system, mock_ensure_directory_exists, mock_timer, mock_observer, mock_thread):
        mock_check_system.return_value = (True, '/path/to/datapath', '/')
        mock_timer_instance = mock_timer.return_value
        mock_observer_instance = mock_observer.return_value
        mock_thread_instance = mock_thread.return_value

        run.run('source', 'material', 'target_material', 'nps', 'tallies', 'planes', 'mode')

        mock_check_system.assert_called_once()
        mock_ensure_directory_exists.assert_called_once_with('output')
        mock_timer_instance.start.assert_called_once()
        mock_observer_instance.schedule.assert_called_once()
        mock_thread.assert_called()
        mock_thread_instance.start.assert_called()
        mock_thread_instance.join.assert_called()
        mock_timer_instance.stop.assert_called_once()

class TestMCNP(unittest.TestCase):
    @patch('Python.MCNPSimulationScripts.simulation.MEDAPP_simulations.with_corrosion.MCNP_simulation.MCNPSimulationBase')
    def test_generate_input_file(self, mock_mcnp_simulation_base):
        mock_mcnp_simulation_base_instance = mock_mcnp_simulation_base.return_value
        mock_mcnp_simulation_base_instance.load_config.return_value = ('D_0', 'D_F')
        mock_mcnp_simulation_base_instance.set_density_values.return_value = ['1.0', '2.0', '3.0']
        mock_mcnp_simulation_base_instance.load_mcnp_blocks.return_value = ('tallies', 'source', 'materials', 'planes', 'mode')

        mcnp = MCNP('1.74', '1.0', 'tallies', 'source', 'materials', 'planes', 'mode', 'nps')
        input_file = mcnp.generate_input_file()

        self.assertIn('MCNPSimulationScripts Runfile for', input_file)
        self.assertIn('C ****** Simulation of the ionization chamber type 33051', input_file)
        self.assertIn('C ***************************************************************', input_file)
        self.assertIn('C ******* Block A: Cells', input_file)
        self.assertIn('101 0 100                           $Graveyard', input_file)
        self.assertIn('11 1 -1.5914 -1                     $Chamber tail', input_file)
        self.assertIn('113 1 -1.5914 -3:-21                $Central anode', input_file)
        self.assertIn('114 2 -1.0 (-4:-22) (5 24)        $Cavity', input_file)
        self.assertIn('117 1 -1.5914 (-2:-23) (6 25)', input_file)
        self.assertIn('20 3 -0.001205 -100 1 7 26     $Space object-graveyard', input_file)
        self.assertIn('planes', input_file)
        self.assertIn('materials', input_file)
        self.assertIn('source', input_file)
        self.assertIn('tallies', input_file)
        self.assertIn('mode', input_file)
        self.assertIn('c PHYS:P 100.0 0.1 $max sigma table energy; analog capture below 100 keV', input_file)
        self.assertIn('PRINT 110', input_file)
        self.assertIn('nps nps $Number of particles', input_file)
        self.assertIn('prdmp 2j 1 1 10E12 $Print and dump card; PRDMP NDP NDM MCT NDMP with 1 for writing tallies for plotting', input_file)

if __name__ == '__main__':
    unittest.main()