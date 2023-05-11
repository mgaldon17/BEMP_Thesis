
class Materials:

    def __init__(self, material):

        self.material = material

    def getDensityOfMg(self):

            with open("input_files/" + self.material, 'r') as f:
                for line in f:
                    if line.startswith('c Mg'):
                        parts = line.strip().split(',')
                        for part in parts:
                            if 'd =' in part:
                                density_str = part.strip().split('=')[1].strip()
                                density = str(density_str.split()[0])
                                return density
            return None
    def get_solute_percentage(self):

        with open("input_files/" + self.material, 'r') as f:
            for line in f:
                if '%' in line:
                    solute_str = line.split("(")[1].split(")")[0]  # extract the string within the parentheses
                    solute_percentage = str(solute_str.split("%")[0])  # extract the percentage and convert to float
                    return solute_percentage
            return None  # return None if the line containing the water percentage is not found

