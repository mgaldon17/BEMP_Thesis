import os


class Materials:

    def __init__(self, material, target_material):
        self.material = material
        self.target_material = target_material

    def get_solute_density(self):
        input_files_dir = os.path.join(os.path.dirname(__file__), 'inputFilesParts')
        with open(os.path.join(input_files_dir, self.material), 'r') as f:
            for line in f:
                if self.target_material in line:
                    parts = line.strip().split(',')
                    for part in parts:
                        if 'd =' in part:
                            density_str = part.strip().split('=')[1].strip()
                            try:
                                density = float(density_str.split()[0])
                                print("Density of", self.target_material, "is:", density, "g/cm3")
                                return str(density)
                            except ValueError:
                                raise ValueError(f"Invalid density value: {density_str}")

    def get_solute_percentage(self):
        input_files_dir = os.path.join(os.path.dirname(__file__), 'inputFilesParts')
        with open(os.path.join(input_files_dir, self.material), 'r') as f:
            for line in f:
                if '%' in line:
                    solute_str = line.split("(")[1].split(")")[0]  # extract the string within the parentheses
                    solute_percentage = str(solute_str.split("%")[0])  # extract the percentage and convert to float
                    return solute_percentage
            return None  # return None if the line containing the water percentage is not found
