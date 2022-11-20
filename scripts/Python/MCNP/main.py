import logging
from threading import Thread
from timer import Timer
import self as self

from MonitorFolder import MonitorFolder
from MCNP import MCNP
from watchdog.observers import Observer

if __name__ == '__main__':
    OUTPUT_PATH = "output/"
    t = Timer()
    plot = True
    gray = True
    event_handler = MonitorFolder()
    observer = Observer()
    observer.schedule(event_handler, path=OUTPUT_PATH, recursive=True)

    t.start()
    logging.info("Monitoring started")
    watcher = Thread(observer.start())
    run = Thread(MCNP.runMCNP(self, gray, plot))
    t.stop()
