# Master's Thesis: Characterization of Neutron Response of Ionisation Chambers 

This is the repository of the Master's Thesis of Manuel Trigueros Galdon. The project is written in Python and is designed to run Monte Carlo N-Particle (MCNP) simulations for analyzing the behavior of different materials under various conditions.

## Prerequisites

To run the MCNP simulations in this project, you must have a valid license from Los Alamos National Laboratory. MCNP is a licensed software and its use is restricted to license holders only. Please visit the [official MCNP website](https://mcnp.lanl.gov/) for more information on how to obtain a license.

However, the analysis of the nuclear data can be performed using this application provided that the user has the necessary data files. Data files are included in this repository.
## Project Structure

The project is organized into several directories, each containing scripts for different types of simulations:

- `MEDAPP Simulations`: This directory contains scripts for running simulations of the ionization chamber with and without a corrosion layer. The simulations are designed to analyze the behavior of the chamber under various conditions, taking into account the effects of the corrosion layer.

- `Strontium 90 Simulations`: This directory contains scripts for running simulations of the ionization chamber with and without a corrosion layer irradiated by a Strontium 90 source. The simulations are designed to analyze the behavior of the chamber under various conditions.

## Getting Started

To get started with the project, you will need to have Python installed on your system. You can then clone the repository and install the required dependencies.

```bash
git clone https://github.com/mgaldon17/BEMP_Thesis.git
cd BEMP_Thesis
pip install -r requirements.txt
```

## Running the Simulations

To run the simulations, you can use the `run.py` script in the respective directory based on the type of simulation you want to run. This script sets up the MCNP simulations with the specified source and material, runs the simulations, and then analyzes the results.
The input parameters of this script can be modified to customize the simulations according to your requirements. Those parameters are: 

| Parameter         | Type   | Description                                                                  | Example                                                        |
|-------------------|--------|------------------------------------------------------------------------------|----------------------------------------------------------------|
| Source            | List   | The source input file                                                        | `["resources/MEDAPP_Source.txt"]`                              |
| Materials         | List   | The materials input files                                                    | `["/hydromagnesite/materials_0%_water + 100%_hydro.txt", ...]` |
| Target Material   | String | The material of the corrosion layer. If there is no layer, simply enter "Mg" | `"hydromagnesite"`                                             |
| Number of Particles | String | The number of particles to simulate                                          | `"10E8"`                                                       |
| Tallies           | String | The tallies input file                                                       | `"resources/tallies.txt"`                                      |
| Planes            | String | The planes input file                                                        | `"resources/planes_with_corrosion"`                            |
| Mode              | String | The mode input file                                                          | `"resources/mode.txt"`                                         |

The parts of the input file stored in the resources folder form the input file that was used in this Master's Thesis. However, this automation tool is capable to execute the MCNP simulation for any other geometry, sources, materials, etc.
In order to do so, the user must provide the input files in the resources folder and modify the parameters in the run.py script accordingly.

To run the simulations, simply execute the `main.py` script:
```bash
python run.py
```

When the execution is finished, a notification will be sent on Twitter including basic details of the simulation. This feature can be disabled by commenting the line  `twitter.send_tweet("Simulation finished")` in the `run.py` script.
In order to use this feature, the user must have a Twitter Developer account and create an application to obtain the necessary keys and tokens.

For this repository, there is a Twitter Account set up with the necessary keys and tokens. Please follow the user @MCNPBot to see the notifications. 
## Understanding the Results

The outcome of the simulations is stored in the `output` directory. MCNP executions generate several output files, including the `.o` file, which contains the results of each simulation. This tool runs multiple executions for a variable density of the argon gas in the cavity of the chamber. 

The output files are then processed by the `analyze.py` script, which extracts the relevant data and generates plots to visualize the results.

The vectors containing the relevant data for the user will be stored in a .txt file  for the user to choose the desired tool to plot them.

# MCNP Simulation Analysis

This repository contains scripts for running and analyzing MCNP (Monte Carlo N-Particle) simulations. The main script for analysis is `analysis.py`, located in the `Python/MCNPSimulationScripts/simulation/analysis` directory.

## Understanding the Scripts

The `analysis.py` script is used to analyze the results of a MCNP simulation. It reads the output files of the simulation, processes the data, and writes the results to a text file.

The script uses the `Analyzer` class to perform the analysis. The `Analyzer` class has methods for reading the simulation output files, processing the data, and writing the results to a text file.

The `outputToTxt` function is used to write the results to a text file. It takes as input a dictionary of tally numbers and their corresponding values and errors, the type of particle used in the simulation, and the number of particles used in the simulation. It writes these data to a text file in the `resources` directory.

## Understanding the MCNP Output Files

The MCNP output files are named `mctal`, `mctam`, `mctan`, etc., and are located in the `resources/simulation_result` directory. These files contain the results of the MCNP simulation.

Each file contains a list of tally numbers and their corresponding values and errors. A tally number represents a specific measurement in the simulation, such as the number of particles that hit a certain target.

## Understanding the Result.txt File

The `result.txt` file is created by the `outputToTxt` function and is located in the `resources` directory. This file contains the processed results of the MCNP simulation.

The file is structured as follows:

- For each tally number, there are two lines: one for the value and one for the error. The lines are formatted as `y_<tally number>_<particle type> = <value>` and `y_err_<tally number>_<particle type> = <error>`.
- After the tally data, there is a section titled "Simulation Details" that contains information about the simulation, such as the type of particle used and the number of particles.

## Running the Scripts

To run the `analysis.py` script, navigate to the `Python/MCNPSimulationScripts/simulation/analysis` directory and run the script with Python:

```bash
python analysis_IC-33051.py
```

## Contributing

Contributions are welcome. Please make sure to update tests as appropriate.
