import logging
import os
import time
from threading import Thread

from watchdog.observers import Observer

from .MCNP_simulation import MCNP
from ....simulation.MCNP_simulation_base import MCNPSimulationBase
from ...utilities.check_os import check_system
from ...utilities.ensure_dir_exists import ensure_directory_exists
from ....simulation.utilities.timer import Timer
from ....monitor import MonitorFolder, queue as q


def run(source, material, target_material, nps, tallies, planes, mode):
    output_path = "output"

    # Checks the operative system
    win, datapath, sep = check_system()

    timer = Timer()
    timer.start()

    event_handler = MonitorFolder(q)
    observer = Observer()
    observer.schedule(event_handler, path=output_path, recursive=True)

    ensure_directory_exists(output_path)
    watcher = Thread(target=observer.start)

    mcnp_run = Thread(target=run_mcnp, args=(source, material, target_material, nps, datapath, tallies, planes, mode))

    watcher.start()  # Start watcher thread
    mcnp_run.start()  # Start MCNPSimulationScripts thread
    logging.info("Monitoring started")
    logging.info("MCNPSimulationScripts started")

    watcher.join()  # Stop watcher thread
    mcnp_run.join()  # Stop MCNPSimulationScripts Thread

    timer.stop()


def run_mcnp(src, material, nps, datapath, tallies, planes, mode):
    os.environ['DATAPATH'] = datapath

    mcnp_base = MCNPSimulationBase()

    D_0, D_F = mcnp_base.load_config()
    argon_density_values = mcnp_base.set_density_values(D_0, D_F)

    tallies, source, materials, planes, mode = mcnp_base.load_mcnp_blocks(src, material, tallies, planes, mode)

    logging.info(f"DATAPATH variable set to {datapath}")

    ensure_directory_exists("output")
    os.chdir("output")
    logging.warning("Working directory changed to output")
    # Argon density values are used to run MCNP simulations with different argon densities
    # However, the solute density (Mg) is fixed at 1.73 g/cm^3
    for d in argon_density_values:
        argon_density = str(d)
        # Run MCNP simulation with a given solute density of 1.73 g/cm^3
        mcnp = MCNP(1.74, argon_density, tallies, source, materials, planes, mode, nps)

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

    DATANAMES.clear()
    os.chdir("../../../..")
    logging.warning("Working directory changed back to root")
    logging.warning("----- END OF THE SCRIPT -----\n")
    time.sleep(3)
