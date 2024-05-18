import os
import logging

def clean_output_folder():
    if os.path.exists("output/"):
        print('Folder exists!')
        os.chdir("output/")
        all_files = os.listdir()

        for f in all_files:
            os.remove(f)

        logging.info("All files in output_nps10E7 simulation were removed")
    else:
        print('Folder does not exist.')

def create_output_folder(OUTPUT_PATH):
    # Create output dir if not exist
    isExist = os.path.exists(OUTPUT_PATH)
    if not isExist:
        # Create a new directory because it does not exist
        print(os.getcwd())
        os.makedirs(OUTPUT_PATH)
        print("The new directory is created!")

if __name__ == '__main__':
    clean_output_folder()
    create_output_folder("your_output_path_here")