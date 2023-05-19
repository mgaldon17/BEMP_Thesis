import os
import logging

def cleanOutputFolder():

    if os.path.exists("output/"):

        print('Folder exists!')
        os.chdir("output/")
        all_files = os.listdir()

        for f in all_files:
            os.remove(f)

        logging.info("All files in output_nps10E7 folder were removed")
    else:
        print('Folder does not exist.')

if __name__ == '__main__':
    cleanOutputFolder()
