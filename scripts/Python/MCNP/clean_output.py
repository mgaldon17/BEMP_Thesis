import os
import logging

def cleanOutputFolder():
    os.chdir("output/")
    all_files = os.listdir()

    for f in all_files:
        os.remove(f)

    logging.info("All files in output folder were removed")


if __name__ == '__main__':
    cleanOutputFolder()
