import unittest
from unittest.mock import patch, MagicMock
from Python.MCNPSimulationScripts.simulation.MEDAPP_simulations.without_corrosion import run

class TestRun(unittest.TestCase):
    @patch('Python.MCNPSimulationScripts.simulation.MEDAPP_simulations.without_corrosion.run.Thread')
    @patch('Python.MCNPSimulationScripts.simulation.MEDAPP_simulations.without_corrosion.run.Observer')
    @patch('Python.MCNPSimulationScripts.simulation.MEDAPP_simulations.without_corrosion.run.Timer')
    @patch('Python.MCNPSimulationScripts.simulation.MEDAPP_simulations.without_corrosion.run.ensure_directory_exists')
    @patch('Python.MCNPSimulationScripts.simulation.MEDAPP_simulations.without_corrosion.run.check_system')
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

if __name__ == '__main__':
    unittest.main()