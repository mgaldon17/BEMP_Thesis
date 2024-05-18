import logging
import os
import time
import numpy as np
import configparser
from threading import Thread
from watchdog.observers import Observer
from Materials import Materials
from Source import Source
from ..analysis.analysis import Analyzer
from ..utilities.ensureDirExists import ensureDirectoryExists
from Python.MCNPSimulationScripts.utilities.timer import Timer
from ..MonitorFolder import MonitorFolder, q
from Python.MCNPSimulationScripts.withCorrosion.MCNP_simulation import MCNP
from Python.MCNPSimulationScripts.utilities.checkOS import checkSystem


def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    D_0 = config.getfloat('DEFAULT', 'D_0')
    D_F = config.getfloat('DEFAULT', 'D_F')

    return D_0, D_F


def run(source, material, target_material, nps, gray, plot):
    output_path = "output"

    # Checks the operative system
    win, datapath, sep = checkSystem()

    timer = Timer()
    timer.start()

    event_handler = MonitorFolder()
    observer = Observer()
    observer.schedule(event_handler, path=output_path, recursive=True)

    ensureDirectoryExists(output_path)
    watcher = Thread(target=observer.start)

    mcnp_run = Thread(target=run_mcnp, args=(source, material, target_material, nps, gray, plot, datapath))

    watcher.start()  # Start watcher thread
    mcnp_run.start()  # Start MCNPSimulationScripts thread
    logging.info("Monitoring started")
    logging.info("MCNPSimulationScripts started")

    watcher.join()  # Stop watcher thread
    mcnp_run.join()  # Stop MCNPSimulationScripts Thread

    timer.stop()


def run_mcnp(src, material, target_material, nps, gray, plot, datapath):
    os.environ['DATAPATH'] = datapath
    D_0, D_F = load_config()
    argon_density_values = set_density_values(D_0, D_F)

    tallies, source, materials, planes, mode = load_mcnp_blocks(src, material)

    logging.info("fDATAPATH variable set to  {datapath}")

    solute_density = Materials(material, target_material).get_solute_density()
    solute_percentage = Materials(material, target_material).get_solute_percentage()
    particle_type = Source(src).get_particle_type()

    ensureDirectoryExists("output")
    os.chdir("output")
    logging.warning("Working directory changed to output")

    for d in argon_density_values:
        argon_density = str(d)
        mcnp = MCNP(solute_density, argon_density, tallies, source, materials, planes, mode, nps)

        input_file = mcnp.get_input_file()

        try:
            with open("input.txt", 'w') as file:
                file.write(input_file)
        except IOError as e:
            logging.error(f"Failed to write to input.txt: {e}")
            return

        mcnp.format_input_file()

        exit_status = os.system("mpiexec -np 96 mcnp6.mpi i = input.txt")
        if exit_status != 0:
            logging.error(f"MCNP simulation failed with exit status {exit_status}")
            return

        try:
            DATANAMES = []
            DATANAMES.append(q.get())
        except Exception as e:
            logging.error(f"Failed to get data name from queue {e}")
            return

    tal = mcnp.get_tallies(tallies)
    nps = mcnp.get_nps()
    analyzer = Analyzer(DATANAMES, gray, plot, tal, nps, argon_density_values, particle_type, solute_percentage)
    analyzer.analyze()
    DATANAMES.clear()
    os.chdir("../..")
    logging.warning("Working directory changed back to root")
    logging.warning("----- END OF THE SCRIPT -----\n")
    time.sleep(3)


def set_density_values(d_0, d_f):
    if not isinstance(d_0, (int, float)) or not isinstance(d_f, (int, float)):
        logging.error("Invalid input: d_0 and d_f must be numbers.")
        raise ValueError("Invalid input: d_0 and d_f must be numbers.")
    if d_0 >= d_f:
        logging.error("Invalid input: d_0 must be less than d_f.")
        raise ValueError("Invalid input: d_0 must be less than d_f.")

    step = (d_f - d_0) / 25
    values = np.arange(d_0, d_f, step)

    if len(values) > 25:
        logging.error("Density vector contains more values than MCNPSimulationScripts can handle.")
        raise ValueError("Density vector contains more values than MCNPSimulationScripts can handle.")

    return values


def load_mcnp_blocks(source, material):
    input_files_dir = os.path.join(os.path.dirname(__file__), '..', 'inputFilesParts')

    try:
        with open(os.path.join(input_files_dir, 'tallies.txt')) as tally_file:
            tallies = tally_file.read().rstrip()

        with open("inputFilesParts/" + source) as src_file:
            source = src_file.read().rstrip()

        with open("inputFilesParts/" + material) as mat_file:
            materials = mat_file.read().rstrip()

        with open(os.path.join(input_files_dir, 'planes.txt')) as planes_file:
            planes = planes_file.read().rstrip()

        with open(os.path.join(input_files_dir, 'mode.txt')) as mode_file:
            mode = mode_file.read().rstrip()
    except FileNotFoundError:
        logging.error("One or more of the required files are missing")
        return None, None, None, None, None
    return tallies, source, materials, planes, mode
