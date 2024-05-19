import configparser
import logging
import os

import numpy as np


class MCNPSimulationBase:
    def load_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        D_0 = config.getfloat('DEFAULT', 'D_0')
        D_F = config.getfloat('DEFAULT', 'D_F')

        return D_0, D_F

    def set_density_values(self, d_0, d_f):
        if not isinstance(d_0, (int, float)) or not isinstance(d_f, (int, float)):
            logging.error("Invalid input: d_0 and d_f must be numbers.")
            raise ValueError("Invalid input: d_0 and d_f must be numbers.")
        if d_0 >= d_f:
            logging.error("Invalid input: d_0 must be less than d_f.")
            raise ValueError("Invalid input: d_0 must be less than d_f.")

        step = (d_f - d_0) / 25
        values = np.arange(d_0, d_f, step)

        if len(values) > 25:
            logging.error("Density vector contains more values than MCNPSimulationScripts can handle.")
            raise ValueError("Density vector contains more values than MCNPSimulationScripts can handle.")

        return values

    def load_mcnp_blocks(self, source, material):
        input_files_dir = os.path.join(os.path.dirname(__file__), '..', 'inputFilesParts')

        try:
            with open(os.path.join(input_files_dir, 'tallies.txt')) as tally_file:
                tallies = tally_file.read().rstrip()

            with open("inputFilesParts/" + source) as src_file:
                source = src_file.read().rstrip()

            with open("inputFilesParts/" + material) as mat_file:
                materials = mat_file.read().rstrip()

            with open(os.path.join(input_files_dir, 'planes.txt')) as planes_file:
                planes = planes_file.read().rstrip()

            with open(os.path.join(input_files_dir, 'mode.txt')) as mode_file:
                mode = mode_file.read().rstrip()
        except FileNotFoundError:
            logging.error("One or more of the required files are missing")
            return None, None, None, None, None
        return tallies, source, materials, planes, mode

    def get_nps(self):
        """Get the number of particles from the input file."""
        try:
            with open("input.txt") as file:
                for line in file:
                    if "nps" in line:
                        return line.split(" ")[1]
        except FileNotFoundError:
            print("Error: The file 'input.txt' was not found.")
        except PermissionError:
            print("Error: Permission denied when trying to open 'input.txt'.")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    def get_tallies(self, tallies):
        """Get the tallies from the input file."""
        tally_array = tallies.split("\n")
        tally_numbers = [tally.split(':')[0] for tally in tally_array if "f" in tally]
        return tally_numbers

    def format_input_file(self):
        """Format the input file to make it more readable."""
        try:
            with open("input.txt", 'r') as file:
                lines = file.readlines()

            formatted_lines = [line[24:].rstrip() if line.startswith("                        ") else line for line in
                               lines]

            with open("input.txt", 'w') as file:
                file.write("\n".join(formatted_lines))
        except FileNotFoundError:
            print("Error: The file 'input.txt' was not found.")
        except PermissionError:
            print("Error: Permission denied when trying to open 'input.txt'.")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

