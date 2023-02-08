import os

def createOutputFile(OUTPUT_PATH):

    # Create output dir if not exist
    isExist = os.path.exists(OUTPUT_PATH)
    if not isExist:
        # Create a new directory because it does not exist
        print(os.getcwd())
        os.makedirs(OUTPUT_PATH)
        print("The new directory is created!")