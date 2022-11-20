import logging
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from MCNP import q


class MonitorFolder(FileSystemEventHandler):
    FILE_SIZE = 1000

    def on_created(self, event):

        print(event.src_path, event.event_type)

        mctan = event.src_path.split("/")[-1]

        if mctan[:2] == "mc":
            q.put(mctan)
        self.checkFolderSize(event.src_path)

    def on_modified(self, event):
        # print(event.src_path, event.event_type)
        self.checkFolderSize(event.src_path)

    def checkFolderSize(self, src_path):
        if os.path.isdir(src_path):
            if os.path.getsize(src_path) > self.FILE_SIZE:
                pass
        else:
            if os.path.getsize(src_path) > self.FILE_SIZE:
                pass


if __name__ == "__main__":
    src_path = "output/"

    event_handler = MonitorFolder()
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
