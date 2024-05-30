from .simulation.MEDAPP_simulations.with_corrosion import run

if __name__ == '__main__':
    # Define the source resources
    source_files = ["resources/MEDAPP_Source.txt"]

    # Define the material resources
    material_files = [
        "/hydromagnesite/materials_0%_water + 100%_hydro.txt",
        "/hydromagnesite/materials_99%_hydro + 1%_water.txt",
        "/hydromagnesite/materials_98%_hydro + 2%_water.txt",
        "/hydromagnesite/materials_97%_hydro + 3%_water.txt"
    ]

    # Define the target material
    target_material = "hydromagnesite"

    # Define the number of particles
    nps = "10E8"

    # Define the tallies file
    tallies = "resources/tallies.txt"

    # Define the planes file
    planes = "resources/planes_with_corrosion"

    # Define the mode file
    mode = "resources/mode.txt"

    # Call the run method with the defined arguments
    run(source_files, material_files, target_material, nps, tallies, planes, mode)
