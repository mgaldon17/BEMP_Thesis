import logging
from threading import Thread
from checkIfFolderExists import *
from timer import Timer
import self as self
from MonitorFolder import MonitorFolder
from MCNP import MCNP
from watchdog.observers import Observer
from checkOS import checkSystem


def run(source, material, nps, gray, plot):
    OUTPUT_PATH = "output"

    # Checks the operative system
    win, DATAPATH, sep = checkSystem()

    t = Timer()
    t.start()

    event_handler = MonitorFolder()
    observer = Observer()
    observer.schedule(event_handler, path=OUTPUT_PATH, recursive=True)

    checkIfFolderExists(OUTPUT_PATH)
    watcher = Thread(observer.start())
    mcnp_run = Thread(MCNP.runMCNP(self, source, material, nps, gray, plot, DATAPATH))

    watcher.start()  # Start watcher thread
    mcnp_run.start()  # Start MCNP thread
    logging.info("Monitoring started")
    logging.info("MCNP started")

    watcher.join()  # Stop watcher thread
    mcnp_run.join()  # Stop MCNP Thread

    t.stop()


if __name__ == '__main__':
    # Source and materials
    source = "Sr90Source.txt"
    material = "materials_MgO_1%.txt"
    nps = "10E7"
    plot = False
    gray = True

    run(source, material, nps, gray, plot)
