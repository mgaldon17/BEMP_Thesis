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

To run the simulations, simply execute the `run.py` script:
```bash
python run.py
```

## Understanding the Results

The outcome of the simulations is stored in the `output` directory. MCNP executions generate several output files, including the `.o` file, which contains the results of each simulation. This tool runs multiple executions for a variable density of the argon gas in the cavity of the chamber. 

The output files are then processed by the `analyze.py` script, which extracts the relevant data and generates plots to visualize the results.

The vectors containing the relevant data for the user will be stored in a .txt file  for the user to choose the desired tool to plot them.

## Contributing

Contributions are welcome. Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

Please note that this is a general overview of the project. For more specific details, please refer to the individual scripts and their respective documentation.