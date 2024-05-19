import logging
import queue
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .main.utilities.checkOS import checkSystem


class MonitorFolder(FileSystemEventHandler):
    """Class to monitor changes in a simulation."""

    def __init__(self, queue, file_size=1000):
        self.queue = queue
        self.FILE_SIZE = file_size

    def on_created(self, event):
        """Handle the event when a file is created."""
        print(event.src_path, event.event_type)
        win, DATAPATH, sep = checkSystem()
        mctan = event.src_path.split(sep)[-1]
        if mctan[:2] == "mc":
            self.queue.put(mctan)

    def on_modified(self, event):
        """Handle the event when a file is modified."""
        pass


if __name__ == "__main__":
    src_path = "/output"
    q = queue.Queue()

    event_handler = MonitorFolder(q)
    observer = Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)
    logging.info("Monitoring started")

    observer.start()

    try:
        while (True):
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()
        observer.join()
