import shutil
from timer import Timer
from run import run
from checkIfFolderExists import *
from Materials import *
from Source import *

if __name__ == '__main__':

    t = Timer()
    t.start()

    # Source and materials
    sources = ["MEDAPP_Source.txt"]
    materials = [ "materials_MgO_1.5%.txt", "materials_MgO_2%.txt",
                 "materials_MgO_3%.txt"]
    nps = "10E8"
    plot = False
    gray = True
    folders_to_move = []
    targetMaterial = "MgO"
    DATAPATH = "D:\MY_MCNP\MCNP_DATA"

    for s in range(0, len(sources)):
        for m in range(0, len(materials)):
            # Run command
            run(sources[s], materials[m], targetMaterial, nps, gray, plot)
            solute_percentage = Materials(materials[m], targetMaterial).get_solute_percentage()
            particle_type = Source(sources[s]).getParticleType()
            folders_to_move.append(solute_percentage)
            os.rename("output", solute_percentage)

        destination_folder = particle_type + " source"

        # Create the destination folder if it doesn't exist
        checkIfFolderExists(destination_folder)

        for folder_name in os.listdir():
            if folder_name in folders_to_move:
                source_folder = os.path.join(os.getcwd(), folder_name)

                destination_folder_path = os.path.join(os.getcwd(), destination_folder)
                shutil.move(source_folder, destination_folder_path)
    t.stop()
