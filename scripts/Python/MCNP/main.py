from simulateMaterialFraction import run_simulate_material_composition

if __name__ == '__main__':
    run_simulate_material_composition(["MEDAPP_Source.txt"],
                                      ["/hydromagnesite/materials_0%_water + 100%_hydro.txt",
                                       "/hydromagnesite/materials_99%_hydro + 1%_water.txt",
                                       "/hydromagnesite/materials_98%_hydro + 2%_water.txt",
                                       "/hydromagnesite/materials_97%_hydro + 3%_water.txt"
                                       ],
                                      "hydromagnesite", #Changeme
                                      "10E8",
                                      True,
                                      False)