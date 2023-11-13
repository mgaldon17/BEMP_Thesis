import shutil
import time
import pytz
import tweepy.errors

import MessageCenter as msg_center
from timer import Timer
from run import run
from checkIfFolderExists import *
from Materials import *
from Source import *


def simulate_material_composition(sources, materials, targetMaterial, nps, gray, plot):
    global particle_type
    t = Timer()
    t.start()

    folders_to_move = []

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

    total_time = t.stop()
    return total_time


def run_simulate_material_composition(sources, materials, targetMaterial, nps, gray, plot):

    single_material = False # Must be false by default
    single_source = False
    mats_msg = ""
    source_msg = ""
    total_time = simulate_material_composition(sources, materials, targetMaterial, nps, gray, plot)

    # Write tailored tweet
    if len(materials) > 2:
        mats_msg = ", ".join([str(elem.split(".")[0]) for elem in materials])
    elif len(materials) == 2:
        mats_msg = " and ".join([str(elem.split(".")[0]) for elem in materials])
    elif len(materials) == 1:
        mats_msg = "".join([str(elem.split(".")[0]) for elem in materials])
        single_material = True

    if len(sources) > 2:
        source_msg = ", ".join([str(elem.split(".")[0]) for elem in sources])
    elif len(sources) == 2:
        source_msg = " and ".join([str(elem.split(".")[0]) for elem in sources])
    elif len(sources) == 1:
        source_msg = "".join([str(elem.split(".")[0]) for elem in sources])
        single_source = True

    timezone = pytz.timezone('Europe/Berlin')
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    message = "Simulation finished at " + str(timestamp) + " h " + str(timezone) + (
        " for material" if single_material else "s :") + " " + mats_msg + (
        " and source" if single_source else "s :") + " " + source_msg + ". " + str(
        total_time)

    # Send tweet
    try:
        msg_center.MessageCenter(message).send_tweet()
    except tweepy.errors.BadRequest:
        message = "Simulation finished at " + str(timestamp) + " h " + str(timezone) + ". " + str(
            total_time)
        msg_center.MessageCenter(message).send_tweet()


