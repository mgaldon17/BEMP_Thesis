import os
import re


class Source:
    PARTICLE_TYPE_N = 1
    PARTICLE_TYPE_P = 2
    PARTICLE_TYPE_E = 3

    def __init__(self, source):
        self.source = source
        self.par_pattern = re.compile(r'\d+')

    def get_particle_type(self):
        input_files_dir = os.path.join(os.path.dirname(__file__), 'inputFiles')
        with open(os.path.join(input_files_dir, self.source), "r") as f:
            for line in f:
                if "MEDAPP" in line:
                    return "MEDAPP"

                if "par" in line or "PAR" in line:
                    match = self.par_pattern.search(line)

                    if match:
                        par = int(match.group())
                        switch = {
                            self.PARTICLE_TYPE_N: "N",
                            self.PARTICLE_TYPE_P: "P",
                            self.PARTICLE_TYPE_E: "E"
                        }

                        return switch.get(par, "")

        raise ValueError("No particle type found")
