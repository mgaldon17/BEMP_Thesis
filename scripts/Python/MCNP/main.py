import logging
import os
from threading import Thread
from timer import Timer
import self as self
from MonitorFolder import MonitorFolder
from MCNP import MCNP
from MCNP_w import MCNP as MCNP_w
from watchdog.observers import Observer
from dotenv import load_dotenv

if __name__ == '__main__':
    OUTPUT_PATH = "output"
    plot = True
    gray = True
    w = True
    t = Timer()
    event_handler = MonitorFolder()
    observer = Observer()
    observer.schedule(event_handler, path=OUTPUT_PATH, recursive=True)
    t.start()
    logging.info("Monitoring started")
    watcher = Thread(observer.start())

    if w:
        run = Thread(MCNP_w.runMCNP(self, gray, plot, OUTPUT_PATH))
    else:
        run = Thread(MCNP.runMCNP(self, gray, plot))

    t.stop()
