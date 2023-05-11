import re


class Source:

    def __init__(self, source):
        self.source = source

    def getParticleType(self):

        with open("input_files/" + self.source, "r") as f:
            for line in f:

                if "par" or "PAR" in line:
                    match = re.search(r'\d+', line)

                    if match:
                        par = int(match.group())
                        switch = {
                            1: "N",
                            2: "P",
                            3: "E"
                        }

                        return switch.get(par, "")
        if match is False:
            print("Not particle type found")
