import os
import unittest
from unittest.mock import patch, MagicMock

from Python.MCNPSimulationScripts.simulation.analysis import analysis_IC_33051

class TestAnalyzer(unittest.TestCase):
    @patch('Python.MCNPSimulationScripts.simulation.analysis.analysis_IC_33051.os')  # Updated line
    def test_analyze(self, mock_os):
        mock_os.path.join.return_value = "/path/to/result.txt"
        mock_os.chdir.return_value = None

        # Get the path of the current file
        current_file_path = os.path.realpath(__file__)


        analyzer = analysis_IC_33051.Analyzer(current_file_path + "/mock_simulation_results", "10E8", [1.0, 2.0], "neutron")
        analyzer.analyze()

        mock_os.path.join.assert_called_once_with("..", "result.txt")
        mock_os.chdir.assert_called_once_with(current_file_path + "/resources/simulation_result")

    def test_convertIntoGray(self):
        analyzer = analysis_IC_33051.Analyzer("/path/to/directory", "10E8", [1.0, 2.0], "neutron")
        val_gray, abs_error_gray = analyzer.convertIntoGray([6.24E9], [6.24E9])

        self.assertEqual(val_gray, [1.0])
        self.assertEqual(abs_error_gray, [1.0])

    def test_get_file_names(self):
        analyzer = analysis_IC_33051.Analyzer("/path/to/directory", "10E8", [1.0, 2.0], "neutron")
        file_names = analyzer.get_file_names()

        self.assertEqual(file_names, ['mctal', 'mctam', 'mctan', 'mctao', 'mctap', 'mctaq', 'mctar', 'mctas', 'mctat', 'mctau',
                                      'mctav', 'mctaw', 'mctax', 'mctay', 'mctaz', 'mctaa', 'mctab', 'mctac', 'mctad', 'mctae', 'mctaf',
                                      'mctag', 'mctah', 'mctai', 'mctaj'])

if __name__ == '__main__':
    unittest.main()