import re


class Source:

    def __init__(self, source):
        self.source = source

    def getParticleType(self):
        with open("input_files/" + self.source, "r") as f:
            for line in f:
                if "MEDAPP" in line:
                    return "MEDAPP"

                if "par" in line or "PAR" in line:
                    match = re.search(r'\d+', line)

                    if match:
                        par = int(match.group())
                        switch = {
                            1: "N",
                            2: "P",
                            3: "E"
                        }

                        return switch.get(par, "")

        print("No particle type found")
