from simulateMaterialFraction import run_simulate_material_composition

if __name__ == '__main__':
    run_simulate_material_composition(["MEDAPP_Source.txt"],
                                      ["/materials/materials_0%_Mg + 100%_MgO.txt",
                                       "/materials/materials_97%_Mg + 3%_MgO.txt",
                                       "materials/materials_98%_Mg + 2%_MgO.txt",
                                       "/materials/materials_98.5%_Mg + 1.5%_MgO.txt",
                                       "/materials/materials_99%_Mg + 1%_MgO.txt"],
                                      "MgO",
                                      "10E8",
                                      True,
                                      False)