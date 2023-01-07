import logging
from threading import Thread
from timer import Timer
import self as self
from MonitorFolder import MonitorFolder
from MCNP import MCNP
from MCNP_w import MCNP as MCNP_w
from watchdog.observers import Observer


if __name__ == '__main__':
    OUTPUT_PATH = "output"
    plot = True
    gray = True
    w = False
    t = Timer()
    event_handler = MonitorFolder()
    observer = Observer()
    observer.schedule(event_handler, path=OUTPUT_PATH, recursive=True)
    t.start()
    logging.info("Monitoring started")
    watcher = Thread(observer.start())
    DATAPATH = "/Users/maga2/MCNP/MCNP_DATA"
    #DATAPATH = "Z:\MY_MCNP\MCNP_DATA"
    run = Thread(MCNP.runMCNP(self, gray, plot, DATAPATH))

    t.stop()
