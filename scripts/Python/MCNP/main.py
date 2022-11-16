import logging
from threading import Thread
from MonitorFolder import MonitorFolder
from MCNP import MCNP
from watchdog.observers import Observer

if __name__ == '__main__':

    OUTPUT_PATH = "output/"
    gray = False
    event_handler = MonitorFolder()
    observer = Observer()
    observer.schedule(event_handler, path=OUTPUT_PATH, recursive=True)
    logging.info("Monitoring started")
    watcher = Thread(observer.start())
    run = Thread(MCNP.runMCNP())
