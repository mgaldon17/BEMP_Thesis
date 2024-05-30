import os


def outputToTxt(tally_dict, error_dict, particle_type, nps):
    """
    Writes the results of the analysis to a text file.

    Parameters:
    tally_dict (dict): A dictionary containing the tally numbers as keys and their corresponding values as lists.
    error_dict (dict): A dictionary containing the tally numbers as keys and their corresponding error values as lists.
    particle_type (str): The type of particle used in the simulation.
    nps (str): The number of particles used in the simulation.
    """
    with open(os.path.join("..", "result.txt"), "w+") as f:
        for tally in tally_dict:
            y = tally_dict[tally]
            f.write("y_" + tally + "_" + particle_type + " = " + str(y))
            f.write("\n")
        f.write("\n")
        f.write("\n")

        for tally in error_dict:
            y_err = error_dict[tally]
            f.write("y_err_" + tally + "_" + particle_type + " = " + str(y_err))
            f.write("\n")

        # Write the signature
        f.write("\n")
        f.write("Simulation Details:\n")
        f.write(f"Particle Type: {particle_type}\n")
        f.write(f"Number of Particles: {nps}\n")
        f.write("Tallies Simulated: " + ', '.join(tally_dict.keys()) + "\n")


class Analyzer:
    """
    A class used to analyze the results of a simulation.

    Attributes:
    directory (str): The directory where the simulation results are stored.
    nps (str): The number of particles used in the simulation.
    argon_density_values (list): A list of argon density values used in the simulation.
    particleType (str): The type of particle used in the simulation.
    """
    def __init__(self, directory, nps, argon_density_values, particleType):
        """
        The constructor for the Analyzer class.

        Parameters:
        directory (str): The directory where the simulation results are stored.
        nps (str): The number of particles used in the simulation.
        argon_density_values (list): A list of argon density values used in the simulation.
        particleType (str): The type of particle used in the simulation.
        """
        self.directory = directory
        self.nps = nps
        self.argon_density_values = argon_density_values
        self.particleType = particleType

    # Return the tally stored in the dict corresponding to the number read off the output_old file
    def analyze(self):
        """
        Analyzes the results of the simulation and writes them to a text file.
        """
        tally_dict = {}
        error_dict = {}

        datanames = self.get_file_names()
        os.chdir(self.directory)

        for d in datanames:
            with open(d, 'r') as file:
                lines = file.readlines()
                for i in range(len(lines)):
                    if 'tally' in lines[i]:
                        tally_number = lines[i].split()[1]
                        # Initialize the lists for this tally number if they don't exist yet
                        if tally_number not in tally_dict:
                            tally_dict[tally_number] = []
                            error_dict[tally_number] = []
                    if 'vals' in lines[i]:
                        values = lines[i + 1].strip().split()
                        vals = [float(values[0])]
                        errors = [float(values[1])]
                        vals_gray, errors_gray = self.convertIntoGray(vals, errors)
                        # Append the new values to the existing lists
                        tally_dict[tally_number].extend(vals_gray)
                        error_dict[tally_number].extend(errors_gray)

        outputToTxt(tally_dict, error_dict, self.particleType, self.nps)

    def convertIntoGray(self, val, abs_error):
        """
        Converts the values and their corresponding errors from MeV/g to Gray.

        Parameters:
        val (list): A list of values in MeV/g.
        abs_error (list): A list of absolute errors corresponding to the values.

        Returns:
        list: A list of values in Gray.
        list: A list of absolute errors in Gray.
        """
        # Conversion rate from MeV/g to Gray
        # 1 gray in MeV/g is 6.24E9
        con_rate = 6.24E9

        val_gray = []
        abs_error_gray = []
        for v in (val):
            v /= con_rate
            val_gray.append(v)

        for r in abs_error:
            r /= con_rate
            abs_error_gray.append(r)

        return val_gray, abs_error_gray

    def get_file_names(self):
        """
        Returns the default name and order of the files where the tallies are stored in the MCNP by default.

        Returns:
        list: A list of file names.
        """
        return ['mctal', 'mctam', 'mctan', 'mctao', 'mctap', 'mctaq', 'mctar', 'mctas', 'mctat', 'mctau',
                 'mctav', 'mctaw', 'mctax', 'mctay', 'mctaz', 'mctaa', 'mctab', 'mctac', 'mctad', 'mctae', 'mctaf',
                 'mctag', 'mctah', 'mctai', 'mctaj']


if __name__ == '__main__':
    """
    Main entry point of the script. This block is executed when the script is run directly, not when it's imported as a module.

    It does the following:
    1. Gets the path of the current file.
    2. Goes up four directories to get the parent directory path.
    3. Defines the number of particles (nps) and the type of particle used in the simulation.
    4. Defines the argon density values used in the simulation.
    5. Creates an instance of the Analyzer class, passing the path to the simulation results, the number of particles, the argon density values, and the particle type.
    6. Calls the analyze method of the Analyzer instance to analyze the simulation results and write them to a text file.
    """
    # Get the path of the current file
    current_file_path = os.path.realpath(__file__)

    # Go up three directories
    parent_dir_path = os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(current_file_path))))
    nps = "10E8"
    argon_density_values = [1.0, 2.0]
    particleType = "neutron"

    # Create an instance of the Analyzer
    analyzer = Analyzer(parent_dir_path + "/resources/simulation_result", nps, argon_density_values, particleType)

    # Call the analyze method
    analyzer.analyze()
