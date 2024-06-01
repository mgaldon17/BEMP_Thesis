import unittest
from unittest.mock import patch, MagicMock
from Python.MCNPSimulationScripts.simulation.MEDAPP_simulations.with_corrosion import run

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

    @patch('Python.MCNPSimulationScripts.simulation.MEDAPP_simulations.with_corrosion.run.os')
    @patch('Python.MCNPSimulationScripts.simulation.MEDAPP_simulations.with_corrosion.run.Materials')
    @patch('Python.MCNPSimulationScripts.simulation.MEDAPP_simulations.with_corrosion.run.MCNPSimulationBase')
    @patch('Python.MCNPSimulationScripts.simulation.MEDAPP_simulations.with_corrosion.run.ensure_directory_exists')
    def test_run_mcnp(self, mock_ensure_directory_exists, mock_mcnp_simulation_base, mock_materials, mock_os):
        mock_mcnp_simulation_base_instance = mock_mcnp_simulation_base.return_value
        mock_materials_instance = mock_materials.return_value
        mock_os.environ = {}

        run.run_mcnp('src', 'material', 'target_material', 'nps', '/path/to/datapath', 'tallies', 'planes', 'mode')

        mock_ensure_directory_exists.assert_called_once_with('output')
        mock_mcnp_simulation_base_instance.load_config.assert_called_once()
        mock_mcnp_simulation_base_instance.set_density_values.assert_called_once()
        mock_mcnp_simulation_base_instance.load_mcnp_blocks.assert_called_once_with('src', 'material', 'tallies', 'planes', 'mode')
        mock_materials.assert_called_once_with('material', 'target_material')
        mock_materials_instance.get_solute_density.assert_called_once()
        self.assertEqual(mock_os.environ['DATAPATH'], '/path/to/datapath')

if __name__ == '__main__':
    unittest.main()