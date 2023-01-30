import logging
from threading import Thread
from timer import Timer
import self as self
from MonitorFolder import MonitorFolder
from MCNP import MCNP
from watchdog.observers import Observer
from create_output import createOutputFile
from checkOS import checkSystem
if __name__ == '__main__':
    OUTPUT_PATH = "output"
    plot = True
    gray = True

    # Checks the operative system
    win, DATAPATH, sep = checkSystem()

    t = Timer()
    event_handler = MonitorFolder()
    observer = Observer()
    observer.schedule(event_handler, path=OUTPUT_PATH, recursive=True)
    t.start()
    logging.info("Monitoring started")
    createOutputFile(OUTPUT_PATH)
    watcher = Thread(observer.start())

    run = Thread(MCNP.runMCNP(self, gray, plot, DATAPATH))

    t.stop()
