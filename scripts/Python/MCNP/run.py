import logging
from threading import Thread
import time
from Materials import Materials
from Source import Source
from analysis import Analyzer
from checkIfFolderExists import *
from timer import Timer
from MonitorFolder import MonitorFolder
from MonitorFolder import q
from MCNP import MCNP
from watchdog.observers import Observer
from checkOS import checkSystem


def run(source, material, nps, gray, plot):
    OUTPUT_PATH = "output"

    # Checks the operative system
    win, DATAPATH, sep = checkSystem()

    t = Timer()
    t.start()

    event_handler = MonitorFolder()
    observer = Observer()
    observer.schedule(event_handler, path=OUTPUT_PATH, recursive=True)

    checkIfFolderExists(OUTPUT_PATH)
    watcher = Thread(observer.start())
    mcnp_run = Thread(MCNP.runMCNP(self, source, material, nps, gray, plot, DATAPATH))

    watcher.start()  # Start watcher thread
    mcnp_run.start()  # Start MCNP thread
    logging.info("Monitoring started")
    logging.info("MCNP started")

    watcher.join()  # Stop watcher thread
    mcnp_run.join()  # Stop MCNP Thread

    t.stop()


def runMCNP(src, material, targetMaterial, nps, gray, plot, DATAPATH):
    # Set environment variables
    os.environ['DATAPATH'] = DATAPATH
    argon_density_values = setDensityValues(d_0, d_f)

    tallies, source, materials, planes, mode = loadMCNPBlocks(src, material)

    logging.info("DATAPATH variable set to " + DATAPATH)

    # Read density of Magnesium from material input file

    soluteDensity = Materials(material, targetMaterial).getDensityOfSolute()
    solute_percentage = Materials(material, targetMaterial).get_solute_percentage()
    particle_type = Source(src).getParticleType()

    # Change working dir to output
    checkIfFolderExists("output")
    os.chdir("output")
    logging.warning("Working directory changed to output")

    for d in argon_density_values:
        argonDensity = str(d)
        mcnp = MCNP(soluteDensity, argonDensity, tallies, source, materials, planes, mode, nps)

        # Get the input file data from object
        input_file = mcnp.get_input_file()

        # Write to input.txt the input data of MCNP
        file = open("input.txt", 'w')
        file.write(input_file)

        file.close()

        # Format input file
        mcnp.format_input_file()

        # Run MCNP command
        os.system("mpiexec -np 96 mcnp6.mpi i = input.txt")
        # os.system("mcnp6 i = " + INPUT_FILE_NAME)
        datanames.append(q.get())

    tal = mcnp.getTallies(tallies)
    nps = mcnp.getNPS()
    analyzer = Analyzer(datanames, gray, plot, tal, nps, argon_density_values, particle_type, solute_percentage)
    analyzer.analyze()
    datanames.clear()
    os.chdir("..")
    logging.warning("Working directory changed back to root")
    logging.warning("----- END OF THE SCRIPT -----\n")
    time.sleep(3)


def setDensityValues(d_0, d_f):
    step = (d_f - d_0) / 25
    values = np.arange(d_0, d_f, step)

    if len(values) > 25:
        logging.warning("Density vector contains more values than MCNP can handle.")
        sys.exit()

    return values


def loadMCNPBlocks(source, material):
    # Open tally file and read the lines
    with open("input_files/tallies.txt") as tally_file:
        tallies = tally_file.read().rstrip()
    tally_file.close()

    with open("input_files/" + source) as src_file:
        source = src_file.read().rstrip()
    src_file.close()

    with open("input_files/" + material) as mat_file:
        materials = mat_file.read().rstrip()
    mat_file.close()

    with open("input_files/planes.txt") as planes_file:
        planes = planes_file.read().rstrip()
    planes_file.close()

    with open("input_files/mode.txt") as mode_file:
        mode = mode_file.read().rstrip()
    mode_file.close()

    return tallies, source, materials, planes, mode
