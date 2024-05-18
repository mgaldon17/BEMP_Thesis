import os
import shutil
import time
import pytz
import logging
import tweepy.errors

from Python.MCNPSimulationScripts.notificationBot import MessageCenter as msg_center
from Python.MCNPSimulationScripts.utilities.timer import Timer
from Python.MCNPSimulationScripts.withCorrosion.run import run
from Python.MCNPSimulationScripts.withCorrosion.Materials import *
from Python.MCNPSimulationScripts.withCorrosion.Source import *
from Python.MCNPSimulationScripts.utilities.ensureDirExists import ensureDirectoryExists


def validate_inputs(sources, materials, target_material, nps, gray, plot):
    if not sources or not materials:
        logging.error("Sources and materials cannot be empty.")
        return False

    if target_material is None:
        logging.error("Target material cannot be None.")
        return False

    if not isinstance(nps, int) or not isinstance(gray, bool) or not isinstance(plot, bool):
        logging.error("Invalid input: nps must be an integer, gray and plot must be boolean.")
        return False

    return True


def simulate_material_composition(sources, materials, target_material, nps, gray, plot):
    # Check if sources and materials are not empty
    particle_type = None

    t = Timer()
    t.start()

    folders_to_move = []

    for s in range(0, len(sources)):
        for m in range(0, len(materials)):
            try:
                # Run command
                run(sources[s], materials[m], target_material, nps, gray, plot)
            except Exception as e:
                logging.error(f"Failed to run simulation: {e}")
                return None

            solute_percentage = Materials(materials[m], target_material).get_solute_percentage()
            particle_type = Source(sources[s]).get_particle_type()
            folders_to_move.append(solute_percentage)

            try:
                os.rename("output", solute_percentage)
            except Exception as e:
                logging.error(f"Failed to rename directory: {e}")
                return None

        destination_folder = particle_type + " source"

        # Create the destination folder if it doesn't exist
        ensureDirectoryExists(destination_folder)

        for folder_name in os.listdir():
            if folder_name in folders_to_move:
                source_folder = os.path.join(os.getcwd(), folder_name)

                destination_folder_path = os.path.join(os.getcwd(), destination_folder)
                try:
                    shutil.move(source_folder, destination_folder_path)
                except Exception as e:
                    logging.error(f"Failed to move directory: {e}")
                    return None

    total_time = t.stop()
    return total_time


def run(sources, materials, target_material, nps, gray, plot):
    # Check if sources and materials are not empty
    if not validate_inputs(sources, materials, target_material, nps, gray, plot):
        return None

    try:
        total_time = simulate_material_composition(sources, materials, target_material, nps, gray, plot)
    except Exception as e:
        logging.error(f"Failed to run simulation: {e}")
        return

    # Create tailored tweet
    create_message(materials, sources, total_time)


def create_message(materials, sources, total_time):
    mats_msg = ""
    source_msg = ""

    if len(materials) > 2:
        mats_msg = ", ".join([str(elem.split(".")[0]) for elem in materials])
    elif len(materials) == 2:
        mats_msg = " and ".join([str(elem.split(".")[0]) for elem in materials])
    elif len(materials) == 1:
        mats_msg = "".join([str(elem.split(".")[0]) for elem in materials])

    if len(sources) > 2:
        source_msg = ", ".join([str(elem.split(".")[0]) for elem in sources])
    elif len(sources) == 2:
        source_msg = " and ".join([str(elem.split(".")[0]) for elem in sources])
    elif len(sources) == 1:
        source_msg = "".join([str(elem.split(".")[0]) for elem in sources])

    timezone = pytz.timezone('Europe/Berlin')
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    message = (f"Simulation finished at {timestamp} h {timezone} for material{'s :' if len(materials) > 1 else ''} "
               f"{mats_msg} and source{'s :' if len(sources) > 1 else ''} {source_msg}. {total_time}")

    send_message(message, timestamp, timezone, total_time)


def send_message(message, timestamp, timezone, total_time):
    # Send tweet
    try:
        msg_center.MessageCenter(message).send_tweet()
    except tweepy.errors.BadRequest:
        message = "Simulation finished at " + str(timestamp) + " h " + str(timezone) + ". " + str(
            total_time)
        msg_center.MessageCenter(message).send_tweet()

    return message